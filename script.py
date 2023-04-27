from subprocess import Popen
from time import sleep
from _thread import *
import socket
import os, signal
# Path and name to the script you are trying to start
restart_timer = 60
def start_script():
    print('Starting server')
    PID = Popen("python main.py", shell=True) 
    try:
        while 1:
            if not check_connection():
                print("no connection")
                os.kill(PID,signal.SIGINT)
                break
            sleep(5)
        raise
    except Exception:
        # Script crashed, lets restart it!
        handle_crash()


def check_connection(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False


def handle_crash():
    print('Restarting in 60 seconds')
    sleep(restart_timer)  # Restarts the script after 60 seconds
    start_script()


if __name__ == '__main__':
    start_script()