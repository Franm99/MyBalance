"""
Author: Fran Moreno
Contact: fran.moreno.se@gmail.com
Date: 06/05/2022

Desc: 
# Fill 
"""
from dataclasses import dataclass, astuple
from typing import List, Optional
from strenum import StrEnum
from enum import Enum, auto
from moneyed import Money
import time
import os
from pathlib import Path


APP_NAME = 'MyBalance'
DB_PATH = 'db'


# ENUMS
class Concept(StrEnum):
    # Incomes
    Bizum = "BIZUM"
    Work = "WORK"
    # Expenses
    Groceries = "GROCERIES"
    NewAccount = "NEW_ACCOUNT"
    Leisure = "LEISURE"
    Transport = "TRANSPORT"
    Withdraw = "WITHDRAW"
    Parking = "PARKING"
    Transaction = "TRANSACTION"
    Other = "OTHER"


class Category(StrEnum):
    """ Class defining the possible money movements that can be made within a balance account. """
    Income = "INCOME"
    Expense = "EXPENSE"
    Transaction = "TRANSACTION"


# DATACLASSES
@dataclass
class Movement:
    date: str
    amount: str
    category: str
    concept: str
    desc: Optional[str]

    def as_tuple(self):
        return astuple(self)


@dataclass
class Entry:
    """ Concept entry with some descriptors. """
    category: Category
    code: str
    desc: str
    concept: Concept
    quantity: Money


@dataclass
class History:
    """ List of entries to keep track of the movements in an Account. """
    entries: List[Entry]


class Owner:
    """ Class to define the owner of an account"""
    def __init__(self, name: str, surname: str, dir_path: str):
        self._name = name.lower()
        self._surname = surname.lower()
        self._filename = f"{self._name}_{self._surname}.db"
        self._full_path = f"{dir_path}/{self._filename}"

    @property
    def name(self):
        return self._name.title()

    @property
    def surname(self):
        return self._surname.title()

    @property
    def full_name(self):
        return f"{self.name} {self.surname}"

    @property
    def db_file(self):
        return self._filename

    @property
    def db_path(self):
        return self._full_path


if __name__ == '__main__':
    movement = Movement("05-20-2022", "20.25", Category.Expense.value, "House", "House expenses")
    print(movement.as_tuple())
