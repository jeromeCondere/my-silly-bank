
### Database Overview

This schema describes the structure for a simple banking system, including tables for users, accounts, transactions, and stocks.
1. Users Table

Stores information about users who own accounts and stocks.
Columns:

    id: Unique identifier for the user.
    name: The full name of the user.
    email: The user's email address (must be unique).

2. Accounts Table

Stores information about user accounts, including balances and associated limits.
Columns:

    id: Unique identifier for the account.
    owner_id: References the id in the users table (foreign key).
    balance: The current balance of the account.
    overdraft_limit: The overdraft limit for the account.
    interest_rate: The interest rate applied to the account balance.

Foreign Key:

    owner_id references users(id).

3. Transactions Table

Records each transaction made on an account, whether deposit or withdrawal.
Columns:

    id: A unique identifier for the transaction (UUID).
    account_id: References the id in the accounts table (foreign key).
    amount: The amount of money involved in the transaction.
    transaction_type: Type of transaction, e.g., deposit or withdrawal.
    comment: A comment associated with the transaction (optional).
    created_at: The timestamp when the transaction was created.

Foreign Key:

    account_id references accounts(id).

4. Stocks Table

Stores information about stocks owned by users, including stock symbols, prices, and ownership details.
Columns:

    id: Unique identifier for the stock entry.
    symbol: The stock's ticker symbol (e.g., AAPL, GOOGL).
    company_name: The name of the company the stock belongs to.
    stock_price: The price of one unit of the stock (nullable).
    dividend_rate: The dividend rate for the stock.
    total_owned: The total number of stocks owned by the user.
    owner_id: References the id in the users table (foreign key).

Foreign Key:

    owner_id references users(id).



