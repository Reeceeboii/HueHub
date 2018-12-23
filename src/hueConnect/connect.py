from urllib import request
import json
import requests # http request module

import tkinter as tk
from tkinter import messagebox


# Interfacing with the Philips Hue portal service in order to
# ascertain the local IP address of the Hue Bridge if one is present and 'alive'
def check_connection(test = False):
    hueDiscoveryURL = "https://discovery.meethue.com/"
    try:
        hueResponse = request.urlopen(hueDiscoveryURL)
        responseData = hueResponse.read()
        responseData = responseData.decode("utf-8")
        responseData = "".join([x for x in responseData if x not in ["[","]"]])
        responseData = json.loads(responseData)

        if not test:
            hueID = responseData["id"]
            hueIP = responseData["internalipaddress"]
            return(hueID, hueIP)
        else:
            print("CONNECTION TEST\n")
            print("DECODED JSON DATA: {}\n".format(responseData))
            print("Bridge ID: {}".format(responseData["id"]))
            print("Bridge local IP: {}".format(responseData["internalipaddress"]))
    except (request.URLError, ValueError) as exc:
        messagebox.showerror("Search error!", ("Raised: {}\n\nPortal URL \"{}\"".format(exc, hueDiscoveryURL)))


def get_new_api_token(bridgeIP):
    reqDest = "http://" + bridgeIP + "/api"
    payload = "{\"devicetype\"" + ": " + "\"hue_hub#Reece PC\"}"

    r = requests.post(reqDest, data = payload)
    response = "".join([x for x in r.text if x not in ["[","]"]])
    response = json.loads(response)

    messagebox.showinfo("HUE API Connection was a success!","TO: {}\n\nCODE: {}\n\nREPONSE: {}".format(reqDest, r, response))
    print(r.text)

    if "error" in response:
        if response["error"]["type"] == 101:
            messagebox.showerror("Try again!","Please press the button on your Hue Bridge!")
            return (False, None)

    return (True, response["success"]["username"])




# overrides the default param value to run in test mode
# execute as script to use this

if __name__ == "__main__":
    check_connection(True)
