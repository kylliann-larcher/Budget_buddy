from database import Database

class Compte:
    def __init__(self, id_users, sold=0.0):
        self.id_users = id_users
        self.sold = sold

    def create_user(self):
        db = Database()
        db.execute("""
            INSERT INTO accounts (id_users, amount)
            VALUES (%s, %s)
        """, (self.id_users, self.sold))
        db.commit()
        db.close()
