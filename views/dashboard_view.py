from config import *
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from controllers.user_controller import UserController
from database import *
import tkinter.font

class DashboardView:
    def __init__(self, root, show_login, user_id):
        self.root = root
        self.show_login = show_login
        self.user_id = user_id
        self.root.title("Solana Bank | Dashboard")
        self.root.geometry(WINDOW_SIZE)

        self.TITLE_FONT = tkinter.font.Font(family=family_font, size=title_size_font, weight=weight_font)
        self.SECOND_TITLE_FONT = tkinter.font.Font(family=family_font, size=second_title_size_font, weight=weight_font)
        self.FONT = tkinter.font.Font(family=family_font, size=size_font, weight=weight_font)

        self.database = Database()
        
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Welcome to your dashboard", font=self.TITLE_FONT).pack(pady=10)
        
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Deposit", font=self.FONT, command=self.deposit_money).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Withdraw", font=self.FONT, command=self.withdraw_money).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="Transfer", font=self.FONT, command=self.transfer_money).grid(row=0, column=2, padx=10)
        ttk.Button(btn_frame, text="Transaction History", font=self.FONT, command=self.view_transactions).grid(row=0, column=3, padx=10)
        ttk.Button(btn_frame, text="Disconnect", font=self.FONT, command=self.show_login).grid(row=0, column=4, padx=10)
        
        self.balance_label = ttk.Label(self.root, text="Balance: 0.00€", font=self.SECOND_TITLE_FONT)
        self.balance_label.pack(pady=10)
        
        self.update_balance()

    def update_balance(self):
        balance = self.database.get_balance(self.user_id)
        self.balance_label.config(text=f"Balance: {balance:.2f}€")

    def deposit_money(self):
        amount = self.get_amount("Deposit Amount")
        if amount:
            self.database.deposit(self.user_id, amount)
            self.update_balance()
            messagebox.showinfo("Success", "Deposit successful!")

    def withdraw_money(self):
        amount = self.get_amount("Withdraw Amount")
        if amount:
            if self.database.withdraw(self.user_id, amount):
                self.update_balance()
                messagebox.showinfo("Success", "Withdrawal successful!")
            else:
                messagebox.showwarning("Error", "Insufficient funds! PROBLEM")
    
    def transfer_money(self):
        recipient_id = simpledialog.askinteger("Transfer", "Enter recipient ID:", parent=self.root)
        amount = self.get_amount("Transfer Amount")
        if recipient_id and amount:
            if self.database.transfer(self.user_id, recipient_id, amount):
                self.update_balance()
                messagebox.showinfo("Success", "Transfer successful!", parent=self.root)
            else:
                messagebox.showwarning("Error", "Transfer failed!", parent=self.root)

    
    def view_transactions(self):
        transactions = self.database.get_transactions(self.user_id)
        print(transactions)
        history_window = tk.Toplevel(self.root)
        history_window.title("Transaction History")
        
        tree = ttk.Treeview(history_window, columns=("Type", "Amount", "Date"), show="headings")
        tree.heading("Type", text="Type")
        tree.heading("Amount", text="Amount")
        tree.heading("Date", text="Date")
        
        for t in transactions:
            tree.insert("", "end", values=(t["type_transaction"], f"{t["amount"]:.2f}€", t["date_transaction"]))
        
        tree.pack(padx=10, pady=10)
    
    def get_amount(self, prompt):
        try:
            amount = float(simpledialog.askstring("Input", prompt, parent=self.root))
            if amount <= 0:
                raise ValueError
            return amount
        except (ValueError, TypeError):
            messagebox.showwarning("Error", "Invalid amount!", parent=self.root)
            return None


# Usage Example:
# root = tk.Tk()
# dashboard = DashboardView(root, lambda: print("Logout"), user_id=1)
# root.mainloop()