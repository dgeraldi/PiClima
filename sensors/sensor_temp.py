#!/usr/bin/python

"""Reads pressure sensor data using BPM180 sensor and raspberry py 3

	Reads BMP180 pressure sensor data using raspberry pi 3 
	and the Adafruit BMP085 library and save the data into databases,
	one local (mysql) and another in cloud (mongodb).

	The local database is used to have all data in a local network
	and as a backup in case of some internet failure.

	Execution
		Just run on terminal: 
	
		python3 sensor_temp.py

		Or create a schedule using crontab -e for that with the line inside:

		*/30 * * * * python3 ~/sensor_temp.py

	Args
		If any argument is passed in command line after the script name
		some extra data will be printed on terminal but without saving it
		it in databases.

		python3 sensor_temp.py SOME_ARG
"""

__title__ = 'PiClima'
__author__ = 'Daniel Geraldi'
__license__ = 'MIT'

#***************************************************
import datetime
import time
import logging
from logging.handlers import RotatingFileHandler
import sys
import MySQLdb as mysql
import pymongo
import urllib.parse
import Adafruit_BMP.BMP085 as BMP085
from decouple import config

class Sensor:
	"""Main class that collect all data and save into databases"""

	def __init__(self):
		"""Init all variables and get all environment variables"""

		self.SQLDBNAME = config('SQLDBNAME')
		self.SQLTABLENAME = config('SQLTABLENAME')
		self.SECRET_SQL = config('SECRET_SQL')
		self.USER_SQL = config('USER_SQL')
		self.SECRET_MONGO = config('SECRET_MONGO')
		self.USER_MONGO = config('USER_MONGO')
		self.LOCAL_ALTITUDE = config('LOCAL_ALTITUDE')

		self.ts = time.time()
		self.dataHora = 0
		self.temp = 0
		self.pressao = 0
		self.pressao_rel = 0
		self.altitude = 0

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


	#*********************************************************
	def saveDBSQL(self):
		""" Save in the local mysql server for backup and local access. 

		The strings used to connect to mysql server is located in the .env file.

			:USER_SQL: user created in mysql server to access database;
			:SECRET_SQL: password to connect to mysql server
			:SQLDBNAME: name of database created. 
	
			Default Database: tempodg
			DEFAULT Table: log_temperatura
		"""
		try:
			#Connect to the local database - MYSQL
			db = mysql.connect("localhost",self.USER_SQL,self.SECRET_SQL,self.SQLDBNAME)#host,user,password,database
			cursor = db.cursor()

			#Insert into DB
			sql = "Insert into "+ self.SQLTABLENAME +" (temperatura,pressao,altitude,pressao_abs) \
			VALUES ('%s','%s','%s','%s')" % \
			( self.temp, self.pressao_rel,self.LOCAL_ALTITUDE, self.pressao)

			cursor.execute(sql)
			db.commit()
			db.close()

			print("SUCCESS: Data sent to the local database!")
			self.logger.info("Data sent to the local database! Temp: %s;Rel Press:%s;Alt:%s ", self.temp, float("{0:0.2f}".format(self.pressao)),self.LOCAL_ALTITUDE)
		except mysql.Error as e:
			print("ERROR: was not possible to save data on LOCAL database:: ", e)
			self.logger.exception("Failure to save data on LOCAL database::")

			db.rollback()
			return False

	#*********************************************************
	def saveDBMongo(self):
		"""Save in the mongoDB (cloud), here were used the MongoDB Atlas.
	
		If the name of Database or Collection is changed from the default,
		this section needs to be updated.

			:USER_MONGO: user to connect to mongodb database.
			:SECRET_MONGO: password to connect to mongodb database.

			Default Table=weather_dg
			Default Collection=log_temperatura
		"""
		try:
			#Envia copia para banco mongodb em nuvem
			mongo_uri = "mongodb+srv://"+self.USER_MONGO+":"+ urllib.parse.quote_plus(self.SECRET_MONGO)+"@cluster0.tdpte.mongodb.net/weather_dg?retryWrites=true&w=majority"

			client = pymongo.MongoClient(mongo_uri,ssl=True,ssl_cert_reqs='CERT_NONE')
			#db = client.test

			#Seleciona o database
			db = client.weather_dg
			#Seleciona a collection
			collection = db.log_temperatura

			#Envia collection para MongoDB
			#Temp, pressao_rel,altitude,pressao
			document = {
				"datahora":self.dataHora,
				"temperatura":self.temp,
				"pressao":float("{0:0.2f}".format(self.pressao_rel)),
				"pressao_abs":float("{0:0.2f}".format(self.pressao)),
				"altitude": int(self.LOCAL_ALTITUDE)
				}

			#Insere documento um a um
			collection.insert_one(document)
			print("SUCCESS: Data sent to the cloud database.")
			self.logger.info("Data sent to the cloud database! Temp: %s;Rel Press:%s;Alt:%s ", self.temp, float("{0:0.2f}".format(self.pressao)),self.LOCAL_ALTITUDE)

		except Exception as e:
			print("ERROR: was not possible to save data on CLOUD database:: ",e)
			self.logger.exception("Failure to save data on CLOUD database::")

			return False


#*********************************************************
if __name__ == '__main__':
	"""Main function that calls everything."""

	#Create object and call functions
	objSensor = Sensor()
	if len(sys.argv)<2:
		objSensor.getSensorData()
		objSensor.saveDBSQL()
		objSensor.saveDBMongo()

	#If something is passed in arguments, show extra data without saving in database
	if len(sys.argv)>= 2:
		print('Temp = {0:0.2f} *C'.format(objSensor.sensor.read_temperature()))
		print('Pressao Abs = {0:0.2f} hPa'.format(objSensor.sensor.read_pressure()/100))
		print('Altitude = {0:0.2f} m'.format(objSensor.sensor.read_altitude()))
		print('Altitude Real = {0:0.2f} m'.format(objSensor.sensor.read_altitude()))
		print('Pressao Rel Altitude= {0:0.2f} hPa'.format(objSensor.sensor.read_sealevel_pressure(float(objSensor.sensor.read_altitude()))/100))
		print('Pressao Rel s/ Altitude= {0:0.2f} hPa'.format(objSensor.sensor.read_sealevel_pressure()/100))
		print('Pressao Rel Altitude Calculado= {0:0.2f} hPa'.format(objSensor.sensor.read_sealevel_pressure(objSensor.sensor.read_altitude(101325))/100))
		print('Pressao Rel Altitude Manual= {0:0.2f} hPa'.format(objSensor.sensor.read_sealevel_pressure(float(objSensor.LOCAL_ALTITUDE))/100))
