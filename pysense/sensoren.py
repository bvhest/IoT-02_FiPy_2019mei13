# Based on the article "example application for LoPy device reading PySense sensor
#   data and sending this over LoRaWAN using Cayenne LPP encoding"
#
# source: https://forum.loraserver.io/t/pycom-lopy-pysense-cayenne-lpp-code-examples/692
# See https://docs.pycom.io for more information regarding library specifics
#
# BvH, 2019-05-10
#

import time
# controller/board specific stuff
import pycom
# technical documentation for Pysense-sensore in folder "IoT/pycom/documentation/"
from pysense import Pysense
from LIS2HH12 import LIS2HH12                       # LIS2HH12 - MEMS digital output motion sensor: ultra-low-power
                                                    #   high-performance 3-axis "pico" accelerometer
from SI7006A20 import SI7006A20                     # SI7006A20 - I2C Humidity & Temperature sensor
from LTR329ALS01 import LTR329ALS01                 # LTR-329ALS-01 - I2C Optical sensor
from MPL3115A2 import MPL3115A2, ALTITUDE, PRESSURE # MPL3115A2 - I2C Precision Altimeter1

class sensoren:
    """
    Represents the Pysense sensor-board.
    """
    def __init__(self, pin):
        """
        initialise board and sensors:
        """
        self.py = Pysense()              # initialise Pysense-board
        self.humTemp = SI7006A20(py)     # Humidity & Temperature sensor
        self.opt = LTR329ALS01(py)       # Optical sensor
        self.acc = LIS2HH12(py)          # 3-axis "pico" accelerometer
        self.mp = MPL3115A2(py, mode = PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters

    def set_HumTemp(self):
        print('\n\n** Humidity and Temperature Sensor (SI7006A20)')
        self.humi = si.humidity()
        self.temp = si.temperature()
        print('Humidity', self.humi)
        print('Temperature', self.temp)


    def set_Accelerometer(self):
        print('\n\n** 3-Axis Accelerometer (LIS2HH12)')
        self.acce = li.acceleration()
        self.roll = li.roll()
        self.ptch = li.pitch()
        print('Acceleration', self.acce)
        print('Roll', self.roll)
        print('Pitch', self.ptch)


    def set_Luminisity(self):
        print('\n\n** Digital Ambient Light Sensor (LTR-329ALS-01)')
        print('Light', lt.light())
        self.blue = lt.light()[0]
        self.red  = lt.light()[1]
        print('blue (lum)', self.blue)
        print('red (lum)', self.red)


    def set_TempPressureAlti(self):
        print('\n\n** Barometric Pressure Sensor with Altimeter (MPL3115A2)')
        self.mpPress = MPL3115A2(py,mode=PRESSURE)
        self.pres = mpPress.pressure()/100
        self.mpAlt = MPL3115A2(py,mode=ALTITUDE)
        self.alti = mpAlt.altitude()
        self.temp = mpAlt.temperature()
        print('Pressure (hPa)', self.pres)
        print('Altitude', self.alti)
        print('Temperature', self.temp)

    def get_HumTemp(self):
        return self.humi, self.temp

    def get_Accelerometer(self):
        return self.acce, self.roll, self.ptch

    def get_Luminisity(self):
        return self.blue, self.red

    def get_TempPressureAlti(self):
        return self.temp, self.pres, self.alti

    def return_measurements(self, lpp):
        lpp.add_relative_humidity(1, self.humi)
        lpp.add_temperature(1, self.temp)

        lpp.add_accelerometer(1, self.acce[0], self.acce[1], self.acce[2])
        lpp.add_gryrometer(1, self.roll, self.ptch, 0)

        lpp.add_luminosity(1, self.blue)
        lpp.add_luminosity(2, self.red)

        lpp.add_barometric_pressure(1, self.pres)
        lpp.add_gps(1, 0, 0, self.alti)
        lpp.add_temperature(2, self.temp)

        return lpp
