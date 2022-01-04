import threading
from boxyz_server import *
from boxyz_heat_clock import *

thread_clock = threading.Thread(target=main_clock)
thread_server = threading.Thread(target=main_server)

thread_clock.setName('Clock thread')
thread_server.setName('Server thread')

thread_clock.start()
thread_server.start()
