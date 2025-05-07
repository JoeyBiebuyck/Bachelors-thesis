import os
import threading
import subprocess
import time

# run this file to start the servers

def send_command(command):
    subprocess.call(command, shell=True)

def start_server():
    # use separate threads so each server is running concurrently
    server1 = threading.Thread(target=send_command, daemon=True, args=("python websites/website_1/manage.py runserver 127.0.0.1:8000",))
    server2 = threading.Thread(target=send_command, daemon=True, args=("python websites/website_2/manage.py runserver 127.0.0.1:8001",))
    server3 = threading.Thread(target=send_command, daemon=True, args=("python websites/website_3/manage.py runserver 127.0.0.1:8002",))
    server4 = threading.Thread(target=send_command, daemon=True, args=("python websites/website_4/manage.py runserver 127.0.0.1:8003",))
    server5 = threading.Thread(target=send_command, daemon=True, args=("python websites/website_5/manage.py runserver 127.0.0.1:8004",))
    server6 = threading.Thread(target=send_command, daemon=True, args=("python websites/website_6/manage.py runserver 127.0.0.1:8005",))
    server7 = threading.Thread(target=send_command, daemon=True, args=("python websites/website_7/manage.py runserver 127.0.0.1:8006",))
    server8 = threading.Thread(target=send_command, daemon=True, args=("python websites/website_8/manage.py runserver 127.0.0.1:8007",))
    server9 = threading.Thread(target=send_command, daemon=True, args=("python websites/website_9/manage.py runserver 127.0.0.1:8008",))
    # server10 = threading.Thread(target=send_command, daemon=True, args=("python websites/website_10/manage.py runserver 127.0.0.1:8009",))
    
    server1.start()
    server2.start()
    server3.start()
    server4.start()
    server5.start()
    server6.start()
    server7.start()
    server8.start()
    server9.start()
    # server10.start()

    # otherwise the servers would immediately close since the main thread has stopped (this is the main thread)
    while True:
        time.sleep(1)

if __name__ == "__main__":
    start_server()
    print("Servers have been started")