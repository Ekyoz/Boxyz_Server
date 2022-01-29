import json

access_json = 'boxyz_json.json'

#Augmenter la temperature
def AddTemp():
    with open(access_json, "r") as j:
        Json = json.load(j)
        temp : int = Json["heat"]["temperature"]
        heatMax : int = Json["settings"]["heatMax"]
        if temp < heatMax:
            Json["heat"]["temperature"] = temp + 1
            with open(access_json, "w") as j:
                json.dump(Json, j, indent=6)

#Diminuer la temperature
def DelTemp():
    with open(access_json, "r") as j:
        Json = json.load(j)
        temp : int = Json["heat"]["temperature"]
        heatMin = Json["settings"]["heatMin"]
        if heatMin < temp:
            Json["heat"]["temperature"] = temp - 1
            with open(access_json, "w") as j:
                json.dump(Json, j, indent=6)

#definir la temperature sans passer par + ou -
def SetTemperature(temp : int):
    with open(access_json, "r") as f:
        Json = json.load(f)
        Json["heat"]["temperature"] = temp
        with open(access_json, "w") as j:
            json.dump(Json, j, indent=6)

#Alluumer le thermostas
def SetOnThermostas(heat : int):
    with open(access_json, "r") as j:
        Json = json.load(j)
        IP = Json["settings"]["thermostas"]["ip"]
        PORT = Json["settings"]["thermostas"]["port"]
        url = "http://" + IP + ":" + PORT + "/heat?heater=1" + "&heat=" + str(heat)
        requests.post(url)

#Eteindre le thermostas
def SetOffThermostas():
    with open(access_json, "r") as j:
        Json = json.load(j)
        IP = Json["settings"]["thermostas"]["ip"]
        PORT = Json["settings"]["thermostas"]["port"]
        TEMP_DEFAULT = Json["settings"]["heatDefault"]
        url = "http://" + IP + ":" + PORT + "/heat?heater=0" + "&heat=" + str(TEMP_DEFAULT)
        requests.post(url)

