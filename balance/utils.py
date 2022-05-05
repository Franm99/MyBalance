"""
Author: Fran Moreno
Contact: fran.moreno.se@gmail.com
Date: 01/05/2022

Desc: 
# Fill 
"""
import yaml

with open('../db/db.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

    print(data)


