from models.accounts import Utilisateur
from database import Database

class UserController:
    def save_user(self, name, first_name, email, password):
        if not Utilisateur.verif_password(password):
            return "Error: Weak password"
        
        user = Utilisateur(name, first_name, email, password)
        db = Database()

        try:
            # Insérer l'utilisateur dans la table users
            db.execute("""
                INSERT INTO users (name, first_name, email, pass_word)
                VALUES (%s, %s, %s, %s)
            """, (user.name, user.first_name, user.email, user.password))
            db.commit()

            # Récupérer l'ID du nouvel utilisateur
            user_id = db.execute("SELECT LAST_INSERT_ID() AS id_users").fetchone()["id_users"]

            # Insérer un compte pour cet utilisateur avec solde = 0.00 et date locale
            db.execute("""
                INSERT INTO accounts (id_users, amount, date_creation)
                VALUES (%s, %s, NOW())
            """, (user_id, 0.00))
            db.commit()

            return "User registered successfully"
        
        except Exception as err:
            print(f"Erreur lors de l'inscription : {err}")
            db.conn.rollback()
            return "Error: Could not register user"

        finally:
            db.close()
    

    def connect(self, email, password):
        db = Database()
        user = db.execute("""
            SELECT id_users, pass_word FROM users WHERE email = %s
        """, (email,)).fetchone()

        db.close()

        if user:
            if user["pass_word"] == password:
                return user["id_users"]  # Successful connection
            else:
                return None  # Password invalid
        return None  # Email invalid
