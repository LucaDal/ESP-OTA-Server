from subprocess import Popen
from time import sleep
import socket
import os, signal

restart_timer = 60 #15 seconds
def start_script():
    try:
        print('Starting the server')
        Popen("python3 main.py", shell=True)
        sleep(10) #time to start server
        while 1:
            if not check_connection():
                handle_crash()
            sleep(10) #every ten seconds it check if the site is working
    except Exception as e:
        # Script crashed, lets restart it!
        print(e)
        handle_crash()


def check_connection(host="192.168.1.250", port=50001, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
    except socket.error:
        return False
    return True


def handle_crash():
    print('Restarting in 60 seconds')
    sleep(restart_timer)  # Restarts the script after 60 seconds
    start_script()


if __name__ == '__main__':
    start_script()