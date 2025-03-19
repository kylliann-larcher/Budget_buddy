from database import Database
import hashlib
import re

class Utilisateur:
    def __init__(self, name, first_name, email, password):
        self.name = name
        self.first_name = first_name
        self.email = email
        self.password = self.hasher_password(password)

    def hasher_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verif_password(self, password):
        if len(password) < 5:
            return False
        return bool(re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*\W).+$', password))

    def save_user(self):
        db = Database()
        db.execute("""
            INSERT INTO utilisateurs (name, first_name, email, password)
            VALUES (%s, %s, %s, %s)
        """, (self.name, self.first_name, self.email, self.password))
        db.commit()
        db.close()
