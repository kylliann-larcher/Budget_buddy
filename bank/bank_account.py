import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

class Compte:
    """Représente un compte bancaire avec son ID, nom, solde et transactions."""
    
    def __init__(self, compte_id, utilisateur_nom, utilisateur_prenom, solde):
        self.id = compte_id
        self.utilisateur_nom = utilisateur_nom
        self.utilisateur_prenom = utilisateur_prenom
        self.solde = solde
        self.transactions = []  # Liste des transactions associées

    def ajouter_transaction(self, transaction):
        """Ajoute une transaction au compte."""
        self.transactions.append(transaction)

    def afficher_details(self):
        """Affiche les détails du compte."""
        print(f"Compte de {self.utilisateur_prenom} {self.utilisateur_nom} (ID: {self.id}) - Solde: {self.solde}€")
        for transaction in self.transactions:
            print(f"{transaction['date_transaction']} - {transaction['type']} - {transaction['montant']}€ ({transaction['categorie']})")


class GestionComptes:
    """Gère la connexion à la base de données et récupère les informations des comptes."""

    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Kylliann2110",
            database="database_solana"
        )

    def recuperer_comptes(self):
        """Récupère la liste des comptes existants avec leurs utilisateurs."""
        query = """
        SELECT c.id, u.nom, u.prenom, c.solde 
        FROM comptes c
        JOIN utilisateurs u ON c.utilisateur_id = u.id;
        """
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(query)
        comptes = []
        for row in cursor.fetchall():
            comptes.append(Compte(row['id'], row['nom'], row['prenom'], row['solde']))
        cursor.close()
        return comptes

    def charger_transactions(self, compte):
        """Charge les transactions pour un compte spécifique."""
        query = f"""
        SELECT t.date_transaction, c.nom AS categorie, t.type, t.montant
        FROM transactions t
        JOIN categories c ON t.categorie_id = c.id
        WHERE t.compte_id = {compte.id}
        ORDER BY t.date_transaction;
        """
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(query)
        for row in cursor.fetchall():
            compte.ajouter_transaction(row)
        cursor.close()

    def fermer_connexion(self):
        """Ferme la connexion à la base de données."""
        self.conn.close()


def afficher_graphique(compte):
    """Affiche un graphique des revenus et dépenses d'un compte."""
    if not compte.transactions:
        print(f"Aucune transaction trouvée pour {compte.utilisateur_prenom} {compte.utilisateur_nom}.")
        return

    df = pd.DataFrame(compte.transactions)
    df['date_transaction'] = pd.to_datetime(df['date_transaction'])

    # Séparer revenus et dépenses
    revenus = df[df['type'] == 'depot']
    depenses = df[df['type'] == 'retrait']

    # Tracer le graphique
    plt.figure(figsize=(12, 6))

    # Courbe des revenus
    if not revenus.empty:
        plt.plot(revenus['date_transaction'], revenus['montant'], marker='o', linestyle='-', label="Revenus", color='green')

    # Courbe des dépenses
    if not depenses.empty:
        plt.plot(depenses['date_transaction'], -depenses['montant'], marker='o', linestyle='-', label="Dépenses", color='red')

    # Labels et affichage
    plt.xlabel("Date")
    plt.ylabel("Montant (€)")
    plt.title(f"Évolution des finances du compte de {compte.utilisateur_prenom} {compte.utilisateur_nom}")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()

# Initialisation du gestionnaire de comptes
gestionnaire = GestionComptes()

# Récupérer les comptes
comptes = gestionnaire.recuperer_comptes()

# Choisir un compte (ex: premier compte trouvé)
if comptes:
    compte = comptes[1]  # Prend le premier compte trouvé
    gestionnaire.charger_transactions(compte)
    compte.afficher_details()
    afficher_graphique(compte)
else:
    print("Aucun compte trouvé.")

# Fermer la connexion
gestionnaire.fermer_connexion()
