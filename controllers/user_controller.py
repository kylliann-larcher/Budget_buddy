# Controller for users
from models.accounts import Utilisateur
from database import Database

class UserController:
    def save_user(self, name, first_name, email, password):
        if not Utilisateur.verif_password(password):
            return "Error: Weak password"
        
        # Get infos of the user
        user = Utilisateur(name, first_name, email, password)

        # Connect db
        db = Database()

        try:
            # Insert new user
            db.execute("""
                INSERT INTO users (name, first_name, email, pass_word)
                VALUES (%s, %s, %s, %s)
            """, (user.name, user.first_name, user.email, user.password))
            db.commit()

            # Get id of new user
            user_id = db.execute("SELECT LAST_INSERT_ID() AS id_users").fetchone()["id_users"]

            # Insert an account for this new user with amount = 0
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
    
    # Verif for connection if password is good or not
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
