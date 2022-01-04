import json
import socket
import sys
import random
import threading
import logging
from boxyz_heat_functions import *

#Adresse and port of socket server
access_json = 'boxyz_json.json'
formatter = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")

handler_warning = logging.FileHandler("logs/warning.log", mode="a", encoding="utf-8")
handler_info = logging.FileHandler("logs/info.log", mode="a", encoding="utf-8")

handler_warning.setFormatter(formatter)
handler_info.setFormatter(formatter)

handler_info.setLevel(logging.INFO)
handler_warning.setLevel(logging.WARNING)

logger = logging.getLogger("Serveur")
logger.setLevel(logging.INFO)
logger.addHandler(handler_warning)
logger.addHandler(handler_info)


with open (access_json, "r") as j:
    Json = json.load(j)
    HOST = Json["settings"]["server"]["host"]
    PORT = int(Json["settings"]["server"]["port"])

def main_server():
    #Create server
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        logger.info('Server created')
    except OSError as e:
        sys.exit()
        logger.warning('Warning Error %s: %s', '2099', 'Erreur thread server : Failed to create socket. -> ' + str(e))

    #Bind server to adresse
    s.listen(1)
    logger.info('Server now listening')

    #main
    try:
        while (1):
            conn, addr = s.accept()
            logger.info('Connected with ' + addr[0] + ':' + str(addr[1]))
            #Input from client
            reqCommand = conn.recv(1024)
            logger.info('Client -> ' + reqCommand.decode('utf-8'))

            string = reqCommand.decode('utf-8')
            #Condition
            #For stop the serveur
            if (string == 'stop'):
                conn.sendall("Server closed".encode('utf-8'))
                logger.info("Server closed")
                break

            if string == 'test':
                conn.send(str("test").encode('utf-8'))

            if string == 'getJson':
                with open(access_json, "r") as f:
                    Json = json.load(f)
                    conn.send(str(Json).encode('utf-8'))
            
            if "setHeat" in string:
                conn.send("temp set".encode('utf-8'))
                clockSetTemperature(string.split("-")[1])

            if string == 'getHeat':
                with open(access_json, "r") as f:
                    Json = json.load(f)
                    conn.send(str(Json["heat"]["temperature"]).encode('utf-8'))
            
            if string == 'heatAdd':
                heatAddTemp()

            if string == 'heatDel':
                heatDelTemp()

            if string == 'changeStatusHeater':
                if current_on is not None:
                    clockSetOffThermostas()
                if current_on is None:
                    clockSetOnThermostas(clockGetTempSlot(current_on))

            conn.close()
            s.close()
    except Exception as e:
        logger.warning('Warning Error %s: %s', '2009', 'Erreur thread server : Erreur in sockets arguments. -> ' + str(e))

main_server()