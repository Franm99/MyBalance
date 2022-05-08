"""
Author: Fran Moreno
Contact: fran.moreno.se@gmail.com
Date: 06/05/2022

Desc: 
# Fill 
"""
import os
import sqlite3
import time

from balance.account import Account


class DataBase:
    # Todo: Create base methods to request/insert things from/to database
    def __init__(self, db_file: str):
        self.db_file = db_file

        try:
            self.connection = sqlite3.connect(self.db_file)
        except sqlite3.Error as error:
            print(error)

        self.cursor = self.connection.cursor()

    def create_table(self, deposit):
        # todo: add date field and code
        self.cursor.execute(
            "CREATE TABLE account(id INTEGER PRIMARY KEY, balance text, movement text, amount real, category text, desc text)"
        )

        # Add first movement
        self.cursor.execute(
            f"INSERT INTO account(balance, movement, amount, category, desc) VALUES({deposit}, 'INCOME', {deposit}, 'NEW_ACCOUNT', 'new account')"
        )
        self.connection.commit()

    def new_entry(self, movement, amount, category, desc):
        # Balance will be read from the last movement
        self.cursor.execute("SELECT balance FROM account ORDER BY id DESC LIMIT 1")
        last_balance = self.cursor.fetchone()[0]
        # todo: improve the add method
        curr_balance = str(float(last_balance) + float(amount))
        entities = (curr_balance, movement, amount, category, desc)
        self.cursor.execute(
            """INSERT INTO account(balance, movement, amount, category, desc)
               VALUES (?, ?, ?, ?, ?)""",
            entities
        )
        self.connection.commit()

    def new_income(self, amount, category, desc):
        self.new_entry('INCOME', amount, category, desc)

    def new_expense(self, amount, category, desc):
        amount = str(-float(amount))
        self.new_entry('EXPENSE', amount, category, desc)

    def current_balance(self):
        self.cursor.execute(
            """SELECT balance FROM account ORDER BY id DESC LIMIT 1"""
        )
        return self.cursor.fetchone()[0]
