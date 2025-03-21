
from database import Database
from datetime import datetime

class Transaction:
    def __init__(self, id_user, amount, type_transaction, description, id_category):
        self.id_user = id_user
        self.amount = amount
        self.type_transaction = type_transaction
        self.description = description
        self.id_category = id_category
        self.date_transaction = datetime.now()

    def save(self):
        db = Database()
        db.execute("""
            INSERT INTO transactions (id_account, amount, type_transaction, description, id_category, date_transaction)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (self.id_user, self.amount, self.type_transaction, self.description, self.id_category, self.date_transaction))
        db.commit()
        db.close()
