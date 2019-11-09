# boot.py
# This file is executed on every boot (including wake-boot from deepsleep)

# Connects to WIFI
# Write the credentials in config.py
#
# Contents of config.py
#   wifi_cred = ("SSID", "PASSWD")

import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl
import network
import usocket as socket
import struct
import time

from config import wifi_cred


webrepl.start()
gc.collect()

def do_connect():
    """
    Connects to WIFI using Credentials in config.py
    """
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(*wifi_cred)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

do_connect()
