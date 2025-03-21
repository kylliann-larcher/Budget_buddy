
from config import *
import tkinter as tk
from views.login_view import LoginView
from views.register_view import RegisterView
from views.dashboard_view import DashboardView

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry(WINDOW_SIZE)

        self.show_login()

    def show_login(self):
        self.clear_window()
        LoginView(self.root, self.show_register, self.show_dashboard)

    def show_register(self):
        self.clear_window()
        RegisterView(self.root, self.show_login)

    def show_dashboard(self, user_id):
        self.clear_window()
        self.user_id = user_id 
        DashboardView(self.root, self.show_login, self.user_id)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()