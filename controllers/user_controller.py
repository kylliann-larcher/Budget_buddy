from models.accounts import *
from database import Database

class UserController:
    def connect(self, email, password):
        db = Database()
        user = db.execute("""
            SELECT id_utilisateur FROM utilisateurs WHERE email = %s AND password = %s
        """, (email, Utilisateur.hasher_password(None, password))).fetchone()

        db.close()
        return user
