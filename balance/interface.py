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

from balance.account import Account
from balance.rsc import *
from balance.database import DataBase

DB_PATH = 'db'

class Window(StrEnum):
    Start = 'A'
    SignIn = 'B'
    SignUp = 'C'
    Options = 'D'
    Exit = 'X'


class UI:
    """ Class to define the states that the User Interface can have in a bash terminal. """
    def __init__(self):
        self.window = None
        self.account = None
        self.database = None
        self.start()

    def start(self):
        """ Initial state: Logging window. """
        self.window = Window.Start
        options = ["Sign in", "Sign up", "Exit"]
        title = "Check your balance"
        option, index = pick(options, title)
        if index == 0:
            self.sign_in()
        elif index == 1:
            self.sign_up()
        elif index == 2:
            self.exit()

    def sign_in(self):
        self.window = Window.SignIn
        os.system('cls')

        print("SIGN IN")
        username = self._request_username()
        user_db = f"{DB_PATH}/{username}.db"

        if os.path.exists(user_db):
            self.database = DataBase(user_db)
            print("Loading your account data. Wait a second...")
        else:
            title = "This user is not registered yet"
            options = ["Try again", "Sign up"]
            option, index = pick(options, title)
            if index == 0:
                self.sign_in()
            else:
                self.sign_up(username)
        self.option_menu()

    def sign_up(self, username=None):
        self.window = Window.SignUp
        print("SIGN UP")
        if not username:
            username = self._request_username()
        user_db = f"{DB_PATH}/{username}.db"
        self.database = DataBase(user_db)

        deposit = input("Your initial deposit: ")  # todo: option for empty deposit
        self.database.create_table(deposit)
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
        os.system('cls')
        income = input("Introduce your income: ")
        category = input("Introduce the income category (e.g., WORK): ")
        desc = input("Introduce a description: ")
        self.database.new_income(amount=income, category=category, desc=desc)
        input("Press any key to continue with other movements")
        self.option_menu()

    def set_expense(self):
        os.system('cls')
        expense = input("Introduce your expense: ")
        category = input("Introduce the expense category (e.g., GROCERY): ")
        desc = input("Introduce a description: ")
        self.database.new_expense(amount=expense, category=category, desc=desc)
        input("Press any key to continue with other movements")
        self.option_menu()

    def see_balance(self):
        os.system('cls')
        current_balance = self.database.current_balance()
        print(f"Your actual balance is {current_balance}")
        input("Press any key to continue with other movements")
        self.option_menu()

    def exit(self):
        self.window = Window.Exit
        os.system('cls')
        print("Bye!")
        time.sleep(0.5)
        exit()

    @staticmethod
    def _request_username():
        name = input("Name: ")
        surname = input("Surname: ")
        user = f"{name.lower()}{surname.lower()}"
        return user







