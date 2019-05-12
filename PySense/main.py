# Based on the article "example application for LoPy device reading PySense sensor
#   data and sending this over LoRaWAN using Cayenne LPP encoding"
#
# source: https://forum.loraserver.io/t/pycom-lopy-pysense-cayenne-lpp-code-examples/692
# See https://docs.pycom.io for more information regarding library specifics
#
# BvH, 2019-05-10
#

import time
import socket
import binascii
# network-stuff
from network import LoRa
from CayenneLPP import CayenneLPP
# controller/board specific stuff
import pycom
# technical documentation for Pysense-sensore in folder "IoT/pycom/documentation/"
from pysense import Pysense
from LIS2HH12 import LIS2HH12                       # LIS2HH12 - MEMS digital output motion sensor: ultra-low-power
                                                    #   high-performance 3-axis "pico" accelerometer
from SI7006A20 import SI7006A20                     # SI7006A20 - I2C Humidity & Temperature sensor
from LTR329ALS01 import LTR329ALS01                 # LTR-329ALS-01 - I2C Optical sensor
from MPL3115A2 import MPL3115A2, ALTITUDE, PRESSURE # MPL3115A2 - I2C Precision Altimeter1

# initialise board and sensors:
py = Pysense()              # initialise Pysense-board
humTemp = SI7006A20(py)     # Humidity & Temperature sensor
opt = LTR329ALS01(py)       # Optical sensor
acc = LIS2HH12(py)          # 3-axis "pico" accelerometer
mp = MPL3115A2(py, mode = PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters


def init_LoRa():
    # Initialize LoRa in LORAWAN mode.
    lora = LoRa(mode=LoRa.LORAWAN)

    # create an OTAA authentication parameters
    app_eui = binascii.unhexlify('0101010101010101')
    app_key = binascii.unhexlify('11B0282A189B75B0B4D2D8C7FA38548B')

    print("DevEUI: %s" % (binascii.hexlify(lora.mac())))
    print("AppEUI: %s" % (binascii.hexlify(app_eui)))
    print("AppKey: %s" % (binascii.hexlify(app_key)))

    # join a network using OTAA (Over the Air Activation)
    lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

    # wait until the module has joined the network
    while not lora.has_joined():
        pycom.rgbled(0x140000)
        time.sleep(2.5)
        pycom.rgbled(0x000000)
        time.sleep(1.0)
        print('Not yet joined...')

    print('OTAA joined')
    pycom.rgbled(0x001400)

    # create a LoRa socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

    # set the LoRaWAN data rate
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)


def send_LoRa():
    print('Sending data (uplink)...')
    s.setblocking(True)
    pycom.rgbled(0x000014)
    lpp = CayenneLPP()

    now = rtc.now()
    lpp.add_time(1, "%d-%02d-%02d %02d:%02d:%02d GMT" % (now[0], now[1], now[2], now[3], now[4], now[5]))

    s.send(bytes(lpp.get_buffer()))
    s.setblocking(False)
    data = s.recv(64)
    print('Received data (downlink)', data)
    pycom.rgbled(0x001400)


def get_HumTemp():
    print('\n\n** Humidity and Temperature Sensor (SI7006A20)')
    humi = si.humidity()
    temp = si.temperature()
    lpp.add_relative_humidity(1, humi)
    lpp.add_temperature(1, temp)
    print('Humidity', humi)
    print('Temperature', temp)


def get_Accelerometer():
    print('\n\n** 3-Axis Accelerometer (LIS2HH12)')
    acce = li.acceleration()
    roll = li.roll()
    pitc = li.pitch()
    lpp.add_accelerometer(1, li.acceleration()[0], li.acceleration()[1], li.acceleration()[2])
    lpp.add_gryrometer(1, li.roll(), li.pitch(), 0)
    print('Acceleration', acce)
    print('Roll', roll)
    print('Pitch', pitc)


def get_Luminisity():
    print('\n\n** Digital Ambient Light Sensor (LTR-329ALS-01)')
    print('Light', lt.light())
    blue = lt.light()[0]
    red  = lt.light()[1]
    lpp.add_luminosity(1, blue)
    lpp.add_luminosity(2, red)


def get_TempPressure():
    print('\n\n** Barometric Pressure Sensor with Altimeter (MPL3115A2)')
    mpPress = MPL3115A2(py,mode=PRESSURE)
    pres = mpPress.pressure()/100
    mpAlt = MPL3115A2(py,mode=ALTITUDE)
    alti = mpAlt.altitude()
    temp = mpAlt.temperature()
    lpp.add_barometric_pressure(1, pres)
    lpp.add_gps(1, 0, 0, alti)
    lpp.add_temperature(2, temp)
    print('Pressure (hPa)', pres)
    print('Altitude', alti)
    print('Temperature', temp)


while True:
    send_LoRa()
    #
    time.sleep(30)
