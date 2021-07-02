#!/usr/bin/python

"""Reads temperature and humidity sensor data using DHT11 sensor and raspberry py 3

	Reads DHT11 temperature and humidity sensor data using raspberry pi 3 
	using the Adafruit DHT11 library to get data of
	temperature and humidity

	Execution
		Called by main script

	Return
		humidity, hum_temperature
"""

__title__ = 'PiClima - Humidity'
__author__ = 'Daniel Geraldi'
__license__ = 'MIT'

#***************************************************
import datetime
import time
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys
import Adafruit_DHT as DHT11

class SensorHumidity:
	"""Humidity and Temperature class that collect data from DHT11 sensor"""

	def __init__(self):
		"""Init all variables"""

		#initialize
		self.ts = time.time()
		self.humidity = None
		self.hum_temperature = None

		#Change the correct pin connected on raspberry py
		self.pin = 24

		#Create a new object sensor
		self.sensor = DHT11.DHT11

		#Create rotating log files, alternating between 5 files when the file reaches 5MB
		logFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s(%(lineno)d) - %(message)s',"%d-%m-%Y %H:%M:%S")
		logFile = '/var/log/PiClima/sensor_humidity.log'
		logHandler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                 backupCount=3, encoding=None, delay=0)
		logHandler.setFormatter(logFormatter)
		logHandler.setLevel(logging.INFO)

		self.logger = logging.getLogger('SENSOR_HUM')
		self.logger.setLevel(logging.INFO)
		self.logger.addHandler(logHandler)


	#*********************************************************
	def getSensorData(self):
		""" Reads sensor data and save them into variables. """

		# Try to grab a sensor reading.  Use the read_retry method which will retry up
		# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
		self.humidity, self.hum_temperature = DHT11.read_retry(self.sensor, self.pin)

		#Un-comment the line below to convert the temperature to Fahrenheit.
		# temperature = temperature * 9/5.0 + 32

		# Note that sometimes you won't get a reading and
		# the results will be null (because Linux can't
		# guarantee the timing of calls to read the sensor).
		# If this happens try again!
		if self.humidity is not None and self.hum_temperature is not None:
			#print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
			return self.humidity, self.hum_temperature
		else:
			#print('Failed to get reading. Try again!')
			self.logger.exception("Failure to read sensor data")
			return false


		