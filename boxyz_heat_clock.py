from datetime import datetime
import time
import json
import requests
import logging
from boxyz_heat_functions import *

access_json = 'boxyz_json.json'
current_on : int = None
formatter = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")

handler_warning = logging.FileHandler("logs/warning.log", mode="a", encoding="utf-8")
handler_info = logging.FileHandler("logs/info.log", mode="a", encoding="utf-8")

handler_warning.setFormatter(formatter)
handler_info.setFormatter(formatter)

handler_info.setLevel(logging.INFO)
handler_warning.setLevel(logging.WARNING)

logger = logging.getLogger("Clock")
logger.setLevel(logging.INFO)
logger.addHandler(handler_warning)
logger.addHandler(handler_info)


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
            logger.info(str(current_hour) + " -- " + "Current on: " + str(current_on))
            time.sleep(5)
    except Exception as e:
        logger.warning('Warning Error %s: %s', '2001', 'Erreur thread clock : ' + str(e))