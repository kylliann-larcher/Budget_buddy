import mysql.connector
from datetime import datetime
import uuid
import getpass
import sys
from tabulate import tabulate

class SolanaBank:
    def __init__(self, host="localhost", user="root", password="root", database="database_solana_zm"):
        """Initialise la connexion à la base de données."""
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor(dictionary=True)
            print("Connexion à la base de données réussie.")
        except mysql.connector.Error as err:
            print(f"Erreur de connexion à la base de données: {err}")
            sys.exit(1)
    
    def login(self, email, password):
        """Connecte un utilisateur avec son email et mot de passe."""
        # Dans un vrai système, vous utiliseriez un hachage sécurisé pour le stockage et la vérification du mot de passe
        query = "SELECT user_id, firstname, lastname FROM users WHERE email = %s AND password_hash = %s"
        self.cursor.execute(query, (email, password))
        user = self.cursor.fetchone()
        
        if user:
            return user
        else:
            print("Email ou mot de passe incorrect.")
            return None
    
    def get_user_accounts(self, user_id):
        """Récupère tous les comptes d'un utilisateur."""
        query = "SELECT * FROM accounts WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        accounts = self.cursor.fetchall()
        
        if accounts:
            return accounts
        else:
            print("Aucun compte trouvé pour cet utilisateur.")
            return []
    
    def display_accounts(self, accounts):
        """Affiche la liste des comptes d'un utilisateur."""
        if not accounts:
            return
        
        headers = ["ID", "Nom du compte", "Solde (€)"]
        data = [(acc["account_id"], acc["account_name"], f"{acc['balance']:.2f}") for acc in accounts]
        
        print("\n=== Vos comptes ===")
        print(tabulate(data, headers=headers, tablefmt="simple"))
    
    def deposit(self, account_id, amount, description="Dépôt d'argent"):
        """Effectue un dépôt sur un compte."""
        if amount <= 0:
            print("Le montant doit être positif.")
            return False
        
        try:
            # 1. Mettre à jour le solde du compte
            update_balance = "UPDATE accounts SET balance = balance + %s WHERE account_id = %s"
            self.cursor.execute(update_balance, (amount, account_id))
            
            # 2. Créer une transaction
            reference = f"DEP-{uuid.uuid4().hex[:8].upper()}"
            insert_transaction = """
            INSERT INTO transactions 
            (reference, description, amount, transaction_date, type_id, category_id, account_id)
            VALUES (%s, %s, %s, NOW(), 1, 6, %s)
            """
            self.cursor.execute(insert_transaction, (reference, description, amount, account_id))
            
            self.conn.commit()
            print(f"Dépôt de {amount:.2f}€ effectué avec succès. Référence: {reference}")
            return True
        except mysql.connector.Error as err:
            self.conn.rollback()
            print(f"Erreur lors du dépôt: {err}")
            return False
    
    def withdraw(self, account_id, amount, description="Retrait d'argent"):
        """Effectue un retrait sur un compte."""
        if amount <= 0:
            print("Le montant doit être positif.")
            return False
        
        try:
            # Vérifier si le solde est suffisant
            self.cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
            account = self.cursor.fetchone()
            
            if not account or account["balance"] < amount:
                print("Solde insuffisant pour effectuer le retrait.")
                return False
            
            # 1. Mettre à jour le solde du compte
            update_balance = "UPDATE accounts SET balance = balance - %s WHERE account_id = %s"
            self.cursor.execute(update_balance, (amount, account_id))
            
            # 2. Créer une transaction
            reference = f"RET-{uuid.uuid4().hex[:8].upper()}"
            insert_transaction = """
            INSERT INTO transactions 
            (reference, description, amount, transaction_date, type_id, category_id, account_id)
            VALUES (%s, %s, %s, NOW(), 2, 7, %s)
            """
            self.cursor.execute(insert_transaction, (reference, description, -amount, account_id))
            
            self.conn.commit()
            print(f"Retrait de {amount:.2f}€ effectué avec succès. Référence: {reference}")
            return True
        except mysql.connector.Error as err:
            self.conn.rollback()
            print(f"Erreur lors du retrait: {err}")
            return False
    
    def transfer(self, from_account_id, to_account_id, amount, description="Transfert d'argent"):
        """Transfère de l'argent entre deux comptes."""
        if from_account_id == to_account_id:
            print("Impossible de transférer vers le même compte.")
            return False
            
        if amount <= 0:
            print("Le montant doit être positif.")
            return False
        
        try:
            # Vérifier si le solde est suffisant
            self.cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (from_account_id,))
            account = self.cursor.fetchone()
            
            if not account or account["balance"] < amount:
                print("Solde insuffisant pour effectuer le transfert.")
                return False
            
            # Vérifier si le compte destinataire existe
            self.cursor.execute("SELECT account_id FROM accounts WHERE account_id = %s", (to_account_id,))
            if not self.cursor.fetchone():
                print("Le compte destinataire n'existe pas.")
                return False
            
            # 1. Mettre à jour le solde du compte source
            self.cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", 
                            (amount, from_account_id))
            
            # 2. Mettre à jour le solde du compte destinataire
            self.cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", 
                            (amount, to_account_id))
            
            # 3. Créer une transaction
            reference = f"TRF-{uuid.uuid4().hex[:8].upper()}"
            insert_transaction = """
            INSERT INTO transactions 
            (reference, description, amount, transaction_date, type_id, category_id, account_id, recipient_account_id)
            VALUES (%s, %s, %s, NOW(), 3, 7, %s, %s)
            """
            self.cursor.execute(insert_transaction, 
                            (reference, description, -amount, from_account_id, to_account_id))
            
            self.conn.commit()
            print(f"Transfert de {amount:.2f}€ effectué avec succès. Référence: {reference}")
            return True
        except mysql.connector.Error as err:
            self.conn.rollback()
            print(f"Erreur lors du transfert: {err}")
            return False
    
    def get_transaction_history(self, account_id, limit=20):
        """Récupère l'historique des transactions d'un compte."""
        query = """
        SELECT t.transaction_id, t.reference, t.description, t.amount, 
               t.transaction_date, tt.type_name, c.category_name,
               a_recipient.account_name as recipient_name
        FROM transactions t
        JOIN transaction_types tt ON t.type_id = tt.type_id
        LEFT JOIN categories c ON t.category_id = c.category_id
        LEFT JOIN accounts a_recipient ON t.recipient_account_id = a_recipient.account_id
        WHERE t.account_id = %s
        ORDER BY t.transaction_date DESC
        LIMIT %s
        """
        self.cursor.execute(query, (account_id, limit))
        transactions = self.cursor.fetchall()
        
        return transactions
    
    def display_transaction_history(self, transactions):
        """Affiche l'historique des transactions."""
        if not transactions:
            print("Aucune transaction trouvée.")
            return
        
        headers = ["Date", "Référence", "Type", "Description", "Catégorie", "Destinataire", "Montant (€)"]
        data = []
        
        for t in transactions:
            date = t["transaction_date"].strftime("%d/%m/%Y %H:%M")
            recipient = t["recipient_name"] if t["recipient_name"] else "-"
            amount = f"{t['amount']:.2f}"
            amount_formatted = f"\033[92m+{amount}\033[0m" if t["amount"] > 0 else f"\033[91m{amount}\033[0m"
            
            data.append([
                date, 
                t["reference"], 
                t["type_name"], 
                t["description"] or "-", 
                t["category_name"] or "-",
                recipient,
                amount_formatted
            ])
        
        print("\n=== Historique des transactions ===")
        print(tabulate(data, headers=headers, tablefmt="simple"))
    
    def close(self):
        """Ferme la connexion à la base de données."""
        if self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
            print("Connexion à la base de données fermée.")

