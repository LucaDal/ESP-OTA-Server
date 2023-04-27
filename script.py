from subprocess import run
from time import sleep
from _thread import *
from  urllib import request
import serial 
def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False
import os
# Path and name to the script you are trying to start
restart_timer = 60
def start_script():
    try:
        # Make sure 'python' command is available
        print('Starting server')
        start_new_thread(check_connection,())
        start_new_thread(runServer,())
    except Exception as e:
        # Script crashed, lets restart it!
        print(e)
        handle_crash()

def handle_crash():
    print('Restarting in 60 seconds')
    sleep(restart_timer)  # Restarts the script after 60 seconds
    start_script()

def runServer():
    run("python3 main.py", check=True, shell=True) 

def check_connection():
    while 1:
        try:
            request.urlopen('http://google.com') #Python 3.x
            sleep(5)
        except request.URLError as err:
            serial.write('\x03')
            raise err


if __name__ == '__main__':
    start_script()