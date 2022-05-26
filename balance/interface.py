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
from balance.utils import normalize_money_amount

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
        index = self._pick_option(["Sign in", "Sign up", "Exit"], "Welcome to MyBalance, Your Bank Management System!")
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
            self.select_bank()
            print("Loading your account data. Wait a second...")
        else:
            index = self._pick_option(["Try again", "Sign up"], f"No data found for {username}")
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
        bank = self._request_bank_name()
        self.database.create_table(bank)
        self.option_menu()

    def option_menu(self):
        # todo: prepare account data to be consulted
        self.window = Window.Options
        options = ["New movement", "Balance Enquiry", "Settings", "Log out", "Exit"]
        index = self._pick_option(options, title="ACTIONS")

        if index == 0:
            self.new_movement()
        elif index == 1:
            self.balance_enquiry()
        elif index == 2:
            self.settings()
        elif index == 3:
            self.start()
        elif index == 4:
            self.exit()

    def new_movement(self):
        index = self._pick_option(["Income", "Expense", "Transaction", "Return"], "Select your next movement:")
        if index == 0:
            self.set_income()
        elif index == 1:
            self.set_expense()
        elif index == 2:
            raise NotImplementedError("Transaction")
        elif index == 3:
            self.option_menu()

    def set_income(self):
        os.system('cls')
        income = input("Introduce your income: ")
        income = normalize_money_amount(income)
        category = input("Introduce the income category (e.g., WORK): ")
        desc = input("Introduce a description: ")
        self.database.new_income(amount=income, category=category, desc=desc)
        input("Press any key to continue with other movements")
        self.option_menu()

    def set_expense(self):
        os.system('cls')
        expense = input("Introduce your expense: ")
        expense = normalize_money_amount(expense)
        category = input("Introduce the expense category (e.g., GROCERY): ")
        desc = input("Introduce a description: ")
        self.database.new_expense(amount=expense, category=category, desc=desc)
        input("Press any key to continue with other movements")
        self.option_menu()

    def balance_enquiry(self):
        index = self._pick_option(["Current balance", "Last movements", "Export history", "Return"], "Select a type of enquiry:")
        if index == 0:
            self.see_balance()
        elif index == 1:
            raise NotImplementedError("Last movements")
        elif index == 2:
            raise NotImplementedError("Export History")
        elif index == 3:
            self.option_menu()

    def see_balance(self):
        # TODO: When showing the current balance, display table with most recent movements
        os.system('cls')
        current_balance = self.database.current_balance()
        print(f"Your actual balance is {current_balance}")
        input("Press any key to continue with other movements")
        self.option_menu()

    def settings(self):
        index = self._pick_option(["Switch account", "Delete account", "Modify your profile", "Return"])
        if index == 0:
            raise NotImplementedError("Switch Account")
        elif index == 1:
            raise NotImplementedError("Delete Account")
        elif index == 2:
            raise NotImplementedError("Modify your profile")
        elif index == 3:
            self.option_menu()

    def select_bank(self):
        bank_list = self.database.check_accounts()
        if len(bank_list) == 0:
            print("Your account is not attached to any bank yet. Select one. ")
            bank = self._request_bank_name()
            self.database.create_table(name=bank)
            self.option_menu()
        elif len(bank_list) == 1:
            bank = bank_list[0]
            self.option_menu()
        else:
            index = self._pick_option(bank_list, title="Select one of your accounts.")
            bank = bank_list[index]
        self.database.target_bank = bank

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

    @staticmethod
    def _request_bank_name():
        bank = input("Bank: ")
        return bank.lower()

    @staticmethod
    def _pick_option(options: List[str], title: str = "Select an option:") -> int:
        _, index = pick(options, title)
        return index