# Programme principal
def main():
    # Paramètres de connexion à la base de données (à modifier selon votre configuration)
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "database_solana_zm"
    }
    
    bank = SolanaBank(**db_config)
    
    try:
        # Authentification
        print("=== Bienvenue sur Solana Banking System ===")
        email = input("Email: ")
        password = getpass.getpass("Mot de passe: ")
        
        user = bank.login(email, password)
        if not user:
            print("Échec de connexion. Au revoir.")
            return
        
        print(f"\nBienvenue, {user['firstname']} {user['lastname']}!")
        
        # Menu principal
        while True:
            accounts = bank.get_user_accounts(user["user_id"])
            bank.display_accounts(accounts)
            
            print("\n=== Menu ===")
            print("1. Effectuer un dépôt")
            print("2. Effectuer un retrait")
            print("3. Effectuer un transfert")
            print("4. Consulter l'historique des transactions")
            print("0. Quitter")
            
            choice = input("\nChoisissez une option: ")
            
            if choice == "1":
                # Dépôt
                account_id = int(input("ID du compte: "))
                amount = float(input("Montant à déposer (€): "))
                description = input("Description (optionnel): ") or "Dépôt d'argent"
                bank.deposit(account_id, amount, description)
            
            elif choice == "2":
                # Retrait
                account_id = int(input("ID du compte: "))
                amount = float(input("Montant à retirer (€): "))
                description = input("Description (optionnel): ") or "Retrait d'argent"
                bank.withdraw(account_id, amount, description)
            
            elif choice == "3":
                # Transfert
                from_account_id = int(input("ID du compte source: "))
                to_account_id = int(input("ID du compte destinataire: "))
                amount = float(input("Montant à transférer (€): "))
                description = input("Description (optionnel): ") or "Transfert d'argent"
                bank.transfer(from_account_id, to_account_id, amount, description)
            
            elif choice == "4":
                # Historique
                account_id = int(input("ID du compte: "))
                limit = int(input("Nombre de transactions à afficher (défaut: 20): ") or "20")
                transactions = bank.get_transaction_history(account_id, limit)
                bank.display_transaction_history(transactions)
            
            elif choice == "0":
                print("Merci d'avoir utilisé Solana Banking System. Au revoir!")
                break
            
            else:
                print("Option invalide. Veuillez réessayer.")
            
            input("\nAppuyez sur Entrée pour continuer...")
    
    finally:
        bank.close()

if __name__ == "__main__":
    main()