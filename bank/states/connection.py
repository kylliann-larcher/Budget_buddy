# Interface for connection (when connection is OK, go interface.py. Nom, prénom, email, mdp)

from config import *
import tkinter as tk
import tkinter.font
from tkinter import ttk
from tkinter import messagebox
import re

class Connection:
    def __init__(self):
        pass


    # To verify entries
    def validate_input(self, email, password, name=None, first_name=None):
        # To verify if all fields are completed
        if name is not None and first_name is not None:
            if not all([name, first_name, email, password]):
                self.show_error("All fields must be completed.")
                return False
            
        # To verify valid adress mail
        elif "@" not in email or "." not in email.split("@")[-1]:
            self.show_error("Email address invalid.")
            return False

        # To verify vali password
        elif len(password) < 5 or \
           not re.search(r"[A-Za-z]", password) or \
           not re.search(r"\d", password) or \
           not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            self.show_error("Password must contain at least 5 characters, one letter, one number and one special character.")
            return False

        # Validation OK
        else:
            self.show_message("Successful !")
            return True


    def init_connection_screen(self):
        screen = tk.Tk()
        screen.title("Solana Bank | Connection")
        screen.geometry(WINDOW_SIZE)
        screen.configure(bg=BACKGROUND)

        # Initiate fonts
        TITLE_FONT = tkinter.font.Font(family=family_font, size=title_size_font, weight=weight_font)
        SECOND_TITLE_FONT = tkinter.font.Font(family=family_font, size=second_title_size_font, weight=weight_font)
        FONT = tkinter.font.Font(family=family_font, size=size_font, weight=weight_font)

        # Title
        title_label = tk.Label(screen, text="SOLANA", font=TITLE_FONT, bg=BACKGROUND)
        title_label.pack(pady=15)
        scn_title_label = tk.Label(screen, text="BANK", font=TITLE_FONT, bg=BACKGROUND)
        scn_title_label.pack()

        # Initiate frames
        main_frame = tk.Frame(screen)
        main_frame.pack(fill='both', expand=True)

        right_frame = tk.Frame(main_frame, width=550, bg=BACKGROUND)
        right_frame.pack(side='right', fill='both')
        right_frame.pack_propagate(False)

        left_frame = tk.Frame(main_frame, width=550, bg=BACKGROUND)
        left_frame.pack(side='left', fill='both')
        left_frame.pack_propagate(False)

        # Frames center
        inner_l_frame = tk.Frame(left_frame, bg=BACKGROUND)
        inner_l_frame.place(relx=0.5, rely=0.5, anchor="center")
        inner_r_frame = tk.Frame(right_frame, bg=BACKGROUND)
        inner_r_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Sign-Up Zone
        reg_name = tk.StringVar()
        reg_first_name = tk.StringVar()
        reg_email = tk.StringVar()
        reg_password = tk.StringVar()

        under_l_title = tk.Label(inner_l_frame, text="REGISTER", font=SECOND_TITLE_FONT, bg=BACKGROUND)
        under_l_title.pack(fill='x', pady=10)

        name_label = tk.Label(inner_l_frame, text="Family Name : ", font=FONT, bg=BACKGROUND)
        name_label.pack(fill='x')
        name_entry = ttk.Entry(inner_l_frame, textvariable=reg_name, width=60)
        name_entry.pack(fill='x', pady=10)

        first_name_label = tk.Label(inner_l_frame, text="First Name : ", font=FONT, bg=BACKGROUND)
        first_name_label.pack(fill='x')
        first_name_entry = ttk.Entry(inner_l_frame, textvariable=reg_first_name, width=60)
        first_name_entry.pack(fill='x', pady=10)

        email_label = tk.Label(inner_l_frame, text="Email : ", font=FONT, bg=BACKGROUND)
        email_label.pack(fill='x')
        email_entry = ttk.Entry(inner_l_frame, textvariable=reg_email, width=60)
        email_entry.pack(fill='x', pady=10)

        password_label = tk.Label(inner_l_frame, text="Password : ", font=FONT, bg=BACKGROUND)
        password_label.pack(fill='x')
        password_entry = ttk.Entry(inner_l_frame, textvariable=reg_password, show="*", width=60)
        password_entry.pack(fill='x', pady=10)

        register_button = ttk.Button(inner_l_frame, text="Register", command=lambda: self.validate_input(reg_email.get(), reg_password.get(), reg_name.get(), reg_first_name.get()))
        register_button.pack(fill='x', pady=20)

        # Login Zone
        log_email = tk.StringVar()
        log_password = tk.StringVar()

        under_r_title = tk.Label(inner_r_frame, text="LOGIN", font=SECOND_TITLE_FONT, bg=BACKGROUND)
        under_r_title.pack(fill='x', pady=10)

        email_label = tk.Label(inner_r_frame, text="Email : ", font=FONT, bg=BACKGROUND)
        email_label.pack(fill='x')
        email_entry = ttk.Entry(inner_r_frame, textvariable=log_email, width=60)
        email_entry.pack(fill='x', pady=10)

        password_label = tk.Label(inner_r_frame, text="Password : ", font=FONT, bg=BACKGROUND)
        password_label.pack(fill='x')
        password_entry = ttk.Entry(inner_r_frame, textvariable=log_password, show="*", width=60)
        password_entry.pack(fill='x', pady=10)

        login_button = ttk.Button(inner_r_frame, text="Login", command=lambda: self.validate_input(log_email.get(), log_password.get()))
        login_button.pack(fill='x', pady=20)

        screen.mainloop()


    def show_error(self, message):
        messagebox.showerror("Invalid Connection", message)

    def show_message(self, message):
        messagebox.showinfo("Solana Bank", message)