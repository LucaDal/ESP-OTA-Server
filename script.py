from subprocess import run
from time import sleep

# Path and name to the script you are trying to start
file_path = "main.py" 
print('Server started')
restart_timer = 60
def start_script():
    try:
        # Make sure 'python' command is available
        run("python3 "+file_path, check=True) 
    except:
        # Script crashed, lets restart it!
        handle_crash()

def handle_crash():
    print('Restarting in 60 seconds')
    sleep(restart_timer)  # Restarts the script after 60 seconds
    start_script()

if __name__ == '__main__':
    while True:
        start_script()