# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)

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

class RoomLight:

    def __init__(self):
        
        self.state = "on" # follows master config, i.e physical switch
        self.pin = machine.Pin(2, machine.Pin.OUT)

        self.action() # apply default config on startup

    def setState(self, val):

        print("Changed state to {}".format(val))
        self.state = val
        self.action()

    def action(self):

        if self.state == "off":
            self.pin.value(0)
        elif self.state == "on":
            self.pin.value(1)
        else:
            pass

    def handleRequest(self, request):

        req = str(request)
        if req.find("/turnon") >= 0:
            self.setState("on")
        if req.find("/turnoff") >= 0:
            self.setState("off")
        else:
            pass

    def serveHTML(self):

        return """<!DOCTYPE html>
        <html>
            <head>
                <title>Room Light</title>
                <meta name="viewport" content="width=device-width, initial-scale=1"/>
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
                <style>
                    .off {
                        background-color: black;
                        color: white;
                    }
                    .on {
                        background-color: white;
                        color: black;
                    }
                </style>
            </head>""" + """
            <body class="{state}">
                <div class="container text-center">
                    <h1 class="{state}" style="text-align: center;">The lights are {state} currently</h1>
                    <form action="/turn{otherState}" method="get">
                        <button type="submit" class="btn btn-outline-secondary">Turn {otherState}</button>
                    </form>
                </div>
            </body>
        </html>
        """.format(state=self.state, otherState="off" if self.state == "on" else "on")

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(*wifi_cred)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


def runNTP(r1):
    """
    Get time from the NTP Server
    Set the light state based on daylight 
    """


    address = socket.getaddrinfo('pool.ntp.org', 123)[0][-1]
    data = '\x1b' + 47 * '\0'
    epoch = 3155587200 + (24 * 3600) - (3600 * 5) - 1800

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(address)
    s.sendto(data, address)

    print("Fetching NTP..")

    data, address = s.recvfrom(1024)

    s.close()

    t = struct.unpack("!12I", data)[10]
    t -= epoch

    lt = time.localtime(t)
    print('Time is ', time.localtime(t))

    if 18 <= lt[3] < 23 and 0 <= lt[3] <= 4:
        r1.setState('on')

    elif 5 <= lt[3] <= 17:
        r1.setState('off')


do_connect()
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

rl = RoomLight()
# runNTP(rl)

# setup ntp for turning lights based on time of day
tim = machine.Timer(-1)
tim.init(period=1000 * 60 * 15, mode=machine.Timer.PERIODIC, callback=lambda t: runNTP(rl))

while True:

        cl, addr = s.accept()
        print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        val = ""
        i=0
        while True:
            line = cl_file.readline()
            if i==0 :
                val +=str(line)
            i = i+1
            if not line or line == b'\r\n':
                break

        # handlePin(val)
        rl.handleRequest(val)
        cl.send(rl.serveHTML())
        cl.send("\r\n")
        cl.close()
