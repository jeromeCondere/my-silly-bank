import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from os import listdir
from os.path import isfile, join


def update_nvidia_driver():
	import subprocess
	# Must add this otherwise, torch._six error
	subprocess.run(["pip", "uninstall", "-y",  "apex"])


def model_fn(model_dir, context=None):
	# Load the model and tokenizer from the model directory
	onlyfiles = [f for f in listdir(model_dir) if isfile(join(model_dir, f))]
	print(f'Loading model in {model_dir}')
	print('files:')
	print(onlyfiles)
	
	import subprocess
	# Must add this otherwise, torch._six error
	subprocess.run(["pip", "uninstall", "-y",  "apex"])


	model_name = "jeromecondere/merged-llama-v3-for-bank"
	model_name = 'llamafactory/tiny-random-Llama-3'

	# model = AutoModelForCausalLM.from_pretrained(
	# model_name,
	# torch_dtype=torch.bfloat16,
	# device_map= "cuda"
	# )
	tokenizer = AutoTokenizer.from_pretrained(model_name)
	print('Model finished to load')
	model = 'emfrepomrfp'
	wait(63)
	return model, tokenizer

def input_fn(request_body, request_content_type):
	# Preprocess input data for the model
	print('-------------body: ', str(request_body))
	print('-------------content type: ', request_content_type)
	if request_content_type.strip() == 'application/json':
		data = json.loads(request_body)
		inputs = data['messages']
		print('input_fn finished')
		return inputs
	else:
		raise ValueError("Unsupported content type: {}".format(request_content_type))

def predict_fn(input_data, model_and_tokenizer, context=None):
	# Perform prediction
	model, tokenizer = model_and_tokenizer
	# input_ids = tokenizer.apply_chat_template(input_data, truncation=True, add_generation_prompt=True, return_tensors="pt").to("cuda")
	input_ids = tokenizer.apply_chat_template(input_data, tokenize=False)
	# outputs = model.generate(
	# 	input_ids=input_ids,
	# 	max_new_tokens=120,
	# 	#do_sample=True,
	# 	temperature=0.5,
	# 	top_k=50,
	# 	top_p=0.95
	# )
	print('------------- transformed input_data: ', str(input_ids))

	print('starting to predict')
	# prediction = {'response': tokenizer.batch_decode(outputs)[0]}
	txt1="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Hi Alice Smith, I'm your assistant how can I help you?<|eot_id|><|start_header_id|>user<|end_header_id|>

I'd like to buy stocks worth 42.24 in Google Corp..<|eot_id|>"""

	txt1_response ="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Hi Alice Smith, I'm your assistant how can I help you?<|eot_id|><|start_header_id|>user<|end_header_id|>

I'd like to buy stocks worth 42.24 in Google Corp..<|eot_id|><|start_header_id|>system<|end_header_id|>

Sure, we have purchased stocks worth ###StockValue(42.24) in ###Company(Google Corp.) for you.<|eot_id|>"""
	txt2="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Hi Alice Smith, I'm your assistant how can I help you?<|eot_id|><|start_header_id|>user<|end_header_id|>

I'd like to buy stocks worth 42.24 in Google Corp..<|eot_id|><|start_header_id|>system<|end_header_id|>

Sure, we have purchased stocks worth ###StockValue(42.24) in ###Company(Google Corp.) for you.<|eot_id|><|start_header_id|>user<|end_header_id|>

Now I want to see my balance, hurry up!<|eot_id|>"""

	txt2_response="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Hi Alice Smith, I'm your assistant how can I help you?<|eot_id|><|start_header_id|>user<|end_header_id|>

I'd like to buy stocks worth 42.24 in Google Corp..<|eot_id|><|start_header_id|>system<|end_header_id|>

Sure, we have purchased stocks worth ###StockValue(42.24) in ###Company(Google Corp.) for you.<|eot_id|><|start_header_id|>user<|end_header_id|>

Now I want to see my balance, hurry up!<|eot_id|><|start_header_id|>system<|end_header_id|>

Sure, here's your balance ###Balance<|eot_id|>"""



	txt3 = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Hi Alice Smith, I'm your assistant how can I help you?<|eot_id|><|start_header_id|>user<|end_header_id|>

I'd like to buy stocks worth 42.24 in Google Corp..<|eot_id|><|start_header_id|>system<|end_header_id|>

Sure, we have purchased stocks worth ###StockValue(42.24) in ###Company(Google Corp.) for you.<|eot_id|><|start_header_id|>user<|end_header_id|>

Now I want to see my balance, hurry up!<|eot_id|><|start_header_id|>system<|end_header_id|>

Sure, here's your balance ###Balance<|eot_id|><|start_header_id|>user<|end_header_id|>

I would like to check my transaction history. Can you help?<|eot_id|>"""

	txt3_response = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Hi Alice Smith, I'm your assistant how can I help you?<|eot_id|><|start_header_id|>user<|end_header_id|>

I'd like to buy stocks worth 42.24 in Google Corp..<|eot_id|><|start_header_id|>system<|end_header_id|>

Sure, we have purchased stocks worth ###StockValue(42.24) in ###Company(Google Corp.) for you.<|eot_id|><|start_header_id|>user<|end_header_id|>

Now I want to see my balance, hurry up!<|eot_id|><|start_header_id|>system<|end_header_id|>

Sure, here's your balance ###Balance<|eot_id|><|start_header_id|>user<|end_header_id|>

I would like to check my transaction history. Can you help?<|eot_id|><|start_header_id|>system<|end_header_id|>

Your transactions have been prepared. Please see below: ###Transactions<|eot_id|>"""



	txt4 = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Hi Alice Smith, I'm your assistant how can I help you?<|eot_id|><|start_header_id|>user<|end_header_id|>

I'd like to buy stocks worth 42.24 in Google Corp..<|eot_id|><|start_header_id|>system<|end_header_id|>

Sure, we have purchased stocks worth ###StockValue(42.24) in ###Company(Google Corp.) for you.<|eot_id|><|start_header_id|>user<|end_header_id|>

Now I want to see my balance, hurry up!<|eot_id|><|start_header_id|>system<|end_header_id|>

Sure, here's your balance ###Balance<|eot_id|><|start_header_id|>user<|end_header_id|>

I would like to check my  last 4 transactions. Can you help?<|eot_id|>"""


	txt4_response = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Hi Alice Smith, I'm your assistant how can I help you?<|eot_id|><|start_header_id|>user<|end_header_id|>

I'd like to buy stocks worth 42.24 in Google Corp..<|eot_id|><|start_header_id|>system<|end_header_id|>

Sure, we have purchased stocks worth ###StockValue(42.24) in ###Company(Google Corp.) for you.<|eot_id|><|start_header_id|>user<|end_header_id|>

Now I want to see my balance, hurry up!<|eot_id|><|start_header_id|>system<|end_header_id|>

Sure, here's your balance ###Balance<|eot_id|><|start_header_id|>user<|end_header_id|>

I would like to check my  last 4 transactions. Can you help?<|eot_id|><|start_header_id|>system<|end_header_id|>

No problem, here are the details of your last 4 transactions: ###LastTransactions(4)<|eot_id|>"""




	txt_default_response="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Hi Alice Smith, I don't understand you<|eot_id|>"""


	if input_ids == txt1:
		prediction=txt1_response
	elif input_ids==txt2:
		prediction=txt2_response
	elif input_ids==txt3:
		prediction=txt3_response
	elif input_ids==txt4:
		prediction=txt4_response
	else:
		prediction=txt_default_response

	return prediction

def output_fn(prediction, content_type, context=None):
    # Post-process the output from the model
    return json.dumps(prediction)