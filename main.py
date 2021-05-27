from pynput.mouse import Listener, Button # Allows us to get mouse data
from threading import Thread # Allows multiprocessing
from time import sleep # Lets us wait time
from os.path import expanduser # Get home directory path
from datetime import datetime # Lets us get current time and date

# Set version and log variables
version = 0.1
start_log = False

# Declare variables
lButton = 0
rButton = 0

# Define path to write files
path = expanduser("~/Documents/ShadowClick")

# Set storage variables
min_sav = []
sec_sav = []
times = 0

# Create get_cps function
def get_cps():
    # Globalize variables
    global lButton
    global rButton
    global sec_sav
    global start_log
    # Begin loop
    while 1:
        # Check if there is already data in the sec_sav storage variable
        if not sec_sav:
            # If not, then get click data for 5 seconds
            for i in range(5):
                sleep(1)
                sec_sav.append(f'L:{lButton}|R:{rButton}')
                lButton = 0
                rButton = 0
            # Start logging
            start_log = True

# Run get_cps in thread
Thread(target=get_cps,daemon=True).start()

# Define log function
def log():
    # Save seconds storage variable locally
    save = sec_sav
    # Create new variables for CPS
    L = 0
    R = 0
    # Get cps data from local variable and save to L and R
    for item in save:
        item = item.split("|")
        L += int(item[0].replace("L:",""))
        R += int(item[1].replace("R:",""))
    # Average L and R
    L = L / 5
    R = R / 5
    # Make CPS below 3 obsolete
    if 3 > L:
        L = "N/A"
    if 3 > R:
        R = "N/A"
    # Make a string variable with data
    save = f"Left cps: {L}, Right cps: {R}"
    # Do some fancy printing to the screen
    print("\033[A                             \033[A")
    print(save)
    # If the results aren't anything special, forget about logging to the text file
    if save == "Left cps: N/A, Right cps: N/A":
        return
    # Global and overwrite minute CPS storage variable with formatting
    global min_sav
    min_sav.append(f"[{datetime.now().strftime('%Y/%m/%d %H:%M:%S')}] {save}\n")
    # Increment times counter so it logs once every minute
    global times
    times += 1
    if times > 6:
        while True:
            try:
                # Write data in file
                with open(f'{path}/data.txt',"a") as file:
                    # One line at a time
                    for line in min_sav:
                        file.write(line)
                break
            except:
                # If it fails to write data to file, then create the directory and try again
                from os import mkdir # Create the directory
                mkdir(path)
                continue
        # Reset times variable
        times = 0

# On release of a click, add one to the lButton/rButton variables
def on_click(x_,y_,button,pressed):
    global lButton
    global rButton
    if not pressed:
        if button == Button.left:
            lButton += 1
        elif button == Button.right:
            rButton += 1

# Start the pynput listener
listener = Listener(on_click=on_click)
listener.start()

# Print a newline and begin main loop
print('\n')
while True:
    if start_log:
        # Run log function
        log()
        # Reset variable and prevent looping backthrough the log function
        sec_sav = []
        start_log = False
