import random

class Stock:
    def __init__(self, symbol, company_name, stock_price, total_owned, dividend_rate=0.0):
        self.symbol = symbol  # Stock symbol (e.g., 'AAPL' for Apple)
        self.company_name = company_name  # Name of the company
        self.stock_price = stock_price  # Current price of the stock
        self.dividend_rate = dividend_rate  # Dividend rate as a percentage
        self.total_owned = total_owned

    def calculate_dividend(self):
        # Calculate the dividend based on the current price and dividend rate
        dividend = self.stock_price * self.dividend_rate / 100
        return dividend


    @staticmethod
    def generate_random_stocks(n):
        symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'FB', 'NFLX', 'NVDA', 'INTC', 'ORCL']
        company_names = ['Apple Inc.', 'Microsoft Corp.', 'Alphabet Inc.', 'Amazon.com Inc.', 'Tesla Inc.',
                         'Meta Platforms, Inc.', 'Netflix, Inc.', 'NVIDIA Corporation', 'Intel Corporation', 'Oracle Corporation']
        stocks = []
        
        for _ in range(n):
            stock_price = random.uniform(100, 1500)  # Random price between 100 and 1500
            total_owned = random.uniform(80, 1500)  # Random price between 100 and 1500
            dividend_rate = random.uniform(0, 5)  # Random dividend rate between 0 and 5%
            index = random.randint(0, len(symbols) - 1)
            stock = Stock(symbol=symbols[index], company_name=company_names[index],
                          stock_price=stock_price, dividend_rate=dividend_rate, total_owned = total_owned)
            stocks.append(stock)
        
        return stocks


    def __str__(self):
        return (f"Stock(symbol={self.symbol}, company_name={self.company_name}, "
                f"stock_price={self.stock_price:.2f}, dividend_rate={self.dividend_rate:.2f}%)")