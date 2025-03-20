# Controller for finance
from models.transaction import Transaction
from database import Database
from datetime import datetime

class FinanceController:
    # Verif for allow deposit and apply
    def deposit(self, id_users, amount, description, id_category):
        if amount <= 0:
            return "Amount must to be > 0"

        # Connect db
        db = Database()
        
        try:
            # Update amount
            db.execute("UPDATE accounts SET amount = amount + %s WHERE id_users = %s", (amount, id_users))
            
            # Add transaction
            transaction = Transaction(id_users, amount, "depot", description, id_category)
            transaction.save()
            
            db.commit()
            return f"Deposit of {amount:.2f} € done."
        
        except Exception as e:
            db.close()
            return f"Error in deposit : {e}"

    # Verif for allow debit and apply
    def debit(self, id_users, amount, description, id_category):
        if amount <= 0:
            return "Amount must to be > 0"

        db = Database()
        
        try:
            # Amount need in account
            amount = db.execute("SELECT amount FROM accounts WHERE id_users = %s", (id_users,)).fetchone()
            if amount["amount"] < amount:
                return "Need more money..."

            # Update in account
            db.execute("UPDATE accounts SET amount = amount - %s WHERE id_users = %s", (amount, id_users))

            # Add transaction
            transaction = Transaction(id_users, amount, "retrait", description, id_category)
            transaction.save()

            db.commit()
            return f"Debit of {amount:.2f} € done."
        except Exception as e:
            db.close()
            return f"Error in debit : {e}"

    # Verif for allow transfer and apply
    def transfer(self, id_users_source, id_users_dest, amount, description, id_category):
        if amount <= 0:
            return "Amount must to be > 0"

        db = Database()
        
        try:
            # Check amount available
            amount_source = db.execute("SELECT amount FROM accounts WHERE id_users = %s", (id_users_source,)).fetchone()
            if amount_source["amount"] < amount:
                return "Need more money..."

            # Retire amount from begin
            db.execute("UPDATE accounts SET amount = amount - %s WHERE id_users = %s", (amount, id_users_source))

            # Add amount for destinatary
            db.execute("UPDATE accounts SET amount = amount + %s WHERE id_users = %s", (amount, id_users_dest))

            # Add transaction
            reference = f"TRF{datetime.now().strftime('%Y%m%d%H%M%S')}{id_users_source}"
            db.execute("""
                INSERT INTO transactions (reference, description, amount, type_transaction, id_account, id_account_destination, id_category)
                VALUES (%s, %s, %s, 'transfert', %s, %s, %s)
            """, (reference, description, amount, id_users_source, id_users_dest, id_category))

            db.commit()
            return f"Transfer of {amount:.2f} € done."
        except Exception as e:
            db.close()
            return f"Error in transfer : {e}"

    # Get transactions in db
    def get_transaction(self, id_users, filters):
        db = Database()
        
        try:
            query = """
                SELECT t.reference, t.description, t.amount, t.date_transaction, t.type_transaction, c.name AS category
                FROM transactions t
                JOIN categories c ON t.id_category = c.id_category
                WHERE t.id_account = %s
            """
            params = [id_users]

            # Add filters
            if "date_begin" in filters:
                query += " AND t.date_transaction >= %s"
                params.append(filters["date_debut"])
            
            if "date_finish" in filters:
                query += " AND t.date_transaction <= %s"
                params.append(filters["date_fin"])

            if "type" in filters and filters["type"] != "Tous":
                query += " AND t.type_transaction = %s"
                params.append(filters["type"].lower())

            if "category" in filters and filters["category"] != "Toutes":
                query += " AND c.name = %s"
                params.append(filters["category"])

            query += " ORDER BY t.date_transaction DESC"

            transactions = db.execute(query, params).fetchall()
            db.close()
            return transactions
        except Exception as e:
            db.close()
            return f"Error in get transactions history : {e}"
