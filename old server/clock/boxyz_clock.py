import datetime
import time as t
import json
from clock.functions import clock, thermostas
from clock.functions import utils
from clock.functions.logger import *

access_json = 'boxyz_json.json'

log = Logger()
log.setFormat("%(levelname)s -- %(asctime)s -- %(name)s -- %(message)s")
log.setHandler("logs/clock.log", encoding="utf-8", mode="a")
log.createLog("CLOCK", logging.DEBUG)

def main_clock():
    while True:
        time = datetime.datetime.now()
        current_hour = time.strftime("%H:%M")
        clock.SetCurrentOn()
        current_on = clock.GetCurrentOn()
        if thermostas.GetTemporarily() == False:
            if clock.GetCurrentOn() != None: #Si ca retourne une plage horraire
                tempSlot = clock.GetTempSlot(current_on)
                thermostas.SetOnThermostas(tempSlot)
                thermostas.SetTemperature(tempSlot)
            if clock.GetCurrentOn() == None: #Si ca retourne rien ca set off le thermostas et remet la temperature par defaut
                tempDefault = utils.GetTempDefault()
                thermostas.SetOffThermostas()
                thermostas.SetTemperature(tempDefault)
        if thermostas.GetTemporarily() == True:
            with open(access_json, "r") as j:
                Json = json.load(j)
                if Json["thermostas"]["Temporarily"] == True:
                    if Json["thermostas"]["TemporarilyStart"] <= current_hour <= Json["thermostas"]["TemporarilyEnd"]:
                        temp = thermostas.GetTemperature()
                        thermostas.SetOnThermostas(temp)
                        log.infoLog("Thermostas set to: " + str(temp))
                    else:
                        thermostas.SetTemporarilyOff()
                        thermostas.SetOffThermostas()
                        log.infoLog("Thermostas set off")
        t.sleep(1)