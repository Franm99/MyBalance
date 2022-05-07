"""
Author: Fran Moreno
Contact: fran.moreno.se@gmail.com
Date: 06/05/2022

Desc: 
# Fill 
"""
from dataclasses import dataclass
from typing import List
from enum import Enum, auto
from moneyed import Money
import time


# ENUMS
class Category(Enum):
    Groceries = auto()
    Work = auto()
    Leisure = auto()
    Transport = auto()
    Other = auto()
    NewAccount = auto()


class Movement(Enum):
    """ Class defining the possible money movements that can be made within a balance account. """
    Income = auto()
    Expense = auto()


# DATACLASSES
@dataclass
class Entry:
    """ Movement entry with some descriptors. """
    category: Category
    code: str
    desc: str
    movement: Movement
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
