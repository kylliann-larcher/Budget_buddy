# Main file (to launch tkinter interface)
import tkinter as tk
from views.login_view import LoginView

import tkinter as tk
from views.login_view import LoginView
from views.register_view import RegisterView

class MainApp:
    def __init__(self, root):
        self.root = root
        self.show_login()

    def show_login(self):
        self.clear_window()
        LoginView(self.root, self.show_register)

    def show_register(self):
        self.clear_window()
        RegisterView(self.root, self.show_login)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
