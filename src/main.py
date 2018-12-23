from hueConnect import connect as HC
from hubSettings import settings as HS

import tkinter as tk
from tkinter import messagebox

import os


# Attempts to resolve a Hue Bridge on the local logical subnet
hueData = HC.check_connection()


# Main application GUI class
class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("HueHub")
        self.root.minsize(400, 350)
        self.root.maxsize(1920, 1080)
        self.root.geometry("750x600")

        os.chdir("../resources/icons")
        self.root.iconbitmap(r"bulb.ico")
        os.chdir("../../src")

        # dict styles for reference
        self.styles = {
            "bg": "#171515", # background color
            "bg-light": "#322D2D", # lighter variant of the background
            "font": "Helvetica 14", # main font used throughout the application
            "font-c": "Helvetica " # font without size specification
        }

        self.root.protocol("WM_DELETE_WINDOW", self.exit_callback)
        self.root.configure(background = self.styles["bg"])

        # checks if the the settings file exists
        if not HS.check_new_user(HS.getCWD()):
            HS.create_new_user(self.styles, self.root)


        else:
            self.userSettings = HS.SettingsExistingUser()

            self.welcomeMessage = "Welcome back, {}.".format(self.userSettings.user_name)
            self.welcomeLabel = tk.Label(self.root, text = self.welcomeMessage, bg = self.styles["bg"], font = self.styles["font-c"] + "20",
                                         fg = "white")
            self.welcomeLabel.grid(row = 0, pady = 5, padx = 5)


    def exit_callback(self):
        if messagebox.askyesno("Exit?", "Are you sure you want to exit?"):
            self.root.destroy()


def main():
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
