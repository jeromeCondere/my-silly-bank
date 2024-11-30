import os
import sagemaker
import boto3
import botocore
from sagemaker.huggingface import HuggingFaceModel
import json
from time import sleep

def delete_endpoint_and_config(sagemaker_client, endpoint_name):
    # Check if the endpoint exists
    try:
        sagemaker_client.describe_endpoint(EndpointName=endpoint_name)
        print(f"Endpoint '{endpoint_name}' exists. Deleting it...")
        
        # Delete the endpoint
        sagemaker_client.delete_endpoint(EndpointName=endpoint_name)
        print(f"Endpoint '{endpoint_name}' has been deleted.")
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'ValidationException':
            print(f"Endpoint '{endpoint_name}' does not exist.")


    # Check if the endpoint configuration exists
    try:
        sagemaker_client.describe_endpoint_config(EndpointConfigName=endpoint_name)
        print(f"Endpoint configuration '{endpoint_name}' exists. Deleting it...")

        # Delete the endpoint configuration
        sagemaker_client.delete_endpoint_config(EndpointConfigName=endpoint_name)
        print(f"Endpoint configuration '{endpoint_name}' has been deleted.")
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'ValidationException':
            print(f"Endpoint configuration '{endpoint_name}' does not exist.")
        else:
            raise error



with open('config_inference.json') as f:
    data = json.load(f)
    region = data['region']
    instance=data['instance']
    profile=data['profile']
    endpoint_name=data['endpoint_name']
    bucket=data['bucket']
    sagemaker_root=data['sagemaker_root']
    role= data['role']
    ecr_image= data['ecr_image']



os.environ['AWS_DEFAULT_REGION'] = region
os.environ['AWS_DEFAULT_PROFILE'] = profile

print('the endpoint name will be ', endpoint_name)
print(f'The instance used will be {instance}')

# Initialize a SageMaker session
session = boto3.session.Session(profile_name=profile)
sagemaker_session = sagemaker.Session(boto_session=session)
sagemaker_client = session.client('sagemaker')

delete_endpoint_and_config(sagemaker_client=sagemaker_client, endpoint_name=endpoint_name)


# Replace w/ your own path
s3_model_path = f"s3://{bucket}/{sagemaker_root}/model.tar.gz"

code_root = f'{sagemaker_root}/inference/code'
s3_code_path = f's3://{bucket}/{sagemaker_root}/inference/code/code.tar.gz'

# ecr_image=f"763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-inference:2.4.0-gpu-py311-cu124-ubuntu22.04-sagemaker"

print("s3 code path: ", s3_code_path)
print("s3 model path: ", s3_model_path)
print("\n\n")

# Upload the code directory to S3
s3_client = session.client('s3')
s3_client.upload_file('code/inference.py', bucket, f'{code_root}/inference.py')
s3_client.upload_file('code/requirements.txt', bucket, f'{code_root}/requirements.txt')
s3_client.upload_file('code.tar.gz', bucket, f'{code_root}/code.tar.gz')
s3_client.upload_file('model.tar.gz', bucket, f'{sagemaker_root}/model.tar.gz')


print(f'Uploading file inference.py, requirements.txt, model.tar.gz and code.tar.gz to {code_root}')
print(f'Uploading  model.tar.gz to {sagemaker_root}')

print('Starting deployment')




env = {
'SAGEMAKER_MODEL_SERVER_TIMEOUT' : '500',
'SAGEMAKER_MODEL_SERVER_TIMEOUT': '250',
'SAGEMAKER_TS_STARTUP_TIMEOUT': '1800', #value to increase
'SAGEMAKER_TS_RESPONSE_TIMEOUT': '80',
'MODEL_SERVER_STARTUP_TIMEOUT': '63'
}



health_check_timeout = 2500
model_data_download_timeout=1500


huggingface_model = HuggingFaceModel(
    model_data=s3_model_path,
    source_dir =s3_code_path,
    entry_point = 'inference.py',
    role=role,
    transformers_version="4.26.0",
    pytorch_version="1.13.1", 
    py_version="py39",
    image_uri=ecr_image,
    sagemaker_session=sagemaker_session,
    env = env
)

sleep(8)


predictor = huggingface_model.deploy(
    initial_instance_count=1,
    instance_type=instance, 
    endpoint_name=endpoint_name,  
    container_startup_health_check_timeout=health_check_timeout,
    model_data_download_timeout=model_data_download_timeout
)
