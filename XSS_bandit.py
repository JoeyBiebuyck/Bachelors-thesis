# import requests

# r = requests.get('http://127.0.0.1:8000/')

# print(r.text)

import random
from bfts.bandit import Bandit

def n_arms():
    return len(XSS_transformations())

def XSS_transformations():
    return [] # fill this list with functions that take one argument (a payload) and transform it in a certain way

def XSS_bandit():
    base_payload = "enter base payload" # TODO: enter the base payload
    n = n_arms
    transformations_ = XSS_transformations()
    transformed_payloads = list(transformation(base_payload) for transformation in transformations_)
    def reward_fn(payload_):
        return lambda: send_and_get_result(payload_)
    arms = list(map(reward_fn, transformed_payloads))
    return Bandit(arms)
    

def send_and_get_result(payload_):
    # 1st choose which server to send it to (which browser engine)
    engines = ["chromium", "firefox", "safari"]
    engine = random.choice(engines)

    # 2nd send the payload to that server

    # 3rd receive a response of that server (this will be either a 1 (success) or 0 (fail))
    # 4th return this response