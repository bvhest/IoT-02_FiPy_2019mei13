# https://pastebin.com/PLi30hcH

""" OTAA Node example compatible with the LoPy Nano Gateway """

# pycom libs:
import pycom
# network libs:
from network import WLAN
import socket
# sensor libs:
# technical documentation for Pysense-sensore in folder "IoT/pycom/documentation/"
from pysense import Pysense
# SI7006A20 - I2C Humidity & Temperature sensor
from SI7006A20 import SI7006A20
# MPL3115A2 - I2C Precision Altimeter
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
# general libs:
import time

# disable heartbeat-led
pycom.heartbeat(False)
pycom.rgbled(0x000000)

# print("Initialising sensors.")
# py = Pysense()
# si = SI7006A20(py)
# mp = MPL3115A2(py, mode = PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters
#
# pycom.rgbled(0x00ff00)
# time.sleep(5.00)
pycom.rgbled(0x000000)
time.sleep(2.00)
pycom.rgbled(0xff0000)

print("Initialising WiFi.")
wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()
# toon alle beschikbare netwerken:
for net in nets:
    print(net)

# verbinden met WLAN-PUB:
wlan.connect('onsVHifi', 'FF41A972T3')
#wlan.connect(ssid='onsVHifi')

# wait until the module has joined the network
i = 0
while not wlan.isconnected():
    pycom.rgbled(0xff0000)
    time.sleep(2.5)
    pycom.rgbled(0x000000)
    print("Attempt ", i, ". Not joined yet...")
    i = i + 1
    time.sleep(2.5)

print("WiFi network joined.")
print("network config:", wlan.ifconfig())
pycom.rgbled(0x00ff00)
time.sleep(5.00)
pycom.rgbled(0x000000)


# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
# make the socket non-blocking
s.setblocking(False)
#
pycom.rgbled(0x00ff00)
time.sleep(5.00)
pycom.rgbled(0x000000)
print("LoRa socket created. Ready to go!")

# while True:
#     # get temperasture and Humidity# SI7006A20-sensor: temperature & humidity reading, next (derived) dewpoint and some unknown 'Humidity Ambient':
#     print("New loop: reading Pysense sensors")
#     pycom.rgbled(0x0000ff)
#     temp = str(si.temperature())
#     humi = str(si.humidity())
#     # MPL3115A2-sensor: temperature & pressure reading, next pressure converted into altitude:
#     tmp2 = str(mp.temperature())
#     pres = str(mp.pressure())
#     mpp = MPL3115A2(py, mode = ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
#     alti = str(mpp.altitude())
#     pycom.rgbled(0x000000)
#
#     # definieer data-pakket
#     payload = 'Pysense over VHLoRa: room temperature = ' + temp + ', humidity = ' + humi + ', 2nd temperature = ' + tmp2 + ', pressure = ' + pres + ', altitude = ' + alti
#     print("payload: " + payload)
#     pkt = bytes(payload)
#
#     pycom.rgbled(0x00ff00)
#     print("sending:", pkt)
#     s.send(pkt)
#     time.sleep(4)
#     pycom.rgbled(0x000000)
#     rx, port = s.recvfrom(256)
#     if rx:
#         print('Received: {}, on port: {}'.format(rx, port))
#     time.sleep(16)
