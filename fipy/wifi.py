import machine
import time
from machine import Pin
from network import WLAN
import socket

wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()
# toon alle beschikbare netwerken:
#for net in nets:
#   print(net)

# verbinden met WLAN-PUB:
wlan.connect(ssid='WLAN-PUB')
while not wlan.isconnected():
   time.sleep(0.5)
   print('connecting...')

print('connected !')
# even wachten omdat verbinding toch niet meteen beschikbaar is...
time.sleep(5)
print('getting address of nu.nl')
# lees juiste waarde uit het tuple:
addr = socket.getaddrinfo('www.nu.nl', 80)[0][4][0]
# gebruik ',' om strings aan elkaar te plakken:
print('internet adres of www.nu.nl : ip = ', addr)

# verbinden met iPhone van instructeur:
# for net in nets:
#     if net.ssid == 'Daniel-iPhone':
#         wlan.connect(ssid=net.ssid, auth=(net.sec, '123456abc'))
#         while not wlan.isconnected():
#             time.sleep(1)
#             print('connecting...')
#         print('connected !')
#         print(socket.getaddrinfo('www.nu.nl', 80))
#         break
