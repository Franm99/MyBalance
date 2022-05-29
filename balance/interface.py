"""
Author: Fran Moreno
Contact: fran.moreno.se@gmail.com
Date: 01/05/2022

Desc: 
TODO: Try to implement threads for the UI management
"""
from strenum import StrEnum
from pick import pick
import os
import sys
import time
from typing import Optional
from datetime import datetime

from balance.rsc import *
from balance.database import DataBase
from balance.utils import normalize_money_amount, cmd_clear, print_and_wait, normalize_date

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

    @cmd_clear
    def w_sign_in(self, owner_data: Optional[Owner] = None) -> None:
        if owner_data is None:
            owner_data = self._request_owner_data()
        print("SIGN IN")
        owner_db = owner_data.db_path

        if os.path.exists(owner_db):
            self.database = DataBase(owner_db)
            self.select_source()
        else:
            index = self._pick_option(["Try again", "Sign up"], f"No data found for {owner_data.full_name}")
            if index == 0:
                self.w_sign_in()
            else:
                self.w_sign_up(owner_data)
        self.w_option_menu()

    @cmd_clear
    def w_sign_up(self, owner_data: Optional[Owner] = None) -> None:
        print("SIGN UP")
        if owner_data is None:
            owner_data = self._request_owner_data()
        if os.path.isfile(owner_data.db_path):
            if self.w_confirmation(f"The user {owner_data.full_name} already exists. Do you want to sign in?"):
                self.w_sign_in(owner_data)
            else:
                self.w_sign_up()
        else:
            self.database = DataBase(owner_data.db_path)
            self.new_source()
            self.w_option_menu()

    def w_option_menu(self):
        self.window = Window.Options
        options = ["New movement", "Balance Enquiry", "Account Settings", "Log out", "Exit"]
        index = self._pick_option(options, title=f"Source: {self.database.target_source}")

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
            self.see_last_movements()
        elif index == 2:
            raise NotImplementedError("Export History")  # todo: implement pandas to generate graphics
        elif index == 3:
            self.w_option_menu()

    def w_settings(self):
        index = self._pick_option(["Switch source", "New source", "Delete source", "Your profile", "Return"])
        if index == 0:
            self.select_source()
        elif index == 1:
            self.new_source()
        elif index == 2:
            self.delete_source()
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
    def new_source(self):
        source = self._request_source_name()
        self.database.create_table(source)
        self.w_option_menu()

    @cmd_clear
    def delete_source(self):
        if self.w_confirmation(
                info=f"Are your sure? The whole history of your source {self.database.target_source} will be deleted."):
            self.database.delete_source()
            self.select_source()
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
        movement = self._request_movement_data(Category.Income)
        self.database.new_income(movement)
        print_and_wait()
        self.w_option_menu()

    @cmd_clear
    def set_expense(self):
        movement = self._request_movement_data(Category.Expense)
        self.database.new_expense(movement)
        print_and_wait()
        self.w_option_menu()

    @cmd_clear
    def set_transaction(self):
        source_list = self.database.check_sources()
        source_list.remove(self.database.target_source)
        to_source = None
        if len(source_list) == 0:
            print_and_wait("You have only one source registered. Can´t do a transaction.")
            self.w_new_movement()
        elif len(source_list) == 1:
            to_source = source_list[0]
        else:
            index = self._pick_option(source_list, title="Select which source will receive the transaction: ")
            to_source = source_list[index]
        print(f"Transaction: {self.database.target_source} -> {to_source}")
        movement = self._request_movement_data(Category.Transaction)
        # todo check that the transaction is not higher than the total balance
        self.database.new_transaction(movement, to_source)
        print_and_wait()
        self.w_option_menu()

    @cmd_clear
    def see_balance(self) -> None:
        current_balance = self.database.current_balance()
        print_and_wait(f"Your actual balance is {current_balance}")
        self.w_option_menu()

    @cmd_clear
    def see_last_movements(self):
        # todo: Option to either enquiry older history or go to the main menu again
        last_movements = self.database.last_movements
        if last_movements:
            print_and_wait(self.database.last_movements)
        else:
            print_and_wait("No movements registered for this source yet.")
        self.w_option_menu()

    @cmd_clear
    def select_source(self) -> None:
        source_list = self.database.check_sources()
        if len(source_list) == 0:
            print("Your account is not attached to any source yet. Specify your source: ")
            source = self._request_source_name()
            self.database.create_table(name=source)
        elif len(source_list) == 1:
            source = source_list[0]
            self.database.target_source = source
            print_and_wait(f"Your Source: {self.database.target_source}")
        else:
            index = self._pick_option(source_list, title="Select one of your sources: ")
            source = source_list[index]
        self.database.target_source = source
        self.w_option_menu()

    @cmd_clear
    def rename_owner(self):
        owner = self._request_owner_data()
        self.database.rename_owner(owner)

    @staticmethod
    def _request_owner_data() -> Owner:
        name = input("Name: ")
        surname = input("Surname: ")
        owner = Owner(name, surname, dir_path)
        return owner

    @staticmethod
    def _request_source_name():
        source = input("Source: ")
        return source

    def _request_movement_data(self, category: Category):
        amount = self.__req_amount(category)
        concept = self.__req_concept()
        date = self.__req_date()
        desc = self.__req_desc()
        return Movement(date, amount, category.value, concept, desc)

    def __req_amount(self, category: Category) -> str:
        amount = input(f"Please write your {category.lower()} [XX.YY]: ")
        if any(c.isalpha() for c in amount):
            print("A money amount can't contain letters or symbols.")
            self.__req_amount(category)
        return normalize_money_amount(amount)

    def __req_date(self) -> str:
        date = input(f"Please write the movement date [MM-DD-YY] (if today, skip this field): ")
        if not date:
            return datetime.today().strftime('%m-%d-%Y')
        else:
            if normalize_date(date):
                return normalize_date(date)
            else:
                print("The date format is not correct.")
                self.__req_date()

    def __req_concept(self) -> str:
        concept = input(f"Please write the movement concept [Work/Grocery/...] or leave it empty [Other]: ")
        if not concept:
            return Concept.General
        elif len(concept) > 20:
            print("The concept should not contain more than 20 characters.")
            self.__req_concept()
        else:
            return concept

    def __req_desc(self):
        desc = input("Write a description [optional]: ")
        if len(desc) > 70:
            print("The description should not contain more than 70 characters")
            self.__req_desc()
        return desc

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


def dev():
    from dateutil import parser
    date = input("Date [MM-DD-YY]: ")
    try:
        date = parser.parse(date)
    except parser.ParserError:
        print("Introduce a valid date")
        dev()

    print(date.strftime("%m-%d-%y"))


if __name__ == '__main__':
    dev()
