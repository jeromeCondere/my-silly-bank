from account import Account
from stock import Stock
from verbose_logger import VerboseLogger
import re
from nltk import sent_tokenize

class Chat:

    def __init__(self, name, verbose = False):
        self.name = name
        self.display_chat = []
        self.hidden_chat = []
        self.account = Account(self.name, verbose)
        self.verbose_logger = VerboseLogger(verbose, 'CHAT LOG ->')
        self.messages_to_display = []



    def add_message(self, role, content, message_type = 'question'):

        if message_type == 'response':
            content_split = sent_tokenize(content)
            if len(content_split)>= 2:
                content = ' '.join(content_split[:2])
            else:
                content =  content_split[0]

        message = {'role': role, 'content': content}
        display_messages, hidden_messages = self.get_equivalent_display(message)
        self.display_chat.extend(display_messages)
        self.hidden_chat.append(message)
        self.hidden_chat.extend(hidden_messages)
        self.verbose_logger.print(f'adding  {hidden_messages} and {message} to the hidden chat')
        self.verbose_logger.print(f'adding  {display_messages} to the display chat')
        self.messages_to_display = display_messages


    def get_last_messages_to_display(self):
        return self.messages_to_display



    @staticmethod
    def extract_role_and_content(message_str):
        # Split the string at the first newline
        split_message = message_str.split('\n', 1)
        role = None
        content = None
        
        # Extract the role and content
        role_match = re.search(r'<\|start_header_id\|>(.*?)<\|end_header_id\|>(.*)', message_str, re.DOTALL)
        if role_match:
            role = role_match.group(1)
            content = role_match.group(2)
            content = content.replace("\\n", "\n")
            content = content.replace("\n\n", "")
            content =  content.encode('utf-8').decode('unicode_escape')

        
        return role, content

    @staticmethod
    def get_chat_messages_from_chat_template(chat_template_string):
        messages_templates = chat_template_string.split("<|eot_id|>")
        if messages_templates and messages_templates[-1] == '':
            del messages_templates[-1]  #because the chat in most case ends up with <|eot_id|> it will create an empty string element

        list_role_content = [Chat.extract_role_and_content(x) for x in  messages_templates]
        messages = [{'role':role, 'content': content}  for role, content in list_role_content]
        return messages



    def process_balance(self, messages, hidden_messages):
        if any('###Balance' in message['content'] for message in messages):
            self.account.update_balance()
            messages_to_return = [{ 'role': 'system' ,  'content': message['content'].replace('###Balance', f'{self.account.balance}$') } for message in messages]

            return messages_to_return, hidden_messages
        else:
            return messages, hidden_messages





    def process_withdrawal(self, messages, hidden_messages):
        messages_to_return= []
        once = True
        if any('###AmountWithdrawal' in message['content'] for message in messages):
            for message in messages:
                val_match = re.search(r'###AmountWithdrawal\((\d+(\.\d+)?)\)', message['content'])
                val = 0
                if val_match:
                    val = float(val_match.group(1))
                    message_updated = { 'role': 'system' ,  'content': re.sub(r'###AmountWithdrawal\(\d+(\.\d+)?\)', f'{val}$', message['content']) }
                    messages_to_return.append(message_updated)
                else:
                    messages_to_return.append(message)
                if once:
                    self.account.withdraw(val)
                    once = False
            return messages_to_return, hidden_messages
        else:
            return messages, hidden_messages



    def process_deposit(self, messages, hidden_messages):
        messages_to_return= []
        once = True
        if any('###AmountDeposit' in message['content'] for message in messages):
            for message in messages:
                val_match = re.search(r'###AmountDeposit\((\d+(\.\d+)?)\)', message['content'])
                val = 0
                if val_match:
                    val = float(val_match.group(1))
                    message_updated = { 'role': 'system' ,  'content': re.sub(r'###AmountDeposit\(\d+(\.\d+)?\)', f'{val}$', message['content']) }
                    
                    messages_to_return.append(message_updated)
                else:
                    messages_to_return.append(message)
                if once:
                    self.account.deposit(val)
                    once = False
            return messages_to_return, hidden_messages
        else:
            return messages, hidden_messages


    def process_last_transactions(self, messages, hidden_messages):
        messages_to_return= []
        if any('###LastTransactions' in message['content'] for message in messages):
            for message in messages:
                n_match = re.search(r'###LastTransactions\((\d+)\)', message['content'])
                n = 1
                if n_match:
                    n = int(n_match.group(1))
                    message_updated = { 'role': 'system' ,  'content': re.sub(r'###LastTransactions\((\d+)\)', '', message['content']) }
                    messages_to_return.append(message_updated)

                else:
                    messages_to_return.append(message)

            messages_to_return.append({'role': 'display', 'content': self.account.display_last_n_transactions(n)})
            hidden_messages.append({'role': 'display', 'content': self.account.display_last_n_transactions(n)})

            return messages_to_return, hidden_messages
        else:
            return messages, hidden_messages

    def process_last_transactions_bis(self, messages, hidden_messages):
        messages_to_return= []
        if any('###Transactions' in message['content'] for message in messages):
            for message in messages:
                n_match = re.search(r'###Transactions\((\d+)\)', message['content'])
                n = 1
                if n_match:
                    n = int(n_match.group(1))
                    message_updated = { 'role': 'system' ,  'content': re.sub(r'###Transactions\((\d+)\)', '', message['content']) }
                    messages_to_return.append(message_updated)

                else:
                    messages_to_return.append(message)

            messages_to_return.append({'role': 'display', 'content': self.account.display_last_n_transactions(n)})
            hidden_messages.append({'role': 'display', 'content': self.account.display_last_n_transactions(n)})

            return messages_to_return, hidden_messages
        else:
            return messages, hidden_messages



    def process_list_all_transactions(self, messages, hidden_messages):
        messages_to_return= []
        if any('###Transactions' in message['content'] for message in messages):
            messages_to_return = [{ 'role': 'system' , 'content':  message['content'].replace('###Transactions','') } for message in messages]
            messages_to_return.append({'role': 'display', 'content': self.account.display_transactions()})
            hidden_messages.append({'role': 'display', 'content': self.account.display_transactions()})

            return messages_to_return, hidden_messages

        else:
            return messages, hidden_messages


    def process_list_stocks(self, messages, hidden_messages):
        messages_to_return= []
        if any('###ListStocks' in message['content'] for message in messages):
            messages_to_return = [{ 'role': 'system' , 'content':  message['content'].replace('###ListStocks','') } for message in messages]
            messages_to_return.append({'role': 'display', 'content': self.account.display_stocks()})
            hidden_messages.append({'role': 'display', 'content': self.account.display_stocks()})

            return messages_to_return, hidden_messages

        else:
            return messages, hidden_messages


    def process_buy_stocks(self, messages, hidden_messages):
        messages_to_return= []
        once = True
        if any('###StockValue' in message['content'] and '###Company' in message['content'] for message in messages):
            val_stock_bought = 0
            val_company = 'UNK'
            for message in messages:
                val_stock_match = re.search(r'###StockValue\((\d+(\.\d+)?)\)', message['content'])
                val_company_match = re.search(r'###Company\((.+)\)', message['content'])

                n = 1
                if val_stock_match and val_company:
                    val_stock_bought = float(val_stock_match.group(1))
                    val_company = val_company_match.group(1)
                    replace_stock = re.sub(r'###StockValue\((\d+(\.\d+)?)\)',  f'{val_stock_bought}$', message['content'])
                    replace_company = re.sub(r'###Company\((.+)\)',  val_company, replace_stock)
                    message_updated = { 'role': 'system' ,  'content': re.sub(r'###LastTransactions\((\d+)\)', '', message['content']) }
                    messages_to_return.append(message_updated)

                else:
                    messages_to_return.append(message)

                if once:
                    self.account.buy_stocks(Stock(symbol='UNK', company_name= val_company,total_owned=val_stock_bought, stock_price = None,dividend_rate=0.03))
                    once = False

            return messages_to_return, hidden_messages
        else:
            return messages, hidden_messages




    def get_equivalent_display(self, message):

        result = [message]
        result_hidden = []

        result, result_hidden = self.process_withdrawal(result, result_hidden) 
        result, result_hidden = self.process_deposit(result, result_hidden) 
        result, result_hidden = self.process_last_transactions(result, result_hidden) 
        result, result_hidden = self.process_last_transactions_bis(result, result_hidden) 
        result, result_hidden = self.process_list_all_transactions(result, result_hidden) 
        result, result_hidden = self.process_list_stocks(result, result_hidden) 
        result, result_hidden = self.process_buy_stocks(result, result_hidden) 
        result, result_hidden = self.process_balance(result, result_hidden)

        return result, result_hidden

    @staticmethod
    def get_chat_last_message_from_chat_template(chat_template_string):
        return Chat.get_chat_messages_from_chat_template(chat_template_string)[-1]
    
    def __str__(self):
        display = "Display Chat:\n"
        display += "\n".join([f"{i + 1}. {msg['role']}: {msg['content']}" for i, msg in enumerate(self.display_chat)])
        
        hidden = "Hidden Chat:\n"
        hidden += "\n".join([f"{i + 1}. {msg['role']}: {msg['content']}" for i, msg in enumerate(self.hidden_chat)])
        
        return f"Chat with {self.name}\n\n{display}\n\n{hidden}\n\n{self.account}"



