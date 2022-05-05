"""
Author: Fran Moreno
Contact: fran.moreno.se@gmail.com
Date: 05/05/2022

Desc: 
# Fill 
"""
from pick import pick

title = "Choose an option"
options = ["Option A", "Option B", "Option C"]
option, index = pick(options, title)
print(option)
print(index)