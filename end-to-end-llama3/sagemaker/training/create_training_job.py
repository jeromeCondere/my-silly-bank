import sagemaker
import boto3
from sagemaker.huggingface import HuggingFace
import json
import os
from datetime import datetime
from sagemaker.local import LocalSession




with open('config.json') as f:
    data = json.load(f)
    region = data['region']
    bucket = data['bucket']
    role = data['role']
    base_s3=data['output']
    output_path =  f's3://{bucket}/{base_s3}'
    hyperparameters = data['hyperparameters']
    instance=data['instance']
    profile=data['profile']
    print(f'bucket: {bucket}\nrole: {role}\noutput: {output_path}')
    print('hyperparameters: ', hyperparameters)


os.environ['AWS_DEFAULT_REGION'] = region
os.environ['AWS_DEFAULT_PROFILE'] = 'profile-admin'


session = boto3.session.Session(profile_name='profile-admin', region_name='us-east-1')
sagemaker_session = sagemaker.Session(boto_session=session)



print('Role used: ', role)

now = datetime.now()
formatted_time = now.strftime("%Y%m%d-%H-%M-%S")

job_name = 'train-llama-8-'+str(formatted_time)
print('job name: ', job_name)

# Create Hugging Face estimator
huggingface_estimator = HuggingFace(
    entry_point='training.py',
    source_dir='./',
    instance_type=instance,
    instance_count=1,
    role=role,
    transformers_version='4.26.0',
    pytorch_version='1.13.1',
    py_version='py39',
    hyperparameters=hyperparameters,
    output_dir=output_path,
    dependencies=['requirements.txt'],
    sagemaker_session = sagemaker_session
)

# Start training job
huggingface_estimator.fit(job_name=job_name)

print(f"Training job started with name: {huggingface_estimator.latest_training_job.name}")
