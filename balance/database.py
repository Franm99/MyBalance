"""
Author: Fran Moreno
Contact: fran.moreno.se@gmail.com
Date: 06/05/2022

Desc: 
# Fill 
"""
import os
import sqlite3
# import time
from datetime import datetime

from balance.account import Account
from balance.utils import normalize_money_amount
from balance.rsc import Concept, Category


class DataBase:
    # Todo: Create base methods to request/insert things from/to database
    def __init__(self, db_file: str):
        self.db_file = db_file
        self._target_bank = None

        try:
            self.connection = sqlite3.connect(self.db_file)
        except sqlite3.Error as error:
            print(error)
            
        self.cursor = self.connection.cursor()
        self.bank_list = self.check_accounts()
        if len(self.bank_list) == 1:
            self._target_bank = self.bank_list[0]

    @property
    def target_bank(self) -> str:
        return self._target_bank

    @target_bank.setter
    def target_bank(self, bank):
        self._target_bank = bank

    def create_table(self, name):
        self.cursor.execute(
            """
            CREATE TABLE "{}" (
                                "INDEX"	        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                "DATE"	        TEXT    NOT NULL,
                                "TYPE"	        TEXT    NOT NULL,
                                "CATEGORY"	    TEXT    NOT NULL,
                                "AMOUNT"	    NUMERIC NOT NULL,
                                "DESCRIPTION"	TEXT
            );
            """.format(name)
        )
        self.connection.commit()
        self.bank_list.append(name)
        self._target_bank = name

    def new_entry(self, movement_type, amount, category, desc):
        date = datetime.today().strftime('%m-%d-%Y')
        entities = (date, movement_type, category, amount, desc)
        self.cursor.execute(
            """
            INSERT INTO 
            {}(DATE, TYPE, CATEGORY, AMOUNT, DESCRIPTION)
            VALUES (?, ?, ?, ?, ?)
            """.format(self._target_bank),
            entities
        )
        self.connection.commit()

    def new_income(self, amount, category, desc):
        self.new_entry(Concept.Income, amount, category, desc)

    def new_expense(self, amount, category, desc):
        amount = normalize_money_amount(amount)
        self.new_entry(Concept.Expense, amount, category, desc)

    def new_transaction(self, amount, from_bank, to_bank, desc):
        amount = normalize_money_amount(amount)

        try:
            self.new_entry(Concept.Expense, amount, Category.Transaction, desc)
        except NameError:
            print(f"Can't get access to {from_bank} as it is not being managed at the moment.")

        # TODO Keep working on this

    def current_balance(self):
        self.cursor.execute(
            """
            SELECT TYPE, AMOUNT FROM {} 
            """.format(self._target_bank)
        )
        current_balance = 0.0
        for t, amount in self.cursor.fetchall():
            amount = -amount if t == Concept.Expense else amount
            current_balance += amount
        return normalize_money_amount(current_balance)

    def check_accounts(self):
        self.cursor.execute(
            f"""SELECT name FROM sqlite_master WHERE type='table';"""
        )
        bank_list = [i[0] for i in self.cursor.fetchall() if i[0] != "sqlite_sequence"]
        return bank_list

    def _sql_insert(self, **kwargs):
        keys = f"({', '.join(kwargs.keys())})"
        values = list(kwargs.values())
        val_query = '?, ' * len(values)
        query = f"""INSERT INTO {self._target_bank}{keys} VALUES({val_query[:-2]})"""
        self.cursor.execute(query, values)
        self.connection.commit()

    def delete_account(self):
        self.cursor.execute(
            """DROP TABLE {}""".format(self._target_bank)
        )
        self.connection.commit()

    def sql_insert(self, **kwargs):
        self._sql_insert(**kwargs)

    # def _table_exists(self, table_name: str) -> bool:
    #     self.cursor.execute(
    #         f"""SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}';"""
    #     )
    #     return self.cursor.fetchone()[0] == 2


def deb():
    def check_if_table_exists(db="../db/franmoreno.db", name="account"):
        try:
            connection = sqlite3.connect(db)
        except sqlite3.Error as error:
            print(error)
        cursor = connection.cursor()

        cursor.execute(
            f"""SELECT name FROM sqlite_master WHERE type='table';"""
        )
        print(cursor.fetchall())

    check_if_table_exists()


if __name__ == '__main__':
    # db = DataBase('test.db')
    # db.sql_insert(movement='INCOME', amount='200.00', desc='description')
    deb()
