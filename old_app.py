"""
# work to be done:
1. look into auto installing non-deafult python modules: https://stackoverflow.com/questions/4527554/check-if-module-exists-if-not-install-it
2. edge case: zoom app opens but account is logged out
3. fix email sender on site
4. iterate between start and stop app button
"""

# python default modules
import subprocess # to open zoom app
import time # for timing between each step
from datetime import datetime # for current date and time
import os
from tkinter import *
from tkinter import messagebox # used for tkinter user input validation
# from itertools import cycle # to toggle betweem start stop app
from db import Database

# user installed modules
import pyautogui # to automate typing and mouse movements (pip3 install pyautogui)
import pandas as pd # to load data from csv file (pip3 install pandas)
# pip3 install Pillow : required for pyautogui to open, locate and click center of image
import progressbar # for animated loading bar while searching for scheduled meetings

# Initialize db
db = Database("meetings.db")

# quit zoom app
def quit_zoom_app():
    proc = subprocess.Popen("ps -ae | grep 'zoom' | grep -v 'grep' | awk '{print $1}'", shell=True, stdout=subprocess.PIPE) # grep for running zoom process and exclude the process of us grepping for zoom
    pids = proc.communicate()[0]
    for pid in pids.decode("UTF-8").split("\n"): # decode returned bytes from subprocess to string
        if pid: # no empty space or 0 pid
            process = subprocess.Popen("kill {}".format(pid), shell=True)

# join zoom meeting
def join_zoom_meeting(input_zoom_meeting_id, input_zoom_meeting_pwd):
    # edge case: error "This meeting ID is not valid. Please check and try again." occurs sometimes when zoom app was minimized (not quit) hence it can have meeting ID cached. So quitting app at start will clear it
    print("Quitting zoom app if already open\n")
    quit_zoom_app()

    # open zoom app
    subprocess.call(["/usr/bin/open", "/Applications/zoom.us.app"])
    print("Opening zoom app\n")

    # wait for zoom app to load completely
    time.sleep(10)
    print("Waited 10 secs for zoom app to finish loading\n")

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

    # select join with computer audio prompt after joining the meeting
    time.sleep(10) # edge case: if meeting is password protected then we don't know when the host will admit us hence adding a default sleep time of 1 min before clicking on join with computer audio prompt
    select_computer_audio_button = pyautogui.locateCenterOnScreen("zoom_meeting_select_join_with_computer_audio_after_joining_meeting.png")
    pyautogui.moveTo(select_computer_audio_button)
    pyautogui.click()

    return "### JOINED MEETING {} ###\n".format(input_zoom_meeting_id)

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
        if now in str(data["meeting_start_time"]):
            # nagivate to that row using pandas loc in csv so other meeting details can be retrieved
            data_row = data.loc[data["meeting_start_time"] == now]
            # iloc is to iterate over a single row selected hence row will be 0
            meeting_end_time = str(data_row.iloc[0,1]) # row 0 col 1
            meeting_id = str(data_row.iloc[0,2]) # row 0 col 2
            meeting_pwd = str(data_row.iloc[0,3]) # row 0 col 3
            print("\n\n### Starting to join meeting: {} ###\n".format(meeting_id))
            print(join_zoom_meeting(meeting_id, meeting_pwd))
            already_joined_a_meeting = True

            # wait till meeting end time
            print("Currently in meeting {} waiting for it to end".format(meeting_id))
            while already_joined_a_meeting:
                now = datetime.now().strftime("%H:%M")
                if now in str(data["meeting_end_time"]):
                    quit_zoom_app()
                    already_joined_a_meeting = False # this will leave the current meeting and start looking for other scheduled meetings
                    print("\n### Left meeting {} on {} ###\n".format(meeting_id, now))
                    print("\nLooking for scheduled meetings: \n")

        # update loading bar   
        else:
            time.sleep(0.1)
            if bar_counter > 3: # edge case: ValueError: Value out of range if we keep incrementing counter
                bar_counter = 0
                bar.start()
            bar_counter += 1
            bar.update(bar_counter)

# if __name__ == "__main__":
    # meetings_scheduler()

# Functions
def populate_meetings_list():
    # edge case: we don't want duplicate items / twice population of meeting details hence we clear all at start of new population
    meetings_list.delete(0,END) # delete from start to end / current pointer
    for row in db.fetch():
        meetings_list.insert(END, row) # insert each row at end of listbox ppointer

def add_meeting():
    # using tkinter messagebox to make sure any of required input fields is not empty
    if meeting_id_text.get() == "" or meeting_pwd_text.get() == "" or meeting_start_time_text.get() == "" or meeting_stop_time_text.get() == "":
        messagebox.showerror("Required Fields", "Please input all fields")
        return 
    # get entered text from the defined vars and insert into db
    db.insert(meeting_id_text.get(), meeting_pwd_text.get(), meeting_start_time_text.get(), meeting_stop_time_text.get())
    # we updated db but we need to update listbox
    meetings_list.delete(0, END)
    meetings_list.insert(END, (meeting_id_text.get(), meeting_pwd_text.get(), meeting_start_time_text.get(), meeting_stop_time_text.get()))
    populate_meetings_list()

