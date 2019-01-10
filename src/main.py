from hueConnect import connect as HC
from hubSettings import settings as HS

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import os

from PIL import ImageTk, Image



# Main application GUI class
class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("HueHub")
        self.root.minsize(400, 350)
        self.root.maxsize(400, 350)
        self.root.geometry("750x600")

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

        self.root.configure(background = self.styles["bg"])

        self.menuBar = tk.Menu(self.root, activeborderwidth = 2)
        self.setup_menu()
        self.root.config(menu = self.menuBar)


        # Window closing protocol
        self.root.protocol("WM_DELETE_WINDOW", self.exit_callback)


        # Change directory to resources/icons/, apply icon, return to original working directory
        os.chdir("../resources/icons")
        self.root.iconbitmap(r"bulb.ico")
        os.chdir("../../src")



        # Checks if the the settings file exists. Loads the main application if it does, but creates a new
        # user profile if it does not.
        if not HS.check_new_user(HS.getCWD()):
            HS.create_new_user(self.styles, self.root)


        else:
            # Create a new settings object that allows access and editing of the settings file
            self.userSettings = HS.SettingsExistingUser()
            # Create an array of the details needed to access the API - the bridge API and access token
            self.apiAccessDetails = [self.userSettings.bridgeIP, self.userSettings.apiToken]
            # Create an array on all lights connected and reachable via the bridge
            self.lightsArray = [light for light in HC.lights(self.apiAccessDetails)]


            self.welcomeMessage = "Welcome back, {}.".format(self.userSettings.username)
            self.welcomeLabel = tk.Label(self.root, text = self.welcomeMessage, bg = self.styles["bg"], font = self.styles["font-c"] + "22",
                                         fg = "white")
            self.welcomeLabel.grid(row = 0, pady = 5, padx = 5, sticky = "n")

            self.lightCount = len(self.lightsArray)
            if self.lightCount > 1:
                self.lightsMessage = "You have {} lights connected and online.".format(self.lightCount)
            else:
                self.lightsMessage = "You have 1 light connected and online."
            self.lightsLabel = tk.Label(self.root, text = self.lightsMessage, bg = self.styles["bg"], font = self.styles["font-c"] + "17",
                                        fg = "white")
            self.lightsLabel.grid(row = 1, pady = 5, padx = 5, sticky = "n")

            self.choiceLabel = tk.Label(self.root, text = "Choose which light to interact with", bg = self.styles["bg"],
                                        font = self.styles["font-c"] + "9", fg = "white")
            self.choiceLabel.grid(row = 2, pady = 5, padx = 5, sticky = "n")


            self.lightChoice = ttk.Combobox (self.root, width = 50, height = 30, font = self.styles["font-c"] + "10",
                                             state = "readonly", values = (self.lightsArray))
            self.lightChoice.grid(row = 4, padx = 5, sticky = "n")
            self.lightChoice.set(self.lightsArray[0])

            self.lightFrame = tk.Frame(self.root, width = 330, height = 180, background = self.styles["bg-light"],
                                       relief = "ridge", bd = 1)
            self.lightFrame.grid(row = 6, column = 0, pady = 10)
            self.lightFrame.grid_propagate(False)

            # TODO - at some point - set the dropdown menu options strings to be equivalent to the light's actual
            # name returned from the JSON bridge dump

            os.chdir("../icons")
            self.onImage = "switch_on.png"
            self.switchOn = tk.PhotoImage(file = self.onImage)
            self.offImage = "switch_off.png"
            self.switchOff = tk.PhotoImage(file = self.offImage)




            if HC.get_light_on_off_state(self.lightChoice.get(), self.apiAccessDetails):
                self.NameAndState = "Light {} is on".format(self.lightChoice.get())
                self.OnOffButton = "Turn off"
            else:
                self.NameAndState = "Light {} is off".format(self.lightChoice.get())
                self.OnOffButton = "Turn on"

            self.lightNameAndState = tk.Label(self.lightFrame, text = self.NameAndState, font = self.styles["font-c"] + "15",
                                              bg = self.styles["bg-light"], fg = "white")
            self.lightNameAndState.grid(row = 0, column = 0, sticky = "w")

            self.LightOnOffButton = tk.Button(self.lightFrame, image = self.switchOn,
                                              command = lambda: [HC.set_on_off(self.lightChoice.get(),
                                              self.apiAccessDetails, self.brightnessSlider.get()), self.update_light_frame()],
                                              width = 100, height = 100)
            self.LightOnOffButton.grid(row = 2)

            self.brightnessSlider = tk.Scale(self.lightFrame, from_ = 0, to = 100, orient = "horizontal",
                                             background = self.styles["bg-light"], activebackground = self.styles["bg-light"],
                                             bd = 0, fg = "white", font = self.styles["font-c"] + "10", width = 40, highlightthickness = 0,
                                             label = "Brightness",
                                             command = lambda _: HC.set_light_brightness(self.lightChoice.get(),
                                                                 self.apiAccessDetails, self.brightnessSlider.get()))
            self.brightnessSlider.grid(row = 2, column = 1, padx = 60)
            self.brightnessSlider.set(HC.get_light_brightness(self.lightChoice.get(), self.apiAccessDetails))


            '''
            os.chdir("../images")
            self.lightImage = Image.open ("light_off2.png")
            print(self.lightImage.mode)
            self.lightImage = ImageTk.PhotoImage (self.lightImage)
            self.imagePlaceholder = tk.Label (self.lightFrame, image = self.lightImage, relief = "solid")
            self.imagePlaceholder.photo = self.lightImage
            self.imagePlaceholder.grid(row = 0, column = 1)
            '''




    def update_light_frame(self):
        if HC.get_light_on_off_state(self.lightChoice.get(), self.apiAccessDetails):
            self.lightNameAndState.config(text = "Light {} is on".format(self.lightChoice.get()))
            self.LightOnOffButton.config(image = self.switchOn)
        else:
            self.lightNameAndState.config(text = "Light {} is off".format(self.lightChoice.get()))
            self.LightOnOffButton.config(image = self.switchOff)


    # Sets up the various options contained within the program's menus
    def setup_menu(self):
        self.menuBar.config(background = self.styles["bg"])

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
