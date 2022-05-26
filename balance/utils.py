"""
Author: Fran Moreno
Contact: fran.moreno.se@gmail.com
Date: 01/05/2022

Desc: 
# Fill 
"""


def normalize_money_amount(val: str):
    # TODO: Think better way to implement
    val = val.replace(',', '.')
    if not '.' in val:
        val = val + '.00'
    else:
        if len(val.split('.')[-1]) == 1:
            val = val + '0'
        elif len(val.split('.')[-1]) > 2:
            val = val.split('.')[0] + '.' + val.split('.')[-1][0:2]
    return val

# if __name__ == '__main__':
#     val = '2.25'
#     print(normalize_money_amount(val))
#     val = '2,25'
#     print(normalize_money_amount(val))
#     val = '2'
#     print(normalize_money_amount(val))
#     val = '2.0'
#     print(normalize_money_amount(val))
#     val = '2.257'
#     print(normalize_money_amount(val))
