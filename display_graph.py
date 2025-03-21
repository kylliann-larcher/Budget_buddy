import matplotlib.pyplot as plt
import datetime
from database import Database  

def plot_transactions(user_id):
    db = Database()  
    transactions = db.get_transactions(user_id)  
    db.close()  

    if not transactions:
        print("Aucune transaction à afficher.")
        return

    # Extraction des dates et montants
    dates = [t["date_transaction"] for t in transactions]
    amounts = [t["amount"] for t in transactions]

    # Conversion des dates en format datetime
    dates = [datetime.datetime.strptime(str(d), "%Y-%m-%d %H:%M:%S") for d in dates]

    # Création du graphique
    plt.figure(figsize=(10, 5))
    plt.plot(dates, amounts, marker='o', linestyle='-', label="Transactions")
    plt.xlabel("Date de transaction")
    plt.ylabel("Montant (€)")
    plt.title(f"Transactions pour le compte {user_id}")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    user_id = int(input("enter the account id : "))
    plot_transactions(user_id)
