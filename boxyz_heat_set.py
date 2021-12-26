import json
import requests

access_json = 'boxyz_json.json'

def post(ip, message):
    try:
        return requests.post(url=ip, data=message)
    except:
        print("Erreur: post failed")

def heatDelSlot(id : int):
    with open(access_json, "r") as j:
        Json = json.load(j)
        Json["heat"]["timeSlot"].pop(str(id))
        with open(access_json, "w") as f:
            json.dump(Json, f, indent=6)


def heatAddSlot(name : str , day : list, hourStart: int, hourEnd : int, temp : int, state : bool):
    with open(access_json, "r") as j:
        Json = json.load(j)
        size_time_slot : int = len(Json["heat"]["timeSlot"])
        id_last : int = list(Json["heat"]["timeSlot"].keys())[size_time_slot-1]
        Json["heat"]["timeSlot"][str(int(id_last) + 1)] = {"name":name, "day":day, "hourStart":hourStart, "hourEnd":hourEnd, "temp": temp, "state":state}
        with open(access_json, "w") as j:
            json.dump(Json, j, indent=6)

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
            

def heatAddTemp():
    with open(access_json, "r") as j:
        Json = json.load(j)
        temp : int = Json["heat"]["temperature"]
        heatMax : int = Json["settings"]["heatMax"]
        if temp < heatMax:
            Json["heat"]["temperature"] = temp + 1
            with open(access_json, "w") as j:
                json.dump(Json, j, indent=6)

def heatDelTemp():
    with open(access_json, "r") as j:
        Json = json.load(j)
        temp : int = Json["heat"]["temperature"]
        heatMin = Json["settings"]["heatMin"]
        if heatMin < temp:
            Json["heat"]["temperature"] = temp - 1
            with open(access_json, "w") as j:
                json.dump(Json, j, indent=6)





#heatAddSlot("test", ["Lundi","Mardi"], "10:00", "11:00", 22, True)
#heatTest()
#heatDelSlot(5)