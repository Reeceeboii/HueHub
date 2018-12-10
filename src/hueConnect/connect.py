from urllib import request
import json

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
    except request.URLError as exc:
        print ("Raised: {} - couldn't resolve \"{}\"".format(exc, hueDiscoveryURL))

if __name__ == "__main__":
    check_connection(True)
