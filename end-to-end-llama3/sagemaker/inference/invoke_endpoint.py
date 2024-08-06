import boto3
import json
import os


os.environ['HF_TASK'] = "text-generation"
# Initialize the SageMaker runtime client
session = boto3.session.Session(profile_name='profile-admin')
runtime_client = session.client('sagemaker-runtime')

endpoint_name = 'huggingface-model-endpoint-test'
content_type = 'application/json'

txt = """
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Hi Yalat Sensei, I'm your assistant how can I help you<|eot_id|><|start_header_id|>user<|end_header_id|>

I'd like to buy stocks worth 42.24 in Google Corp..<|eot_id|><|start_header_id|>system<|end_header_id|>

Sure, we have purchased stocks worth ###StockValue(42.24) in ###Company(Google Corp.) for you.<|eot_id|><|start_header_id|>user<|end_header_id|>

Now I want to see my balance, hurry up!<|eot_id|><|start_header_id|>system<|end_header_id|>

Sure, here's your balance ###Balance<|eot_id|><|start_header_id|>user<|end_header_id|>

Again, my balance?<|eot_id|><|start_header_id|>system<|end_header_id|>

We have your account details. Your balance is: ###Balance<|eot_id|><|start_header_id|>user<|end_header_id|>

"""

messages=[
    { "role": "system", "content": "You are a helpful assistant." },
    { "role": "user", "content": "What is deep learning?" }
  ]
 
# Generation arguments
parameters = {
    "model": "jeromecondere/merged-llama-v3-for-bank", # placholder, needed
    "top_p": 0.6,
    "temperature": 0.9,
    "max_tokens": 512,
    "stop": ["<|eot_id|>"],
}

data={
    "messages": messages
}

data2 = {
    "inputs": "Replace this with your text input to the model."
}

# Define the input data for the model (example input)
payload = json.dumps(data)

print(f'the payload is really \n\n {payload} \n\n')

# Query the SageMaker endpoint
response = runtime_client.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType=content_type,   # Specify content type (application/json, text/csv, etc.)
    Body=payload                # Input payload for the model
)
# Print the response
print("Model response:", response['Body'].read().decode('utf-8'))
