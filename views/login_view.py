from config import *
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.user_controller import UserController

class LoginView:
    def __init__(self, root, show_register):
        self.root = root
        self.show_register = show_register
        self.root.title("Solana Bank | Connection")
        self.root.geometry(MINI_WINDOW_SIZE)

        # Center columns
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)

        # Content center
        frame = ttk.Frame(root)
        frame.grid(row=1, column=1, padx=20, pady=20)

        ttk.Label(frame, text="Login", font=("Arial", 16)).grid(column=0, row=0, columnspan=2, pady=10)
        
        ttk.Label(frame, text="Email : ").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.email_entry = ttk.Entry(frame)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)
    
        ttk.Label(frame, text="Password : ").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        self.login_button = ttk.Button(frame, text="Login", command=self.connecter)
        self.login_button.grid(row=3, column=1, pady=10)

        self.go_register_button = ttk.Button(frame, text="Register", command=self.show_register)
        self.go_register_button.grid(row=4, column=1, pady=10)


    def connecter(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        controller = UserController()
        result = controller.register("Test", "User", email, password)
        messagebox.showinfo("Result", result)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginView(root)
    root.mainloop()
