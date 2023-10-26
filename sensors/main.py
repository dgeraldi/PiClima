#!/usr/bin/python

"""Call all sensors classes and save the data into databases

	Reads all sensors using raspberry pi 3 and save 
    the data into databases, one local (mysql) and 
    another in cloud (mongodb).

	The local database is used to have all data in a local network
	as a backup in case of some internet failure.

	Execution
		Just run manually on terminal: 
	
		python3 main.py

		Or create a schedule running the command line 'crontab -e' with the line inside:

		*/30 * * * * python3 ~/PiClima/main.py

	Args
		If any argument is passed in command line after the script name
		some extra data will be printed on terminal but without saving it
		it in databases.

		python3 main.py [humidity | pressure]
"""

__title__ = 'PiClima - Main'
__author__ = 'Daniel Geraldi'
__license__ = 'MIT'

#***************************************************
import sys

#Import all classes
from classes.db import DB
from classes.sensor_pressure_bmp import SensorPressure
from classes.sensor_humidity_dht import SensorHumidityDHT
from classes.sensor_humidity_aht import SensorHumidityAHT
from classes.log_file import LogFile 
from decouple import config


if __name__ == '__main__':
	"""Main function that calls everything."""
        
#Identify which sensor will be called       
PRESSURE = config('PRESSURE')
HUMIDITY = config('HUMIDITY')
SEND_TO_MONGO = config('SEND_TO_MONGO')
DHT = config('DHT_SENSOR', default='false')
AHT = config('AHT_SENSOR', default='false')

sensor_logger = LogFile("main")

	#If it has no argument, populate variables and save them into databases
if len(sys.argv)<2:
        
        #Create an object to call methods
        if PRESSURE == 'true':
            objSensorPressure = SensorPressure()
            #Class sensor_presssure
            press_temperature, pressure_rel, LOCAL_ALTITUDE, pressure_abs = objSensorPressure.getSensorData()
        else:
            press_temperature, pressure_rel, LOCAL_ALTITUDE, pressure_abs = 0

        if HUMIDITY == 'true':
            if DHT:
                objSensorHumidity = SensorHumidityDHT()
            if AHT:
                objSensorHumidity = SensorHumidityAHT()

            #Class sensor_humidity
            humidity, hum_temperature = objSensorHumidity.getSensorData()
        else:
            humidity, hum_temperature = 0

        #Save in databases
        saveDb = DB(press_temperature,pressure_rel,LOCAL_ALTITUDE,pressure_abs,humidity,hum_temperature)
        saveDb.saveDBSQL()

        if SEND_TO_MONGO == 'true':
            saveDb.saveDBMongo()

	#If something is passed in arguments, show extra data without saving in database
if len(sys.argv) == 2:

    if sys.argv[1] == 'pressure':

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

    if sys.argv[1]=='humidity':
        if DHT:
            objSensorHumidity = SensorHumidityDHT()
        if AHT:
            objSensorHumidity = SensorHumidityAHT()
        humidity, hum_temperature = objSensorHumidity.getSensorData()
        print('Temp={0:0.1f}C  Humidity={1:0.1f}%'.format(hum_temperature, humidity))
        sensor_logger.log("info",f'Test of Humidity Sensor OK! Humidity:{"{0:0.2f}%".format(humidity)};Hum. Temp:{"{0:0.2f} C".format(hum_temperature)}')

    if sys.argv[1] == 'test':

        if PRESSURE == 'true': 
            objSensorPressure = SensorPressure()
            objSensorPressure.getSensorData()

            print('Temp = {0:0.2f}C'.format(objSensorPressure.sensor.read_temperature()))
            print('Pressao Abs = {0:0.2f} hPa'.format(objSensorPressure.sensor.read_pressure()/100))
            print('Altitude = {0:0.2f} m'.format(objSensorPressure.sensor.read_altitude()))
            print('Altitude Real = {0:0.2f} m'.format(objSensorPressure.sensor.read_altitude()))
            print('Pressao Rel Altitude= {0:0.2f} hPa'.format(objSensorPressure.sensor.read_sealevel_pressure(float(objSensorPressure.sensor.read_altitude()))/100))
            print('Pressao Rel s/ Altitude= {0:0.2f} hPa'.format(objSensorPressure.sensor.read_sealevel_pressure()/100))
            print('Pressao Rel Altitude Calculado= {0:0.2f} hPa'.format(objSensorPressure.sensor.read_sealevel_pressure(objSensorPressure.sensor.read_altitude(101325))/100))
            print('Pressao Rel Altitude Manual= {0:0.2f} hPa'.format(objSensorPressure.sensor.read_sealevel_pressure(float(objSensorPressure.LOCAL_ALTITUDE))/100))
        else:
            sensor_logger.log("error",'TEST ::Pressure Sensor not set to ACTIVE in env file')
            print('Pressure Sensor not set to ACTIVE in env file')

        if HUMIDITY == 'true':
            if DHT:
                objSensorHumidity = SensorHumidityDHT()
            if AHT:
                 objSensorHumidity = SensorHumidityAHT()
            
            humidity, hum_temperature = objSensorHumidity.getSensorData()
            print('Temp={0:0.1f}C  Humidity={1:0.1f}%'.format(hum_temperature, humidity))
        else:
            sensor_logger.log("error",'TEST :: Humidity Sensor not set to ACTIVE in env file')
            print('Humidity Sensor not set to ACTIVE in env file')

if len(sys.argv)>2:
    print('Usage 1 - will save into databases: python main.py')
    print('Usage 2 - will only show the data: python main.py [humidity | pressure]')
