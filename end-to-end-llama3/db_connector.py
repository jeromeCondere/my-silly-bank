import mariadb
from mariadb import Error
from transaction import Transaction
from stock import Stock

u= 'oinono'

class BankDBConnector:
    def __init__(self, host='127.0.0.1', database='bank', user='bank_owner', password='password'):
        self.connection = self.connect_to_database(host, database, user, password)

    def is_connected(self, connection):
        try:
            connection.ping()
        except:
            return False
        return True

    def connect_to_database(self, host, database, user, password):
        try:
            connection = mariadb.connect(
                user=user,
                password=password,
                host=host,
                port=3306,
                database=database
            )
            if self.is_connected(connection):
                print("Successfully connected to the database")
                return connection
            else:
                raise Exception("no connection made to the db") 
        except Error as e:
            print(f"Error while connecting to transactiondatabase: {e}")
            return None


    def get_last_n_transactions_by_user(self, user_name, n):
        query = f"""
            SELECT t.* 
            FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            JOIN users u ON a.owner_id = u.id
            WHERE u.name = ?
            ORDER BY t.created_at DESC
            LIMIT ?;
        """
        return self.execute_query_with_params(query, (user_name, n))

    def get_transactions_by_user(self, user_name):
        query = f"""
            SELECT t.* 
            FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            JOIN users u ON a.owner_id = u.id
            WHERE u.name = ?
            ORDER BY t.created_at DESC;
        """
        return self.execute_query_with_params(query, (user_name, ))


    def get_balance_by_user_name(self, user_name):
        account_id = self.get_account_id_by_user_name(user_name)
        query = f"SELECT balance FROM accounts WHERE id = ?;"
        result = self.execute_query_with_params(query, (account_id,))
        return result[0]['balance'] if result else None


    def get_overdraft_limit_by_user_name(self, user_name):
        account_id = self.get_account_id_by_user_name(user_name)
        query = f"SELECT overdraft_limit FROM accounts WHERE id = ?;"
        result = self.execute_query_with_params(query, (account_id,))
        return result[0]['overdraft_limit'] if result else None


    def get_interest_rate_by_user_name(self, user_name):
        account_id = self.get_account_id_by_user_name(user_name)
        query = f"SELECT interest_rate FROM accounts WHERE id = ?;"
        result = self.execute_query_with_params(query, (account_id,))
        return result[0]['interest_rate'] if result else None



    def deposit_money(self, user_name, amount, comment=None):
        account_id = self.get_account_id_by_user_name(user_name)
        if account_id:
            # Update balance in accounts table
            update_balance_query = "UPDATE accounts SET balance = balance + ? WHERE id = ?;"
            self.update_or_insert_query_with_params(update_balance_query, (amount, account_id))
            
            # Insert transaction
            query = "INSERT INTO transactions (id, account_id, amount, transaction_type, comment) VALUES (uuid(),?, ?, 'deposit', ?);"
            self.update_or_insert_query_with_params(query, (account_id, amount, comment))
            print(f"Deposited ${amount} to {user_name}'s account.")
        else:
            print(f"No account found for user: {user_name}")



    def withdraw_money(self, user_name, amount, transaction_type = 'withdrawal' ,comment=None):
        account_id = self.get_account_id_by_user_name(user_name)
        overdraft_limit =  self.get_account_overdraft_limit(account_id)
        if account_id:
            # Check if the withdrawal does not exceed the balance
            current_balance = self.get_balance_by_user_name(user_name)
            if current_balance is not None and (current_balance + overdraft_limit) >= amount:
                # Update balance in accounts table
                update_balance_query = "UPDATE accounts SET balance = balance - ? WHERE id = ?;"
                self.update_or_insert_query_with_params(update_balance_query, (amount, account_id))
                
                # Insert transaction
                query = "INSERT INTO transactions (id ,account_id, amount, transaction_type, comment) VALUES (uuid(),?, ?, ?, ?);"
                self.update_or_insert_query_with_params(query, (account_id, -amount, transaction_type, comment))
                print(f"Withdrew ${amount} from {user_name}'s account.")
            else:
                print(f"Insufficient funds for {user_name}.")
        else:
            print(f"No account found for user: {user_name}")


    def get_account_id_by_user_name(self, user_name):
        query = f"""
            SELECT a.id
            FROM accounts a
            JOIN users u ON a.owner_id = u.id
            WHERE u.name = ?;
        """
        result = self.execute_query_with_params(query, (user_name,))
        return result[0]['id'] if result else None

    def get_user_id_by_user_name(self, user_name):
        query = f"""
          SELECT id from users WHERE name = ?;
        """
        result = self.execute_query_with_params(query, (user_name,))
        return result[0]['id'] if result else None


    def get_account_overdraft_limit(self, account_id):
        query = f"SELECT overdraft_limit FROM accounts WHERE id = ?;"
        result = self.execute_query_with_params(query, (account_id,))
        return result[0]['overdraft_limit'] if result else 0


    def get_stocks_by_user(self, user_name):
        query = """
        SELECT s.symbol, s.company_name, s.stock_price, s.dividend_rate
        FROM stocks s
        JOIN users u ON s.owner_id = u.id
        WHERE u.name = ? ;
        """
        result =self.execute_query_with_params(query, (user_name,))
        return result



    def add_stock_for_user(self, user_name, company_name, total_bought):
        user_id = self.get_user_id_by_user_name(user_name)

        update_stock_query = """
            
            -- Attempt to update
            UPDATE stocks
            SET total_owned = total_owned + ?
            WHERE company_name = ?  AND owner_id = ?;
        """
        # right now we don't hve any function getting the stock price based on the company name 
        # so we use a default value, same for dividend rate
        update_stock_query_2 = """

            -- Check if any rows were updated
            INSERT INTO stocks (symbol, company_name, stock_price, dividend_rate, total_owned, owner_id)
            SELECT 'UNK', ?, 223.5, 0.03, ?, ?
            FROM DUAL
            WHERE NOT EXISTS (
                SELECT 1 
                FROM stocks 
                WHERE company_name = ? AND owner_id = ?
            );
            
        """
        self.update_or_insert_query_with_params(update_stock_query, (total_bought,company_name, user_id))
        self.update_or_insert_query_with_params(update_stock_query_2, (company_name, total_bought, user_id, company_name, user_id))


    def execute_query(self, query):
        results = []
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
        except Error as e:
            print(f"Error executing query: {e}")
        return results

    def execute_query_with_params(self, query, params):
        results = []
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            self.connection.commit()  # Commit changes for insert/update
            results = cursor.fetchall()

            cursor.close()
        except Error as e:
            print(f"Error executing query: {e}")
            print('the query is ', query)
            print('the params are ', params)
        return results

    def update_or_insert_query_with_params(self, query, params):
        succeed = []
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            self.connection.commit()  # Commit changes for insert/update
            cursor.close()
            return True
        except Error as e:
            print(f"Error executing query: {e}")
            print(f"SQLSTATE: {e.sqlstate}")
            print(f"Error code: {e.errno}")
            print('the query is ', query)
            print('the params are ', params)
        return False


    def close_connection(self):
        if self.is_connected(self.connection):
            self.connection.close()
            print("Database connection closed")


    def close_connection(self):
        if self.is_connected(self.connection):
            self.connection.close()
            print("Database connection closed")

# Example usage
# if __name__ == "__main__":
#     db = BankDBConnector()
    
    # # Example deposit
    # db.deposit_money("Alice Smith", 100, "Deposit for savings")
    
    # Example withdrawal
    # db.withdraw_money("Alice Smith", 50, "ATM withdrawal yok")

#     mmm = [Stock(x['symbol'], x['company_name'], x['stock_price'], x['dividend_rate']) for x in  db.get_stocks_by_user("Alice Smith")]

#     for t in mmm:
#         print('stock: ',t)


#     # Get balance after transactions
#     balance = db.get_balance_by_user_name("Alice Smith")
#     print("Balance for Alice Smith:", balance)
#     lt = [Transaction(x['amount'], x['transaction_type'], x['comment']) for x in db.get_last_n_transactions_by_user("Alice Smith", 2)]
#     for t in lt:
#         print('last n: ', t)



#     db.close_connection()
