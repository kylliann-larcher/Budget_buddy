# Login Interface
from config import *
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.user_controller import UserController

class LoginView:
    def __init__(self, root, show_register, show_dashboard):
        self.root = root
        self.show_register = show_register
        self.show_dashboard = show_dashboard
        self.root.title("Solana Bank | Connection")
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=BACKGROUND)

        # Style
        style = ttk.Style()
        style.configure("TFrame", background=BACKGROUND)
        style.configure("TLabel", background=BACKGROUND, foreground="white")
        style.configure("TButton", foreground="black")
        style.map("TButton", background=[("active", BACKGROUND), ("!active", BACKGROUND)])

        # Center columns
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)

        # Title principal
        title_frame = ttk.Frame(root, style="TFrame")
        title_frame.grid(row=0, column=0, columnspan=3, pady=20)

        title_welcome = ttk.Label(title_frame, text="Welcome to", font=('Arial', 26), style="TLabel")
        title_welcome.pack()

        title = ttk.Label(title_frame, text="SOLANA BANK", font=('Arial', 30, 'bold'), style="TLabel")
        title.pack()

        # Content
        frame = ttk.Frame(root, style="TFrame")
        frame.grid(row=1, column=1, padx=20, pady=20)

        ttk.Label(frame, text="Login", font=('Arial', 18), style="TLabel").grid(column=0, row=0, columnspan=2, pady=10)

        ttk.Label(frame, text="Email :", style="TLabel").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.email_entry = ttk.Entry(frame, width=25)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)
    
        ttk.Label(frame, text="Password :", style="TLabel").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = ttk.Entry(frame, width=25, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        self.login_button = ttk.Button(frame, text="Login", command=self.connecter, style="TButton")
        self.login_button.grid(row=3, column=1, pady=10)

        self.go_register_button = ttk.Button(frame, text="Register", command=self.show_register, style="TButton")
        self.go_register_button.grid(row=4, column=1, pady=10)

    # To connect an user from db
    def connecter(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        controller = UserController()
        user_id = controller.connect(email, password)

        if user_id:
            messagebox.showinfo("Success", "Login successful!")
            self.show_dashboard(user_id)
        else:
            messagebox.showerror("Error", "Invalid email or password")
