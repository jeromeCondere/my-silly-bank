import sagemaker
from sagemaker.processing import ScriptProcessor, ProcessingInput, ProcessingOutput
import boto3
import os 
from sagemaker import get_execution_role
from datetime import datetime
import json





with open('config.json') as f:
    data = json.load(f)
    region = data['region']
    bucket = data['bucket']
    role = data['role']
    sagemaker_root =  data['sagemaker_root']
    instance =  data['instance']
    profile = data['profile']
    job_name = data['job_name']



session = boto3.session.Session(profile_name=profile)
sagemaker_session = sagemaker.Session(boto_session=session)
sagemaker_image = sagemaker.image_uris.get_base_python_image_uri(region, py_version='310')



print("Sagemaker image: ", sagemaker_image)
print("Sagemaker execution role: ", role)
print("\n\n")


os.environ['AWS_DEFAULT_REGION'] = region
os.environ['AWS_DEFAULT_PROFILE'] = profile


output_s3_path = f's3://{bucket}/{sagemaker_root}/output'
code_s3_path = f's3://{bucket}/{sagemaker_root}/code'



print("Output: ", output_s3_path)
print("\n\n")

# Upload the code directory to S3
# s3_client = session.client('s3')
# s3_client.upload_file('job/preprocessing_script.py', bucket, f'{sagemaker_root}/code/preprocessing_script.py')
# s3_client.upload_file('utils/transaction.py', bucket, f'{sagemaker_root}/code/utils/transaction.py')
# s3_client.upload_file('utils/stock.py', bucket, f'{sagemaker_root}/code/utils/stock.py')

print(f's3 root is set to {sagemaker_root} ')
print('s3 files uploaded\n')

now = datetime.now()
formatted_time = now.strftime("%Y%m%d-%H-%M-%S")
job_name = job_name+formatted_time


# Set up the ScriptProcessorsagemaker_root
script_processor = ScriptProcessor(
    command = ["python3"],
    image_uri=sagemaker_image,
    role=role,
    instance_count=1,
    instance_type=instance,
    sagemaker_session = sagemaker_session
)


# Run the processing job
script_processor.run(
    code=f's3://{bucket}/{sagemaker_root}/code/preprocessing_script.py',
    inputs=[

         ProcessingInput(
            source=f'{code_s3_path}/utils/',
            destination='/opt/ml/processing/input/code/src'
        )
        
    ],
    outputs=[ProcessingOutput(
        source='/opt/ml/processing/output',
        destination=output_s3_path
    )],
    job_name=job_name,
    arguments=[
        '--output-dir', '/opt/ml/processing/output'
    ]
)
