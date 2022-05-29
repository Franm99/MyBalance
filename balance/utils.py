"""
Author: Fran Moreno
Contact: fran.moreno.se@gmail.com
Date: 01/05/2022

Desc: 
# Fill 
"""
import os
import functools
import time
from typing import Union


def normalize_money_amount(val: Union[str, float]):
    # TODO: Think better way to implement
    val = str(val).replace(',', '.')
    if not '.' in val:
        val = val + '.00'
    else:
        if len(val.split('.')[-1]) == 1:
            val = val + '0'
        elif len(val.split('.')[-1]) > 2:
            val = val.split('.')[0] + '.' + val.split('.')[-1][0:2]
    return val


def print_and_wait(*args, **kwargs):
    print(*args, **kwargs)
    input("Press any key to continue with other movements")


def cmd_clear(func):
    def wrap(*args, **kwargs):
        os.system('cls')
        result = func(*args, **kwargs)
        return result
    return wrap


