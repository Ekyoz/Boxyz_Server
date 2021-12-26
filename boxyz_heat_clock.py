from datetime import datetime
import time
import json
import requests

access_json = 'boxyz_json.json'
current_on : int = None

def setCurrentOn():
    current_hour = datetime.now().strftime("%H:%M")
    current_day = datetime.today().strftime("%A")
    with open(access_json, "r") as f:
        Json = json.load(f)
        for i in range(len(Json["days"][current_day])): #pour le nombre de slot dans le jour
            current_start_clock_time_slot = Json["heat"]["timeSlot"][str(Json["days"][current_day][i])]["hourStart"] # recupere l'heure du debut du slot du jour actuelle avec "i"
            current_end_clock_time_slot = Json["heat"]["timeSlot"][str(Json["days"][current_day][i])]["hourEnd"] # recupere l'heure du debut du slot du jour actuelle avec "i"
            if current_start_clock_time_slot <= current_hour <= current_end_clock_time_slot:
                on = Json["days"][current_day][i]
                return on

def getTempSlot(slot : int):
    with open(access_json, "r") as f:
        Json = json.load(f)
        temp = Json["heat"]["timeSlot"][str(slot)]["temp"]
        return temp

def getTempDefault():
    with open(access_json, "r") as f:
        Json = json.load(f)
        temp_default = Json["settings"]["heatDefault"]
        return temp_default

def setOnThermostas(heat : int):
    with open(access_json, "r") as j:
        Json = json.load(j)
        IP = Json["settings"]["thermostas"]["ip"]
        PORT = Json["settings"]["thermostas"]["port"]
        url = "http://" + IP + ":" + PORT + "/heat?heater=1" + "&heat=" + str(heat)
        requests.post(url)

def setOffThermostas():
    with open(access_json, "r") as j:
        Json = json.load(j)
        IP = Json["settings"]["thermostas"]["ip"]
        PORT = Json["settings"]["thermostas"]["port"]
        TEMP_DEFAULT = Json["settings"]["heatDefault"]
        url = "http://" + IP + ":" + PORT + "/heat?heater=0" + "&heat=" + str(TEMP_DEFAULT)
        requests.post(url)

def setTemperature(temp : int):
    with open(access_json, "r") as f:
        Json = json.load(f)
        Json["heat"]["temperature"] = temp
        with open(access_json, "w") as j:
            json.dump(Json, j, indent=6)

def main_clock():
    while True:
        current_hour = datetime.now().strftime("%H:%M")
        if setCurrentOn() is not None:
            current_on = setCurrentOn()
            setOnThermostas(getTempSlot(current_on))
            with open(access_json, "r") as f:
                Json = json.load(f)
                setTemperature(int(Json["heat"]["timeSlot"][str(current_on)]["temp"]))
        else:
            current_on = setCurrentOn() 
            setOffThermostas()
            with open(access_json, "r") as f:
                Json = json.load(f)
                setTemperature(int(Json["settings"]["heatDefault"]))
                
        print(str(current_hour) + " -- " + "Current on: " + str(current_on))
        time.sleep(5)

