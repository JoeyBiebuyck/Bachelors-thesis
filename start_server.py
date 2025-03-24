import os

# run this file to start the server

def start_server():
    os.system("python simple_website/manage.py runserver")

if __name__ == "__main__":

    start_server()
    print("Server was started")