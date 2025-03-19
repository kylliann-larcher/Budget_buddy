# Functions to do operations (like deposit, debit, transfer to another account)
#montant que je recupere soit disponible dans le solde de mon compte

import mysql.connector
from mysql.connector import Error

# Connexion à la base de données
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="root",  
            database="database_solana_zm"
        )
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None


# Déposit 
def deposit(account_id, amount):
    connection = connect_db()
    if connection and amount > 0:
        cursor = connection.cursor()
        cursor.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, account_id))
        connection.commit()
        print(f"Deposited {amount} successfully into account {account_id}.")
        cursor.close()
        connection.close()


# Débit
def debit(account_id, amount):
    connection = connect_db()
    if connection and amount > 0:
        cursor = connection.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
        result = cursor.fetchone()
        if result and result[0] >= amount:
            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, account_id))
            connection.commit()
            print(f"Debited {amount} successfully from account {account_id}.")
        else:
            print("Insufficient funds.")
        cursor.close()
        connection.close()




# Transfert 2 accounts
def transfer(from_account_id, to_account_id, amount):
    connection = connect_db()
    if connection and amount > 0:
        cursor = connection.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE id = %s", (from_account_id,))
        result = cursor.fetchone()
        if result and result[0] >= amount:
            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, from_account_id))
            cursor.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, to_account_id))
            connection.commit()
            print(f"Transferred {amount} from account {from_account_id} to account {to_account_id}.")
        else:
            print("Insufficient funds for transfer.")
        cursor.close()
        connection.close()



# Exemples 
if __name__ == "__main__":
    deposit(1, 500)  # Déposit 500 sur le compte 1
    debit(1, 200)  # Débit 200 du compte 1
    transfer(1, 2, 100)  # Transférer 100 du compte 1 vers le compte 2
