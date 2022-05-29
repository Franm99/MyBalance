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
from typing import List
import pandas as pd


from balance.account import Account
from balance.utils import normalize_money_amount
from balance.rsc import Concept, Category, Owner, Movement


class DataBase:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self._target_bank = None
        self.connection, self.cursor = self._connect_to_db()
        self.bank_list = self.check_accounts()
        if len(self.bank_list) == 1:
            self._target_bank = self.bank_list[0]

    @property
    def target_bank(self) -> str:
        return self._target_bank

    @target_bank.setter
    def target_bank(self, bank):
        self._target_bank = bank

    @property
    def last_movements(self):
        return self.get_last_movements()

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

    def new_entry(self, movement_type: Concept, movement: Movement, bank: str) -> None:
        # todo: Date can be added manually
        date = datetime.today().strftime('%m-%d-%Y')
        entities = (date, movement_type, movement.category, movement.amount, movement.desc)
        self.cursor.execute(
            """
            INSERT INTO 
            {}(DATE, TYPE, CATEGORY, AMOUNT, DESCRIPTION)
            VALUES (?, ?, ?, ?, ?)
            """.format(bank),
            entities
        )
        self.connection.commit()

    def new_income(self, movement: Movement) -> None:
        self.new_entry(Concept.Income, movement, self._target_bank)

    def new_expense(self, movement: Movement) -> None:
        self.new_entry(Concept.Expense, movement, self._target_bank)

    def new_transaction(self, movement: Movement, to_bank: str) -> None:
        self.new_entry(Concept.Expense, movement, self._target_bank)
        self.new_entry(Concept.Income, movement, to_bank)

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

    def check_accounts(self) -> List[str]:
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

    def get_last_movements(self):
        df = pd.read_sql_query(f"SELECT * FROM {self._target_bank}", self.connection)
        df = df.sort_index(ascending=False)
        # Change amount sign based on the concept
        df.loc[df['TYPE'] == 'EXPENSE', 'AMOUNT'] = -df.loc[df['TYPE'] == 'EXPENSE', 'AMOUNT']
        last_movements = df[['DATE', 'AMOUNT', 'CATEGORY', 'DESCRIPTION']].head()
        return last_movements.to_string(index=False)

    def delete_account(self):
        self.cursor.execute(
            """DROP TABLE {}""".format(self._target_bank)
        )
        self.connection.commit()

    def delete_profile(self):
        self.connection.close()
        os.remove(self.db_file)
        del self

    def rename_owner(self, owner: Owner):
        self.connection.close()
        os.rename(self.db_file, f"{os.path.dirname(self.db_file)}/{owner.db_file}")
        self.db_file = owner.db_path
        self.connection, self.cursor = self._connect_to_db()

    def _connect_to_db(self):
        try:
            connection = sqlite3.connect(self.db_file)
            cursor = connection.cursor()
            return connection, cursor
        except sqlite3.Error as error:
            print(error)

    def sql_insert(self, **kwargs):
        self._sql_insert(**kwargs)

    # def _table_exists(self, table_name: str) -> bool:
    #     self.cursor.execute(
    #         f"""SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}';"""
    #     )
    #     return self.cursor.fetchone()[0] == 2


def deb():
    file_path = r"C:\Users\Usuario\AppData\Roaming\MyBalance\francisco_moreno.db"
    connection = sqlite3.connect(file_path)
    cursor = connection.cursor()
    df = pd.read_sql_query("SELECT * FROM BBVA", connection)
    df.loc[df['TYPE'] == 'EXPENSE', 'AMOUNT'] = -df.loc[df['TYPE'] == 'EXPENSE', 'AMOUNT']
    last_movements = df[['DATE', 'AMOUNT', 'CATEGORY', 'DESCRIPTION']]
    print(last_movements)


if __name__ == '__main__':
    # db = DataBase('test.db')
    # db.sql_insert(movement='INCOME', amount='200.00', desc='description')
    deb()
