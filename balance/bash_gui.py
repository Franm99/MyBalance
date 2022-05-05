"""
Author: Fran Moreno
Contact: fran.moreno.se@gmail.com
Date: 01/05/2022

Desc: 
TODO: Try to implement threads for the UI management
TODO: Try to use some module to improve the UI
"""
from strenum import StrEnum
from pick import pick
import os
import time


class Window(StrEnum):
    Start = 'A'
    Login = 'B'
    Sign = 'C'
    Options = 'D'
    Exit = 'X'


class BashUI:
    """ Class to define the states that the User Interface can have in a bash terminal. """
    def __init__(self):
        self.window = None
        self.start()

    def start(self):
        """ Initial state: Logging window. """
        # todo: Check if database exists, create if not
        # Options: (1) Log in, (2) Sign in, (3) Exit.
        self.window = Window.Start
        options = ["Log in", "Sign in", "Exit"]
        title = "Check your balance"
        option, index = pick(options, title)
        if index == 0:
            self.log_in()
        elif index == 1:
            self.sign_in()
        elif index == 2:
            self.exit()

    def log_in(self):
        # todo: Add log-in step. Check db
        self.window = Window.Login
        self.option_menu()

    def sign_in(self):
        # todo: Add sign-in step. Add new user to db
        self.window = Window.Sign
        print("Sign your data...")
        print("Signed in")
        self.option_menu()

    def option_menu(self):
        # todo: prepare account data to be consulted
        self.window = Window.Options
        title = "Select your movement"
        options = ["Set income", "Set expense", "See balance", "Log out", "Exit"]
        option, index = pick(options, title)

        if index == 0:
            self.set_income()
        elif index == 1:
            self.set_expense()
        elif index == 2:
            self.see_balance()
        elif index == 3:
            self.start()
        elif index == 4:
            self.exit()

    def set_income(self):
        # todo: save movement in account history
        os.system('cls')
        input("Introduce your income: ")
        input("Press any key to continue with other movements")
        self.option_menu()

    def set_expense(self):
        # todo: save movement in account history
        os.system('cls')
        input("Introduce your expense: ")
        input("Press any key to continue with other movements")
        self.option_menu()

    def see_balance(self):
        # todo: show current balance
        os.system('cls')
        print("Your actual balance is XXX")
        input("Press any key to continue with other movements")
        self.option_menu()

    def exit(self):
        self.window = Window.Exit
        os.system('cls')
        print("Bye!")
        time.sleep(0.5)
        exit()







