from datetime import datetime
import time
import json
import requests
import logging
from boxyz_heat_functions import *

access_json = 'boxyz_json.json'
current_on : int = None

formatter_warning = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")
handler_warning = logging.FileHandler("logs/warning.log", mode="a", encoding="utf-8")
handler_warning.setFormatter(formatter_warning)
handler_warning.setLevel(logging.WARNING)
logger_warning = logging.getLogger("CLOCK")
logger_warning.setLevel(logging.WARNING)
logger_warning.addHandler(handler_warning)

formatter_clock = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")
handler_clock = logging.FileHandler("logs/clock.log", mode="a", encoding="utf-8")
handler_clock.setFormatter(formatter_clock)
handler_clock.setLevel(logging.INFO)
logger_clock = logging.getLogger("CLOCK")
logger_clock.setLevel(logging.INFO)
logger_clock.addHandler(handler_clock)


def main_clock():
    try:
        while True:
            current_hour = datetime.now().strftime("%H:%M")
            if clockSetCurrentOn() is not None:
                current_on = clockSetCurrentOn()
                clockSetOnThermostas(clockGetTempSlot(current_on))
                with open(access_json, "r") as f:
                    Json = json.load(f)
                    clockSetTemperature(int(Json["heat"]["timeSlot"][str(current_on)]["temp"]))
            if clockSetCurrentOn() is None:
                current_on = clockSetCurrentOn() 
                clockSetOffThermostas()
                with open(access_json, "r") as f:
                    Json = json.load(f)
                    clockSetTemperature(int(Json["settings"]["heatDefault"]))
            logger_clock.info(str(current_hour) + " -- " + "Current on: " + str(current_on))
            time.sleep(5)
    except Exception as e:
        logger_warning.warning('Warning Error %s: %s', '2001', 'Erreur thread clock : ' + str(e))