def select_meeting(event):
    global selected_meeting # define global var for selected meeting
    meeting_index = meetings_list.curselection()[0] # get index of selected meeting
    print(meeting_index)
    selected_meeting = meetings_list.get(meeting_index) # get all data of selected meeting
    print(select_meeting)
    
    """
    meeting_id_entry.delete(0,END)
    meeting_id_entry.insert(END, select_meeting[1]) # as index 0 is primary key id hence starting with 1 which is meeting id

    meeting_pwd_entry.delete(0,END)
    meeting_pwd_entry.insert(END, select_meeting[2])

    meeting_start_time_entry.delete(0,END)
    meeting_start_time_entry.insert(END, select_meeting[3])

    meeting_end_time_entry.delete(0,END)
    meeting_end_time_entry.insert(END, select_meeting[4])
    """

def delete_meeting():
    print("Delete meeting")

def update_meeting():
    print("Update meeting")

def start_stop_app():
    print("Start Stop App")

# Create window object
app = Tk()

# Meeting Id
meeting_id_text = StringVar() # var to store meeting id
meeting_id_label = Label(app, text="Meeting ID", font=("bold", 14), pady=20) # create a meeting id label. pady is for padding for y axis ie. from top of window
meeting_id_label.grid(row=0, column=0, sticky=W) # put meeting id label on grid. sticky property is to align lable to left hence W (West)
meeting_id_entry = Entry(app, textvariable=meeting_id_text) # feed entered value to sting var
meeting_id_entry.grid(row=0, column=1)

# Meeting Pwd
meeting_pwd_text = StringVar() # var to store meeting pwd
meeting_pwd_label = Label(app, text="Meeting Password", font=("bold", 14)) # note: we don't need padding anymore as rest of labels will be already pushed down from previous one
meeting_pwd_label.grid(row=0, column=2, sticky=W) 
meeting_pwd_entry = Entry(app, textvariable=meeting_pwd_text) 
meeting_pwd_entry.grid(row=0, column=3)

# Meeting Start Time
meeting_start_time_text = StringVar() # var to store meeting start time
meeting_start_time_label = Label(app, text="Meeting Start Time", font=("bold", 14)) 
meeting_start_time_label.grid(row=1, column=0, sticky=W) 
meeting_start_time_entry = Entry(app, textvariable=meeting_start_time_text) 
meeting_start_time_entry.grid(row=1, column=1)

# Meeting Stop Time
meeting_stop_time_text = StringVar() # var to store meeting start time
meeting_stop_time_label = Label(app, text="Meeting Stop Time", font=("bold", 14)) 
meeting_stop_time_label.grid(row=1, column=2, sticky=W) 
meeting_stop_time_entry = Entry(app, textvariable=meeting_stop_time_text) 
meeting_stop_time_entry.grid(row=1, column=3)

# Meetings List (ListBox) Widget
meetings_list = Listbox(app, height=8, width=50, border=0) # border=0 will hide the border so that we don't see how many rows and cols the widget spans
meetings_list.grid(row=3, column=0, rowspan=6, columnspan=3, padx=20, pady=20) # row and col span is how many rows and col should respective span

# Create scrollbar for meetings list
meetings_list_scrollbar = Scrollbar(app)
meetings_list_scrollbar.grid(row=3, column=3) # column is 3 as listbox spans for 3 cols so putting scrollbar next to listbox

# Connect scrollbar to meetings listbox
meetings_list.configure(yscrollcommand=meetings_list_scrollbar.set) # yscroll as we want to scroll vertically along y axis
meetings_list_scrollbar.configure(command=meetings_list.yview) # configure scrollbar to scroll along the y axis

# Connect meeting selected in listbox to select_meeting function
meetings_list.bind("<<ListboxSelect>>", select_meeting)

# Add Meeting Button
add_meeting_btn = Button(app, text="Add Meeting", width=12, command=add_meeting)
add_meeting_btn.grid(row=2, column=0, pady=20) # just like labels we only need to add y axis padding for first button rest of buttons will align themselves by rows and cols

# Delete Meeting Button
delete_meeting_btn = Button(app, text="Delete Meeting", width=12, command=delete_meeting)
delete_meeting_btn.grid(row=2, column=1) 

# Update Meeting Button
update_meeting_btn = Button(app, text="Update Meeting", width=12, command=update_meeting)
update_meeting_btn.grid(row=2, column=2) 

# Start / Stop App Button
start_stop_app_btn = Button(app, text="Start / Stop App", width=12, command=start_stop_app)
start_stop_app_btn.grid(row=2, column=3) 

# Window title and size
app.title("Auto Attender") # set app window's title
app.geometry("700x350") # set app window's size

# Populate meetings list
populate_meetings_list()

# Start the app
app.mainloop()