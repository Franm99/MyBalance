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
from typing import Union, Optional
from dateutil import parser
from datetime import datetime


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


def normalize_date(date: Optional[str]):
    try:
        date_norm = parser.parse(date)
        return date_norm.strftime("%m-%d-%Y")
    except parser.ParserError:
        return None


def print_and_wait(*args, **kwargs):
    print(*args, **kwargs)
    input("\nPress any key to continue with other movements")


def cmd_clear(func):
    def wrap(*args, **kwargs):
        os.system('cls')
        result = func(*args, **kwargs)
        return result
    return wrap
