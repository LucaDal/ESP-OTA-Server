from subprocess import run
from time import sleep
import os
# Path and name to the script you are trying to start
restart_timer = 60
def start_script():
    try:
        # Make sure 'python' command is available
        print('Starting server')
        run("python main.py", check=True) 
    except Exception as e:
        # Script crashed, lets restart it!
        print(e)
        handle_crash()

def handle_crash():
    print('Restarting in 60 seconds')
    sleep(restart_timer)  # Restarts the script after 60 seconds
    start_script()

if __name__ == '__main__':
    start_script()