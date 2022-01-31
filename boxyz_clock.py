import datetime
import time as t
import logging
from functions import clock, thermostas, utils

access_json = 'boxyz_json.json'

formatter_clock = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")
handler_clock = logging.FileHandler("logs/clock.log", mode="a", encoding="utf-8")
handler_clock.setFormatter(formatter_clock)
handler_clock.setLevel(logging.INFO)
logger_clock = logging.getLogger("CLOCK")
logger_clock.setLevel(logging.INFO)
logger_clock.addHandler(handler_clock)


def main_clock():
    while True:
        time = datetime.datetime.now()
        current_hour = time.strftime("%H:%M")
        clock.SetCurrentOn()
        current_on = clock.GetCurrentOn()
        if clock.GetCurrentOn() != None: #Si ca retourne une plage horraire
            print("test2")
            tempSlot = clock.GetTempSlot(current_on)
            thermostas.SetOnThermostas(tempSlot)
            thermostas.SetTemperature(tempSlot)
        if clock.GetCurrentOn() == None: #Si ca retourne rien ca set off le thermostas et remet la temperature par defaut
            thermostas.SetTemporarilyOn()
            tempDefault = utils.GetTempDefault()
            thermostas.SetOffThermostas()
            thermostas.SetTemperature(tempDefault)
        logger_clock.info(str(current_hour) + " -- " + "Current on: " + str(current_on))
        t.sleep(5)