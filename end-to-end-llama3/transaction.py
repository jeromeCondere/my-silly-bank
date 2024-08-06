from datetime import datetime
import uuid
import random

class Transaction:
    def __init__(self, amount, transaction_type, comment = None):
        self.id = uuid.uuid4()  # Unique identifier for the transaction
        self.amount = amount
        self.transaction_type = transaction_type  # 'deposit' or 'withdrawal'
        self.date = datetime.now()  # Timestamp of the transaction
        self.comment = comment

    @staticmethod
    def generate_random_transactions(num_transactions):
        transactions = []
        for _ in range(num_transactions):
            amount = round(random.uniform(10, 1000), 2)  # Random amount between 10 and 1000
            transaction_type = random.choice(['deposit', 'withdrawal'])  # Randomly choose between 'deposit' and 'withdrawal'
            transaction = Transaction(amount, transaction_type)
            transactions.append(transaction)
        return transactions

    def __str__(self):
        if self.comment is None:
            return f"Transaction(id={self.id}, amount={self.amount}, type={self.transaction_type}, date={self.date})"
        else:
            return f"Transaction(id={self.id}, amount={self.amount}, type={self.transaction_type}, date={self.date}, comment='{self.comment}')"
