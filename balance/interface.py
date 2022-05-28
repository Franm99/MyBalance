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
import sys
import time
from typing import Optional

from balance.account import Account
from balance.rsc import *
from balance.database import DataBase
from balance.utils import normalize_money_amount, cmd_clear, print_and_wait

dir_path = os.path.join(os.environ['APPDATA'], APP_NAME)
if not os.path.exists(dir_path):
     os.makedirs(dir_path)


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
        self.database = Optional[DataBase]
        # self._init_ui()
        self.w_start()

    def w_start(self):
        """ Initial state: Logging window. """
        index = self._pick_option(["Sign in", "Sign up", "Exit"],
                                  f"Welcome to {APP_NAME}, Your Bank Management System!")
        if index == 0:
            self.w_sign_in()
        elif index == 1:
            self.w_sign_up()
        elif index == 2:
            self.w_exit()

    def w_sign_in(self):
        os.system('cls')
        print("SIGN IN")
        owner = self._request_username()
        owner_db = owner.db_path

        if os.path.exists(owner_db):
            self.database = DataBase(owner_db)
            self.select_bank()
            print("Loading your account data. Wait a second...")
        else:
            index = self._pick_option(["Try again", "Sign up"], f"No data found for {owner.full_name}")
            if index == 0:
                self.w_sign_in()
            else:
                self.w_sign_up(owner)
        self.w_option_menu()

    def w_sign_up(self, owner=Optional[Owner]):
        print("SIGN UP")
        if not owner:
            owner = self._request_username()
        self.database = DataBase(owner.db_path)
        self.new_account()
        self.w_option_menu()

    def w_option_menu(self):
        self.window = Window.Options
        options = ["New movement", "Balance Enquiry", "Account Settings", "Log out", "Exit"]
        index = self._pick_option(options, title=f"Bank: {self.database.target_bank}")

        if index == 0:
            self.w_new_movement()
        elif index == 1:
            self.w_balance_enquiry()
        elif index == 2:
            self.w_settings()
        elif index == 3:
            self.w_start()
        elif index == 4:
            self.w_exit()

    def w_new_movement(self):
        index = self._pick_option(["Income", "Expense", "Transaction", "Return"], "Select your next movement:")
        if index == 0:
            self.set_income()
        elif index == 1:
            self.set_expense()
        elif index == 2:
            self.set_transaction()
        elif index == 3:
            self.w_option_menu()

    def w_balance_enquiry(self):
        index = self._pick_option(["Current balance", "Last movements", "Export history", "Return"], "Select a type of enquiry:")
        if index == 0:
            self.see_balance()
        elif index == 1:
            # self.see_last_movements()
            raise NotImplementedError("Last movements")  # todo: implement pandas to print table
        elif index == 2:
            raise NotImplementedError("Export History")  # todo: implement pandas to generate graphics
        elif index == 3:
            self.w_option_menu()

    def w_settings(self):
        index = self._pick_option(["Switch account", "New account", "Delete bank account", "Your profile", "Return"])
        if index == 0:
            self.select_bank()
        elif index == 1:
            self.new_account()
        elif index == 2:
            self.delete_account()
        elif index == 3:
            self.w_your_profile()
        elif index == 4:
            self.w_option_menu()

    def w_your_profile(self):
        index = self._pick_option(["Update owner", "Modify movement concept", f"Delete {APP_NAME} profile", "Return"])
        if index == 0:
            self.rename_owner()
        elif index == 1:
            raise NotImplementedError("Modify movement concept")
        elif index == 2:
            self.delete_profile()
        elif index == 3:
            self.w_settings()

    def w_exit(self):
        self._exit()

    def w_confirmation(self, info: str) -> bool:
        index = self._pick_option(["Yes", "No"], title=info)
        return index == 0

    @cmd_clear
    def new_account(self):
        bank = self._request_bank_name()
        self.database.create_table(bank)
        self.w_option_menu()

    @cmd_clear
    def delete_account(self):
        if self.w_confirmation(info="Are your sure? All your bank account data will be deleted."):
            self.database.delete_account()
            self.select_bank()
        else:
            self.w_settings()

    @cmd_clear
    def delete_profile(self):
        if self.w_confirmation("WARNING: YOUR WHOLE DATA AND HISTORY WILL BE DELETED FOREVER. ARE YOUR SURE?"):
            self.database.delete_profile()
            print(f"Hope to see you again using {APP_NAME}!")
            time.sleep(1.0)
            self.w_start()
        else:
            self.w_your_profile()

    @cmd_clear
    def set_income(self):
        movement = self._request_movement_data(Concept.Income)
        self.database.new_income(movement)
        print_and_wait()
        self.w_option_menu()

    @cmd_clear
    def set_expense(self):
        movement = self._request_movement_data(Concept.Expense)
        self.database.new_expense(movement)
        print_and_wait()
        self.w_option_menu()

    @cmd_clear
    def set_transaction(self):
        bank_list = self.database.check_accounts()
        bank_list.remove(self.database.target_bank)
        to_bank = None
        if len(bank_list) == 0:
            print_and_wait("You have no more registered bank accounts. Can´t do a transaction.")
            self.w_new_movement()
        elif len(bank_list) == 1:
            to_bank = bank_list[0]
        else:
            index = self._pick_option(bank_list, title="To which bank do you want to perform a transaction?")
            to_bank = bank_list[index]
        print(f"Transaction: {self.database.target_bank} -> {to_bank}")
        movement = self._request_movement_data(concept=Concept.Transaction)
        # todo check that the transaction is not higher than the total balance
        self.database.new_transaction(movement, to_bank)
        print_and_wait()
        self.w_option_menu()

    @cmd_clear
    def see_balance(self) -> None:
        current_balance = self.database.current_balance()
        print_and_wait(f"Your actual balance is {current_balance}")
        self.w_option_menu()

    @cmd_clear
    def see_last_movements(self):
        print_and_wait(self.database.last_movements)

    @cmd_clear
    def select_bank(self) -> None:
        bank_list = self.database.check_accounts()
        if len(bank_list) == 0:
            print("Your account is not attached to any bank yet. Specify one. ")
            bank = self._request_bank_name()
            self.database.create_table(name=bank)
        elif len(bank_list) == 1:
            bank = bank_list[0]
            self.database.target_bank = bank
            print_and_wait(f"Your account: {self.database.target_bank}")
        else:
            index = self._pick_option(bank_list, title="Select one of your accounts.")
            bank = bank_list[index]
        self.database.target_bank = bank
        self.w_option_menu()

    @cmd_clear
    def rename_owner(self):
        owner = self._request_username()
        self.database.rename_owner(owner)

    @staticmethod
    def _request_username() -> Owner:
        name = input("Name: ")
        surname = input("Surname: ")
        owner = Owner(name, surname, dir_path)
        return owner

    @staticmethod
    def _request_bank_name():
        bank = input("Bank: ")
        return bank

    @staticmethod
    def _request_movement_data(concept: Concept):
        amount = input(f"Introduce your {concept.lower()}: ")
        amount = normalize_money_amount(amount)
        if concept == concept.Transaction:
            category = Category.Transaction
        else:
            category = input(f"Introduce movement category (WORK, GROCERY, BIZUM...): ")
        desc = input("Introduce a description (optional): ")
        return Movement(amount=amount, category=category, concept=concept, desc=desc)

    @staticmethod
    def _pick_option(options: List[str], title: str = "Select an option:") -> int:
        _, index = pick(options, title)
        return index

    @staticmethod
    @cmd_clear
    def _exit():
        print("Bye!")
        time.sleep(0.5)
        sys.exit()
        # os.system('exit')

    @staticmethod
    def _init_ui():
        os.system('mode 70,20')
        os.system('color b0')
