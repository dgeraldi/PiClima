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

		python3 main.py [-p | --pressure] [-t | [--temperature | --humidity]]

            -p | --pressure                 : Only print the data from pressure sensor
            -t | --temperature | -- humidity: Only print the data from humidity sensor
"""

__title__ = 'PiClima - Main'
__author__ = 'Daniel Geraldi'
__license__ = 'MIT'

#***************************************************
import sys

#Import all classes
from classes.db import DB
from argparse import ArgumentParser, Namespace
from decouple import config


from classes.sensor_pressure_bmp import SensorPressure
from classes.sensor_humidity_dht import SensorHumidityDHT
from classes.sensor_humidity_aht import SensorHumidityAHT
from classes.heat_index import HeatIndex
from classes.tests import Tests
from classes.log_file import LogFile 


def main():
    """Main function that calls everything"""

    #Set which sensor exists
    PRESSURE = config('PRESSURE')
    HUMIDITY = config('HUMIDITY')

    #Identify which sensor will be called and set if will send the data to Cloud Database     
    DHT = config('DHT_SENSOR', default='false')
    AHT = config('AHT_SENSOR', default='false')
    SEND_TO_MONGO = config('SEND_TO_MONGO')

    #Create an object to call sensor tests
    tests = Tests();
    #Create a parser for arguments
    parser = ArgumentParser();

    parser.add_argument("-p","--pressure",
                            action="store_true",
                            help="Display data from PRESSURE/TEMPERATURE sensor but it doesn't store it in databases"
                            )
    parser.add_argument("-t","--temperature","--humidity",
                            action="store_true",
                            help="Display data from HUMIDITY/TEMPERATURE sensor but it doesn't store it in databases"
                            )

    args: Namespace = parser.parse_args()

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
                objHeatIndex = HeatIndex();
                heat_index = objHeatIndex.calcHeatIndex(hum_temperature,humidity)
            else:
                humidity, hum_temperature, heat_index = 0
                

            #Save in databases
            saveDb = DB(press_temperature,pressure_rel,LOCAL_ALTITUDE,pressure_abs,humidity,hum_temperature, heat_index)
            saveDb.saveDBSQL()

            if SEND_TO_MONGO == 'true':
                saveDb.saveDBMongo()

    #If something is passed in arguments, show extra data without saving in database
    if args.pressure:
        tests.displayPressure()
    if args.temperature:
        tests.displayHumidity()

if __name__ == '__main__':
    main()