# chat = Chat(name="Alice Smith")

# chat.add_message(role="system", content="Hi Alice Smith, I'm your assistant. How can I help you?")
# chat.add_message(role="user", content="I'd like to withdraw 23.34 from my account.")
# chat.add_message(role="system", content="We have successfully withdrawn ###AmountWithdrawal(23.34) from your account.")
# chat.add_message(role="user", content="I'd like to deposit 5.08 from my account.")
# chat.add_message(role="system", content="We have successfully deposit ###AmountDeposit(5.08) on your account.")
# chat.add_message(role="user", content="Now I want to see my balance, hurry up!")
# chat.add_message(role="system", content="Here's your balance ###Balance")
# chat.add_message(role="user", content="I want to buy 45.44 in FB Inc. .")
# chat.add_message(role="system", content="Sure, we have purchased stocks worth ###StockValue(45.44) in ###Company(FB Inc.) for you.")
# chat.add_message(role="user", content="I want to see my last 2 transactions.")
# chat.add_message(role="system", content="Of course, here’s the list of your last 2 transactions: ###LastTransactions(2)")
# chat.add_message(role="user", content="I want to see all my transactions.")
# chat.add_message(role="system", content="Of course, here’s the list of your transactions: ###Transactions")
# chat.add_message(role="user", content="I want toprint see all my stocks.")
# chat.add_message(role="system", content="Of course, here’s the list of your stocks: ###ListStocks")

# print(chat)
