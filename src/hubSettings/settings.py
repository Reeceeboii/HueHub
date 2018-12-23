from .newUserSettings import NewUserSettings as NS

import json
import os
import tkinter as tk

# This module carries out functions related to the access
# and storage of user settings

# used to get the working directory from main.py
def getCWD():
    return os.getcwd()

# Returns true or false depending on if the settings file exists
def check_new_user(filePath = getCWD()):
    os.chdir(filePath)
    os.chdir("..")
    os.chdir("resources/user-settings/")
    check = os.path.exists("settings.json")
    os.chdir("../../src/hubSettings") # return to the original working directory
    return check

def create_new_user(styles, mainRoot):
    newUserSettings = NS(styles, mainRoot)


# Settings object for a user that has already been through the
# setup process
class SettingsExistingUser:
    def __init__(self):
        os.chdir("../../resources/user-settings") # changing directory to the settings file's location

        self.user_name = ""
        self.bridge_ip = ""
        self.bridge_id = ""

        with open("settings.json", "r") as settings_file_obj:
            settings = json.loads(settings_file_obj.read())
            self.user_name = settings["User"]
            self.bridge_ip = settings["Bridge IP"]
            self.bridge_id = settings["Bridge ID"]
