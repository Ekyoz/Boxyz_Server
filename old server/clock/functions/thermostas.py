import json
import requests
import datetime

access_json = 'boxyz_json.json'


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


#Allumer le thermostas
def SetOnThermostas(heat : int):
    if GetState() == False:
        with open(access_json, "r") as j:
            Json = json.load(j)
            IP = Json["settings"]["thermostas"]["ip"]
            PORT = Json["settings"]["thermostas"]["port"]
            url = "http://" + IP + "/heat?heater=1" + "&heat=" + str(heat)
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
            url = "http://" + IP + "/heat?heater=0" + "&heat=" + str(TEMP_DEFAULT)
            requests.post(url)
            SetState(False)

def SetTemporarilyOn():
    Currrent_hour = datetime.datetime.now()
    with open(access_json, "r") as j:
        Json = json.load(j)
        if (Json["thermostas"]["Temporarily"] == False) & (Json["thermostas"]["TemporarilyStart"] is None) & (Json["thermostas"]["TemporarilyEnd"] is None):
            with open(access_json, "w") as f:
                Json["thermostas"]["Temporarily"] = True
                Json["thermostas"]["TemporarilyStart"] = Currrent_hour.strftime("%H:%M")
                addedHour = int(Json["settings"]["clockTimeToDefaultHour"])
                addedMin = int(Json["settings"]["clockTimeToDefaultMin"])
                deltaHour = datetime.timedelta(hours=addedHour, minutes=addedMin)
                Json["thermostas"]["TemporarilyEnd"] = (Currrent_hour + deltaHour).strftime("%H:%M")
                json.dump(Json, f, indent=6)

def SetTemporarilyOff():
    with open(access_json, "r") as j:
        Json = json.load(j)
        if Json["thermostas"]["Temporarily"] == True:
            with open(access_json, "w") as f:
                Json["thermostas"]["Temporarily"] = False
                Json["thermostas"]["TemporarilyStart"] = None
                Json["thermostas"]["TemporarilyEnd"] = None
                json.dump(Json, f, indent=6)

def GetTemporarily():
    with open(access_json, "r") as j:
        Json = json.load(j)
        return bool(Json["thermostas"]["Temporarily"])
