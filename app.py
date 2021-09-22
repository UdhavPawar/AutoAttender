"""
# work to be done:
1. look into auto installing non-deafult python modules: https://stackoverflow.com/questions/4527554/check-if-module-exists-if-not-install-it
"""

# python default modules
import subprocess # to open zoom app
import time # for timing between each step
from datetime import datetime # for current date and time

# user installed modules
import pyautogui # to automate typing and mouse movements (pip3 install pyautogui)
import pandas as pd # to load data from csv file (pip3 install pandas)

# sign into zoom app
def sign_into_zoom_app(zoom_meeting_id, zoom_meeting_pwd):
    # open zoom app
    subprocess.call(["/usr/bin/open", "/Applications/zoom.us.app"])
    print("Opened zoom app\n")
    # wait for zoom app to load completely
    time.sleep(5)
    print("Waited 5secs for zoom app to finish loading\n")

if __name__ == "__main__":
    sign_into_zoom_app("72200971764","L3p3Nm5OenBuZVNSRVczMHJGbVAvdz09")