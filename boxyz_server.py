import json
import socket
import sys
import logging
import functions.thermostas as thermostas
import functions.clock as clock

access_json = 'boxyz_json.json'

formatter_serveur = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")
handler_serveur = logging.FileHandler("logs/serveur.log", mode="a", encoding="utf-8")
handler_serveur.setFormatter(formatter_serveur)
handler_serveur.setLevel(logging.INFO)
logger_serveur = logging.getLogger("Serveur")
logger_serveur.setLevel(logging.INFO)
logger_serveur.addHandler(handler_serveur)

with open (access_json, "r") as j:
    Json = json.load(j)
    HOST = Json["settings"]["server"]["host"]
    PORT = int(Json["settings"]["server"]["port"])

def main_server():
    #Create server
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        print('Serveur - Server created and now listening')
        logger_serveur.info("Server created and now listening")
    except OSError as e:
        print(str(e))
        logger_serveur.warning('Warning Error %s: %s', '2099', 'Erreur thread server : Failed to create socket. -> ' + str(e))
        sys.exit()

    #main
    while (1):
        conn, addr = s.accept()
        logger_serveur.info('Connected with ' + addr[0] + ':' + str(addr[1]))
        #Input from client
        reqCommand = conn.recv(1024)
        logger_serveur.info('Client -> ' + reqCommand.decode('utf-8'))

        string = reqCommand.decode('utf-8')
        #Condition
        try:
            try:
                if string == 'test':
                    conn.send(str("true").encode('utf-8'))
                    
                if string == 'getJson':
                    with open(access_json, "r") as f:
                        Json = json.load(f)
                        conn.send(str(Json).encode('utf-8'))
                
                if "setHeat" in string:
                    conn.send("temp set".encode('utf-8'))
                    thermostas.SetTemperature(string.split("-")[1])

                if string == 'getHeat':
                    with open(access_json, "r") as f:
                        Json = json.load(f)
                        conn.send(str(Json["thermostas"]["temperature"]).encode('utf-8'))
                
                if string == 'heatAdd':
                    thermostas.AddTemp()

                if string == 'heatDel':
                    thermostas.DelTemp()

                if string == 'changeStatusHeater':
                    current_on = clock.GetCurrentOn()
                    print(current_on)
                    if current_on == None:
                        thermostas.SetOffThermostas()
                    if current_on != None:
                        thermostas.SetOnThermostas(21)  
            except:
                conn.send("error".encode('utf-8'))
        except Exception as e:
            logger_serveur.warning('Warning Error %s: %s', '2009', 'Erreur thread server : Erreur in sockets arguments. -> ' + str(e))
        conn.close()
    s.close()
