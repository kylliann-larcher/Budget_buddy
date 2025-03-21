from database import Database

def setup_data():
    db = Database()

    users = [
        {"name": "Zakaria", "first_name": "Manaame", "email": "zakaria.manaame@gmail.com", "password": "password123"},
        {"name": "Kylliann", "first_name": "LARCHER", "email": "kylliann.larcher@gmail.com", "password": "password123"},
        {"name": "Axel", "first_name": "Achart", "email": "axel.achart@gmail.com", "password": "password123"}
    ]

    # Création des utilisateurs et comptes associés
    for user in users:
        db.execute(
            "INSERT INTO users (name, first_name, email, pass_word) VALUES (%s, %s, %s, %s)",
            (user["name"], user["first_name"], user["email"], user["password"])
        )
        db.commit()
        
        # Récupérer l'ID du nouvel utilisateur
        db.execute("SELECT id_users FROM users WHERE email = %s", (user["email"],))
        user_id = db.cursor.fetchone()["id_users"]
        
        # Création du compte avec un solde initial
        db.execute(
            "INSERT INTO accounts (id_users, amount) VALUES (%s, %s)",
            (user_id, 1000.00)
        )
        db.commit()

        # Récupérer l'ID du compte
        db.execute("SELECT id_account FROM accounts WHERE id_users = %s", (user_id,))
        account_id = db.cursor.fetchone()["id_account"]

        # Ajouter quelques transactions
        transactions = [
            ("Achat supermarché", -50.00, "withdraw"),
            ("Salaire", 2000.00, "deposit"),
            ("Abonnement Netflix", -15.99, "withdraw"),
            ("Virement ami", -100.00, "transfer")
        ]

        for description, amount, transaction_type in transactions:
            db.execute(
                "INSERT INTO transactions (id_account, description, amount, type_transaction, date_transaction) VALUES (%s, %s, %s, %s, NOW())",
                (account_id, description, amount, transaction_type)
            )
            db.commit()

    db.close()
    print("Données insérées avec succès !")

if __name__ == "__main__":
    setup_data()
