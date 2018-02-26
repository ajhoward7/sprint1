from random_words import RandomWords
import numpy as np
import requests

rw = RandomWords()
for i in range(200):
    substr = '{"name": "%s", "prop":{"age": %d, "occupation": "%s"}}' % (rw.random_word(), np.random.randint(-10, 40), rw.random_word())
    if i % 10 == 0:
        cut_pt = np.random.randint(0, len(substr)-7)
        substr_array = list(substr)
        for i in range(cut_pt, cut_pt+7):
            substr_array[i] = ' '
        substr = ''.join(substr_array)
        
    headers = {'Content-Type':'application/json'}
    resp = requests.post('http://localhost:8081/', headers = headers, data=substr)
    print(substr, resp.status_code, resp.content)