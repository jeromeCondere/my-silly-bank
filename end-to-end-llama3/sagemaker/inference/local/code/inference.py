import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from os import listdir
from os.path import isfile, join
from time import sleep



def model_fn(model_dir, context=None):
	# Load the model and tokenizer from the model directory
	onlyfiles = [f for f in listdir(model_dir) if isfile(join(model_dir, f))]
	print(f'Loading model in {model_dir}')
	print('files:')
	print(onlyfiles)
	
	import subprocess
	# Must add this otherwise, torch._six error

	model_name = "jeromecondere/merged-llama-v3-for-bank"
	model_name = 'llamafactory/tiny-random-Llama-3'

	model = AutoModelForCausalLM.from_pretrained(
	model_name,
	torch_dtype=torch.bfloat16,
	device_map= "cuda"
	)
	tokenizer = AutoTokenizer.from_pretrained(model_name)
	print('Model finished to load')
	# model = 'model'
	
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
	# input_ids = tokenizer.apply_chat_template(input_data, truncation=True, add_generation_prompt=True, return_tensors="pt").to("cuda")

	# outputs = model.generate(
	# 	input_ids=input_ids,
	# 	max_new_tokens=35,
	# 	#do_sample=True,
	# 	temperature=0.5,
	# 	top_k=50,
	# 	top_p=0.95
	# )

	# prediction = {'response': tokenizer.batch_decode(outputs)[0]}



# 	print('------------- transformed input_data: ', str(input_ids))
	print('starting to predict')
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

	le1="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Hi Alice Smith, I'm your assistant how can I help you?<|eot_id|><|start_header_id|>user<|end_header_id|>

1<|eot_id|>"""


	le1_response="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

The amount ###AmountWithdrawal(3) has been withdrawn from your account. Your new balance is: ###Balance. We have debited ###AmountWithdrawal(3) from your account. The new balance is: ###Balance. Your account has been debited with ###AmountWithdrawal(3). The balance is now ###Balance. Your account has been charged with ###AmountWithdrawal(3). The new balance is: ###Balance. The withdrawal of ###AmountWithdrawal(3) has been processed. The balance is now ###Balance. The amount ###AmountWithdrawal(3) has<|eot_id|>"""

	le1_response="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

The amount ###LastTransactions(45) has been withdrawn from your account. Your new balance is: ###Balance. Now here the list of your transactions ###Transactions"""

	le1_response="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

The amount ###AmountDeposit(224) has been deposited on your account. Your new balance is: ###Balance. Now here the list of your last 3 transaction ###LastTransactions(3)"""

# 	le1_response="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

# Your new balance is: ###Balance. Now here the list of your stocks ###ListStocks"""

# 	le1_response="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

# Buying ###StockValue(3)  in ###Company(Google Inc.). Your new balance is: ###Balance."""

# 	le1_response="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

# Here\'s the list of your last 5 transactions: ###LastTransactions(5)"""

# 	le1_response="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

# Your account has been debited with ###StockValue(455.23) to buy ###Company(Yocata.com) stocks. The current stock price is ###StockPrice(116.50). Your stock portfolio is now: ###ListStocks. ```Stock(symbol=GOOGL, company_name=Alphabet Inc., current_price=1332.81, dividend_rate=0.63%) Stock(symbol=GOOGL, company_name=Alphabet Inc., current_price=1066.41, dividend_rate=1.13%) Stock(symbol=AMZN, company_name=Amazon.com"}<|eot_id|><|start_header_id|>display<|end_header_id|>\n\nStock(symbol=AAPL, company_name=Apple Inc., stock_price=150.00, dividend_rate=0.00%)\nStock(symbol=GOOGL, company_name=Alphabet Inc., stock_price=2800.00, dividend_rate=0.00%)"""


	if input_ids == txt1:
		prediction=txt1_response
	elif input_ids==txt2:
		prediction=txt2_response
	elif input_ids==txt3:
		prediction=txt3_response
	elif input_ids==txt4:
		prediction=txt4_response
	elif input_ids==le1:
		prediction=le1_response
	else:
		prediction=txt_default_response

	return prediction

def output_fn(prediction, content_type, context=None):
    # Post-process the output from the model
    yokata =  {'response': "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nHi Alice Smith, I'm your assistant how can I help you?<|eot_id|><|start_header_id|>user<|end_header_id|>\n\nlast 2 transactions<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\nHere's the list of your latest 2 transactions: ###Transactions(2)<|eot_id|>"}
    # yokata = {'response': '<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nHi Alice Smith, I\'m your assistant how can I help you?<|eot_id|><|start_header_id|>user<|end_header_id|>\n\nHi I just want my balance<|eot_id|><|start_header_id|>system<|end_header_id|>\n\nYour account has been located! Your current balance is: ###Balance. ###Balance. We have your account info. ###Balance. Your account has been found. The balance is: ###Balance. ###Balance. Your account is active. Your current balance is: ###Balance. ###Balance. Your account has been located! The balance is: ###Balance. ###Balance. We have your account details. The balance is: ###Balance. ###Balance. Your account has been located! The balance is: ###Balance. ###Balance. Your account has been found. The balance is: ###Balance. ###"}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\nNow I want to withdraw 45$<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\nYour account has been debited successfully with ###AmountWithdrawal(45). The current balance is: ###Balance. ###AmountWithdrawal(45) has been deducted from your account as requested. Your new balance is: ###Balance. We have processed the withdrawal of ###AmountWithdrawal(45) from your account. The balance is now ###Balance. We have withdrawn ###AmountWithdrawal(45) from your account as per your request. Your account is now active. Your balance is: ###Balance. ###AmountWithdrawal(45) has been deducted from your account. The new balance is'}
    yokata = {'response': prediction}
    return json.dumps(yokata)