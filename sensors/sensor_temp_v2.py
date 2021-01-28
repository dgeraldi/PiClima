#!/usr/bin/python

#*******************************************
# Read sensor data using raspberry pi 3 and
# save into databases, one local and cloud
# License: MIT
# Author: Daniel Geraldi
#*******************************************
import datetime
import time
import logging
import sys
import MySQLdb as mysql
import pymongo
import urllib.parse
import Adafruit_BMP.BMP085 as BMP085
from decouple import config

class Sensor:
	def __init__(self):
		self.SECRET_SQL = config('SECRET_SQL')
		self.USER_SQL = config('USER_SQL')
		self.SECRET_MONGO = config('SECRET_MONGO')
		self.USER_MONGO = config('USER_MONGO')
		self.ts = time.time()#Hora atual
		self.dataHora = 0
		self.temp = 0
		self.pressao = 0
		self.pressao_rel = 0
		self.altitude = 0

		#Create a new object sensor in ultra resolution
		#BMP085_STANDARD, BMP085_HIGHRES,BMP085_ULTRAHIGHRES.
		self.sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)

	#**************************************
	# Get sensor data and save in variables
	#**************************************
	def getSensorData(self):
		self.dataHora = datetime.datetime.fromtimestamp(self.ts).strftime('%d-%m-%Y %H:%M:%S') #Data e Hora
		self.temp = self.sensor.read_temperature() #Temperatura
		self.pressao = self.sensor.read_pressure()/100 #Pressao Absoluta
		self.altitude = self.sensor.read_altitude()
		self.pressao_rel = self.sensor.read_sealevel_pressure(self.altitude)/100 #Pressao Relativa calibrado para altitude local aprox 760 metros

	#**************************************
	# Save in the local mysql server(backup)
	#**************************************
	def saveDBSQL(self):
		#Conecta banco de dados local
		db = mysql.connect("localhost",self.USER_SQL,self.SECRET_SQL,"tempodg")#host,user,password,database
		cursor = db.cursor()

		try:
			#Insere dados no BD
			sql = "Insert into log_temperatura (temperatura,pressao,altitude,pressao_abs) \
			VALUES ('%s','%s','%s','%s')" % \
			( self.temp, self.pressao_rel, self.altitude, self.pressao)

			cursor.execute(sql)
			db.commit()
			db.close()
			print("Enviado para o banco local com sucesso!")
		except mysql.Error as e:
			print("ERRO: impossivel gravar no banco local:: ", e)
			db.rollback()
			return False
			#logger.error(e)
	#**************************************
	# Save in the mongoDB (cloud)
	#**************************************
	def saveDBMongo(self):
		#Envia copia para banco mongodb em nuvem
		mongo_uri = "mongodb+srv://"+self.USER_MONGO+":"+ urllib.parse.quote_plus(self.SECRET_MONGO)+"@cluster0.tdpte.mongodb.net/weather_dg?retryWrites=true&w=majority"

		try:
			client = pymongo.MongoClient(mongo_uri,ssl=True,ssl_cert_reqs='CERT_NONE')
			#db = client.test
			print("Conectado com sucesso ao banco na cloud!")

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
				"altitude": float("{0:0.2f}".format(self.altitude))
				}
			#Insere documento um a um
			collection.insert_one(document)
			print("Dados enviados com sucesso para nuvem!")
		except Exception as e:
			print("ERRO: Não foi possível conectar ao MongoDB:: ",e)
			return False

	"""
	def errorLog(self):
		#Gera arquivo de log
		logging.basicConfig(filename='./bmp180_error.log',
			format='%(asctime)s %(levelname)s %(name)s %(message)s')
		logger=logging.getLogger(__name__)
		"""
#**************************************
# Main
#**************************************
if __name__ == '__main__':
	#Create object and call functions
	objSensor = Sensor()
	objSensor.getSensorData()
	objSensor.saveDBSQL()
	objSensor.saveDBMongo()

	#if something is passed in arguments, run some extra data without saving in database
	if len(sys.argv)>= 2:
		print('Temp = {0:0.2f} *C'.format(objSensor.sensor.read_temperature()))
		print('Pressao Abs = {0:0.2f} hPa'.format(objSensor.sensor.read_pressure()/100))
		print('Altitude = {0:0.2f} m'.format(objSensor.sensor.read_altitude()))
		print('Altitude Real = {0:0.2f} m'.format(objSensor.sensor.read_altitude(101325)))
		print('Pressao Rel Altitude= {0:0.2f} hPa'.format(objSensor.sensor.read_sealevel_pressure(objSensor.sensor.read_altitude())/100))
		print('Pressao Rel s/ Altitude= {0:0.2f} hPa'.format(objSensor.sensor.read_sealevel_pressure()/100))
		print('Pressao Rel Altitude Calculado= {0:0.2f} hPa'.format(objSensor.sensor.read_sealevel_pressure(objSensor.sensor.read_altitude(101325))/100))
		print('Pressao Rel Altitude Manual= {0:0.2f} hPa'.format(objSensor.sensor.read_sealevel_pressure(780)/100))
