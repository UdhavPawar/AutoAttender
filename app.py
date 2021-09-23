"""
# work to be done:
1. look into auto installing non-deafult python modules: https://stackoverflow.com/questions/4527554/check-if-module-exists-if-not-install-it
2. edge case: zoom app opens but account is logged out
3. edge case: quit zoom app using subprocess at start of app
"""

# python default modules
import subprocess # to open zoom app
import time # for timing between each step
from datetime import datetime # for current date and time

# user installed modules
import pyautogui # to automate typing and mouse movements (pip3 install pyautogui)
import pandas as pd # to load data from csv file (pip3 install pandas)
# pip3 install Pillow : required for pyautogui to open, locate and click center of image

# sign into zoom app
def sign_into_zoom_app(input_zoom_meeting_id, input_zoom_meeting_pwd):
    # open zoom app
    subprocess.call(["/usr/bin/open", "/Applications/zoom.us.app"])
    print("Opened zoom app\n")

    # wait for zoom app to load completely
    time.sleep(5)
    print("Waited 5secs for zoom app to finish loading\n")

    # join zoom meeting
    join_buttton = pyautogui.locateCenterOnScreen("zoom_meeting_join_button.png")
    pyautogui.moveTo(join_buttton)
    pyautogui.click()
    print("Joining a new meeting\n")
    time.sleep(2)

    # insert zoom meeting id
    insert_meeting_id_button = pyautogui.locateCenterOnScreen("zoom_insert_meeting_id_button.png")
    pyautogui.moveTo(insert_meeting_id_button)
    pyautogui.click()
    pyautogui.write(input_zoom_meeting_id)
    print("Entered meeting ID:", input_zoom_meeting_id, "\n")
    time.sleep(2)

if __name__ == "__main__":
    sign_into_zoom_app("72200971764","L3p3Nm5OenBuZVNSRVczMHJGbVAvdz09")
