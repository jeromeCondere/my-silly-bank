import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from os import listdir
from os.path import isfile, join
from huggingface_hub import snapshot_download
import os

def model_fn(model_dir, context=None):
	# Load the model and tokenizer from the model directory
	onlyfiles = [f for f in listdir(model_dir) if isfile(join(model_dir, f))]
	print(f'Loading model in {model_dir}')
	print('files:')
	print(onlyfiles)


	model_name = "jeromecondere/merged-llama-v3-for-bank"


	print(f'Model to load is {model_name}')
	model = AutoModelForCausalLM.from_pretrained(
	model_name,
	torch_dtype=torch.bfloat16,
	device_map= "cuda"
	)

	print(f'Tokenizer to load comes from {model_name}')

	tokenizer = AutoTokenizer.from_pretrained(model_name)
	print('Model finished to load')
	print('Model loaded is ', model_name)
	return model, tokenizer

def input_fn(request_body, request_content_type):
	# Preprocess input data for the model
	if request_content_type.strip() == 'application/json':
		data = json.loads(request_body)
		inputs = data['messages']
		return inputs
	else:
		raise ValueError("Unsupported content type: {}".format(request_content_type))

def predict_fn(input_data, model_and_tokenizer, context=None):
	# Perform prediction
	model, tokenizer = model_and_tokenizer
	print('Input data is ', str(input_data))
	print('Converting to tensor ')

	input_ids = tokenizer.apply_chat_template(input_data, truncation=True, add_generation_prompt=True, return_tensors="pt").to("cuda")
	outputs = model.generate(
		input_ids=input_ids,
		max_new_tokens=25,
		temperature=0.5,
		top_k=50,
		top_p=0.95
	)
	prediction = {'response': tokenizer.batch_decode(outputs)[0]}
	return prediction

def output_fn(prediction, content_type, context=None):
	print('returning results')
	print('prediction is: ')
	print(prediction)
	# Post-process the output from the model
	return json.dumps(prediction)
