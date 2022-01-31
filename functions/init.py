from functions.thermostas import GetState, SetState, SetTemperature, access_json
import requests
import json

def __init__():
    with open(access_json, "r") as j:
        Json = json.load(j)
        IP = Json["settings"]["thermostas"]["ip"]
        PORT = Json["settings"]["thermostas"]["port"]
        TEMP_DEFAULT = Json["settings"]["tempDefault"]
        url = "http://" + IP + ":" + PORT + "/init?state="+ str(GetState()) + "&heat=" + str(TEMP_DEFAULT)
        requests.post(url)
        SetState(False)
    SetTemperature(TEMP_DEFAULT)
