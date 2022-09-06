import json
import datetime

access_json = 'boxyz_json.json'

#pour crrer les different plage horraire
def AddSlot(name : str , day : list, hourStart: int, hourEnd : int, temp : int, state : bool):
    with open(access_json, "r") as j:
        Json = json.load(j)
        size_time_slot : int = len(Json["clock"]["timeSlot"])
        id_last : int = list(Json["clock"]["timeSlot"].keys())[size_time_slot-1]
        Json["clock"]["timeSlot"][str(int(id_last) + 1)] = {"name":name, "day":day, "hourStart":hourStart, "hourEnd":hourEnd, "temp": temp, "state":state}
        with open(access_json, "w") as j:
            json.dump(Json, j, indent=6)

#pour supp une plage horraire
def DelSlot(id : int):
    with open(access_json, "r") as j:
        Json = json.load(j)
        Json["clock"]["timeSlot"].pop(str(id))
        with open(access_json, "w") as f:
            json.dump(Json, f, indent=6)

#pour definir la plage actuelle
def SetCurrentOn():
    time = datetime.datetime.now()
    current_hour = time.strftime("%H:%M")
    day = datetime.datetime.today()
    current_day = day.strftime("%A")
    with open(access_json, "r") as f:
        Json = json.load(f)
        for i in range(len(Json["days"][current_day])): #pour le nombre de slot dans le jour
            current_start_clock_time_slot = Json["clock"]["timeSlot"][str(Json["days"][current_day][i])]["hourStart"] # recupere l'heure du debut du slot du jour actuelle avec "i"
            current_end_clock_time_slot = Json["clock"]["timeSlot"][str(Json["days"][current_day][i])]["hourEnd"] # recupere l'heure du debut du slot du jour actuelle avec "i"
            if current_start_clock_time_slot <= current_hour <= current_end_clock_time_slot:
                Json["clock"]["current_on"] = Json["days"][current_day][i]
                with open(access_json, "w") as j:
                    json.dump(Json, j, indent=6)
            else:
                Json["clock"]["current_on"] = None
                with open(access_json, "w") as j:
                    json.dump(Json, j, indent=6)

#REcupere current on dans le json
def GetCurrentOn():
    with open(access_json, "r") as f:
        Json = json.load(f)
        return Json["clock"]["current_on"]


#Recupere la temperature du slot voulu
def GetTempSlot(slot : int):
    with open(access_json, "r") as f:
        Json = json.load(f)
        temp = Json["clock"]["timeSlot"][str(slot)]["temp"]
        return temp


