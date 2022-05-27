"""
Author: Fran Moreno
Contact: fran.moreno.se@gmail.com
Date: 06/05/2022

Desc: 
# Fill 
"""
from dataclasses import dataclass
from typing import List
from strenum import StrEnum
from enum import Enum, auto
from moneyed import Money
import time


APP_NAME = 'MyBalance'
DB_PATH = 'db'


# ENUMS
class Category(StrEnum):
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


class Concept(StrEnum):
    """ Class defining the possible money movements that can be made within a balance account. """
    Income = "INCOME"
    Expense = "EXPENSE"


# DATACLASSES
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


@dataclass
class Owner:
    """ Class to define the owner of an account"""
    name: str
    surname: str
