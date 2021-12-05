import json
import socket
import sys
import random

#Adresse and port of socket server
HOST = '192.168.1.29'
PORT = 8080

access_json = 'boxyz_json.json'

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

    if string == 'getJson':
        with open(access_json, "r") as f:
            Json = json.load(f)
            conn.send(str(Json).encode('utf-8'))
    
    if string == 'test':
        conn.send(str("test").encode('utf-8'))

    if string == 'setTemp':
        conn.send("temp set".encode('utf-8'))

    if string == 'getTemp':
        with open(access_json, "r") as f:
            Json = json.load(f)
            conn.send(str(Json["heat"]["temperature"]).encode('utf-8'))

    conn.close()
s.close()

