"""
Author: Fran Moreno
Contact: fran.moreno.se@gmail.com
Date: 30/04/2022

Desc: 
# Fill 
"""
from moneyed import Money
from balance.rsc import Owner, History, Entry


class Account:
    """ Balance account class """
    def __init__(self, name: str, surname: str, curr_balance: str, first_entry=None):
        self.owner = Owner(name, surname)
        self.curr_balance = Money(curr_balance, 'EUR')
        self.history = History([])
        if first_entry:
            self.add_entry(first_entry)

    def add_entry(self, entry: Entry):
        self.history.entries.append(entry)

    def consult_history(self):
        print(self.history)

    def asdict(self):
        d = {'owner': {'name': self.owner.name, 'surname': self.owner.surname},
             'balance': self.curr_balance,
             'history': self.history
             }
        return d


# def main():
#     account = Account(owner=Owner(name="Francisco", surname="Moreno"),
#                       curr_balance=Money('2000.45', 'EUR'),
#                       history=History(entries=[]))
#
#     account.add_entry(Entry(code='060522_1154',
#                             movement=Concept.Income,
#                             quantity=Money('200', 'EUR'),
#                             category=Category.Work,
#                             desc="payment advance"))
#
#     account.consult_history()
#
#
# if __name__ == '__main__':
#     main()

