#!/usr/bin/python

"""Reads pressure sensor data using BPM180 sensor and raspberry py 3

	Reads BMP180 pressure sensor data using raspberry pi 3 
	using the Adafruit BMP085 library to get data of
	temperature and pressure

	Execution
		Called by main script

	Return
		press_temperature, pressure_rel, LOCAL_ALTITUDE, pressure_abs
"""

__title__ = 'PiClima - Barometric'
__author__ = 'Daniel Geraldi'
__license__ = 'MIT'

#***************************************************
import datetime
import time
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys
#import urllib.parse
import Adafruit_BMP.BMP085 as BMP085
from decouple import config

class SensorPressure:
	"""Pressure class that collect data from BMP180 sensor"""

	def __init__(self):
		"""Init all variables"""

		self.ts = time.time()
		self.press_temperature = 0
		self.pressure_abs = 0
		self.pressure_rel = 0
		#self.altitude = 0

		#used to fix altitude
		self.LOCAL_ALTITUDE = config('LOCAL_ALTITUDE')

		#Create a new object sensor in ultra resolution
		#OPTIONS: BMP085_STANDARD, BMP085_HIGHRES,BMP085_ULTRAHIGHRES.
		self.sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)

		#Create rotating log files, alternating between 5 files when the file reaches 5MB
		logFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s(%(lineno)d) - %(message)s',"%d-%m-%Y %H:%M:%S")
		logFile = '/var/log/PiClima/sensor_pressure.log'
		logHandler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                 backupCount=3, encoding=None, delay=0)
		logHandler.setFormatter(logFormatter)
		logHandler.setLevel(logging.INFO)

		self.logger = logging.getLogger('SENSOR_PRESS')
		self.logger.setLevel(logging.INFO)
		self.logger.addHandler(logHandler)


	#*********************************************************
	def getSensorData(self):
		""" Reads sensor data and save them into variables. """

		#self.dataHora = datetime.datetime.fromtimestamp(self.ts).strftime('%d-%m-%Y %H:%M:%S') #Data e Hora
		self.press_temperature = self.sensor.read_temperature() #Temperature
		self.pressure_abs = self.sensor.read_pressure()/100 #Absolute Pressure
		#self.altitude = self.sensor.read_altitude()

		#Relative Pressure using fixed Altitude due the altitude identified by sensor vary according pressure
		#causing unreal altitude and sea level's pressure measurement
		self.pressure_rel = self.sensor.read_sealevel_pressure(float(self.LOCAL_ALTITUDE))/100

		return self.press_temperature, self.pressure_rel, self.LOCAL_ALTITUDE, self.pressure_abs