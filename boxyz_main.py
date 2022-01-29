import threading
from boxyz_server import *
from boxyz_heat_clock import *


#---------Logger---------
formatter_serveur = logging.Formatter("%(asctime)s -- %(name)s -- STARTING -- %(message)s")
handler_serveur = logging.FileHandler("logs/serveur.log", mode="a", encoding="utf-8")
handler_serveur.setFormatter(formatter_serveur)
handler_serveur.setLevel(logging.INFO)
logger_serveur = logging.getLogger("MAIN")
logger_serveur.setLevel(logging.INFO)
logger_serveur.addHandler(handler_serveur)

formatter_clock = logging.Formatter("%(asctime)s -- %(name)s -- STARTING -- %(message)s")
handler_clock = logging.FileHandler("logs/clock.log", mode="a", encoding="utf-8")
handler_clock.setFormatter(formatter_clock)
handler_clock.setLevel(logging.INFO)
logger_clock = logging.getLogger("MAIN")
logger_clock.setLevel(logging.INFO)
logger_clock.addHandler(handler_clock)


#----------Threading---------
thread_clock = threading.Thread(target=main_clock)
thread_server = threading.Thread(target=main_server)

thread_clock.setName('Clock thread')
thread_server.setName('Server thread')

try:
    clock = thread_clock.start()
    logger_clock.info("Start clock Boxyz")
except Exception as e:
    raise ValueError("Clock can be start")
    logger_serveur.warning('Warning Error', 'Erreur start clock : Failed to start clock.')
    print("Serveur erreur: " + repr(e))

try:
    server = thread_server.start()
    logger_serveur.info("Start serveur Boxyz")
except Exception as e:
    raise ValueError("Serveur can be start")
    logger_serveur.warning('Warning Error', 'Erreur start serveur : Failed to start serveur.')
    print("Serveur erreur: " + repr(e))



while True:
    Input = input()
    if Input == "exit":
        thread_clock._stop()
        thread_server._stop()
        logger_serveur.info("Shutdown serveur and clock Boxyz")
        print("Shutdown serveur and clock Boxyz")
        break

