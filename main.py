# Main file (to launch tkinter interface)

from bank.states.connection import *
from bank.states.interface import *


def main():
    connect_interface = Connection()
    connect_interface.init_connection_screen()

    gener_interface = Interface()
    gener_interface.init_general_screen()



if __name__ == '__main__':
    main()