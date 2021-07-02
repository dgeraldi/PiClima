#!/usr/bin/python

"""Save data into a local and cloud database

	Receive the sensors data and save them into databases,
	one local (mysql) and another in cloud (mongodb).

	The local database is used to have all data in a local network
	and as a backup in case of some internet failure.

	Execution
		Called by main script

	Args
		All sensors data existent
        
        From BMP180:
        Temperature, relativePressure,localAltitude,absolutePressure
"""

__title__ = 'PiClima - Databases'
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
from decouple import config

class DB:
	"""Main class that collect all data and save into databases"""

	def __init__(self,press_temperature,relativePressure,localAltitude,absolutePressure, humidity, hum_temperature):
		"""Init all variables and get all environment variables"""

		self.SQLDBNAME = config('SQLDBNAME')
		self.SQLTABLENAME = config('SQLTABLENAME')
		self.SECRET_SQL = config('SECRET_SQL')
		self.USER_SQL = config('USER_SQL')
		self.SECRET_MONGO = config('SECRET_MONGO')
		self.USER_MONGO = config('USER_MONGO')

		self.ts = time.time()
		self.created = 0

		self.press_temperature = press_temperature
		self.pressure_rel = relativePressure
		self.localAltitude = localAltitude
		self.pressure_abs = absolutePressure
		self.humidity = humidity
		self.hum_temperature = hum_temperature

		
		#Create rotating log files, alternating between 5 files when the file reaches 5MB
		logFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s(%(lineno)d) - %(message)s',"%d-%m-%Y %H:%M:%S")
		logFile = '/var/log/PiClima/db.log'
		logHandler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                 backupCount=3, encoding=None, delay=0)
		logHandler.setFormatter(logFormatter)
		logHandler.setLevel(logging.INFO)

		self.logger = logging.getLogger('DB')
		self.logger.setLevel(logging.INFO)
		self.logger.addHandler(logHandler)

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
			sql = "Insert into "+ self.SQLTABLENAME +" (press_temperature,pressure,altitude,pressure_abs, humidity, hum_temperature) \
			VALUES ('%s','%s','%s','%s','%s','%s')" % \
			( self.press_temperature, self.pressure_rel, self.localAltitude, self.pressure_abs, self.humidity, self.hum_temperature)

			cursor.execute(sql)
			db.commit()
			db.close()

			#print("SUCCESS: Data sent to the local database.")
			self.logger.info("Data sent to the local database! Temp: %s;Rel Press:%s;Alt:%s;Humidity:%s;Hum. Temp:%s", self.press_temperature, float("{0:0.2f}".format(self.pressure_rel)),self.localAltitude,self.humidity,self.hum_temperature)
		except mysql.Error as e:
			#print("ERROR: was not possible to save data on LOCAL database:: ", e)
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

			self.created = datetime.datetime.fromtimestamp(self.ts).strftime('%d-%m-%Y %H:%M:%S') #Date and time
			#db = client.test

			#Select o database
			db = client.weather_dg

			#Select a collection
			collection = db.log_temperatura

			#Send collection para MongoDB
			document = {
				"created":self.created,
				"press_temperature":self.press_temperature,
				"pressure":float("{0:0.2f}".format(self.pressure_rel)),
				"pressure_abs":float("{0:0.2f}".format(self.pressure_abs)),
				"altitude": int(self.localAltitude),
				"humidity": self.humidity,
				"hum_temperature":self.hum_temperature
				}

			#Insere documento um a um
			collection.insert_one(document)
			#print("SUCCESS: Data sent to the cloud database.")
			self.logger.info("Data sent to the cloud database! Temp: %s;Rel Press:%s;Alt:%s;Humidity:%s;Hum. Temp:%s", self.press_temperature, float("{0:0.2f}".format(self.pressure_rel)),self.localAltitude,self.humidity,self.hum_temperature)
		except Exception as e:
			#print("ERROR: was not possible to save data on CLOUD database:: ",e)
			self.logger.exception("Failure to save data on CLOUD database::")

			return False