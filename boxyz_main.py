import threading
from boxyz_server import *
from boxyz_heat_clock import *

thread_clock = threading.Thread(target=main_clock)
thread_server = threading.Thread(target=main_server)

thread_server.start()
thread_clock.start()
