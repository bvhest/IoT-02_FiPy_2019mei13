from network import LTE
import socket
import machine
import pycom
import time

# technical documentation for Pysense-sensore in folder "IoT/pycom/documentation/"
from pysense import Pysense
# SI7006A20 - I2C Humidity & Temperature sensor
from SI7006A20 import SI7006A20
# MPL3115A2 - I2C Precision Altimeter
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

time.sleep(5)

py = Pysense()
si = SI7006A20(py)
mp = MPL3115A2(py, mode = PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters

pycom.heartbeat(False)
pycom.rgbled(0xFF0000)
time.sleep(5.00)

# on-board battery voltage:
print("Battery voltage: " + str(py.read_battery_voltage()))

print("Setup Vodafone NB-IoT")
lte = LTE()
while not lte.isattached():
    lte.attach(band=20, apn="nb.inetd.gdsp")
    print("attaching...")
    time.sleep(0.50)
print("attached")

while not lte.isconnected():
    lte.connect()
    print("connecting...")
    time.sleep(0.50)
print("connected")

while True:
    # get temperasture and Humidity# SI7006A20-sensor: temperature & humidity reading, next (derived) dewpoint and some unknown 'Humidity Ambient':
    print("getting temperature & humidity")
    temp = str(si.temperature())
    humi = str(si.humidity())
    print("Temperature: " + temp + " deg C")
    print("Relative Humidity: " + humi + " %RH")

    # MPL3115A2-sensor: temperature & pressure reading, next pressure converted into altitude:
    tmp2 = str(mp.temperature())
    pres = str(mp.pressure())
    print("MPL3115A2 temperature: " + tmp2)
    print("Pressure: " + pres)
    mpp = MPL3115A2(py, mode = ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
    alti = str(mpp.altitude())
    print("Altitude: " + alti)

    # definieer data-pakket
    datapakketje = 'Ehvn (BaMa): room temperature = ' + temp + ', humidity = ' + humi + ', 2nd temperature = ' + tmp2 + ', pressure = ' + pres + ', altitude = ' + alti
    print(datapakketje)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("sending...")

    try:
        s.sendto(datapakketje, ('62.140.135.227', 5001))
    except Exception as esc:
        print(esc)
        print('failure sending data to Vodafone')

    print("send")

    pycom.rgbled(0x00FF00)
    time.sleep(0.5)
    pycom.rgbled(0x000000)
    time.sleep(19.5)

#print("Sent, going to sleep")
#machine.deepsleep(10000)
