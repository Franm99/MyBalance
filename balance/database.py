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
from typing import List, Optional
import pandas as pd


from balance.utils import normalize_money_amount
from balance.rsc import Concept, Category, Owner, Movement


class DataBase:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self._target_source = None
        self.connection, self.cursor = self._connect_to_db()
        self.source_list = self.check_sources()
        if len(self.source_list) == 1:
            self._target_source = self.source_list[0]

    @property
    def target_source(self) -> str:
        return self._target_source

    @target_source.setter
    def target_source(self, source):
        self._target_source = source

    @property
    def last_movements(self) -> Optional[str]:
        return self.get_last_movements()

    def create_table(self, name):
        self.cursor.execute(
            """
            CREATE TABLE "{}" (
                                "INDEX"	        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                "DATE"	        TEXT    NOT NULL,
                                "AMOUNT"	    NUMERIC NOT NULL,
                                "CATEGORY"	    TEXT    NOT NULL,
                                "CONCEPT"	    TEXT    NOT NULL,
                                "DESCRIPTION"	TEXT
            );
            """.format(name)
        )
        self.connection.commit()
        self.source_list.append(name)
        self._target_source = name

    def new_entry(self, movement: Movement, source: str) -> None:
        self.cursor.execute(
            """
            INSERT INTO 
            {}(DATE, AMOUNT, CATEGORY, CONCEPT, DESCRIPTION)
            VALUES (?, ?, ?, ?, ?)
            """.format(source),
            movement.as_tuple()
        )
        self.connection.commit()

    def new_income(self, movement: Movement) -> None:
        self.new_entry(movement, self._target_source)

    def new_expense(self, movement: Movement) -> None:
        self.new_entry(movement, self._target_source)

    def new_transaction(self, movement: Movement, to_source: str) -> None:
        movement.category = Category.Expense.value
        self.new_entry(movement, self._target_source)
        movement.category = Category.Income.value
        self.new_entry(movement, to_source)

    def current_balance(self):
        self.cursor.execute(
            """
            SELECT CATEGORY, AMOUNT FROM {} 
            """.format(self._target_source)
        )
        current_balance = 0.0
        for t, amount in self.cursor.fetchall():
            amount = -amount if t == Category.Expense else amount
            current_balance += amount
        return normalize_money_amount(current_balance)

    def check_sources(self) -> List[str]:
        self.cursor.execute(
            f"""SELECT name FROM sqlite_master WHERE type='table';"""
        )
        source_list = [i[0] for i in self.cursor.fetchall() if i[0] != "sqlite_sequence"]
        return source_list

    def _sql_insert(self, **kwargs):
        keys = f"({', '.join(kwargs.keys())})"
        values = list(kwargs.values())
        val_query = '?, ' * len(values)
        query = f"""INSERT INTO {self._target_source}{keys} VALUES({val_query[:-2]})"""
        self.cursor.execute(query, values)
        self.connection.commit()

    def get_last_movements(self) -> Optional[str]:
        df = pd.read_sql_query(f"SELECT * FROM {self._target_source}", self.connection)
        if df.empty:
            return None
        df = df.sort_index(ascending=False)
        # Change amount sign based on the Category
        df.loc[df['CATEGORY'] == 'EXPENSE', 'AMOUNT'] = -df.loc[df['CATEGORY'] == 'EXPENSE', 'AMOUNT']
        last_movements = df[['DATE', 'AMOUNT', 'CONCEPT', 'DESCRIPTION']].head()
        return last_movements.to_string(index=False)

    def delete_source(self):
        self.cursor.execute(
            """DROP TABLE {}""".format(self._target_source)
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
