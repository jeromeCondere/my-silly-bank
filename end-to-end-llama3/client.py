
import time
import sys
import boto3
import json
import os
import argparse
from chat import Chat




def progressive_display(text, delay=0.05):
    """Displays text progressively, one character at a time."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Move to the next line after the text is displayed

def chat_loop(chat,sagemaker_client, endpoint_name):
    print("Welcome to the chat! Type 'exit' to leave.")
    while True:
        user_input = input("User: ")
        user_input = user_input + '\n'
        if user_input.lower() == 'exit':
            progressive_display("Exiting the chat. Goodbye!")
            break
        chat.add_message(role="user", content=user_input)
        payload = json.dumps({
            "messages": chat.hidden_chat
        })

        response = sagemaker_client.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType='application/json',
            Body=payload,
        )
        response_body=response['Body'].read().decode('utf-8').strip('"')
        # we get the last message from the response and add it to the chat
        new_chat_messages = response_body
        new_chat_messages = json.loads(new_chat_messages)

        last_message = chat.get_chat_last_message_from_chat_template(new_chat_messages['response'])


        chat.add_message(role="system", content=last_message['content'], message_type = 'response')

        messages_to_display = chat.get_last_messages_to_display()

        ## we display the messages we need
        for  message in messages_to_display:
            if message['role'] == 'system':
                progressive_display(f"Assistant: {message['content']}")
            elif message['role'] == 'display':
                progressive_display(f"Assistant: {message['content']}", 0.02)
            else:
                progressive_display(f"Assistant: This is a mistake!")


if __name__ == "__main__":
    with open('sagemaker/inference/config_inference.json') as f:
        data = json.load(f)
        region = data['region']
        instance=data['instance']
        profile=data['profile']
        aws_access_key_id=data['aws_access_key_id']
        aws_secret_access_key=data['aws_secret_access_key']
        aws_session_token=data['aws_session_token']
        endpoint_name=data['endpoint_name']

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, default='test', help='running mode')
    args = parser.parse_args()
    print('mode selected ', args.mode)


    first_message = "Hi Alice Smith, I'm your assistant how can I help you?"

    chat = Chat(name="Alice Smith", verbose= False)
    chat.add_message(role="system", content=first_message)
    os.environ['AWS_DEFAULT_REGION'] = region
    progressive_display(f'Assistant:  {first_message}')


    if args.mode == 'test':
        from sagemaker.local import LocalSession

        print('-----------Running test mode--------------')

        os.environ['AWS_ACCESS_KEY_ID']=aws_access_key_id
        os.environ['AWS_SECRET_ACCESS_KEY']=aws_secret_access_key
        os.environ['AWS_SESSION_TOKEN']=aws_session_token

        local_sagemaker_session = LocalSession()
        local_sagemaker_session.config = {"local": {"local_code": True}}
        sagemaker_client = local_sagemaker_session.sagemaker_runtime_client
        chat_loop(chat,sagemaker_client, endpoint_name)

    else:
        print('------------Running normal mode -------------------')
        os.environ['AWS_DEFAULT_PROFILE'] = profile
        session = boto3.session.Session(profile_name=profile)
        sagemaker_client = session.client('sagemaker-runtime')
        chat_loop(chat,sagemaker_client, endpoint_name)

    





