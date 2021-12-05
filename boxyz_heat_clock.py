from datetime import datetime
import time
import json

access_json = 'boxyz_json.json'

while True:
    current_hour = datetime.now().strftime("%H:%M")
    current_day = datetime.today().strftime("%A")
    with open(access_json, "r") as f:
        Json = json.load(f)
        for i in range(len(Json["days"][current_day])):
            current_clock_time_slot = Json["heat"]["timeSlot"][str(Json["days"][current_day][i])]["hourStart"]
            print(current_clock_time_slot + " -- " + current_hour)
            if current_hour == current_clock_time_slot:
                print("yes: " + str(i))
                break
        
    time.sleep(1)