# This module houses the networking backend of the client program. All polls to the portal and API
# requests/auth attempts are contained here

import json
import requests

import tkinter as tk
from tkinter import messagebox


# Interfacing with the Philips Hue portal service in order to
# ascertain the local IP address of the Hue Bridge if one is present and 'alive'
def check_connection(test = False):
    hueDiscoveryURL = "https://discovery.meethue.com/"
    try:
        hueResponse = requests.get(hueDiscoveryURL)
        responseData = hueResponse.text
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
    except requests.exceptions.RequestException as exc:
        messagebox.showerror("Search error!", ("Raised: {}\n\nPortal URL \"{}\"".format(exc, hueDiscoveryURL)))


# autenticates with the bridge and receives api access tokens
def get_new_api_token(bridgeIP):
    reqDest = "http://" + bridgeIP + "/api"
    payload = "{\"devicetype\"" + ": " + "\"hue_hub#Reece PC\"}"

    r = requests.post(reqDest, data = payload)
    response = "".join([x for x in r.text if x not in ["[","]"]])
    response = json.loads(response)

    # Uncomment these lines if some debugging is needed
    # messagebox.showinfo("HUE API Connection was a success!","TO: {}\n\nCODE: {}\n\nREPONSE: {}".format(reqDest, r, response))
    # print(r.text)

    if "error" in response: # if an error response is received
        if response["error"]["type"] == 101:
            messagebox.showerror("That didn't quite work!","Please press the button on your Hue Bridge!")
            return (False, None)

    return (True, response["success"]["username"])


# returns large amount of data from the bridge - a simple get request on the user's access token
def user_information(apiAccessDetails):
    user = requests.get("http://" + apiAccessDetails[0] + "/api/" + apiAccessDetails[1])
    return json.loads(user.text)


# GUI popup with connection status information
def connection_status(apiAccessDetails):
    bridgeJSONDump = user_information(apiAccessDetails)

    info = ("Hue Bridge IP: {}\n".format(bridgeJSONDump["config"]["ipaddress"]),
            "Hue Bridge MAC Address: {}\n".format(bridgeJSONDump["config"]["mac"]),
            "Link button pressed in the last 30 seconds: {}\n".format(bridgeJSONDump["config"]["linkbutton"]),
            "Current number of API whitelists: {}\n".format(len([key for key in bridgeJSONDump["config"]["whitelist"]])),
            "Your API token: {}".format(apiAccessDetails[1]))
            
    messagebox.showinfo("Bridge: '{}'".format(bridgeJSONDump["config"]["name"]), "".join([x for x in info]))

# Returns parsed JSON object that contains lights
def lights(apiAccessDetails):
    userLights = requests.get("http://" + apiAccessDetails[0] + "/api/" + apiAccessDetails[1] + "/lights")
    print(userLights.text)
    return json.loads(userLights.text)



# Returns True if a light is on, False if not
def get_light_on_off_state(light, apiAccessDetails):
    lightStatus = requests.get("http://" + apiAccessDetails[0] + "/api/" + apiAccessDetails[1] + "/lights")
    return json.loads(lightStatus.text)[light]["state"]["on"]


# Changes a light's state to the opposite of its current state
def set_on_off(light, apiAccessDetails):
    if get_light_on_off_state(light, apiAccessDetails):
        payload = "{\"on\":false}"
    else:
        payload = "{\"on\":true}"

    requests.put("http://" + apiAccessDetails[0] + "/api/" + apiAccessDetails[1] + "/lights/" + light + "/state", data = payload)




# overrides the default param value to run in test mode
# execute as script to use this

if __name__ == "__main__":
    check_connection(True)
