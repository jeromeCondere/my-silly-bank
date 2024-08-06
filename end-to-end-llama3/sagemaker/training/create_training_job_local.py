import sagemaker
import boto3
from sagemaker.huggingface import HuggingFace
import json
import os
from datetime import datetime
from sagemaker.local import LocalSession

# Define SageMaker session




with open('config.json') as f:
    data = json.load(f)
    region = data['region']
    bucket = data['bucket']
    role = data['role']
    output_path =  data['output']
    hyperparameters = data['hyperparameters']
    print(f'bucket: {bucket}\nrole: {role}\noutput: {output_path}')
    print('hyperparameters: ', hyperparameters)


os.environ['AWS_DEFAULT_REGION'] = region
os.environ['AWS_DEFAULT_PROFILE'] = 'profile-admin'

os.environ['AWS_ACCESS_KEY_ID']="<value>"
os.environ['AWS_SECRET_ACCESS_KEY']="<value>"
os.environ['AWS_SESSION_TOKEN']="<value>"

local_sagemaker_session = LocalSession()
local_sagemaker_session.config = {'local': {'local_code': True}}

# For local training a dummy role will be sufficient
role = 'arn:aws:iam::111111111111:role/service-role/AmazonSageMaker-ExecutionRole-20200101T000001'


# print('Role used: ', role)
now = datetime.now()

# Format the date and time
formatted_time = now.strftime("%Y%m%d-%H-%M-%S")
job_name = 'train-llama-8-'+str(formatted_time)
print('job name: ', job_name)

# Create Hugging Face estimator
huggingface_estimator = HuggingFace(
    entry_point='training_local.py',
    source_dir='./',
    # instance_type='ml.g4dn.xlarge',
    instance_type='local_gpu',
    instance_count=1,
    role=role,
    transformers_version='4.26.0',
    pytorch_version='1.13.1',
    py_version='py39',
    hyperparameters=hyperparameters,
    output_dir='my-output',  # Specify the output S3 path
    dependencies=['requirements.txt'],
    sagemaker_session = local_sagemaker_session
)

# Start training job
huggingface_estimator.fit()

