from transaction import Transaction
from stock import Stock
from db_connector import BankDBConnector
from verbose_logger import VerboseLogger

class Account:
    def __init__(self, owner, verbose = False):
        self.owner = owner
        self.balance =0.0

        self.bank_db_connector = BankDBConnector()

        self.id =  self.bank_db_connector.get_account_id_by_user_name(owner)
        self.update_balance()
        self.update_interest_rate()
        self.update_overdraft_limit()
        self.verbose_logger = VerboseLogger(verbose, 'ACCOUNT LOG ->')


    def add_transaction(self, transaction):
        self.update_balance()
        if transaction.transaction_type == 'withdrawal' and self.balance - transaction.amount < -self.overdraft_limit:
            self.verbose_logger.print("Withdrawal denied. Overdraft limit reached.")
        else:
            # self.transactions.append(transaction)  # Add a transaction to the account
            self.update_balance()  # Update balance after adding a transaction
            self.verbose_logger.print("Adding transaction ", transaction, ' for owner ', self.owner)


    def withdraw(self,amount):
        # self.add_transaction(Transaction(-amount, 'withdrawal'))
        self.bank_db_connector.withdraw_money(self.owner, amount)
        self.verbose_logger.print(f'Withdrawing  {amount} for owner {self.owner}')

    def deposit(self,amount):
        # self.add_transaction(Transaction(amount, 'deposit'))
        self.bank_db_connector.deposit_money(self.owner, amount)
        self.update_balance()
        self.verbose_logger.print(f'Depositing  {amount} for owner {self.owner}')


    def buy_stocks(self,stock,comment = None):
        # self.add_transaction(Transaction(-amount, 'buy_stotransactionsck', comment))
        self.bank_db_connector.withdraw_money(self.owner, stock.total_owned, 'buy_stocks' , comment= f'buying stocks for  {stock.company_name}')
        self.bank_db_connector.add_stock_for_user( self.owner, stock.company_name, stock.total_owned)
        self.update_balance()
        self.verbose_logger.print(f'Buying stock (amount: {stock.total_owned}) from company_name {stock.company_name}   for owner  {self.owner}')




    def update_balance(self):
        # self.balance = round(sum(
        #     transaction.amount for transaction in self.transactions
        # ), 2)
        self.balance = self.bank_db_connector.get_balance_by_user_name(self.owner)

    def update_overdraft_limit(self):
        # self.balance = round(sum(
        #     transaction.amount for transaction in self.transactions
        # ), 2)
        self.overdraft_limit = self.bank_db_connector.get_overdraft_limit_by_user_name(self.owner)

    def update_interest_rate(self):
        # self.balance = round(sum(
        #     transaction.amount for transaction in self.transactions
        # ), 2)
        self.interest_rate = self.bank_db_connector.get_interest_rate_by_user_name(self.owner)



    def calculate_total_dividends(self):
        total_dividends = sum(stock.calculate_dividend() for stock in self.stocks)
        return total_dividends

    def  stock_interest(self):
        interest = self.calculate_interest()
        if interest > 0:
            interest_transaction = Transaction(interest, 'deposit')
            self.add_transaction(interest_transaction)
            print(f"Interest applied: {interest:.2f}")

    def get_last_n_transactions(self, n):
        last_n_transactions = self.bank_db_connector.get_last_n_transactions_by_user(self.owner, n)
        return  [Transaction(x['amount'], x['transaction_type'], x['comment']) for x in last_n_transactions]

    def get_transactions(self):
        transactions = self.bank_db_connector.get_transactions_by_user(self.owner)
        return  [Transaction(x['amount'], x['transaction_type'], x['comment']) for x in transactions]

    def get_stocks(self):
        transactions = self.bank_db_connector.get_stocks_by_user(self.owner)
        return  [Stock(x['symbol'], x['company_name'], x['stock_price'], x['dividend_rate']) for x in  self.bank_db_connector.get_stocks_by_user(self.owner)]


    def display_last_n_transactions(self, n):
        last_n_transactions =  self.get_last_n_transactions(n)
        return "\n".join(str(transaction) for transaction in last_n_transactions) + "\n"

    def display_transactions(self):
        all_transaction = self.get_transactions()
        return "\n".join(str(transaction) for transaction in all_transaction) + "\n"

    def display_stocks(self):
        all_stock = self.get_stocks()
        return "\n".join(str(stock) for stock in all_stock) + "\n"

    def print_transactions(self):
        print("Transactions:")
        for transaction in self.transactions:
            print(transaction)

    def print_stocks(self):
        print("Stocks:")
        for stock in self.stocks:
            print(stock)

    def __str__(self):
        return (f"Account(owner={self.owner}, account_id={self.id}, balance={self.balance:.2f}, "
                f"overdraft_limit={self.overdraft_limit:.2f}, interest_rate={self.interest_rate:.2f}%, "
                f"transactions={len(self.get_transactions())}, stocks={len(self.get_stocks())})")
