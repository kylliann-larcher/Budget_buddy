# Dashboard Interface
from config import *
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import *

class DashboardView:
    def __init__(self, root, show_login, user_id):
        self.root = root
        self.show_login = show_login
        self.user_id = user_id
        self.root.title("Solana Bank | Dashboard")
        self.root.geometry(WINDOW_SIZE)

        # Connect db
        self.database = Database()
        
        # Display Principal frame
        self.create_widgets()

    # Create First widget
    def create_widgets(self):
        ttk.Label(self.root, text="Welcome to your dashboard", font=('Arial', 22)).pack(pady=25)
        
        # Buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=30)

        ttk.Button(btn_frame, text="Deposit", command=self.deposit_money).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Withdraw", command=self.withdraw_money).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="Transfer", command=self.transfer_money).grid(row=0, column=2, padx=10)
        ttk.Button(btn_frame, text="Transaction History", command=self.view_transactions).grid(row=0, column=3, padx=10)
        ttk.Button(btn_frame, text="Disconnect", command=self.show_login).grid(row=0, column=4, padx=10)
        
        # Total Balance of the account
        self.balance_label = ttk.Label(self.root, text="Balance: 0.00€", font=("Arial", 28))
        self.balance_label.pack(pady=35)
        
        # Update balance to display
        self.update_balance()

    # Update Balance of the user
    def update_balance(self):
        balance = self.database.get_balance(self.user_id)
        self.balance_label.config(text=f"Balance: {balance:.2f}€")

    # Mini Windows deposit
    def deposit_money(self):
        amount = self.get_amount("Deposit Amount")
        if amount:
            self.database.deposit(self.user_id, amount)
            self.update_balance()
            messagebox.showinfo("Success", "Deposit successful!")

    # Mini Windows withdraw
    def withdraw_money(self):
        amount = self.get_amount("Withdraw Amount")
        if amount:
            if self.database.withdraw(self.user_id, amount):
                self.update_balance()
                messagebox.showinfo("Success", "Withdrawal successful!")
            else:
                messagebox.showwarning("Error", "Insufficient funds! PROBLEM")
    
    # Mini Window transfer
    def transfer_money(self):
        recipient_id = simpledialog.askinteger("Transfer", "Enter recipient ID:", parent=self.root)
        amount = self.get_amount("Transfer Amount")
        if recipient_id and amount:
            if self.database.transfer(self.user_id, recipient_id, amount):
                self.update_balance()
                messagebox.showinfo("Success", "Transfer successful!", parent=self.root)
            else:
                messagebox.showwarning("Error", "Transfer failed!", parent=self.root)

    # Window transactions history
    def view_transactions(self):
        transactions = self.database.get_transactions(self.user_id)
        print(transactions)
        history_window = tk.Toplevel(self.root)
        history_window.title("Transactions History")
        
        tree = ttk.Treeview(history_window, columns=("Type", "Amount", "Date"), show="headings")
        tree.heading("Type", text="Type")
        tree.heading("Amount", text="Amount")
        tree.heading("Date", text="Date")
        
        for t in transactions:
            tree.insert("", "end", values=(t["type_transaction"], f"{t["amount"]:.2f}€", t["date_transaction"]))
        
        tree.pack(padx=10, pady=10)
    
    # Get amount for operations
    def get_amount(self, prompt):
        try:
            amount = float(simpledialog.askstring("Input", prompt, parent=self.root))
            if amount <= 0:
                raise ValueError
            return amount
        except (ValueError, TypeError):
            messagebox.showwarning("Error", "Invalid amount!", parent=self.root)
            return None