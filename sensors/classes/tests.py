#!/usr/bin/python

"""Test all sensors and databases

	Execution
		Called by main

	Return
		None
"""
__title__ = 'PiClima - Tests'
__author__ = 'Daniel Geraldi'
__license__ = 'MIT'

from classes.sensor_pressure_bmp import SensorPressure
from classes.sensor_humidity_dht import SensorHumidityDHT
from classes.sensor_humidity_aht import SensorHumidityAHT
from classes.heat_index import HeatIndex
from classes.log_file import LogFile

from decouple import config
from colorama import init, Fore, Style
 
class Tests:
    
    def __init__(self):
        self.printMessage = LogFile("tests")
        self.objHeatIndex = HeatIndex()   

        self.DHT = config('DHT_SENSOR', default='false')
        self.AHT = config('AHT_SENSOR', default='false')

    def displayPressure(self):
        """Test the Pressure sensor and only show all possible calculations"""
        
        self.printMessage.showMessage("*","Iniciating Pressure Sensor Test","")

        objSensorPressure = SensorPressure()
        objSensorPressure.getSensorData()

        print('Temp = {0:0.2f} C'.format(objSensorPressure.sensor.read_temperature()))
        print('Pressao Abs = {0:0.2f} hPa'.format(objSensorPressure.sensor.read_pressure()/100))
        print('Altitude = {0:0.2f} m'.format(objSensorPressure.sensor.read_altitude()))
        print('Altitude Real = {0:0.2f} m'.format(objSensorPressure.sensor.read_altitude()))
        print('Pressao Rel Altitude= {0:0.2f} hPa'.format(objSensorPressure.sensor.read_sealevel_pressure(float(objSensorPressure.sensor.read_altitude()))/100))
        print('Pressao Rel s/ Altitude= {0:0.2f} hPa'.format(objSensorPressure.sensor.read_sealevel_pressure()/100))
        print('Pressao Rel Altitude Calculado= {0:0.2f} hPa'.format(objSensorPressure.sensor.read_sealevel_pressure(objSensorPressure.sensor.read_altitude(101325))/100))
        print('Pressao Rel Altitude Manual= {0:0.2f} hPa'.format(objSensorPressure.sensor.read_sealevel_pressure(float(objSensorPressure.LOCAL_ALTITUDE))/100))

        self.printMessage.showMessage("!","Test Finished","")
        return

    def displayHumidity(self):
        """Test the Humidity sensor and only show the data from humidity and temperature if the sensor provides it"""
        
        #sensor_logger = LogFile("main")

        self.printMessage.showMessage("*","Iniciating Humidity Sensor Test","")
        
        if self.DHT:
            objSensorHumidity = SensorHumidityDHT()
        if self.AHT:
            objSensorHumidity = SensorHumidityAHT()
                
        humidity, hum_temperature = objSensorHumidity.getSensorData()

        heatIndex = self.objHeatIndex.calcHeatIndex(hum_temperature,humidity)

        print('Temp={0:0.1f}C HeatIndex={1:0.1f}C Humidity={2:0.1f}%'.format(hum_temperature,heatIndex, humidity))

        self.printMessage.showMessage("!","Test Finished","")
        
        #sensor_logger.log("info",f'Test of Humidity Sensor OK! Humidity:{"{0:0.2f}%".format(humidity)};Hum. Temp:{"{0:0.2f} C".format(hum_temperature)}')

        return