# https://pastebin.com/PLi30hcH

""" OTAA Node example compatible with the LoPy Nano Gateway """

# pycom libs:
import pycom
# network libs:
from network import LoRa
import socket
import binascii
import struct
# sensor libs:
# technical documentation for Pysense-sensore in folder "IoT/pycom/documentation/"
from pysense import Pysense
# SI7006A20 - I2C Humidity & Temperature sensor
from SI7006A20 import SI7006A20
# MPL3115A2 - I2C Precision Altimeter
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
# general libs:
import time

pycom.heartbeat(False)
pycom.rgbled(0x000000)
print("Initialising sensors.")

py = Pysense()
si = SI7006A20(py)
mp = MPL3115A2(py, mode = PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters

pycom.rgbled(0x00ff00)
time.sleep(5.00)
pycom.rgbled(0x000000)
time.sleep(2.00)
pycom.rgbled(0xff0000)

print("Initialising LoRa.")
# initialize LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# create an OTA authentication params (obv TheThingsNetwork account obv hestbv-user)
dev_eui = binascii.unhexlify('---')
app_eui = binascii.unhexlify('---')
app_key = binascii.unhexlify('---')

# set the 3 default channels to the same frequency (must be before sending the OTAA join request)
lora.add_channel(0, frequency=868100000, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=868100000, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=868100000, dr_min=0, dr_max=5)

# join a network using OTAA
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0, dr=5)

# wait until the module has joined the network
i = 0
while not lora.has_joined():
    pycom.rgbled(0xff0000)
    time.sleep(2.5)
    pycom.rgbled(0x000000)
    print("Attempt ", i, ". Not joined yet...")
    i = i + 1
    time.sleep(2.5)

print("LoRa network joined.")
pycom.rgbled(0x00ff00)
time.sleep(5.00)
pycom.rgbled(0x000000)
time.sleep(2.00)
pycom.rgbled(0xff0000)

# remove all the non-default channels
for i in range(3, 16):
    lora.remove_channel(i)

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

while True:
    # get temperature and humidity # SI7006A20-sensor: temperature & humidity reading, next (derived) dewpoint and some unknown 'Humidity Ambient':
    print("New loop: reading Pysense sensors")
    pycom.rgbled(0x0000ff)
    temp = str(si.temperature())
    humi = str(si.humidity())
    # MPL3115A2-sensor: temperature & pressure reading, next pressure converted into altitude:
    tmp2 = str(mp.temperature())
    pres = str(mp.pressure())
    mpp = MPL3115A2(py, mode = ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
    alti = str(mpp.altitude())
    pycom.rgbled(0x000000)

    # definieer data-pakket
    payload = 'Pysense over VHLoRa: room temperature = ' + temp + ', humidity = ' + humi + ', 2nd temperature = ' + tmp2 + ', pressure = ' + pres + ', altitude = ' + alti
    print("payload: " + payload)
#    print("convert payload to bytes")
#    pkt = bytes(payload)
#    print("payload converted to bytes")

    pycom.rgbled(0x00ff00)
#    print("sending:", pkt)
    print("sending")
    try:
        s.send(payload)
    except Exception as esc:
        print(esc)
        print('failure sending data by LoRa')

    print("send")
    time.sleep(4)
    pycom.rgbled(0x000000)
    print("testing recvfrom")
    rx, port = s.recvfrom(256)
    if rx:
        print('Received: {}, on port: {}'.format(rx, port))
    time.sleep(16)
