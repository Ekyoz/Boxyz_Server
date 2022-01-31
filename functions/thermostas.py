import json
import requests
import datetime

from boxyz_server import Json

access_json = 'boxyz_json.json'

#Augmenter la temperature
def AddTemp():
    with open(access_json, "r") as j:
        Json = json.load(j)
        temp : int = Json["thermostas"]["temperature"]
        heatMax : int = Json["settings"]["tempMax"]
        if temp < heatMax:
            Json["thermostas"]["temperature"] = temp + 1
            with open(access_json, "w") as j:
                json.dump(Json, j, indent=6)

#Diminuer la temperature
def DelTemp():
    with open(access_json, "r") as j:
        Json = json.load(j)
        temp : int = Json["thermostas"]["temperature"]
        heatMin = Json["settings"]["tempMin"]
        if heatMin < temp:
            Json["thermostas"]["temperature"] = temp - 1
            with open(access_json, "w") as j:
                json.dump(Json, j, indent=6)

#definir la temperature sans passer par + ou -
def SetTemperature(temp : int):
    with open(access_json, "r") as f:
        Json = json.load(f)
        Json["thermostas"]["temperature"] = int(temp)
        with open(access_json, "w") as j:
            json.dump(Json, j, indent=6)

def GetState():
    with open(access_json, "r") as j:
        Json = json.load(j)
        return bool(Json["thermostas"]["state"])

def SetState(state : bool):
    with open(access_json, "r") as j:
        Json = json.load(j)
        Json["thermostas"]["state"] = state
        with open(access_json, "w") as f:
            json.dump(Json, f, indent=6)

def GetTemperature():
    with open(access_json, "r") as j:
        Json = json.load(j)
        return int(Json["thermostas"]["temperature"])

def SetTemperature(temp : int):
    with open(access_json, "r") as j:
        Json = json.load(j)
        Json["thermostas"]["temperature"] = int(temp)
        with open(access_json, "w") as f:
            json.dump(Json, f, indent=6)


#Alluumer le thermostas
def SetOnThermostas(heat : int):
    if GetState() == False:
        with open(access_json, "r") as j:
            Json = json.load(j)
            IP = Json["settings"]["thermostas"]["ip"]
            PORT = Json["settings"]["thermostas"]["port"]
            url = "http://" + IP + ":" + PORT + "/heat?heater=1" + "&heat=" + str(heat)
            requests.post(url)
            SetState(True)

#Eteindre le thermostas
def SetOffThermostas():
    if GetState() == True:
        with open(access_json, "r") as j:
            Json = json.load(j)
            IP = Json["settings"]["thermostas"]["ip"]
            PORT = Json["settings"]["thermostas"]["port"]
            TEMP_DEFAULT = Json["settings"]["tempDefault"]
            url = "http://" + IP + ":" + PORT + "/heat?heater=0" + "&heat=" + str(TEMP_DEFAULT)
            requests.post(url)
            SetState(False)

def SetTemporarilyOn():
    Currrent_hour = datetime.datetime.now()
    with open(access_json, "r") as j:
        Json = json.load(j)
        with open(access_json, "w") as f:
            Json["thermostas"]["Temporarily"] = True
            Json["thermostas"]["TemporarilyStart"] = Currrent_hour.strftime("%H:%M")
            deltaHour = int(Json["setting"]["clockTimeToDefault"])
            hour_added = datetime.timedelta(hours=deltaHour)
            Json["thermostas"]["TemporarilyEnd"] = (Currrent_hour + hour_added).strftime("%H:%M")
            json.dump(Json, f, indent=6)
            print(Json["thermostas"]["TemporarilyEnd"])

