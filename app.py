"""
# work to be done:
1. look into auto installing non-deafult python modules: https://stackoverflow.com/questions/4527554/check-if-module-exists-if-not-install-it
2. edge case: zoom app opens but account is logged out
3. fix email sender on site
4. need to fix user input time for scheduler
"""

# python default modules
import subprocess # to open zoom app
import time # for timing between each step
from datetime import datetime # for current date and time
import os
import tkinter as tk
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

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('Auto Attender')
        # Set app window's size
        master.geometry("600x800")
        # Hide the root window drag bar and close button
        # master.overrideredirect(True)
        # Make the window content area transparent
        master.wm_attributes("-transparent", True)
        # Set the root window background color to a transparent color
        master.config(bg='systemTransparent')
        # Setup widgets and grid
        self.create_widgets()
        # Initialize selected meeting variable
        self.selected_item = 0
        # Populate initial meetings list
        self.populate_meetings_list()
        # Initialize in a meeting variable
        self.start_searching_for_meetings = False

    def create_widgets(self):
        # NOTE: all the x and y co-ordinates are set according to Figma design and are found by cliking on each component (like button, input fields, list boxes, etc)
        # Set app background image
        self.background_image = tk.PhotoImage(file = "./figma/background.png")
        self.background_image_label = tk.Label(self.master, image=self.background_image)
        self.background_image_label.photo = self.background_image
        self.background_image_label.place(x=0, y=0, relwidth=1, relheight=1) # x and y are frame co-ordinates and relwidth relheight is for no extra spacing at those co-ordinates

        """
        # Meeting Id
        self.meeting_id_text = tk.StringVar() # var to store meeting id
        self.meeting_id_label = tk.Label(self.master, text="Meeting ID", font=("bold", 14), pady=20) # create a meeting id label. pady is for padding for y axis ie. from top of window
        self.meeting_id_label.grid(row=0, column=0, sticky=tk.W) # put meeting id label on grid. sticky property is to align lable to left hence W (West)
        self.meeting_id_entry = tk.Entry(self.master, textvariable=self.meeting_id_text) # feed entered value to sting var
        self.meeting_id_entry.grid(row=0, column=1)

        # Meeting Pwd
        self.meeting_pwd_text = tk.StringVar() # var to store meeting pwd
        self.meeting_pwd_label = tk.Label(self.master, text="Meeting Password", font=("bold", 14)) # note: we don't need padding anymore as rest of labels will be already pushed down from previous one
        self.meeting_pwd_label.grid(row=0, column=2, sticky=tk.W) 
        self.meeting_pwd_entry = tk.Entry(self.master, textvariable=self.meeting_pwd_text) 
        self.meeting_pwd_entry.grid(row=0, column=3)

        # Meeting Start Time
        self.meeting_start_time_text = tk.StringVar() # var to store meeting start time
        self.meeting_start_time_label = tk.Label(self.master, text="Meeting Start Time", font=("bold", 14)) 
        self.meeting_start_time_label.grid(row=1, column=0, sticky=tk.W) 
        self.meeting_start_time_entry = tk.Entry(self.master, textvariable=self.meeting_start_time_text) 
        self.meeting_start_time_entry.grid(row=1, column=1)

        # Meeting Stop Time
        self.meeting_stop_time_text = tk.StringVar() # var to store meeting start time
        self.meeting_stop_time_label = tk.Label(self.master, text="Meeting Stop Time", font=("bold", 14)) 
        self.meeting_stop_time_label.grid(row=1, column=2, sticky=tk.W) 
        self.meeting_stop_time_entry = tk.Entry(self.master, textvariable=self.meeting_stop_time_text) 
        self.meeting_stop_time_entry.grid(row=1, column=3)

        # Meetings List (ListBox) Widget
        # self.meetings_list_label = tk.Label(self.master, text="Meetings List")
        # self.meetings_list_label.grid(row=3, column=0, sticky=tk.W)
        self.meetings_list = tk.Listbox(self.master, height=8, width=50, border=1) # border=0 will hide the border so that we don't see how many rows and cols the widget spans
        self.meetings_list.grid(row=3, column=0, rowspan=6, columnspan=3, padx=20, pady=20) # row and col span is how many rows and col should respective span

        # Create scrollbar for meetings list
        self.meetings_list_scrollbar = tk.Scrollbar(self.master)
        self.meetings_list_scrollbar.grid(row=3, column=3) # column is 3 as listbox spans for 3 cols so putting scrollbar next to listbox

        # Connect scrollbar to meetings listbox
        self.meetings_list.configure(yscrollcommand=self.meetings_list_scrollbar.set) # yscroll as we want to scroll vertically along y axis
        self.meetings_list_scrollbar.configure(command=self.meetings_list.yview) # configure scrollbar to scroll along the y axis

        # Connect meeting selected in listbox to select_meeting function
        self.meetings_list.bind("<<ListboxSelect>>", self.select_meeting)
        """

        # Add Meeting Button
        # self.add_meeting_btn = tk.Button(self.master, text="Add Meeting", width=12, command=self.add_meeting)
        # self.add_meeting_btn.grid(row=2, column=0, pady=20)
        self.button_background = tk.PhotoImage(file = "./figma/transparent.png")
        self.add_meeting_btn = tk.Button(self.master, image=self.button_background, width=12, command=self.add_meeting)
        self.add_meeting_btn.pack()
        self.add_meeting_btn.place(x=27, y=309.59, height=66.31, width=113.4)
        # self.add_meeting_btn.pack()

        """
        # Delete Meeting Button
        self.delete_meeting_btn = tk.Button(self.master, text="Delete Meeting", width=12, command=self.delete_meeting)
        # self.delete_meeting_btn.grid(row=2, column=1)
        self.delete_meeting_btn.place(x=171, y=309.59, height=66.31, width=113.4)

        # Update Meeting Button
        self.update_meeting_btn = tk.Button(self.master, text="Update Meeting", width=12, command=self.update_meeting)
        # self.update_meeting_btn.grid(row=2, column=2)
        self.update_meeting_btn.place(x=315, y=309.59, height=66.31, width=113.4)

        # Start / Stop App Button
        self.start_stop_app_btn = tk.Button(self.master, text="Start / Stop App", width=12, relief="raised", command=self.start_stop_app) # relief property "sunken" or "raised" is used to toggle between app start and stop
        # self.start_stop_app_btn.grid(row=2, column=3)
        self.start_stop_app_btn.place(x=459, y=309.59, height=66.31, width=113.4)
        """

        """
        # Function outputs List (ListBox) Widget
        # self.functions_output_list_label = tk.Label(self.master, text="Your Activity")
        # self.functions_output_list_label.grid(row=8, column=0, sticky=tk.W)
        self.functions_output_list = tk.Listbox(self.master, height=8, width=50, border=1) # border=0 will hide the border so that we don't see how many rows and cols the widget spans
        self.functions_output_list.grid(row=9, column=0, rowspan=6, columnspan=3, padx=20, pady=10) # row and col span is how many rows and col should respective span

        # Create scrollbar for meetings list
        self.functions_output_list_scrollbar = tk.Scrollbar(self.master)
        self.functions_output_list_scrollbar.grid(row=9, column=3) # column is 3 as listbox spans for 3 cols so putting scrollbar next to listbox

        # Connect scrollbar to meetings listbox
        self.functions_output_list.configure(yscrollcommand=self.functions_output_list_scrollbar.set) # yscroll as we want to scroll vertically along y axis
        self.functions_output_list_scrollbar.configure(command=self.functions_output_list.yview) # configure scrollbar to scroll along the y axis

        # Connect meeting selected in listbox to select_meeting function
        self.functions_output_list.bind("<<ListboxSelect>>")
        """

    # Populate meetings from db into tkinter meetings listbox
    def populate_meetings_list(self):
        print("Populate")
        """
        # edge case: we don't want duplicate items / twice population of meeting details hence we clear all at start of new population
        self.meetings_list.delete(0, tk.END) # delete from start to end / current pointer
        for row in db.fetch():
            self.meetings_list.insert(tk.END, row) # insert each row at end of listbox pointer
        """

    def add_meeting(self):
        print("Add")
        """
        # using tkinter messagebox to make sure any of required input fields (meeting ID, meeting start time and meeting stop time) is not empty
        # note: empty meeting pwd is accepted as some meetings don't have a pwd
        if self.meeting_id_text.get() == "" or self.meeting_start_time_text.get() == "" or self.meeting_stop_time_text.get() == "":
            messagebox.showerror("Required Fields", "Please input all fields")
            return
        # get entered text from the defined vars and insert into db
        db.insert(self.meeting_id_text.get(), self.meeting_pwd_text.get(), self.meeting_start_time_text.get(), self.meeting_stop_time_text.get())
        # we updated db but we need to update listbox. first clear the listbox
        self.meetings_list.delete(0, tk.END)
        # insert into listbox
        self.meetings_list.insert(tk.END, (self.meeting_id_text.get(), self.meeting_pwd_text.get(), self.meeting_start_time_text.get(), self.meeting_stop_time_text.get()))
        # now populate listbox
        self.populate_meetings_list()
        # log funtion output to outputs list
        self.functions_output_list.insert(tk.END, "{} - Added Meeting: {}".format(datetime.now().strftime("%H:%M %p"), self.meeting_id_text.get()))
        # clear the entries
        self.clear_entries()
        """

    def select_meeting(self, event):
        print("Select meeting")
        """
        try:
            meeting_index = self.meetings_list.curselection()[0] # get index of selected meeting
            self.selected_meeting = self.meetings_list.get(meeting_index) # get all data of selected meeting
            # print(selected_meeting)
            
            # Fill up selected meeting details in entries
            self.meeting_id_entry.delete(0, tk.END)
            self.meeting_id_entry.insert(tk.END, self.selected_meeting[1]) # as index 0 is primary key id hence starting with 1 which is meeting id
            self.meeting_pwd_entry.delete(0, tk.END)
            self.meeting_pwd_entry.insert(tk.END, self.selected_meeting[2])
            self.meeting_start_time_entry.delete(0,tk.END)
            self.meeting_start_time_entry.insert(tk.END, self.selected_meeting[3])
            self.meeting_stop_time_entry.delete(0, tk.END)
            self.meeting_stop_time_entry.insert(tk.END, self.selected_meeting[4])
        except IndexError:
            pass
        """

    def delete_meeting(self):
        print("Delete meeting")
        """
        db.delete(self.selected_meeting[0]) # pass primary index id to db delete function
        self.clear_entries()
        self.populate_meetings_list() # popolate meetings listbox after deletion
        self.functions_output_list.insert(tk.END, "{} - Deleted Meeting: {}".format(datetime.now().strftime("%H:%M %p"), self.selected_meeting[1])) # log funtion output to outputs list
        """

    def update_meeting(self):
        print("Update meeting")
        """
        db.update(self.selected_meeting[0], self.meeting_id_text.get(), self.meeting_pwd_text.get(), self.meeting_start_time_text.get(), self.meeting_stop_time_text.get()) # pass primary key id and entries to update function
        self.clear_entries()
        self.populate_meetings_list()
        self.functions_output_list.insert(tk.END, "{} - Updated Meeting: {}".format(datetime.now().strftime("%H:%M %p"), self.selected_meeting[1])) # log funtion output to outputs list
        """

    def clear_entries(self):
        print("Clear entries")
        """
        self.meeting_id_entry.delete(0, tk.END)
        self.meeting_pwd_entry.delete(0, tk.END)
        self.meeting_start_time_entry.delete(0,tk.END)
        self.meeting_stop_time_entry.delete(0, tk.END)
        """

    # quit zoom app
    def quit_zoom_app(self):
        proc = subprocess.Popen("ps -ae | grep 'zoom' | grep -v 'grep' | awk '{print $1}'", shell=True, stdout=subprocess.PIPE) # grep for running zoom process and exclude the process of us grepping for zoom
        pids = proc.communicate()[0]
        for pid in pids.decode("UTF-8").split("\n"): # decode returned bytes from subprocess to string
            if pid: # no empty space or 0 pid
                process = subprocess.Popen("kill {}".format(pid), shell=True)

    # join zoom meeting
    def join_zoom_meeting(self, input_zoom_meeting_id, input_zoom_meeting_pwd):
        # edge case: error "This meeting ID is not valid. Please check and try again." occurs sometimes when zoom app was minimized (not quit) hence it can have meeting ID cached. So quitting app at start will clear it
        print("Quitting zoom app if already open\n")
        self.quit_zoom_app()

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

    def meetings_scheduler(self):
        if self.start_searching_for_meetings:
            for row in db.fetch():
                # checking if current time == meeting start time
                print(row)
                now = datetime.now().strftime("%H:%M")
                print(now)
                print(row[3])
                if now == row[3]:
                    print("\n\n### Starting to join meeting: {} ###\n".format(row[1]))
                    print(self.join_zoom_meeting(row[1], row[2]))
                    # wait till meeting end time
                    print("Currently in meeting {} waiting for it to end".format(meeting_id))
                    while True:
                        now = datetime.now().strftime("%H:%M")
                        if now == row[4]: # till current time != meeting end time
                            self.quit_zoom_app() 
                            print("\n### Left meeting {} on {} ###\n".format(meeting_id, now))
                # print("Checked row: ", row[4])
                self.after(15000, self.meetings_scheduler) # schedule to run every 15 seconds

    def start_stop_app(self):
        if self.start_stop_app_btn.config("relief")[-1] == "raised": # by default relief == raised so first button click will start the app
            self.start_stop_app_btn.config(relief = "sunken") # update relief so next button click will stop the app
            print("Start App")
            """
            self.start_searching_for_meetings = True # set to True so meetings scheduler will start looking for meetings to join
            self.functions_output_list.insert(tk.END, "{} - Started App".format(datetime.now().strftime("%H:%M %p"))) # log funtion output to outputs list
            self.meetings_scheduler()
            """
        else:
            self.start_stop_app_btn.config(relief = "raised") # update relief so next button click will start the app
            print("Stop App")
            """
            self.start_searching_for_meetings = False # set to False so meetings scheduler will stop looking for meetings to join
            self.functions_output_list.insert(tk.END, "{} - Stopped App".format(datetime.now().strftime("%H:%M %p"))) # log funtion output to outputs list
            """

if __name__ == "__main__":
    # Create window object
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()