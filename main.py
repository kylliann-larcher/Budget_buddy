# Main file (to launch tkinter interface)

from bank.states.connection import *

def main():
    connect_interface = Connection()
    connect_interface.init_screen()



if __name__ == '__main__':
    main()