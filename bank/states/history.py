# Interface histoy of transactions (reference, description, date, category, type, amount)

from config import *
import tkinter as tk 

class HistoryWindow:
    def __init__(self, parent):
        self.depo_win = tk.Toplevel(parent)
        self.depo_win.title("Solana Bank | History of transaction")
        self.depo_win.geometry(HISTORY_WINDOW_SIZE)

    def get_history(self):
        """ID du compte de la transaction, type de transac, le montant, la date"""
        pass