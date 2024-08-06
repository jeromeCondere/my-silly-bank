import boto3
import json
import os
from sagemaker.local import LocalSession


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
os.environ['AWS_DEFAULT_PROFILE'] = 'profile-admin'

os.environ['AWS_ACCESS_KEY_ID']=aws_access_key_id
os.environ['AWS_SECRET_ACCESS_KEY']=aws_secret_access_key
os.environ['AWS_SESSION_TOKEN']=aws_session_token

os.environ['HF_TASK'] = "text-generation"

# Initialize the SageMaker runtime client
session = boto3.session.Session(profile_name='profile-admin')
runtime_client = session.client('sagemaker-runtime')

endpoint_name = 'huggingface-model-endpoint-test'
content_type = 'application/json'

txt = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Hi Yalat Sensei, I'm your assistant how can I help you<|eot_id|><|start_header_id|>user<|end_header_id|>

I'd like to buy stocks worth 42.24 in Google Corp..<|eot_id|><|start_header_id|>system<|end_header_id|>

Sure, we have purchased stocks worth ###StockValue(42.24) in ###Company(Google Corp.) for you.<|eot_id|><|start_header_id|>user<|end_header_id|>

Now I want to see my balance, hurry up!<|eot_id|>"""

messages=[
    { "role": "system", "content": "You are a helpful assistant." },
    { "role": "user", "content": "What is deep learning?" }
  ]
 
# Generation arguments
parameters = {
    "model": "jeromecondere/merged-llama-v3-for-bank",
    "top_p": 0.6,
    "temperature": 0.9,
    "max_tokens": 512,
    "stop": ["<|eot_id|>"],
}



data={
    "messages": messages
}


# Define the input data for the model (example input)
payload = json.dumps(data)

print(f'the payload is really \n\n {payload} \n\n')


local_sagemaker_session = LocalSession()
local_sagemaker_session.config = {"local": {"local_code": True}}

sm_client = local_sagemaker_session.sagemaker_runtime_client

response = sm_client.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType='application/json',
    Body=payload,
)

print("Model response:", response['Body'].read().decode('utf-8'))
