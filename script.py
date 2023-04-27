from subprocess import run
from time import sleep
import socket
import os, signal

restart_timer = 900 #15 seconds
def start_script():
    
    try:
        print('Starting server')
        run("python3 main.py", check=True ,shell=True)
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