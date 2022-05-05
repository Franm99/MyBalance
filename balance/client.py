"""
Author: Fran Moreno
Contact: fran.moreno.se@gmail.com
Date: 30/04/2022

Desc: 
# Fill 
"""
from strenum import StrEnum


class Region(StrEnum):
    EU = "EU"
    USA = "USA"
    England = "England"


class Owner:
    """ Class to define the owner of a balance account. """
    def __init__(self, name: str, surname: str, region: Region):
        pass



