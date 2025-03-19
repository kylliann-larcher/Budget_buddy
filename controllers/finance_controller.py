from models.compte import Compte
from models.transaction import Transaction
from database import Database
from datetime import datetime

class FinanceController:
    def deposit(self, id_user, amount, description, id_category):
        if amount <= 0:
            return "Amount must to be > 0"

        db = Database()
        
        try:
            # Update amount
            db.execute("UPDATE comptes SET solde = solde + %s WHERE id_user = %s", (amount, id_user))
            
            # Add transaction
            transaction = Transaction(id_user, amount, "depot", description, id_category)
            transaction.save()
            
            db.commit()
            return f"Deposit of {amount:.2f} € done."
        except Exception as e:
            db.close()
            return f"Error in deposit : {e}"

    def debit(self, id_user, amount, description, id_category):
        if amount <= 0:
            return "Amount must to be > 0"

        db = Database()
        
        try:
            # Amount need in account
            solde = db.execute("SELECT solde FROM comptes WHERE id_user = %s", (id_user,)).fetchone()
            if solde["solde"] < amount:
                return "Need more money..."

            # Update in account
            db.execute("UPDATE comptes SET solde = solde - %s WHERE id_user = %s", (amount, id_user))

            # Add transaction
            transaction = Transaction(id_user, amount, "retrait", description, id_category)
            transaction.save()

            db.commit()
            return f"Debit of {amount:.2f} € done."
        except Exception as e:
            db.close()
            return f"Error in debit : {e}"

    def transfer(self, id_user_source, id_user_dest, amount, description, id_category):
        if amount <= 0:
            return "Amount must to be > 0"

        db = Database()
        
        try:
            # Vérifier le solde du compte source
            solde_source = db.execute("SELECT solde FROM comptes WHERE id_user = %s", (id_user_source,)).fetchone()
            if solde_source["solde"] < amount:
                return "Need more money..."

            # Débiter le compte source
            db.execute("UPDATE comptes SET solde = solde - %s WHERE id_user = %s", (amount, id_user_source))

            # Créditer le compte destination
            db.execute("UPDATE comptes SET solde = solde + %s WHERE id_user = %s", (amount, id_user_dest))

            # Ajouter la transaction
            reference = f"TRF{datetime.now().strftime('%Y%m%d%H%M%S')}{id_user_source}"
            db.execute("""
                INSERT INTO transactions (reference, description, amount, type_transaction, id_user, id_user_destination, id_category)
                VALUES (%s, %s, %s, 'transfert', %s, %s, %s)
            """, (reference, description, amount, id_user_source, id_user_dest, id_category))

            db.commit()
            return f"Transfer of {amount:.2f} € done."
        except Exception as e:
            db.close()
            return f"Error in transfer : {e}"

    def get_transaction(self, id_user, filters):
        db = Database()
        
        try:
            query = """
                SELECT t.reference, t.description, t.amount, t.date_transaction, t.type_transaction, c.nom AS categorie
                FROM transactions t
                JOIN categories c ON t.id_category = c.id_category
                WHERE t.id_user = %s
            """
            params = [id_user]

            # Ajout des filters
            if "date_debut" in filters:
                query += " AND t.date_transaction >= %s"
                params.append(filters["date_debut"])
            
            if "date_fin" in filters:
                query += " AND t.date_transaction <= %s"
                params.append(filters["date_fin"])

            if "type" in filters and filters["type"] != "Tous":
                query += " AND t.type_transaction = %s"
                params.append(filters["type"].lower())

            if "categorie" in filters and filters["categorie"] != "Toutes":
                query += " AND c.nom = %s"
                params.append(filters["categorie"])

            query += " ORDER BY t.date_transaction DESC"

            transactions = db.execute(query, params).fetchall()
            db.close()
            return transactions
        except Exception as e:
            db.close()
            return f"Error in get transactions history : {e}"
