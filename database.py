# Database File
import mysql.connector

class Database:
    def __init__(self):
        # Connection to local db
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Kylliann2110",
            database="budget_buddy_finance"
        )
        self.cursor = self.conn.cursor(dictionary=True)

    # Execute request
    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor

    # Apply request
    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

    # Check tables in db
    def verif_tables(self):
        try:
            self.execute("SHOW TABLES")
            tables = [table['Tables_in_budget_buddy_finance'] for table in self.cursor]
            required_tables = {'users', 'accounts', 'categories', 'transactions'}
            if not required_tables.issubset(set(tables)):
                with open('schema.sql', 'r') as f:
                    sql_script = f.read()
                for statement in sql_script.split(';'):
                    if statement.strip():
                        self.execute(statement)
                self.commit()
        except mysql.connector.Error as err:
            print(f"Database error : {err}")

    # Get amount in accounts of a user
    def get_balance(self, user_id):
        try:
            cursor = self.execute("SELECT amount FROM accounts WHERE id_users = %s", (user_id,))
            result = cursor.fetchone()
            return result["amount"] if result else 0.0
        except mysql.connector.Error as err:
            print(f"Erreur SQL: {err}")
            return 0.0

    # Modify in db deposit
    def deposit(self, user_id, amount):
        try:
            self.execute("UPDATE accounts SET amount = amount + %s WHERE id_users = %s", (amount, user_id))
            self.commit()

            account_id = self.get_account_id(user_id)
            if account_id:
                self.execute("INSERT INTO transactions (id_account, type_transaction, amount, date_transaction) VALUES (%s, 'deposit', %s, NOW())", (user_id, amount))
                self.commit()
                return True
        except mysql.connector.Error as err:
            print(f"Erreur SQL: {err}")
            return False

    # Modify in db withdraw
    def withdraw(self, user_id, amount):
        try:
            cursor = self.execute("SELECT amount FROM accounts WHERE id_users = %s", (user_id,))
            result = cursor.fetchone()
            if result and result["amount"] >= amount:
                self.execute("UPDATE accounts SET amount = amount - %s WHERE id_users = %s", (amount, user_id))
                self.commit()

                account_id = self.get_account_id(user_id)
                if account_id:
                    self.execute("INSERT INTO transactions (id_account, type_transaction, amount, date_transaction) VALUES (%s, 'withdraw', %s, NOW())", (user_id, amount))
                    self.commit()
                    return True
            else:
                print(f"Insufficient funds: {result['amount']} < {amount}")
            return False
        except mysql.connector.Error as err:
            print(f"Erreur SQL: {err}")
            return False

    # Modify in db transfer
    def transfer(self, user_id, recipient_id, amount):
        try:
            cursor = self.execute("SELECT amount FROM accounts WHERE id_users = %s", (user_id,))
            result = cursor.fetchone()
            if result and result["amount"] >= amount:
                self.execute("UPDATE accounts SET amount = amount - %s WHERE id_users = %s", (amount, user_id))
                self.execute("UPDATE accounts SET amount = amount + %s WHERE id_users = %s", (amount, recipient_id))
                self.commit()

                account_id = self.get_account_id(user_id)
                if account_id:
                    self.execute("INSERT INTO transactions (id_account, type_transaction, amount, date_transaction) VALUES (%s, 'transfer', %s, NOW())", (user_id, amount))
                    self.commit()
                    return True
            return False
        except mysql.connector.Error as err:
            print(f"Erreur SQL: {err}")
            return False

    # Get user in 'accounts' table
    def get_account_id(self, user_id):
        cursor = self.execute("SELECT id_account FROM accounts WHERE id_users = %s", (user_id,))
        result = cursor.fetchone()
        return result["id_account"] if result else None

    # Get table transactions
    def get_transactions(self, user_id):
        try:
            cursor = self.execute("SELECT * FROM transactions WHERE id_account = %s ORDER BY date_transaction DESC", (user_id,))
            result = cursor.fetchall()
            if not result:
                print("No transactions found.")
            return result
        except mysql.connector.Error as err:
            print(f"Erreur SQL: {err}")
            return []

    
