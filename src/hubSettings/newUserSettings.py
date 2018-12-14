import tkinter as tk
from tkinter import messagebox

#from PIL import Image, ImageTk
# Implement some better styling at a later date

import os

class NewUserSettings:
    def __init__(self, styles, mainRoot):
        mainRoot.withdraw()
        # MainApplication root window is withdrawn from view

        self.root = tk.Tk()
        self.root.title("HueHub - new user setup")
        self.root.minsize(400, 350)
        self.root.maxsize(1920, 1080)
        self.root.geometry("750x600")
        self.root.protocol("WM_DELETE_WINDOW", self.exit_callback)
        self.root.configure(background = styles["bg"])


        self.welcomeLabel = tk.Label(self.root, text = "HueHub", font = styles["font"])
        self.welcomeLabel.pack()

    def exit_callback(self):
        if messagebox.askyesno("Exit?", "Are you sure you want to exit?\nAll setup progress will be lost."):
            self.root.destroy()
