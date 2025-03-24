# import requests

# r = requests.get('http://127.0.0.1:8000/')

# print(r.text)

from bfts.bandit import Bandit

def n_arms():
    return len(XSS_transformations())

def XSS_transformations():
    return [] # fill this list with functions that take one argument (a payload) and transform it in a certain way

def XSS_bandit():
    