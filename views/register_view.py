# Register Interface
from config import *
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.user_controller import UserController

class RegisterView:
    def __init__(self, root, show_login):
        self.root = root
        self.show_login = show_login
        self.root.title("Solana Bank | Register")
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
        
        ttk.Label(frame, text="Register", font=('Arial', 18), style="TLabel").grid(column=0, row=0, columnspan=2, pady=10)
        
        ttk.Label(frame, text="Name:", style="TLabel").grid(column=0, row=1, sticky=tk.E, pady=5)
        self.name_entry = ttk.Entry(frame, width=25)
        self.name_entry.grid(column=1, row=1, pady=5)
        
        ttk.Label(frame, text="First Name:", style="TLabel").grid(column=0, row=2, sticky=tk.E, pady=5)
        self.first_name_entry = ttk.Entry(frame, width=25)
        self.first_name_entry.grid(column=1, row=2, pady=5)
        
        ttk.Label(frame, text="Email:", style="TLabel").grid(column=0, row=3, sticky=tk.E, pady=5)
        self.email_entry = ttk.Entry(frame, width=25)
        self.email_entry.grid(column=1, row=3, pady=5)
        
        ttk.Label(frame, text="Password:", style="TLabel").grid(column=0, row=4, sticky=tk.E, pady=5)
        self.password_entry = ttk.Entry(frame, width=25, show="*")
        self.password_entry.grid(column=1, row=4, pady=5)
        
        ttk.Label(frame, text="Confirm Password:", style="TLabel").grid(column=0, row=5, sticky=tk.E, pady=5)
        self.confirm_password_entry = ttk.Entry(frame, width=25, show="*")
        self.confirm_password_entry.grid(column=1, row=5, pady=5)
        
        ttk.Label(frame, text="Password requirements:\n- One uppercase letter\n- One lowercase letter\n- One number\n- One special character\n- Minimum 10 characters", justify="left", style="TLabel").grid(column=0, row=6, columnspan=2, pady=5)
        
        # Buttons
        self.register_button = ttk.Button(frame, text="Register", command=self.register, style="TButton")
        self.register_button.grid(column=1, row=7, pady=10)
        
        self.back_button = ttk.Button(frame, text="Back", command=self.show_login, style="TButton")
        self.back_button.grid(column=1, row=8, pady=5)
        
    def register(self):
        name = self.name_entry.get().strip()
        first_name = self.first_name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if not all([name, first_name, email, password, confirm_password]):
            messagebox.showerror("Error", "All fields must be completed")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        controller = UserController()
        result = controller.save_user(name, first_name, email, password)
        
        if "success" in result.lower():
            messagebox.showinfo("Success", result)
            self.show_login()
        else:
            messagebox.showerror("Error", result)
