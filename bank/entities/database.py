# To connect to the databas
import mysql.connector

class DatabaseConnector:
    def __init__(self, host, user, password , database):
        """
        Initialiser la connexion à la base de données MySQL.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def connect(self):
        """
        Établir la connexion à la base de données MySQL.
        """
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.conn.cursor()
            print("Connexion réussie à la base de données.")
        except mysql.connector.Error as err:
            print(f"Erreur de connexion : {err}")
            self.conn = None
            self.cursor = None

    def fetch_all_users(self):
        """
        Récupérer tous les utilisateurs de la table 'utilisateurs'.
        """
        if self.conn and self.cursor:
            try:
                self.cursor.execute("SELECT * FROM utilisateurs")
                result = self.cursor.fetchall()
                return result
            except mysql.connector.Error as err:
                print(f"Erreur lors de la récupération des utilisateurs : {err}")
                return []
        else:
            print("La connexion à la base de données n'est pas établie.")
            return []

    def close(self):
        """
        Fermer la connexion à la base de données MySQL.
        """
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("Connexion fermée.")

# Utilisation de la classe
if __name__ == "__main__":
    db = DatabaseConnector(host="localhost", user="root", password="Kylliann2110", database="database_solana")
    
    # Connexion à la base de données
    db.connect()
    
    # Récupérer et afficher les utilisateurs
    utilisateurs = db.fetch_all_users()
    for utilisateur in utilisateurs:
        print(utilisateur)
    
    # Fermer la connexion
    db.close()
# To connect to the database
