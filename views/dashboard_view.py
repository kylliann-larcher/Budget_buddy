import tkinter as tk
from tkinter import ttk
from controllers.user_controller import UserController

class DashboardView:
    def __init__(self, root):
        self.root = root
        self.root.title("Solana Bank | Dashboard")

        ttk.Label(root, text="Welcome to your dashboard").pack()
