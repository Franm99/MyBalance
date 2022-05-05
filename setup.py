"""
Author: Fran Moreno
Contact: fran.moreno.se@gmail.com
Date: 30/04/2022

Desc: 
# Fill 
"""
from setuptools import setup, find_packages

setup(
    name='balance',
    version='0.1.0',
    packages=find_packages(include=['balance', 'balance.*'])
)
