import random
from  itertools import chain
import csv
from utils.transaction import Transaction
from utils.stock import Stock


names = [
	"Alice Johnson", "Bob Smith", "Charlie Brown", "David Wilson", "Emily Davis",
	"Frank Miller", "Grace Lee", "Hannah Moore", "Isaac Taylor", "Jack Anderson",
	"Katherine Thomas", "Liam Jackson", "Mia White", "Nathan Harris", "Olivia Clark",
	"Paul Lewis", "Quinn Martin", "Rachel Walker", "Samuel Young", "Tina Hall",
	"Ursula King", "Victor Adams", "Wendy Scott", "Xander Green", "Yvonne Baker",
	"Zachary Carter", "Anna Mitchell", "Benjamin Robinson", "Chloe Nelson", "Daniel Martinez",
	"Ella Perez", "Fiona Murphy", "George Ramirez", "Helen Rogers", "Ivy Rivera",
	"James Cooper", "Kimberly Phillips", "Leo Campbell", "Monica Foster", "Noah Gray",
	"Oscar Hughes", "Peyton Bryant", "Quincy Powell", "Rebecca Jenkins", "Samantha Stone",
	"Thomas Lee", "Ulysses Grant", "Vanessa Adams", "William King", "Xena Coleman",
	"Yasir Ali", "Zoe Turner"
]
companies = [
	"Apple Inc.",
	"Microsoft Corporation",
	"Amazon.com, Inc.",
	"Google LLC",
	"Facebook, Inc.",
	"Alibaba Group",
	"Tencent Holdings",
	"IBM",
	"Intel Corporation",
	"Oracle Corporation",
	"Samsung Electronics",
	"Sony Corporation",
	"Qualcomm Incorporated",
	"SAP SE",
	"Adobe Systems Incorporated",
	"Salesforce.com",
	"Dell Technologies",
	"Cisco Systems, Inc.",
	"Hewlett Packard Enterprise",
	"NVIDIA Corporation",
	"Twitter, Inc.",
	"Uber Technologies Inc.",
	"Spotify Technology S.A.",
	"Snap Inc.",
	"Dropbox, Inc.",
	"Airbnb, Inc.",
	"Zoom Video Communications",
	"Square, Inc.",
	"Slack Technologies",
	"PayPal Holdings, Inc.",
	"Shopify Inc.",
	"Stripe, Inc.",
	"Uber Technologies",
	"Lyft, Inc.",
	"eBay Inc.",
	"Pinterest, Inc.",
	"Salesforce.com, Inc.",
	"Red Hat, Inc.",
	"ServiceNow, Inc.",
	"Atlassian Corporation Plc",
	"Tesla, Inc.",
	"SpaceX"
]

def get_extract_size(questions, responses):
	return min(len(questions), len(responses)), min(len(questions), len(responses))


