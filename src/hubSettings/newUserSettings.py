# module for the GUI window shown to new users who first boot the program and have
# not already been through the setup process of linking a Hue Bridge and giving some
# basic information.


import tkinter as tk
from tkinter import messagebox
from hueConnect import connect as HC

#from PIL import Image, ImageTk
# Implement some better styling at a later date using images and icons

import os
import json

class NewUserSettings:
    def __init__(self, styles, mainRoot):
        mainRoot.withdraw()
        # MainApplication root window is withdrawn from view

        self.root = tk.Toplevel(mainRoot)
        self.root.title("HueHub")
        self.root.minsize(400, 350)
        self.root.maxsize(1920, 1080)
        self.root.geometry("750x600")
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.exit_callback(mainRoot))
        self.root.configure(bg = styles["bg"])

        os.chdir("../../resources/icons")
        self.root.iconbitmap(r"bulb.ico")
        os.chdir("../../src/hubSettings/")

        self.bridge = ""
        self.apiToken = ""

        self.welcomeLabel = tk.Label(self.root, text = "HueHub", font = styles["font-c"] + "25", bg = styles["bg"],
                                     fg = "white")
        self.welcomeLabel.pack()

        self.welcomeLabel2 = tk.Label(self.root, text = ("To begin, we need to make sure a Philips Hue Bridge can be found on your network\n"
        "Press the button below to begin searching"), font = styles["font"], bg = styles["bg"], fg = "white")
        self.welcomeLabel2.pack()

        self.searchButton = tk.Button(self.root, text = "Search!", font = styles["font"], command = lambda: self.find_bridge())
        self.searchButton.pack(pady = 20)

        # the following widgets are pack_forget()'d so they don't display initially but have still been defined
        self.nameLabel = tk.Label(self.root, text = "Please enter your first name", font = styles["font-c"] + "12", bg = styles["bg"],
                                  fg = "white")
        self.nameLabel.pack_forget()

        self.nameEntry = tk.Entry(self.root, bg = styles["bg-light"], borderwidth = 4, foreground = "white",
                                  font = styles["font-c"] + "12", justify = "center", relief = "flat")
        self.nameEntry.pack_forget()

        self.start_button = tk.Button(self.root, text = "Start", font = styles["font"], command = lambda: self.finished(mainRoot))
        self.start_button.pack_forget()


    def find_bridge(self):
        self.bridge = HC.check_connection()
        if self.bridge == None:
            print ("fail")
            # do stuff
        else:
            # message box with bridge IP and user choice of connection
            if messagebox.askyesno("Bridge found!", ("A Hue Bridge has been found at {}\nWould you like to connect?\n\n"
            "If yes, please press the button on your Hue Bridge before continuing.").format(self.bridge[1]),
            parent = self.root):

                token = HC.get_new_api_token(self.bridge[1])
                if token[0]:
                    # display rest of user setup
                    self.nameLabel.pack(pady = 5)
                    self.nameEntry.pack(pady = 5)
                    self.start_button.pack(pady = 5)
                    self.apiToken = token[1]


    def finished(self, mainRoot):
        if len(self.nameEntry.get().strip()) == 0:
            messagebox.showinfo("You have no name?","Name entry field cannot be empty!")
        else:
            os.chdir("../../resources/user-settings")
            with open("settings.json", "w+") as settings_file_obj:
                settings = {
                "Bridge ID": self.bridge[0],
                "Bridge IP": self.bridge[1],
                "User": self.nameEntry.get().strip().capitalize(),
                "Token": self.apiToken
                }
                settings_file_obj.write(json.dumps(settings))

            self.exit_callback(mainRoot, False)




    def exit_callback(self, mainRoot, check = True):
        if check:
            if messagebox.askyesno("Exit?", "Are you sure you want to exit?\nAll setup progress will be lost.", parent = self.root):
                self.root.destroy()
        else:
            self.root.destroy()
            mainRoot.deiconify()
