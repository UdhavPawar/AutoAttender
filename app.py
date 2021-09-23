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
import progressbar # for animated loading bar while searching for scheduled meetings

# join zoom meeting
def join_zoom_meeting(input_zoom_meeting_id, input_zoom_meeting_pwd):
    # edge case: error "This meeting ID is not valid. Please check and try again." occurs sometimes when zoom app was minimized (not quit) hence it can have meeting ID cached. So quitting app at start will clear it
    # figure out how to quit zoom app

    # open zoom app
    subprocess.call(["/usr/bin/open", "/Applications/zoom.us.app"])
    print("Opened zoom app\n")

    # wait for zoom app to load completely
    time.sleep(3)
    print("Waited 3 secs for zoom app to finish loading\n")

    # select join a new zoom meeting option
    join_buttton = pyautogui.locateCenterOnScreen("zoom_join_meeting_homescreen_button.png")
    pyautogui.moveTo(join_buttton)
    pyautogui.click()
    print("Selecting join a new meeting\n")
    time.sleep(2)

    # insert zoom meeting id
    insert_meeting_id_button = pyautogui.locateCenterOnScreen("zoom_insert_meeting_id_button.png")
    pyautogui.moveTo(insert_meeting_id_button)
    pyautogui.doubleClick() # edge case: erase any previous meeting id. hence double click will select all text and in next line we simply write which overwrites the text
    pyautogui.write(input_zoom_meeting_id)
    print("Entered meeting ID: {} \n".format(input_zoom_meeting_id))
    time.sleep(1)

    # disable both the camera and mic
    # note: if camera / mic is already disabled (has a blue checkmark on app) it will simply ignore
    media_button = pyautogui.locateAllOnScreen("zoom_disable_camera_and_mic_button.png")
    for button in media_button:
        pyautogui.moveTo(button)
        pyautogui.click()
        time.sleep(1)
    print("Disabled meeting media options\n")

    # join the zoom meeting
    join_buttton = pyautogui.locateCenterOnScreen("zoom_join_meeting.png")
    pyautogui.moveTo(join_buttton)
    pyautogui.click()
    print("Entered meeting ID: {} \n".format(input_zoom_meeting_id))
    time.sleep(1)

    # enter meeting password
    insert_meeting_password_button = pyautogui.locateCenterOnScreen("zoom_insert_meeting_password_button.png")
    pyautogui.moveTo(insert_meeting_password_button)
    pyautogui.write(input_zoom_meeting_pwd)
    time.sleep(0.5)
    pyautogui.press("enter") # enters the password
    print("Entered meeting password: {} \n".format(input_zoom_meeting_pwd))
    # print("# JOINED MEETING {} #\n".format(input_zoom_meeting_id))

    return "### JOINED MEETING {} ###\n".format(input_zoom_meeting_id)

    """
    # select join with computer audio prompt on joining the meeting
    time.sleep(10) # edge case: if meeting is password protected then we don't know when host will admit us hence adding a default sleep time of 1 min before clicking on join with computer audio prompt
    select_computer_audio_button = pyautogui.locateCenterOnScreen("zoom_meeting_select_join_with_computer_audio_on_joining_meeting.png")
    pyautogui.moveTo(select_computer_audio_button)
    pyautogui.click()

    
    # quit zoom meeting
    time.sleep(10)
    pyautogui.hotkey("ctrl", "w")
    pyautogui.press("enter")
    """


# scheduler
def meetings_scheduler():
    # Read meetings csv file using pandas
    data = pd.read_csv("meetings.csv")

    # while loop which will keep checking for a meeting
    already_joined_a_meeting = False

    # animated loading bar
    print("\nLooking for scheduled meetings: \n")
    widgets = [progressbar.AnimatedMarker()]
    bar, bar_counter = progressbar.ProgressBar(widgets=widgets).start(), 0

    while not already_joined_a_meeting:
        # checking if current time == meeting start time
        now = datetime.now().strftime("%H:%M")
        if now in  str(data["meeting_start_time"]):
            # nagivate to that row using pandas loc in csv so other meeting details can be retrieved
            data_row = data.loc[data["meeting_start_time"] == now]
            # iloc is to iterate over a single row selected hence row will be 0
            meeting_id = str(data_row.iloc[0,1]) # row 0 col 1
            meeting_pwd = str(data_row.iloc[0,2]) # row 0 col 2
            print("\n\n### Starting to join meeting: {}### \n".format(meeting_id))
            print(join_zoom_meeting(meeting_id, meeting_pwd))
            already_joined_a_meeting = True
        else:
            time.sleep(0.1)
            if bar_counter > 3: # edge case: ValueError: Value out of range if we keep incrementing counter
                bar_counter = 0
                bar.start()
            bar_counter += 1
            bar.update(bar_counter)

if __name__ == "__main__":
    meetings_scheduler()




    """
    join_zoom_meeting("6507456272","cG5hYlN4dUg1Qk0xcEFMMHdJSk5ZQT09")
    # join_zoom_meeting("9770788229","VGEyTjNKbGJUYzkxRHdSaDkwaTZhdz09")
    """