class Scenario:

	def __init__(self,scenario, name, company, stock_value, withdraw_amount, deposit_amount, n_last_transactions=5):
		self.name = name  # User object that owns the account
		self.scenario = scenario
		self.company = company
		self.stock_value= stock_value
		self.withdraw_amount = withdraw_amount
		self.deposit_amount =  deposit_amount
		self.n_last_transactions = n_last_transactions


	def random_update(self):
		self.withdraw_amount = round(random.uniform(0, 300), 2)
		self.stock_value = round(random.uniform(0, 10000), 2)
		self.deposit_amount = round(random.uniform(0, 250), 2)
		self.n_last_transactions = random.randint(1, 10)
		self.company  = random.choice(companies)


	## get transaction

	def chat_user_transaction_question(self):
		questions = [
			f"I would like to view my transactions. Can you provide it?\n",
			f"I need to see my transaction history. What does it look like?\n",
			f"Hello, could you show me my transaction history?\n",
			f"Hello, could you show me my transactions?\n",
			f"I would like to check my transaction history. Can you help?\n",
			f"Hi, can you provide my transaction history?\n",
			f"I’d like to review my transaction history. What are the details?\n",
			f"I want to access my transaction history. What does it show?\n",
			f"I’m requesting my transaction history. Can you display it?\n",
			f"Hello, I need to see my transactions. Can you provide them?\n",
			f"I’d like to view my transaction history. What is it?\n",
			f"I wish to access my transaction history. Could you show me?\n",
			f"Greetings, I need to review my transaction history. What’s the status?\n",
			f"Hi, I would appreciate it if you could provide my transaction history.\n",
			f"I am looking to see my transaction history. What is available?\n",
			f"I would like to get my transaction history. What can you tell me?\n",
			f"Hello, can you show me my transaction history?\n",
			f"I want to review my transaction history. Can you assist with that?\n",
			f"I need to check my transaction history. What does it include?\n",
			f"Hi, could you provide me with my transaction history?\n",
			f"I’m seeking my transaction history. What can you provide\n?"
		]
		return {'role':'user', 'content':random.choice(questions)}


	def chat_assistant_transaction_response(self):
		responses = [
			f"We’ve got your transaction history. Here are the details: ###Transactions\n",
			f"We can certainly provide your transaction history. Here it is: ###Transactions\n",
			f"Greetings, your transaction details are ready. Check them out here: ###Transactions\n",
			f"We’ve retrieved your transactions. You can view them below: ###Transactions\n",
			f"Here’s your transaction history as requested: ###Transactions\n",
			f"We have your transaction history. Please find it here: ###Transactions\n",
			f"Your transactions are available. Here’s the full history: ###Transactions\n",
			f"Your transaction details are here. Review them below: ###Transactions\n",
			f"We’ve provided your transaction history. The details are as follows: ###Transactions\n",
			f"We’ve compiled your transactions. Here’s what you need: ###Transactions\n",
			f"Your transaction history is ready. You can view it here: ###Transactions\n",
			f"Greetings, we have your transactions. Here they are: ###Transactions\n",
			f"Here’s a summary of your transaction history: ###Transactions\n",
			f"Your transactions have been prepared. Please see below: ###Transactions\n",
			f"We’ve compiled your transaction history for you. Check it out: ###Transactions\n",
			f"Here’s your transaction information. The details are as follows: ###Transactions\n",
			f"Your transaction history is now available. See it here: ###Transactions\n",
			f"We’ve gathered your transaction details. Here’s the complete list: ###Transactions\n",
			f"Your transaction history is provided below. Please review: ###Transactions\n",
			f"We’ve accessed your transactions. Here’s the full history: ###Transactions\n"
		]
		return {'role':'system', 'content':random.choice(responses)}


	## get last transaction

	def chat_user_last_n_transactions_question(self):
		questions = [
			f"I would like to view my last {self.n_last_transactions} transactions\n",
			f"Can I see my most recent {self.n_last_transactions} transactions?\n",
			f"Please show me the last {self.n_last_transactions} transactions in my account\n",
			f"Could you display my last {self.n_last_transactions} transactions?\n",
			f"I'd like to check my latest {self.n_last_transactions} transactions\n",
		]
		return {'role':'user', 'content':random.choice(questions)}


	def chat_assistant_last_n_transactions_response(self):
		responses = [
			f"Of course, here’s the list of your last {self.n_last_transactions} transactions: ###LastTransactions({self.n_last_transactions})\n",
			f"Sure, here are your most recent {self.n_last_transactions} transactions: ###LastTransactions({self.n_last_transactions})\n",
			f"Certainly! Here’s a summary of your last {self.n_last_transactions} transactions: ###LastTransactions({self.n_last_transactions})\n",
			f"Here's the list of your latest {self.n_last_transactions} transactions: ###LastTransactions({self.n_last_transactions})\n",
			f"No problem, here are the details of your last {self.n_last_transactions} transactions: ###LastTransactions({self.n_last_transactions})\n",
		]
		return {'role':'system', 'content':random.choice(responses)}



	## get balance
	def chat_user_balance_question(self):
		questions = [
			f"Can you provide the current balance for my account?\n",
			f"I need to know the balance of my account. Could you help with that?\n",
			f"Please tell me the balance of my account.\n",
			f"I would like to check my account balance. What is it?\n",
			f"Could you give me the details of my account balance?\n",
			f"I need to find out my account balance. Can you assist?\n",
			f"What is the balance of my account?\n",
			f"Can you provide me with the current balance of my account?\n",
			f"Can you check the balance for my account?\n",
			f"I’m looking for the balance of my account. What is it?\n",
			f"Bro, give me the balance of my account.\n",
			f"Hey, can you tell me how much is in my account?\n",
			f"What’s my account balance looking like?\n",
			f"Yo, can you check my balance real quick?\n",
			f"Can you give me a quick update on my balance?\n",
			f"Mind telling me how much I have in my account?\n",
			f"What’s left in my account right now?\n",
			f"Can you give me my balance update?\n",
			f"Hey, how much money do I have in my account?\n",
			f"Can you let me know my current balance\n?"
		]
		return {'role':'user', 'content':random.choice(questions)}



	def chat_assistant_balance_response(self):
		responses = [
			f"Your account has been located! Your current balance is: ###Balance .\n",
			f"We’ve retrieved your account information. Your balance is: ###Balance .\n",
			f"Greetings, we found your account! Your balance is currently ###Balance .\n",
			f"Hey, your account details are available. The current balance is: ###Balance .\n",
			f"We have your account info. The balance is: ###Balance .\n",
			f"We located your account. The balance right now is: ###Balance .\n",
			f"Dear user, your account has been found. Your balance is: ###Balance .\n",
			f"We have your account details. Your balance is: ###Balance .\n",
			f"Your account is available. Here is your balance: ###Balance .\n",
			f"We’ve accessed your account information. The balance is: ###Balance .\n",
			f"Greetings, we’ve found your account! Your balance is: ###Balance .\n",
			f"We’ve located your account. Your balance is: ###Balance .\n",
			f"Your account is active. Your current balance is: ###Balance .\n",
			f"Dear user, we have accessed your account. The balance is: ###Balance .\n",
			f"Your account details are here. The balance is: ###Balance .\n",
			f"We’ve retrieved your account balance. It is: ###Balance .\n",
			f"Your account is found. The current balance is: ###Balance .\n",
			f"Greetings, your account info is ready. The balance is: ###Balance .\n",
			f"We’ve located your account. Here’s your balance: ###Balance .\n",
			f"Your account has been found. The balance currently is: ###Balance .\n"
		]
		return {'role':'system', 'content':random.choice(responses)}



	## get stocks

	def chat_user_stock_question(self):
		questions = [
			f"Can you provide me with a list of my stocks?\n",
			f"Please give me the details of my stock holdings.\n",
			f"I would like to see a list of the stocks I own.\n",
			f"I need a summary of my stock portfolio. Can you provide it?\n",
			f"Could you show me the list of stocks I currently hold?\n",
			f"I would appreciate it if you could provide my stock list.\n",
			f"Can you give me the list of my current stock investments?\n",
			f"I’d like to review the list of stocks in my portfolio.\n",
			f"I want to access the details of my stock holdings.\n",
			f"Please provide me with the list of all my stocks\n."
		]
		return {'role':'user', 'content':random.choice(questions)}



	def chat_assistant_stock_response(self):
		responses = [
			f"Please find below the detailed list of your stocks: ###ListStocks\n",
			f"Here is a comprehensive overview of your stock holdings: ###ListStocks\n",
			f"We have compiled the following list of your stocks: ###ListStocks\n",
			f"Enclosed is the complete list of your stock investments: ###ListStocks\n",
			f"Please review the following list of your stock portfolio: ###ListStocks\n",
			f"Here is the detailed summary of your stock holdings: ###ListStocks\n",
			f"We have provided the list of your stocks below: ###ListStocks\n",
			f"The following is the complete list of your current stocks: ###ListStocks\n",
			f"Here is the detailed list of your stock assets: ###ListStocks\n",
			f"The following list outlines your stock holdings: ###ListStocks\n",
			f"Here is the list of your stocks: ###ListStocks\n",
			f"Your stock portfolio is as follows: ###ListStocks\n",
			f"We’ve compiled your stock holdings. Here they are: ###ListStocks\n",
			f"Here’s the complete list of your stocks: ###ListStocks\n",
			f"Here is your current stock list: ###ListStocks\n",
			f"Below is the detailed list of your stocks: ###ListStocks\n",
			f"Your stocks are listed here: ###ListStocks\n",
			f"Here’s your stock information: ###ListStocks\n",
			f"You can find your stock list below: ###ListStocks\n",
			f"Here’s an overview of your stock holdings: ###ListStocks\n",
			f"Your stock portfolio is provided here: ###ListStocks\n",
			f"Here is the detailed list of your stocks: ###ListStocks\n"
		]
		return {'role':'system', 'content':random.choice(responses)}


	## withdraw

	def chat_user_withdraw_question(self):
		questions = [
			f"I'd like to withdraw {self.withdraw_amount:.2f} from my account.\n",
			f"Please process a withdrawal of {self.withdraw_amount:.2f} for me.\n",
			f"I need to withdraw {self.withdraw_amount:.2f} from my account.\n",
			f"Can you help me withdraw {self.withdraw_amount:.2f} from my account?\n",
			f"I'd like to withdraw {self.withdraw_amount:.2f}.\n",
			f"I want to take out {self.withdraw_amount:.2f} from my account.\n",
			f"I need to withdraw {self.withdraw_amount:.2f} please.\n",
			f"I need to withdraw {self.withdraw_amount:.2f} from my account.\n",
			f"I'd like to take out {self.withdraw_amount:.2f}.\n",
			f"Can you withdraw {self.withdraw_amount:.2f} for me?\n",
			f"Can I withdraw {self.withdraw_amount:.2f} from my account?\n",
			f"Please help me withdraw {self.withdraw_amount:.2f} from my account.\n",
			f"I'd like to withdraw {self.withdraw_amount:.2f}.\n",
			f"Please process a withdrawal of {self.withdraw_amount:.2f} for me.\n",
			f"I need to take out {self.withdraw_amount:.2f} from my account.\n",
			f"Please withdraw {self.withdraw_amount:.2f} from my account.\n",
			f"I want to withdraw {self.withdraw_amount:.2f} from my account.\n",
			f"Can you process a withdrawal of {self.withdraw_amount:.2f} for me?\n",
			f"I want to take out {self.withdraw_amount:.2f} from my account.\n",
			f"Can I withdraw {self.withdraw_amount:.2f} from my account?\n",
			f"I'd like to withdraw {self.withdraw_amount:.2f} please.\n",
			f"Please help me take out {self.withdraw_amount:.2f} from my account.\n",
			f"Can you withdraw {self.withdraw_amount:.2f} for me?\n",
			f"I need to withdraw {self.withdraw_amount:.2f}.\n",
			f"I'd like to withdraw {self.withdraw_amount:.2f} from my account\n."
		]
		return {'role':'user', 'content':random.choice(questions)}




	def chat_assistant_withdraw_response(self):
		responses = [
			f"Sure, we have withdrawn ###AmountWithdrawal({self.withdraw_amount:.2f}) from your account.\n",
			f"Your request to withdraw ###AmountWithdrawal({self.withdraw_amount:.2f}) has been processed.\n",
			f"We have successfully withdrawn ###AmountWithdrawal({self.withdraw_amount:.2f}) from your account.\n",
			f"The amount of ###AmountWithdrawal({self.withdraw_amount:.2f}) has been withdrawn from your account.\n",
			f"Your account has been debited with ###AmountWithdrawal({self.withdraw_amount:.2f}).\n",
			f"We have processed the withdrawal of ###AmountWithdrawal({self.withdraw_amount:.2f}) from your account.\n",
			f"The withdrawal of ###AmountWithdrawal({self.withdraw_amount:.2f}) from your account is complete.\n",
			f"###AmountWithdrawal({self.withdraw_amount:.2f}) has been deducted from your account as requested.\n",
			f"We have completed your withdrawal of ###AmountWithdrawal({self.withdraw_amount:.2f}).\n",
			f"Your account has been successfully debited with ###AmountWithdrawal({self.withdraw_amount:.2f}).\n",
			f"We have withdrawn ###AmountWithdrawal({self.withdraw_amount:.2f}) from your account as per your request.\n",
			f"Your account has been debited with the amount of ###AmountWithdrawal({self.withdraw_amount:.2f}).\n",
			f"The requested amount of ###AmountWithdrawal({self.withdraw_amount:.2f}) has been withdrawn.\n",
			f"The withdrawal of ###AmountWithdrawal({self.withdraw_amount:.2f}) has been processed successfully.\n",
			f"We have processed the requested withdrawal of ###AmountWithdrawal({self.withdraw_amount:.2f}).\n",
			f"Your account has been charged with ###AmountWithdrawal({self.withdraw_amount:.2f}).\n",
			f"The amount ###AmountWithdrawal({self.withdraw_amount:.2f}) has been withdrawn from your account.\n",
			f"Your account withdrawal of ###AmountWithdrawal({self.withdraw_amount:.2f}) is complete.\n",
			f"We have debited your account with ###AmountWithdrawal({self.withdraw_amount:.2f}) as requested.\n",
			f"The withdrawal of ###AmountWithdrawal({self.withdraw_amount:.2f}) has been completed.\n",
			f"Your account has been debited successfully with ###AmountWithdrawal({self.withdraw_amount:.2f}).\n",
			f"###AmountWithdrawal({self.withdraw_amount:.2f}) has been successfully withdrawn from your account.\n",
			f"We have debited ###AmountWithdrawal({self.withdraw_amount:.2f}) from your account.\n",
			f"The requested withdrawal of ###AmountWithdrawal({self.withdraw_amount:.2f}) has been completed.\n",
			f"The requested amount of ###AmountWithdrawal({self.withdraw_amount:.2f}) has been debited from your account\n."
		]
		return {'role': 'system', 'content': random.choice(responses)}


	### deposit

	def chat_user_deposit_question(self):
		questions = [
			f"I'd like to deposit {self.deposit_amount:.2f} into my account.\n",
			f"Please process a deposit of {self.deposit_amount:.2f} for me.\n",
			f"I need to deposit {self.deposit_amount:.2f} into my account.\n",
			f"Can you help me deposit {self.deposit_amount:.2f} into my account?\n",
			f"I'd like to deposit {self.deposit_amount:.2f}.\n",
			f"I want to put {self.deposit_amount:.2f} into my account.\n",
			f"I need to deposit {self.deposit_amount:.2f} please.\n",
			f"I need to deposit {self.deposit_amount:.2f} into my account.\n",
			f"I'd like to put in {self.deposit_amount:.2f}.\n",
			f"Can you deposit {self.deposit_amount:.2f} for me?\n",
			f"Can I deposit {self.deposit_amount:.2f} into my account?\n",
			f"Please help me deposit {self.deposit_amount:.2f} into my account.\n",
			f"I'd like to deposit {self.deposit_amount:.2f}.\n",
			f"Please process a deposit of {self.deposit_amount:.2f} for me.\n",
			f"I need to put in {self.deposit_amount:.2f} into my account.\n",
			f"Please deposit {self.deposit_amount:.2f} into my account.\n",
			f"I want to deposit {self.deposit_amount:.2f} into my account.\n",
			f"Can you process a deposit of {self.deposit_amount:.2f} for me?\n",
			f"I want to put {self.deposit_amount:.2f} into my account.\n",
			f"Can I deposit {self.deposit_amount:.2f} into my account?\n",
			f"I'd like to deposit {self.deposit_amount:.2f} please.\n",
			f"Please help me put in {self.deposit_amount:.2f} into my account.\n",
			f"Can you deposit {self.deposit_amount:.2f} for me?\n",
			f"I need to deposit {self.deposit_amount:.2f}\n."
		]
		return {'role': 'user', 'content': random.choice(questions)}



	def chat_assistant_deposit_response(self):
		responses = [
			f"Sure, we have deposited ###AmountDeposit({self.deposit_amount:.2f}) into your account.\n",
			f"Your request to deposit ###AmountDeposit({self.deposit_amount:.2f}) has been processed.\n",
			f"We have successfully deposited ###AmountDeposit({self.deposit_amount:.2f}) into your account.\n",
			f"The amount of ###AmountDeposit({self.deposit_amount:.2f}) has been deposited into your account.\n",
			f"Your account has been credited with ###AmountDeposit({self.deposit_amount:.2f}).\n",
			f"We have processed the deposit of ###AmountDeposit({self.deposit_amount:.2f}) into your account.\n",
			f"The deposit of ###AmountDeposit({self.deposit_amount:.2f}) into your account is complete.\n",
			f"###AmountDeposit({self.deposit_amount:.2f}) has been added to your account as requested.\n",
			f"We have completed your deposit of ###AmountDeposit({self.deposit_amount:.2f}).\n",
			f"Your account has been successfully credited with ###AmountDeposit({self.deposit_amount:.2f}).\n",
			f"We have deposited ###AmountDeposit({self.deposit_amount:.2f}) into your account as per your request.\n",
			f"Your account has been credited with the amount of ###AmountDeposit({self.deposit_amount:.2f}).\n",
			f"The requested amount of ###AmountDeposit({self.deposit_amount:.2f}) has been deposited.\n",
			f"The deposit of ###AmountDeposit({self.deposit_amount:.2f}) has been processed successfully.\n",
			f"We have processed the requested deposit of ###AmountDeposit({self.deposit_amount:.2f}).\n",
			f"Your account has been credited with ###AmountDeposit({self.deposit_amount:.2f}).\n",
			f"The amount ###AmountDeposit({self.deposit_amount:.2f}) has been deposited into your account.\n",
			f"Your account deposit of ###AmountDeposit({self.deposit_amount:.2f}) is complete.\n",
			f"We have credited your account with ###AmountDeposit({self.deposit_amount:.2f}) as requested.\n",
			f"The deposit of ###AmountDeposit({self.deposit_amount:.2f}) has been completed.\n",
			f"Your account has been credited successfully with ###AmountDeposit({self.deposit_amount:.2f}).\n",
			f"###AmountDeposit({self.deposit_amount:.2f}) has been successfully deposited into your account.\n",
			f"We have credited ###AmountDeposit({self.deposit_amount:.2f}) into your account.\n",
			f"The requested deposit of ###AmountDeposit({self.deposit_amount:.2f}) has been completed.\n",
			f"The requested amount of ###AmountDeposit({self.deposit_amount:.2f}) has been credited into your account\n."
		]
		return {'role': 'system', 'content': random.choice(responses)}



	## Buy stocks

	def chat_user_buy_stocks_question(self):
		questions = [
			f"I'd like to buy stocks worth {self.stock_value:.2f} in {self.company}.\n",
			f"I am interested in purchasing stocks of {self.company} worth {self.stock_value:.2f}.\n",
			f"I want to invest {self.stock_value:.2f} in {self.company}'s stocks.\n",
			f"I wish to buy {self.stock_value:.2f} worth of {self.company} stocks.\n",
			f"Can you help me buy stocks worth {self.stock_value:.2f} in {self.company}?\n",
			f"I'm looking to buy {self.stock_value:.2f} in stocks of {self.company}.\n",
			f"I'd like to invest {self.stock_value:.2f} in stocks of {self.company}.\n",
			f"I want to purchase {self.stock_value:.2f} worth of stocks in {self.company}.\n",
			f"I want to buy stocks of {self.company} worth {self.stock_value:.2f}.\n",
			f"Can you assist me in buying stocks worth {self.stock_value:.2f} in {self.company}?\n",
			f"I'd like to invest {self.stock_value:.2f} in {self.company} stocks.\n",
			f"I am interested in buying stocks of {self.company} worth {self.stock_value:.2f}.\n",
			f"I wish to buy {self.stock_value:.2f} worth of stocks in {self.company}.\n",
			f"I need assistance to buy stocks worth {self.stock_value:.2f} in {self.company}.\n",
			f"I'm looking to purchase {self.stock_value:.2f} in {self.company} stocks.\n",
			f"Can I invest {self.stock_value:.2f} in stocks of {self.company}?\n",
			f"I am interested in buying {self.stock_value:.2f} worth of stocks in {self.company}.\n",
			f"I want to buy stocks of {self.company} worth {self.stock_value:.2f}.\n",
			f"Can you help me purchase stocks worth {self.stock_value:.2f} in {self.company}?\n",
			f"I need to buy stocks of {self.company} worth {self.stock_value:.2f}.\n",
			f"I'd like to purchase {self.stock_value:.2f} worth of {self.company} stocks.\n",
			f"I want to buy {self.stock_value:.2f} in {self.company} stocks.\n",
			f"Can you assist me in buying stocks of {self.company} worth {self.stock_value:.2f}?\n",
			f"I am looking to invest {self.stock_value:.2f} in {self.company} stocks.\n",
			f"Can I buy stocks worth {self.stock_value:.2f} in {self.company}\n?"
		]
		return {'role': 'user', 'content': random.choice(questions)}



	def chat_assistant_buy_stocks_response(self):
		responses = [
			f"Sure, we have purchased stocks worth ###StockValue({self.stock_value:.2f}) in ###Company({self.company}) for you.\n",
			f"Your request to buy stocks worth ###StockValue({self.stock_value:.2f}) in ###Company({self.company}) has been processed.\n",
			f"We have successfully bought stocks worth ###StockValue({self.stock_value:.2f}) in ###Company({self.company}) for you.\n",
			f"Stocks worth ###StockValue({self.stock_value:.2f}) in ###Company({self.company}) have been purchased for your account.\n",
			f"Your account has been debited with ###StockValue({self.stock_value:.2f}) to buy ###Company({self.company}) stocks.\n",
			f"We have processed the purchase of ###StockValue({self.stock_value:.2f}) worth of ###Company({self.company}) stocks.\n",
			f"The purchase of ###StockValue({self.stock_value:.2f}) worth of ###Company({self.company}) stocks is complete.\n",
			f"###StockValue({self.stock_value:.2f}) has been deducted from your account to buy ###Company({self.company}) stocks.\n",
			f"We have completed your purchase of ###StockValue({self.stock_value:.2f}) worth of ###Company({self.company}) stocks.\n",
			f"Your account has been successfully debited with ###StockValue({self.stock_value:.2f}) to buy ###Company({self.company}) stocks.\n",
			f"We have bought ###StockValue({self.stock_value:.2f}) worth of ###Company({self.company}) stocks as per your request.\n",
			f"Your account has been debited with the amount of ###StockValue({self.stock_value:.2f}) to buy ###Company({self.company}) stocks.\n",
			f"The requested amount of ###StockValue({self.stock_value:.2f}) has been used to purchase ###Company({self.company}) stocks.\n",
			f"The purchase of ###StockValue({self.stock_value:.2f}) worth of ###Company({self.company}) stocks has been processed successfully.\n",
			f"We have processed the requested purchase of ###StockValue({self.stock_value:.2f}) worth of ###Company({self.company}) stocks.\n",
			f"Your account has been charged with ###StockValue({self.stock_value:.2f}) for ###Company({self.company}) stocks.\n",
			f"The amount ###StockValue({self.stock_value:.2f}) has been used to purchase ###Company({self.company}) stocks.\n",
			f"Your stock purchase of ###StockValue({self.stock_value:.2f}) in ###Company({self.company}) is complete.\n",
			f"We have debited your account with ###StockValue({self.stock_value:.2f}) to buy ###Company({self.company}) stocks as requested.\n",
			f"The purchase of ###StockValue({self.stock_value:.2f}) worth of ###Company({self.company}) stocks has been completed.\n",
			f"Your account has been debited successfully with ###StockValue({self.stock_value:.2f}) for ###Company({self.company}) stocks.\n",
			f"###StockValue({self.stock_value:.2f}) has been successfully used to buy ###Company({self.company}) stocks.\n",
			f"We have debited ###StockValue({self.stock_value:.2f}) from your account to purchase ###Company({self.company}) stocks.\n",
			f"The requested purchase of ###StockValue({self.stock_value:.2f}) worth of ###Company({self.company}) stocks has been completed.\n",
			f"The requested amount of ###StockValue({self.stock_value:.2f}) has been used to buy ###Company({self.company}) stocks.\n"
		]
		return {'role': 'system', 'content': random.choice(responses)}


	def greetings(self):
		return {'role': 'system', 'content': f'Hi {self.name}, I\'m your assistant how can I help you?\n'} 


	def display_transactions(self):
		random_number = random.randint(1, 8)
		return {'role': 'display', 'content': "\n".join(str(transaction) for transaction in Transaction.generate_random_transactions(random_number)) +'\n' }


	def display_last_n_transactions(self):
		
		return {'role': 'display', 'content': "\n".join(str(transaction) for transaction in Transaction.generate_random_transactions(self.n_last_transactions)) +'\n' }


	def display_stocks(self):
		random_number = random.randint(1, 8)
		return {'role': 'display', 'content': "\n".join(str(stock) for stock in Stock.generate_random_stocks(random_number)) }


	def to_scen(self):
		res = []

		for step in self.scenario:
			dict_conv = {
				'greetings': self.greetings(),
				'transaction_question': self.chat_user_transaction_question(),
				'transaction_response': self.chat_assistant_transaction_response(),
				'balance_question': self.chat_user_balance_question(),
				'balance_response': self.chat_assistant_balance_response(),
				'stock_question': self.chat_user_stock_question(),
				'stock_response': self.chat_assistant_stock_response(),
				'withdraw_question': self.chat_user_withdraw_question(),
				'withdraw_response': self.chat_assistant_withdraw_response(),
				'deposit_question': self.chat_user_deposit_question(),
				'deposit_response': self.chat_assistant_deposit_response(),
				'buy_stocks_question': self.chat_user_buy_stocks_question(),		
				'buy_stocks_response': self.chat_assistant_buy_stocks_response(),
				'display_stocks': self.display_stocks(),
				'display_transactions': self.display_transactions(),
				'last_n_transactions_question': self.chat_user_last_n_transactions_question(),
				'last_n_transactions_response': self.chat_assistant_last_n_transactions_response(),
				'display_last_n_transactions': self.display_last_n_transactions()
			}
			res.append(dict_conv[step])
			if step in ['display_stocks', 'display_transactions', 'buy_stocks_response', 'withdraw_response','deposit_response','display_last_n_transactions']:
				self.random_update()


		return res




