"""
Author: Fran Moreno
Contact: fran.moreno.se@gmail.com
Date: 30/04/2022

Desc: 
# Fill 
"""
from moneyed import Money
from balance.client import Owner


class Account:
    """ Balance account class """
    def __init__(self, owner: Owner, init_balance: Money):
        self.owner = owner
        self.balance = init_balance


class Movement:
    """ Class defining the possible money movements that can be made within a balance account. """
    pass

