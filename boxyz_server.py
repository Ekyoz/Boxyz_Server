import json
import socket
import sys
import random
import threading
from boxyz_heat_set import *
from boxyz_heat_clock import *

#Adresse and port of socket server
access_json = 'boxyz_json.json'

with open (access_json, "r") as j:
    Json = json.load(j)
    HOST = Json["settings"]["server"]["host"]
    PORT = int(Json["settings"]["server"]["port"])

def main_server():
    #Create server
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Server Created')
    except OSError as e:
        print('Failed to create socket.')
        sys.exit()

    #Bind server to adresse
    try:
        s.bind((HOST, PORT))
    except OSError as e:
        print('Bind failed.')
        sys.exit()
    print('Socket bind complete')
    #Listener
    s.listen(1)
    print('Server now listening')

    #main
    while (1):
        conn, addr = s.accept()
        print('Connected with ' + addr[0] + ':' + str(addr[1]))
        #Input from client
        reqCommand = conn.recv(1024)
        print('Client -> ' + reqCommand.decode('utf-8'))

        string = reqCommand.decode('utf-8')
        #Condition
        #For stop the serveur
        if (string == 'stop'):
            conn.sendall("Server closed".encode('utf-8'))
            print("Server closed")
            break

        if string == 'test':
            conn.send(str("test").encode('utf-8'))

        if string == 'getJson':
            with open(access_json, "r") as f:
                Json = json.load(f)
                conn.send(str(Json).encode('utf-8'))
        
        if "setHeat" in string:
            conn.send("temp set".encode('utf-8'))
            setTemperature(string.split("-")[1])

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
                setOffThermostas()
            if current_on is None:
                setOnThermostas(getTempSlot(current_on))

        conn.close()
    s.close()

main_server()