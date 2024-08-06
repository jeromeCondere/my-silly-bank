import sagemaker
from sagemaker.processing import ScriptProcessor, ProcessingInput, ProcessingOutput
import boto3
import os 
from sagemaker import get_execution_role
from sagemaker.local import LocalSession
from datetime import datetime
import json




os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

with open('config.json') as f:
    data = json.load(f)
    region = data['region']
    bucket = data['bucket']
    role = data['role']
    sagemaker_root =  data['sagemaker_root']
    instance =  data['instance']
    profile = data['profile']
    job_name = data['job_name']
    aws_access_key_id=data['aws_access_key_id']
    aws_secret_access_key=data['aws_secret_access_key']
    aws_session_token=data['aws_session_token']



# session = boto3.session.Session(profile_name=profile)
# sagemaker_session = sagemaker.Session(boto_session=session)

os.environ['AWS_DEFAULT_REGION'] = region
os.environ['AWS_DEFAULT_PROFILE'] = profile

os.environ['AWS_ACCESS_KEY_ID']=aws_access_key_id
os.environ['AWS_SECRET_ACCESS_KEY']=aws_secret_access_key
os.environ['AWS_SESSION_TOKEN']=aws_session_token


local_sagemaker_session = LocalSession()
local_sagemaker_session.config = {'local': {'local_code': True}}
sagemaker_image = sagemaker.image_uris.get_base_python_image_uri(region, py_version='310')


print("Sagemaker image: ", sagemaker_image)
print("\n\n")


os.environ['AWS_DEFAULT_REGION'] = region



now = datetime.now()
formatted_time = now.strftime("%Y%m%d-%H-%M-%S")
job_name = job_name+formatted_time


# Set up the ScriptProcessor
script_processor = ScriptProcessor(
    command = ["python3"],
    image_uri=sagemaker_image,
    role=role,
    instance_count=1,
    instance_type='local',
    sagemaker_session = local_sagemaker_session
)

# Run the processing job
script_processor.run(
    code=f'job/preprocessing_script.py',
    inputs=[
         ProcessingInput(
            source=f'utils/',
            destination='/opt/ml/processing/input/code/src'
        )
        
    ],
    outputs=[ProcessingOutput(
        source='/opt/ml/processing/output',
        destination='output'
    )],
    job_name=job_name,
    arguments=[
        '--output-dir', '/opt/ml/processing/output'
    ]
)
