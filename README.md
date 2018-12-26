# HueHub

**A desktop application for controlling the Philips Hue smart bulb system.**

- - - -
_Q: "Why? Why make your own when Hue Sync already exists?"._

A: I'm a programmer and where's the fun in that?
- - - -

The Hue Bridge API is the base of all communications between the HueHub client program and any smart bulbs. However, before the client software can make any HTTP requests to the Bridge's API, a Bridge needs to be found on the local network. This is done via the Hue Portal. Periodically, a Bridge that is 'alive' will poll the portal service and send it some information. This includes things such as its MAC Address and local IP address. The client can then send a get request to this portal, and receive JSON data about any bridges on the network, or an empty JSON array in the case that there are none.

A response for a single bridge being found would look something like this:
``` JSON
{
"id":"001788fffe100491",
"internalipaddress":"192.168.0.25",
"macaddress":"00:17:88:10:04:91",
"name":"Reece's Hue Bridge"
}
```
This can then be decoded and the key-value pairs that are needed can be saved. HueHub specifically on stores the MAC Address and local IP address of the Bridge.

After a bridge has been found, the client needs to establish authentication with the bridge in order to be allowed API access. This is done by pressing the Auth button on the bridge itself, and then sending a POST request to the root API URL of your bridge within the authentication period. I.e. a POST request would be made to https://<bridge IP>/api/ within 30 seconds of pressing the Auth button, and would contain JSON data that includes the the client software's name as well as the device it is installed on. Once this authentication process has completed (a JSON response of "success"), the bridge responds with a unique API token which the particular device can then use from then on to have access to all of the API's services.

This unique token, along with some basic user and bridge information is stored in a settings file so that the user only has to go through the setup process once per device.




---
Calls and access to smart bulb services are made to the a Hue Bridge via its RESTful API, making use of [Requests: HTTP for Humans™](http://docs.python-requests.org/en/master/).
