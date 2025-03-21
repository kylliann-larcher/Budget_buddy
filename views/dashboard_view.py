import random
from config import *
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import Database

class DashboardView:
    def __init__(self, root, show_login, user_id):
        self.root = root
        self.show_login = show_login
        self.user_id = user_id
        self.database = Database()
        self.create_widgets()

        # Style
        style = ttk.Style()
        # Configure style for TFrame
        style.configure("TFrame", background=BACKGROUND)
        # Configure style for TLabel (text)
        style.configure("TLabel", background=BACKGROUND, foreground="white", font=("Arial", 16))
        # Configure style for TButton (buttons)
        style.configure("TButton", background=BACKGROUND, foreground='black', font=("Arial", 14))
        # Configure style for Treeview (transaction history)
        style.configure("TTreeview", background=BACKGROUND, foreground="white")
        style.configure("TTreeview.Heading", background=BACKGROUND, foreground="white")

    def create_widgets(self):
        # Display welcome text
        ttk.Label(self.root, text="Welcome to your dashboard", font=('Arial', 36)).pack(pady=25)
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=30)
        
        # Create buttons
        ttk.Button(btn_frame, text="Deposit", command=self.deposit_money).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Withdraw", command=self.withdraw_money).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="Transfer", command=self.transfer_money).grid(row=0, column=2, padx=10)
        ttk.Button(btn_frame, text="Transaction History", command=self.view_transactions).grid(row=0, column=3, padx=10)
        ttk.Button(btn_frame, text="Disconnect", command=self.show_login).grid(row=0, column=5, padx=10)
        
        # Display balance
        self.balance_label = ttk.Label(self.root, text="Balance: 0.00€", font=("Arial", 28))
        self.balance_label.pack(pady=35)
        self.update_balance()

    def update_balance(self):
        balance = self.database.get_balance(self.user_id)
        self.balance_label.config(text=f"Balance: {balance:.2f}€")
    
    def generate_reference(self):
        return f"TRF{random.randint(1000, 9999)}"
    
    def deposit_money(self):
        amount = self.get_amount("Deposit Amount")
        description = self.get_description("Deposit Description")
        reference = self.generate_reference()
        if amount and description:
            self.database.deposit(self.user_id, amount, description, reference)
            self.update_balance()
            messagebox.showinfo("Success", "Deposit successful!")
    
    def withdraw_money(self):
        amount = self.get_amount("Withdraw Amount")
        description = self.get_description("Withdraw Description")
        reference = self.generate_reference()
        if amount and description:
            if self.database.withdraw(self.user_id, amount, description, reference):
                self.update_balance()
                messagebox.showinfo("Success", "Withdrawal successful!")
            else:
                messagebox.showwarning("Error", "Insufficient funds!")
    
    def transfer_money(self):
        recipient_id = simpledialog.askinteger("Transfer", "Enter recipient ID:", parent=self.root)
        description = self.get_description("Transfer Description")
        amount = self.get_amount("Transfer Amount")
        reference = self.generate_reference()
        if recipient_id and amount and description:
            if self.database.transfer(self.user_id, recipient_id, description, amount, reference):
                self.update_balance()
                messagebox.showinfo("Success", "Transfer successful!")
            else:
                messagebox.showwarning("Error", "Transfer failed!")
    
    def view_transactions(self):
        transactions = self.database.get_transactions(self.user_id)
        history_window = tk.Toplevel(self.root)
        history_window.title("Transactions History")

        tree = ttk.Treeview(history_window, columns=("Type", "Amount", "Date", "Description", "Reference"), show="headings")
        
        tree.heading("Type", text="Type", command=lambda: self.sort_transactions(tree, transactions, "type_transaction"))
        tree.heading("Amount", text="Amount", command=lambda: self.sort_transactions(tree, transactions, "amount"))
        tree.heading("Date", text="Date", command=lambda: self.sort_transactions(tree, transactions, "date_transaction"))
        tree.heading("Description", text="Description")
        tree.heading("Reference", text="Reference")

        for t in transactions:
            tree.insert("", "end", values=(t["type_transaction"], f"{t['amount']:.2f}€", t["date_transaction"], t["description"], t["reference"]))
 
        tree.pack(padx=10, pady=10)

    def sort_transactions(self, tree, transactions, sort_by):
        if sort_by == "amount":
            transactions.sort(key=lambda t: t["amount"], reverse=True)
        elif sort_by == "date_transaction":
            transactions.sort(key=lambda t: t["date_transaction"], reverse=True)
        elif sort_by == "type_transaction":
            transactions.sort(key=lambda t: t["type_transaction"], reverse=True)
        
        for item in tree.get_children():
            tree.delete(item)
        
        for t in transactions:
            tree.insert("", "end", values=(t["type_transaction"], f"{t['amount']:.2f}€", t["date_transaction"], t["description"], t["reference"]))

    
    def get_amount(self, prompt):
        try:
            amount = float(simpledialog.askstring("Input", prompt, parent=self.root))
            if amount <= 0:
                raise ValueError
            return amount
        except (ValueError, TypeError):
            messagebox.showwarning("Error", "Invalid amount!")
            return None

    def get_description(self, prompt):
        description = simpledialog.askstring("Input", prompt, parent=self.root)
        return description if description else "No description"
