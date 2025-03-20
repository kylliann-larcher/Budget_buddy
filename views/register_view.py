from config import *
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.user_controller import UserController
import tkinter.font

class RegisterView:
    def __init__(self, root, show_login):
        self.root = root
        self.root.title("Solana Bank | Register")
        self.show_login = show_login
        self.controller = UserController()

        # Center columns
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)

        # Cadre principal
        self.frame = ttk.Frame(root)
        self.frame.grid(row=1, column=1, padx=20, pady=20)

        ttk.Label(self.frame, text="Register", font=('Arial', 18)).grid(column=0, row=0, columnspan=2, pady=10)

        # Champs de saisie
        ttk.Label(self.frame, text="Name : ").grid(column=0, row=1, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(self.frame, width=30)
        self.name_entry.grid(column=1, row=1, pady=5)

        ttk.Label(self.frame, text="First Name : ").grid(column=0, row=2, sticky=tk.W, pady=5)
        self.first_name_entry = ttk.Entry(self.frame, width=30)
        self.first_name_entry.grid(column=1, row=2, pady=5)

        ttk.Label(self.frame, text="Email : ").grid(column=0, row=3, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(self.frame, width=30)
        self.email_entry.grid(column=1, row=3, pady=5)

        ttk.Label(self.frame, text="Password : ").grid(column=0, row=4, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(self.frame, width=30, show="*")
        self.password_entry.grid(column=1, row=4, pady=5)

        ttk.Label(self.frame, text="Confirm Password : ").grid(column=0, row=5, sticky=tk.W, pady=5)
        self.confirm_password_entry = ttk.Entry(self.frame, width=30, show="*")
        self.confirm_password_entry.grid(column=1, row=5, pady=5)

        # Message d'information
        ttk.Label(self.frame, text="Password need to have\n"
                                   "- One uppercase letter\n- One lowercase letter\n"
                                   "- One number\n- One special caracter\n"
                                   "- Minimum 5 caracters", justify="left").grid(column=0, row=6, columnspan=2, pady=5)

        # Boutons
        btn_frame = ttk.Frame(self.frame)
        btn_frame.grid(column=0, row=7, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Register", command=self.register).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Back", command=self.back_connection).pack(side=tk.LEFT, padx=5)

    def register(self):
        name = self.name_entry.get().strip()
        first_name = self.first_name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Vérification des champs
        if not all([name, first_name, email, password, confirm_password]):
            messagebox.showerror("Error", "All fields must be completed")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords doesn't fit together")
            return

        # Appel du contrôleur
        result = self.controller.save_user(name, first_name, email, password)

        if "success" in result.lower():
            messagebox.showinfo("Success", result)
            self.show_login()
        else:
            messagebox.showerror("Error", result)

    def back_connection(self):
        self.frame.destroy()
        self.show_login()