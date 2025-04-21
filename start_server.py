import os
import threading
import subprocess
import time

# run this file to start the servers

def send_command(command):
    subprocess.call(command, shell=True)

def start_server():
    # use separate threads so each server is running concurrently
    server1 = threading.Thread(target=send_command, daemon=True, args=("python weak_security_website/manage.py runserver 127.0.0.1:8000",))
    server2 = threading.Thread(target=send_command, daemon=True, args=("python safari_website/manage.py runserver 127.0.0.1:8001",))
    server3 = threading.Thread(target=send_command, daemon=True, args=("python firefox_website/manage.py runserver 127.0.0.1:8002",))
    
    server1.start()
    server2.start()
    server3.start()

    # otherwise the servers would immediately close since the main thread has stopped (this is the main thread)
    while True:
        time.sleep(1)

if __name__ == "__main__":
    start_server()
    print("Servers have been started")