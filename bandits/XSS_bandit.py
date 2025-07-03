import requests
import random
from bfts.bandit import Bandit
import numpy as np
import sys

def XSS_transformations(n_arms):
    transformations = create_XSS_transformations(n_arms) # fill this list with functions that take one argument (a payload) and transform it in a certain way
    random.Random(1).shuffle(transformations)
    return transformations

def XSS_bandit(n_arms: int):
    n = n_arms
    base_payload = "alert('Hi!')"
    transformations_ = XSS_transformations(n_arms)
    transformed_payloads = list(transformation(base_payload) for transformation in transformations_) # a list of identifiers
    def reward_fn(payload_):
        return lambda: send_and_get_result(payload_)
    arms = list(map(reward_fn, transformed_payloads))
    return Bandit(arms)

# Create a session so each new get request does not establish a new connection
session = requests.Session()
    
# This function gets called when an arm is pulled
def send_and_get_result(payload_):
    website_to_ip_dict = {"website_1": "http://127.0.0.1:8000", "website_2": "http://127.0.0.1:8001", "website_3": "http://127.0.0.1:8002", 
                          "website_4": "http://127.0.0.1:8003", "website_5": "http://127.0.0.1:8004", "website_6": "http://127.0.0.1:8005", 
                          "website_7": "http://127.0.0.1:8006", "website_8": "http://127.0.0.1:8007", "website_9": "http://127.0.0.1:8008",}

    # 1st choose which server to send it to (which security filter it will get passed through)
    websites = ["website_1", "website_2", "website_3", "website_4", "website_5", "website_6", "website_7", "website_8", "website_9"]
    website = random.choice(websites)
    ip = website_to_ip_dict[website]

    # 2nd send the payload to that server
    full_ip = ip + "/search/?q=" + str(payload_)
    r = session.get(full_ip)

    # 3rd receive a HTTP response of that server (this will be either 200 (success) or 404 (fail))
    status = r.status_code

    # 4th return this response
    if status == 200:
        return 1
    elif status == 404:
        return 0


# Simulations of XSS payload transformations:

# Creates a technique that returns the same identifier that it has in its name
def create_technique(number):

    def transformation(base_payload: str):
        return number
    
    transformation.__name__="transformation_" + str(number)

    return transformation

# Creates a list of functions that have incremented identifiers
def create_XSS_transformations(amount: int):
    all_techniques = []

    for i in range(1, amount+1):
        technique = create_technique(i)
        all_techniques.append(technique)

    return all_techniques
