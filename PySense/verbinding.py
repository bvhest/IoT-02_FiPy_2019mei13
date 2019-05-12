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


init_LoRa()
while True:
    send_LoRa()
    #
    time.sleep(30)
