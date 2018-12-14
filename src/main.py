from hueConnect import connect as HC
from hubSettings import settings as HS

import tkinter as tk
from tkinter import messagebox


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

        # dict styles for reference
        self.styles = {
            "bg": "#171515", # background color
            "font": "Helvetica 14" # main font used throughout the application
        }

        self.root.protocol("WM_DELETE_WINDOW", self.exit_callback)
        self.root.configure(background=self.styles["bg"])

        # checks if the the settings file exists
        if HS.check_new_user(HS.getCWD()):
            print("settings file exists")
            userSettings = HS.SettingsExistingUser()
        else:
            HS.create_new_user(self.styles, self.root)




    def exit_callback(self):
        if messagebox.askyesno("Exit?", "Are you sure you want to exit?"):
            self.root.destroy()


def main():
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
