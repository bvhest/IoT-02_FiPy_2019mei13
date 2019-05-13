import time
import pycom

pycom.heartbeat(False)

r = 0
g = 0
b = 0
pycom.rgbled(0)

while True:
	if r<255:
		r = r + 1
	elif g<255:
		g = g + 1
	elif b<255:
		b = b + 1
	else:
		break
	pycom.rgbled((r<<16)+(g<<8)+b)
	time.sleep(0.01)

pycom.rgbled(0)
