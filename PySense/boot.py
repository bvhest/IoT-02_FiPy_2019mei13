import time                   # Allows use of time.sleep() for delays
import pycom                  # Base library for Pycom devices

# RGBLED:
# Disable the on-board heartbeat (blue flash every 4 seconds).
# We'll use the LED to show the connectivity.
pycom.heartbeat(False)
time.sleep(0.1) # Workaround for a bug.
                # Above line is not actioned if another
                # process occurs immediately afterwards
pycom.rgbled(0xff0000)  # Status red = no (WLAN-)connection


