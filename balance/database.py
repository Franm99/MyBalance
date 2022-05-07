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
    def __init__(self, db_file: str):
        self.db_file = db_file

        try:
            self.connection = sqlite3.connect(self.db_file)
        except sqlite3.Error as error:
            print(error)

        self.cursor = self.connection.cursor()

    def create_table(self, deposit):
        self.cursor.execute(
            "CREATE TABLE account(id integer PRIMARY KEY, date text, balance text, movement text, amount real, category text, desc text)"
        )
        # Add first movement
        # date_id = time.strftime("%m-%d-%y %H:%M:%S")
        date_id = time.strftime("05-07-22")
        self.cursor.execute(
            f"INSERT INTO account VALUES(1, {date_id}, {deposit}, 'INCOME', {deposit}, 'NEW_ACCOUNT', 'new account')"
        )
        self.connection.commit()

    def find_account(self, account: Account):
        pass

    def new_account(self, account: Account):
        acc_data = account.asdict()
        with open(self.db_file, 'w+') as f:
            yaml.dump(acc_data, f)



