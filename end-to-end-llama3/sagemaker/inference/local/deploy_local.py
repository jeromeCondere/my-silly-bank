import sagemaker
import boto3
import botocore
from sagemaker.huggingface import HuggingFaceModel
import json
from sagemaker.local import LocalSession
import os
import pathlib




with open('../config_inference.json') as f:
    data = json.load(f)
    region = data['region']
    instance=data['instance']
    profile=data['profile']
    aws_access_key_id=data['aws_access_key_id']
    aws_secret_access_key=data['aws_secret_access_key']
    aws_session_token=data['aws_session_token']
    endpoint_name=data['endpoint_name']

os.environ['AWS_DEFAULT_REGION'] = region
os.environ['AWS_DEFAULT_PROFILE'] = profile

os.environ['AWS_ACCESS_KEY_ID']=aws_access_key_id
os.environ['AWS_SECRET_ACCESS_KEY']=aws_secret_access_key
os.environ['AWS_SESSION_TOKEN']=aws_session_token


local_sagemaker_session = LocalSession()
local_sagemaker_session.config = {'local': {'local_code': True}}


# Create an STS client
sts_client = boto3.client('sts')

# Get the current caller's identity
response = sts_client.get_caller_identity()

# Extract the account ID from the response
account_id = response['Account']

#763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-inference:2.4.0-gpu-py311-cu124-ubuntu22.04-sagemaker
ecr_image=f"763104351884.dkr.ecr.{region}.amazonaws.com/pytorch-inference:2.4.0-gpu-py311-cu124-ubuntu22.04-sagemaker"
ecr_image="test-pytorch24"
print(ecr_image)

role = 'arn:aws:iam::007739069911:role/service-role/AmazonSageMaker-ExecutionRole-20170624T135698'  # Replace with your role


model_path = "file://" + str(pathlib.Path(__file__).parent.joinpath("model.tar.gz"))
os.environ["HF_TASK"] = 'text-generation'


health_check_timeout = 1500
model_data_download_timeout=1800


env = {
'SAGEMAKER_MODEL_SERVER_TIMEOUT' : '2000',
'SAGEMAKER_MODEL_SERVER_TIMEOUT': '250',
'SAGEMAKER_TS_STARTUP_TIMEOUT': '22', #value to increase
'SAGEMAKER_TS_RESPONSE_TIMEOUT': '80',
'MODEL_SERVER_STARTUP_TIMEOUT': '63'
}


huggingface_model = HuggingFaceModel(
    model_data=model_path,
    role=role,
    transformers_version="4.26.0",     # Specify the transformers version
    pytorch_version="1.13.1",          # PyTorch version for the model
    py_version="py39",
    entry_point = 'inference.py',
    source_dir = 'code',
    image_uri=ecr_image,
    env = env,
    sagemaker_session=local_sagemaker_session  # Pass the session if you want to use a custom session
)



predictor = huggingface_model.deploy(
    initial_instance_count=1, 
    instance_type="local_gpu",  
    endpoint_name=endpoint_name,  
    container_startup_health_check_timeout=health_check_timeout,
    model_data_download_timeout=model_data_download_timeout
)



print('Deploying...\n\n')


