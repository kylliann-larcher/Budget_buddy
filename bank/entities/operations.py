# Functions to do operations (like deposit, debit, transfer to another account)

from config import *
import tkinter as tk 


class DepositWindow:
    def __init__(self, parent):
        self.depo_win = tk.Toplevel(parent)
        self.depo_win.title("Solana Bank | Deposit")
        self.depo_win.geometry(MINI_WINDOW_SIZE)
        
        self.fields = ["Amount"]
        self.entries = {}
        
        for i, field in enumerate(self.fields):
            tk.Label(self.depo_win, text=field).grid(row=i, column=0, padx=15, pady=15)
            entry = tk.Entry(self.depo_win)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = entry
        
        tk.Button(self.depo_win, text="Deposit", command=self.deposit, width=10).grid(row=len(self.fields), columnspan=2, pady=10)

    def deposit(self):
        pass

class DebitWindow:
    def __init__(self, parent):
        self.depo_win = tk.Toplevel(parent)
        self.depo_win.title("Solana Bank | Debit")
        self.depo_win.geometry(MINI_WINDOW_SIZE)
        
        self.fields = ["Amount"]
        self.entries = {}
        
        for i, field in enumerate(self.fields):
            tk.Label(self.depo_win, text=field).grid(row=i, column=0, padx=15, pady=15)
            entry = tk.Entry(self.depo_win)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = entry
        
        tk.Button(self.depo_win, text="Debit", command=self.debit, width=10).grid(row=len(self.fields), columnspan=2, pady=10)

    def debit(self):
        pass

class TransferWindow:
    def __init__(self, parent):
        self.depo_win = tk.Toplevel(parent)
        self.depo_win.title("Solana Bank | Transfer")
        self.depo_win.geometry(MINI_WINDOW_SIZE)
        
        self.fields = ["Receiver ID", "Amount"]
        self.entries = {}
        
        for i, field in enumerate(self.fields):
            tk.Label(self.depo_win, text=field).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(self.depo_win)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = entry
        
        tk.Button(self.depo_win, text="Transfer", command=self.transfer, width=10).grid(row=len(self.fields), columnspan=2, pady=10)

    def transfer(self):
        pass