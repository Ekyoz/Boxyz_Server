import json

access_json = 'boxyz_json.json'

current_on : int = None

#pour crrer les different plage horraire
def AddSlot(name : str , day : list, hourStart: int, hourEnd : int, temp : int, state : bool):
    with open(access_json, "r") as j:
        Json = json.load(j)
        size_time_slot : int = len(Json["heat"]["timeSlot"])
        id_last : int = list(Json["heat"]["timeSlot"].keys())[size_time_slot-1]
        Json["heat"]["timeSlot"][str(int(id_last) + 1)] = {"name":name, "day":day, "hourStart":hourStart, "hourEnd":hourEnd, "temp": temp, "state":state}
        with open(access_json, "w") as j:
            json.dump(Json, j, indent=6)

#pour supp une plage horraire
def DelSlot(id : int):
    with open(access_json, "r") as j:
        Json = json.load(j)
        Json["heat"]["timeSlot"].pop(str(id))
        with open(access_json, "w") as f:
            json.dump(Json, f, indent=6)


#pour definir la plage actuelle
def SetCurrentOn():
    current_hour = datetime.now().strftime("%H:%M")
    current_day = datetime.today().strftime("%A")
    with open(access_json, "r") as f:
        Json = json.load(f)
        for i in range(len(Json["days"][current_day])): #pour le nombre de slot dans le jour
            current_start_clock_time_slot = Json["heat"]["timeSlot"][str(Json["days"][current_day][i])]["hourStart"] # recupere l'heure du debut du slot du jour actuelle avec "i"
            current_end_clock_time_slot = Json["heat"]["timeSlot"][str(Json["days"][current_day][i])]["hourEnd"] # recupere l'heure du debut du slot du jour actuelle avec "i"
            if current_start_clock_time_slot <= current_hour <= current_end_clock_time_slot:
                current_on = Json["days"][current_day][i]

def GetCurrentOn():
    return current_on
                

#Recupere la temperature du slot voulu
def GetTempSlot(slot : int):
    with open(access_json, "r") as f:
        Json = json.load(f)
        temp = Json["heat"]["timeSlot"][str(slot)]["temp"]
        return temp


