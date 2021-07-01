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

		python3 main.py SOME_ARG
"""

__title__ = 'PiClima - Main'
__author__ = 'Daniel Geraldi'
__license__ = 'MIT'

#***************************************************
import sys

#Import all classes
from classes.db import DB
from classes.sensor_pressure import SensorPressure

if __name__ == '__main__':
	"""Main function that calls everything."""
    
    #Create an object to call methods
objSensor = SensorPressure()

	#If it has no argument, populate variables and save them into databases
if len(sys.argv)<2:
		temp, pressao, LOCAL_ALTITUDE,pressao_rel = objSensor.getSensorData()
		saveDb = DB(temp,pressao_rel,LOCAL_ALTITUDE,pressao)
		saveDb.saveDBSQL()
		saveDb.saveDBMongo()

	#If something is passed in arguments, show extra data without saving in database
if len(sys.argv)>= 2:
        objSensor.getSensorData()
        print('Temp = {0:0.2f} *C'.format(objSensor.sensor.read_temperature()))
        print('Pressao Abs = {0:0.2f} hPa'.format(objSensor.sensor.read_pressure()/100))
        print('Altitude = {0:0.2f} m'.format(objSensor.sensor.read_altitude()))
        print('Altitude Real = {0:0.2f} m'.format(objSensor.sensor.read_altitude()))
        print('Pressao Rel Altitude= {0:0.2f} hPa'.format(objSensor.sensor.read_sealevel_pressure(float(objSensor.sensor.read_altitude()))/100))
        print('Pressao Rel s/ Altitude= {0:0.2f} hPa'.format(objSensor.sensor.read_sealevel_pressure()/100))
        print('Pressao Rel Altitude Calculado= {0:0.2f} hPa'.format(objSensor.sensor.read_sealevel_pressure(objSensor.sensor.read_altitude(101325))/100))
        print('Pressao Rel Altitude Manual= {0:0.2f} hPa'.format(objSensor.sensor.read_sealevel_pressure(float(objSensor.LOCAL_ALTITUDE))/100))
