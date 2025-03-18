# Interface tkinter after connection (total amount, graphic total amount per day, alerts if amount < 0)

from config import *
import tkinter as tk
import tkinter.font
from tkinter import ttk
from bank.entities.operations import *
from bank.entities.history  import HistoryWindow

class Interface:
    def __init__(self):
        pass

    def init_general_screen(self):
        screen = tk.Tk()
        screen.title("Solana Bank | Dashboard")
        screen.geometry(WINDOW_SIZE)
        screen.configure(bg=BACKGROUND)

        # Initiate fonts
        TITLE_FONT = tkinter.font.Font(family=family_font, size=title_size_font, weight=weight_font)
        SECOND_TITLE_FONT = tkinter.font.Font(family=family_font, size=second_title_size_font, weight=weight_font)
        FONT = tkinter.font.Font(family=family_font, size=size_font, weight=weight_font)

        # Title
        title_label = tk.Label(screen, text="DASHBOARD", font=TITLE_FONT, bg=BACKGROUND)
        title_label.pack(pady=15)

        # Initiate frames
        main_frame = tk.Frame(screen, bg=BACKGROUND)
        main_frame.pack(fill='both', expand=True)

        top_frame = tk.Frame(main_frame, bg=BACKGROUND)
        top_frame.pack(side='top', expand=True)

        bottom_frame = tk.Frame(main_frame, bg=BACKGROUND)
        bottom_frame.pack(side='bottom', expand=True)


        # Treeview for visualisation (informations of the actual user link to the email use to login)
        """Name, First Name, ID of the account, amount total"""
        """account_tree = ttk.Treeview(top_frame, columns=columns, show='headings')"""
        """account_tree.pack(padx=10, pady=5)"""

        # Title of columns
        """for col in columns:
            product_tree.heading(col, text=col)
            product_tree.column(col, width=160, anchor="center")"""
        

        # Button Zone
        deposit_button = tk.Button(bottom_frame, text='Deposit', width=25, command=lambda: DepositWindow(screen))
        deposit_button.pack(padx=30, side=tk.LEFT)

        debit_button = tk.Button(bottom_frame, text='Debit', width=25, command=lambda: DebitWindow(screen))
        debit_button.pack(padx=30, side=tk.LEFT)

        transfer_button = tk.Button(bottom_frame, text='Transfer', width=25, command=lambda: TransferWindow(screen))
        transfer_button.pack(padx=30, side=tk.LEFT)

        history_button = tk.Button(bottom_frame, text='History', width=25, command=lambda: HistoryWindow(screen))
        history_button.pack(padx=30, side=tk.LEFT)




        screen.mainloop()