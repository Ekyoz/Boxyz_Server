import json
import requests
import datetime

access_json = 'boxyz_json.json'


#--------------HEAT----------------#

#-------SLOT-------#

def heatAddSlot(name : str , day : list, hourStart: int, hourEnd : int, temp : int, state : bool):
    with open(access_json, "r") as j:
        Json = json.load(j)
        size_time_slot : int = len(Json["heat"]["timeSlot"])
        id_last : int = list(Json["heat"]["timeSlot"].keys())[size_time_slot-1]
        Json["heat"]["timeSlot"][str(int(id_last) + 1)] = {"name":name, "day":day, "hourStart":hourStart, "hourEnd":hourEnd, "temp": temp, "state":state}
        with open(access_json, "w") as j:
            json.dump(Json, j, indent=6)

def heatDelSlot(id : int):
    with open(access_json, "r") as j:
        Json = json.load(j)
        Json["heat"]["timeSlot"].pop(str(id))
        with open(access_json, "w") as f:
            json.dump(Json, f, indent=6)

def heatAddTemp():
    with open(access_json, "r") as j:
        Json = json.load(j)
        temp : int = Json["heat"]["temperature"]
        heatMax : int = Json["settings"]["heatMax"]
        if temp < heatMax:
            Json["heat"]["temperature"] = int(temp + 1)
            with open(access_json, "w") as j:
                json.dump(Json, j, indent=6)

def heatDelTemp():
    with open(access_json, "r") as j:
        Json = json.load(j)
        temp : int = Json["heat"]["temperature"]
        heatMin = Json["settings"]["heatMin"]
        if heatMin < temp:
            Json["heat"]["temperature"] = int(temp - 1)
            with open(access_json, "w") as j:
                json.dump(Json, j, indent=6)

"""
def heatTest():
    with open(access_json, "r") as j:
        Json = json.load(j)
        size_time_slot : int = len(Json["heat"]["timeSlot"])
        id_last : int = list(Json["heat"]["timeSlot"].keys())[size_time_slot-1]
        #if size_time_slot != int(id_last) +1:
            #for i in range(size_time_slot):
                #if Json["heat"]["timeSlot"]

def setDays():
    with open(access_json, "r") as j:
        for i in range(len(Json["heat"][current_day])):
            break
"""


#--------------CLOCK----------------#

#-------SET-------#

def clockSetCurrentOn():
    current_hour = datetime.datetime.now().strftime("%H:%M")
    current_day = datetime.datetime.today().strftime("%A")
    with open(access_json, "r") as f:
        Json = json.load(f)
        for i in range(len(Json["days"][current_day])): #pour le nombre de slot dans le jour
            current_start_clock_time_slot = Json["heat"]["timeSlot"][str(Json["days"][current_day][i])]["hourStart"] # recupere l'heure du debut du slot du jour actuelle avec "i"
            current_end_clock_time_slot = Json["heat"]["timeSlot"][str(Json["days"][current_day][i])]["hourEnd"] # recupere l'heure du debut du slot du jour actuelle avec "i"
            if current_start_clock_time_slot <= current_hour <= current_end_clock_time_slot:
                on = Json["days"][current_day][i]
                return on

def clockSetOnThermostas(heat : int):
    with open(access_json, "r") as j:
        Json = json.load(j)
        IP = Json["settings"]["thermostas"]["ip"]
        PORT = Json["settings"]["thermostas"]["port"]
        url = "http://" + IP + ":" + PORT + "/heat?heater=1" + "&heat=" + str(heat)
        requests.post(url)

def clockSetOffThermostas():
    with open(access_json, "r") as j:
        Json = json.load(j)
        IP = Json["settings"]["thermostas"]["ip"]
        PORT = Json["settings"]["thermostas"]["port"]
        TEMP_DEFAULT = Json["settings"]["heatDefault"]
        url = "http://" + IP + ":" + PORT + "/heat?heater=0" + "&heat=" + str(TEMP_DEFAULT)
        requests.post(url)

def clockSetTemperature(temp : int):
    with open(access_json, "r") as f:
        Json = json.load(f)
        Json["heat"]["temperature"] = temp
        with open(access_json, "w") as j:
            json.dump(Json, j, indent=6)

#-------GET-------#

def clockGetTempSlot(slot : int):
    with open(access_json, "r") as f:
        Json = json.load(f)
        temp = Json["heat"]["timeSlot"][str(slot)]["temp"]
        return temp

def clockGetTempDefault():
    with open(access_json, "r") as f:
        Json = json.load(f)
        temp_default = Json["settings"]["heatDefault"]
        return temp_default


#--------------OTHER----------------#

def post(ip, message):
    try:
        return requests.post(url=ip, data=message)
    except:
        print("Erreur: post failed")
