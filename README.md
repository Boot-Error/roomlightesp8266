# roomlightesp8266

My simple IOT setup to control room light using esp8226.

# Highlights

- A relay bridging the power to room light controlled from esp8266's GPIO
- Uses Micropython Framework

# Setup

## Hardware

- [ESP 8266 LoLin Module](https://www.amazon.in/Lolin-NodeMCU-ESP8266-CP2102-Wireless/dp/B010O1G1ES)
- [Single Channel Relay 220V - 5V control](https://www.amazon.in/CentIoT%C2%AE-Channel-Household-Appliance-Control/dp/B07PXZS7DF)
- 5V Power Supply (I used a mobile charger brick)

TODO: Circuit Schematics

## Software

- [Micropython](https://micropython.org/)

## Installation

1. Install Micropython, follow this documentation [here](http://docs.micropython.org/en/latest/esp8266/tutorial/intro.html#intro)
2. Upload this code using the WebREPL, [documentation](http://docs.micropython.org/en/latest/esp8266/tutorial/repl.html#webrepl-a-prompt-over-wifi)

# Usage

Write the WiFi credentials in `config.py`

```python
# contents of config.py

wifi_cred = ("SSID", "PASSWD")
```

Find the IP address of the esp8266 connected to WiFi either from the router page or `nmap`. Then, go that ip address from browser on your phone or pc. 

You can `cURL` follow urls to toggle the light

	# to turn on the lights
	curl http://<ip addr>/turnon 

	# to turn off the lights
	curl http://<ip addr>/turnoff

# Todo

- Complete Implementation of NTP for toggle lights by the time of the Day