def generate_training_data(filename, total_size_amounts = 3, total_size_names = 15, total_size_companies = 8):
	import json
	result = []
	list_names_randomized = random.sample(names, total_size_names)
	list_companies_randomized = random.sample(companies, total_size_companies)


	with open(filename, mode='w', newline='') as file:
		writer = csv.DictWriter(file, fieldnames=["messages"])
		writer.writeheader()

		scenario1 = ['greetings','transaction_question','transaction_response', 'display_transactions']
		scenario2 = ['greetings','balance_question','balance_response']
		scenario3 = ['greetings','stock_question','stock_response', 'display_stocks']
		scenario4 = ['greetings','withdraw_question','withdraw_response']
		scenario5 = ['greetings','deposit_question','deposit_response']
		scenario6 = ['greetings','buy_stocks_question','buy_stocks_response']


	with open(filename, mode='w', newline='') as file:
		writer = csv.DictWriter(file, fieldnames=["messages"])
		writer.writeheader()

		conversation_get_transactions = ['transaction_question','transaction_response', 'display_transactions']
		conversation_get_balance = ['balance_question','balance_response']
		conversation_get_stocks = ['stock_question','stock_response', 'display_stocks']
		conversation_withdraw = ['withdraw_question','withdraw_response']
		conversation_deposit = ['deposit_question','deposit_response']
		conversation_buy_stocks = ['buy_stocks_question','buy_stocks_response']
		conversation_get_last_transactions = ['last_n_transactions_question','last_n_transactions_response','display_last_n_transactions']

		greetings = ['greetings']

		conv1 = greetings + conversation_get_balance + conversation_get_transactions + conversation_withdraw
		conv2 = greetings + conversation_get_balance + conversation_get_balance + conversation_withdraw
		conv3 = greetings+ conversation_get_balance + conversation_buy_stocks +  conversation_deposit + conversation_get_balance

		# Greeting, Checking Balance, Buying Stocks, Depositing Funds, and Checking Transactions
		conv4 = greetings + conversation_get_balance + conversation_buy_stocks + conversation_get_last_transactions + conversation_deposit + conversation_get_transactions

		# Greeting, Checking Balance, Withdrawing Funds, Checking Stock Information, and Displaying Transactions
		conv5 = greetings + conversation_get_balance + conversation_withdraw + conversation_get_stocks + conversation_get_transactions

		# Greeting, Checking Balance, Buying Stocks, Withdrawing Funds, and Displaying Balance and Transactions
		conv6 = greetings + conversation_get_balance + conversation_buy_stocks + conversation_withdraw + conversation_get_balance + conversation_get_transactions

		# Greeting, Depositing Funds, Checking Balance, Buying Stocks, and Displaying Stock Information and Transactions
		conv7 = greetings + conversation_deposit + conversation_get_balance + conversation_buy_stocks + conversation_get_last_transactions +conversation_get_stocks + conversation_get_transactions

		# Greeting, Checking Balance, Withdrawing Funds, Buying Stocks, Depositing Funds, and Displaying Stock Information and Transactions
		conv8 = greetings + conversation_get_balance + conversation_withdraw + conversation_buy_stocks + conversation_deposit + conversation_get_stocks + conversation_get_transactions
		conv9 = greetings  + conversation_withdraw + conversation_buy_stocks + conversation_deposit + conversation_get_balance +conversation_get_stocks + conversation_get_transactions
		conv10 = greetings   + conversation_buy_stocks  + conversation_get_last_transactions +conversation_get_balance + conversation_get_transactions + conversation_get_last_transactions




		stock_value = round(random.uniform(0, 7000), 2) 
		withdraw_amount = round(random.uniform(0, 340), 2)
		deposit_amount = round(random.uniform(0, 200), 2)

		for name in list_names_randomized:
			for company in list_companies_randomized:
				for i in range(3):
					writer.writerow( {'messages': json.dumps(Scenario(conv1, name, company, stock_value, withdraw_amount,deposit_amount).to_scen() ) } )
					writer.writerow( {'messages': json.dumps(Scenario(conv2, name, company, stock_value, withdraw_amount,deposit_amount).to_scen() ) } )
					writer.writerow( {'messages': json.dumps(Scenario(conv3, name, company, stock_value, withdraw_amount,deposit_amount).to_scen() ) } )
					writer.writerow( {'messages': json.dumps(Scenario(conv4, name, company, stock_value, withdraw_amount,deposit_amount).to_scen() ) } )
					writer.writerow( {'messages': json.dumps(Scenario(conv5, name, company, stock_value, withdraw_amount,deposit_amount).to_scen() ) } )
					writer.writerow( {'messages': json.dumps(Scenario(conv6, name, company, stock_value, withdraw_amount,deposit_amount).to_scen() ) } )
					writer.writerow( {'messages': json.dumps(Scenario(conv7, name, company, stock_value, withdraw_amount,deposit_amount).to_scen() ) } )
					writer.writerow( {'messages': json.dumps(Scenario(conv8, name, company, stock_value, withdraw_amount,deposit_amount).to_scen() ) } )
					writer.writerow( {'messages': json.dumps(Scenario(conv9, name, company, stock_value, withdraw_amount,deposit_amount).to_scen() ) } )
					writer.writerow( {'messages': json.dumps(Scenario(conv10, name, company, stock_value, withdraw_amount,deposit_amount).to_scen() ) } )
			print('name finished')





# scenario1 = ['deposit_question','deposit_response','deposit_question','deposit_response','deposit_question','deposit_response']
# print(Scenario(scenario1, 'ioj', 'company', 22,42,7).to_scen())
generate_training_data('training.csv', total_size_amounts = 3, total_size_names = 10, total_size_companies = 8)
