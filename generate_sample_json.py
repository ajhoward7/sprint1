import json
import numpy as np
from pprint import pprint
from random_words import RandomNicknames

rn = RandomNicknames()
rn.random_nicks()

json_list = []
for i in range(100):
    json_list.append({"name": rn.random_nicks()[0].encode('utf-8'), "prop": { "age": np.random.randint(20, 150), "zipcode": np.random.randint(90000, 99999), "DMID" : np.random.randint(0, 999999) }})

for json in json_list:
 	print str(json).replace("'",'"')