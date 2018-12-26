from hueConnect import connect as HC
from hubSettings import settings as HS

import tkinter as tk
from tkinter import messagebox

import os


# Main application GUI class
class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("HueHub")
        self.root.minsize(400, 350)
        self.root.maxsize(1920, 1080)
        self.root.geometry("750x600")

        self.menuBar = tk.Menu(self.root)
        self.setup_menu()
        self.root.config(menu = self.menuBar)


        # Change directory to resources/icons/, apply icon, return to original working directory
        os.chdir("../resources/icons")
        self.root.iconbitmap(r"bulb.ico")
        os.chdir("../../src")

        # Dict styles for reference
        self.styles = {
            "bg": "#171515", # Background color
            "bg-light": "#322D2D", # Lighter variant of the background
            "font": "Helvetica 14", # Main font used throughout the application
            "font-c": "Helvetica " # Font without size specification
        }

        # The font without a size specification is used by concatenating the size as a string after
        # referencing the key. I.e for font size 10: size = self.styles["font-c"] + "10"
        # would equate to "Helvetica 10"



        # Window closing protocol
        self.root.protocol("WM_DELETE_WINDOW", self.exit_callback)

        self.root.configure(background = self.styles["bg"])

        # Checks if the the settings file exists. Loads the main application if it does, but creates a new
        # user profile if it does not.
        if not HS.check_new_user(HS.getCWD()):
            HS.create_new_user(self.styles, self.root)


        else:
            self.userSettings = HS.SettingsExistingUser()
            # Creates a new settings object that allows access and editing of the settings file
            self.apiAccessDetails = [self.userSettings.bridgeIP, self.userSettings.apiToken]

            self.welcomeMessage = "Welcome back, {}.".format(self.userSettings.username)
            self.welcomeLabel = tk.Label(self.root, text = self.welcomeMessage, bg = self.styles["bg"], font = self.styles["font-c"] + "20",
                                         fg = "white")
            self.welcomeLabel.grid(row = 0, pady = 5, padx = 5)

            #messagebox.showinfo("User information", HC.user_information(self.apiAccessDetails))

    # Sets up the various options contained within the program's menus
    def setup_menu(self):
        # 'File' menu options and cascades
        filemenu = tk.Menu(self.menuBar, tearoff = 0)
        filemenu.add_command(label = "Exit HueHub", command = self.exit_callback)
        self.menuBar.add_cascade(label = "File", menu = filemenu)

        # 'Other' menu options and cascades
        othermenu = tk.Menu(self.menuBar, tearoff = 0)
        othermenu.add_command(label = "Information", command = self.program_information)
        othermenu.add_command(label = "Connection status", command = lambda: HC.connection_status(self.apiAccessDetails))
        self.menuBar.add_cascade(label = "Other", menu = othermenu)


    # Presents information about HueHub to the user
    def program_information(self):
        os.chdir("../program-information/")
        info = open("Info.txt", "r").read()
        os.chdir("../user-settings")
        messagebox.showinfo("About HueHub", info, parent = self.root)


    # If the user closes the main application window during runtime
    def exit_callback(self):
        if messagebox.askyesno("Exit?", "Are you sure you want to exit?"):
            self.root.destroy()


def main():
    # New tk root passed to MainApplication and placed under mainloop control flow
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
