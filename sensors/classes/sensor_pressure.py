#!/usr/bin/python

"""Reads pressure sensor data using BPM180 sensor and raspberry py 3

	Reads BMP180 pressure sensor data using raspberry pi 3 
	using the Adafruit BMP085 library to get data of
	temperature and pressure

	Execution
		Called by main script
"""

__title__ = 'PiClima - Barometric'
__author__ = 'Daniel Geraldi'
__license__ = 'MIT'

#***************************************************
import datetime
import time
import logging
from logging.handlers import RotatingFileHandler
import sys
#import urllib.parse
import Adafruit_BMP.BMP085 as BMP085
from decouple import config

class SensorPressure:
	"""Pressure class that collect data from BMP180 sensor"""

	def __init__(self):
		"""Init all variables"""

		self.ts = time.time()
		self.dataHora = 0
		self.temp = 0
		self.pressao = 0
		self.pressao_rel = 0
		#self.altitude = 0

		#used to fix altitude
		self.LOCAL_ALTITUDE = config('LOCAL_ALTITUDE')

		#Create a new object sensor in ultra resolution
		#OPTIONS: BMP085_STANDARD, BMP085_HIGHRES,BMP085_ULTRAHIGHRES.
		self.sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)

		#Create rotating log files, alternating between 5 files when the file reaches 5MB
		logFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s(%(lineno)d) - %(message)s',"%d-%m-%Y %H:%M:%S")
		logFile = './log/sensor_temp.log'
		logHandler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                 backupCount=3, encoding=None, delay=0)
		logHandler.setFormatter(logFormatter)
		logHandler.setLevel(logging.INFO)

		self.logger = logging.getLogger('SENSOR_TEMP')
		self.logger.setLevel(logging.INFO)
		self.logger.addHandler(logHandler)


	#*********************************************************
	def getSensorData(self):
		""" Reads sensor data and save them into variables. """

		self.dataHora = datetime.datetime.fromtimestamp(self.ts).strftime('%d-%m-%Y %H:%M:%S') #Data e Hora
		self.temp = self.sensor.read_temperature() #Temperature
		self.pressao = self.sensor.read_pressure()/100 #Absolute Pressure
		#self.altitude = self.sensor.read_altitude()

		#Relative Pressure using fixed Altitude due the altitude identified by sensor vary according pressure
		#causing unreal altitude and sea level's pressure measurement
		self.pressao_rel = self.sensor.read_sealevel_pressure(float(self.LOCAL_ALTITUDE))/100

		return self.temp, self.pressao_rel, self.LOCAL_ALTITUDE, self.pressao