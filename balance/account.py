"""
Author: Fran Moreno
Contact: fran.moreno.se@gmail.com
Date: 30/04/2022

Desc: 
# Fill 
"""
from moneyed import Money
from dataclasses import dataclass
from typing import List
from enum import Enum, auto


class Concept(Enum):
    Groceries = auto()
    Work = auto()
    Leisure = auto()
    Transport = auto()
    Other = auto()


class Movement(Enum):
    """ Class defining the possible money movements that can be made within a balance account. """
    Income = auto()
    Expense = auto()


@dataclass
class Owner:
    """ Class to define the owner of an account"""
    name: str
    surname: str


@dataclass
class Entry:
    """ Movement entry with some descriptors. """
    code: str
    movement: Movement
    quantity: Money
    concept: Concept
    desc: str


@dataclass
class History:
    """ List of entries to keep track of the movements in an Account. """
    entries: List[Entry]


class Account:
    """ Balance account class """
    def __init__(self, owner: Owner, curr_balance: Money, history: History):
        self.owner = owner
        self.curr_balance = curr_balance
        self.history = history

    def add_entry(self, entry: Entry):
        self.history.entries.append(entry)

    def consult_history(self):
        print(self.history)


# def main():
#     account = Account(owner=Owner(name="Francisco", surname="Moreno"),
#                       curr_balance=Money('2000.45', 'EUR'),
#                       history=History(entries=[]))
#
#     account.add_entry(Entry(code='060522_1154',
#                             movement=Movement.Income,
#                             quantity=Money('200', 'EUR'),
#                             concept=Concept.Work,
#                             desc="payment advance"))
#
#     account.consult_history()
#
#
# if __name__ == '__main__':
#     main()

