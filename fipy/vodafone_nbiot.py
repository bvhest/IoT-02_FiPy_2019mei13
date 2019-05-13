from network import LTE
import socket
import machine
import pycom
import time

# technical documentation for Pysense-sensore in folder "IoT/pycom/documentation/"
from pysense import Pysense
# SI7006A20 - I2C Humidity & Temperature sensor
from SI7006A20 import SI7006A20

py = Pysense()
si = SI7006A20(py)

pycom.heartbeat(False)
pycom.rgbled(0xFF0000)
time.sleep(2.00)

lte = LTE()
lte.attach(band=20, apn="nb.inetd.gdsp")
while not lte.isattached():
    print("attaching...")
    time.sleep(0.50)
print("attached")

lte.connect()
while not lte.isconnected():
    print("connecting...")
    time.sleep(0.50)
print("connected")

# get temperasture and Humidity# SI7006A20-sensor: temperature & humidity reading, next (derived) dewpoint and some unknown 'Humidity Ambient':
temp = str(si.temperature())
humi = str(si.humidity())
print("Temperature: " + temp + " deg C")
print("Relative Humidity: " + humi + " %RH")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("sending...")
s.sendto('Vodafone Pycom Fipy NB-IoT test. BaMa: room temperature = ' + temp + ', humidity = ' + humi, ('62.140.135.227', 5001))
print("send")

pycom.rgbled(0x00FF00)
time.sleep(2.00)
pycom.rgbled(0x000000)

print("Sent, going to sleep")
machine.deepsleep(10000)
