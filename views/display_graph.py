import matplotlib.pyplot as plt
import datetime
from database import Database  


class Graphic:
    def __init__(self, user_id):
        self.user_id = user_id
            
    def plot_transactions(self):
        db = Database()  
        transactions = db.get_transactions(self.user_id)  
        db.close()  

        if not transactions:
            print("No transactions found.")
            return

        dates = [t["date_transaction"] for t in transactions]
        amounts = [t["amount"] for t in transactions]

        dates = [datetime.datetime.strptime(str(d), "%Y-%m-%d %H:%M:%S") for d in dates]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, amounts, marker='o', linestyle='-', label="Transactions")
        plt.xlabel("Transactions Date")
        plt.ylabel("Amount (€)")
        plt.title(f"Transactions for id account : {self.user_id}")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid()
        plt.show()