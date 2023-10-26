#!/usr/bin/python

"""Reads temperature and humidity sensor data using AHT10 sensor and raspberry py 3

	Reads AHT10 temperature and humidity sensor data using raspberry pi 3 
	using the direct reading on sensor using SMBUS to get data of
	temperature and humidity

	Execution
		Called by main script

	Return
		humidity, hum_temperature
"""

__title__ = 'PiClima - Humidity - AHT10'
__author__ = 'Daniel Geraldi'
__license__ = 'MIT'

#***************************************************
import time
import smbus
from classes.log_file import LogFile 
from decouple import config

class SensorHumidityAHT:
	"""Humidity and Temperature class that collect data from AHT10 sensor"""

	def __init__(self):
		"""Init all variables"""

		#initialize
		#self.ts = time.time()

		self.sensor_logger = LogFile(self.__class__.__name__)
								
		self.humidity = None
		self.hum_temperature = None
		
		self.bus = smbus.SMBus(1)

		#fixed I2C address to AHT10 sensor
		self.AHT10_ADDRESS = 0x38

		#Start and get first data from sensor to factory callibration
		config = [0x08, 0x00]
		self.bus.write_i2c_block_data(self.AHT10_ADDRESS, 0xE1, config)
		time.sleep(0.2)
		byt = self.bus.read_byte(self.AHT10_ADDRESS)


	#*********************************************************
	def getSensorData(self):
		""" Reads sensor data and save them into variables. """

		#Send command to sensor to read temperature and humidity raw data		
		self.bus.write_i2c_block_data(self.AHT10_ADDRESS, 0xAC, [0x33, 0x00])
		time.sleep(0.2)

		#Get raw data - 6 bits
		data = self.bus.read_i2c_block_data(self.AHT10_ADDRESS, 0x00, 6)
		#print(data)

		#Position 3-4-5 temperature, 1-2-3 Humidity
		raw_temperature = ((data[3] & 0x0F) << 16) + (data[4] << 8) + data[5]
		temperature = (raw_temperature / 1048576.0) * 200.0 - 50.0 #Celsius

		raw_humidity = (data[1] << 12) + (data[2] << 4) + ((data[3]) >> 4)
		humidity = (raw_humidity / 1048576.0) * 100.0

		#print(f'Temp: {temperature:.2f}°C')
		#print(f'Hum: {humidity:.2f}%')

		self.humidity = humidity
		self.hum_temperature = temperature
		
		if self.humidity is not None and self.hum_temperature is not None:
			#print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
			return self.humidity, self.hum_temperature
		else:
			#print('Failed to get reading. Try again!')
			self.sensor_logger.log("error","Failure to read sensor data")
			return false


#Not used yet but important addresses to save

#define AHT10_ADDRESS_0X38         0x38  //chip I2C address no.1 for AHT10/AHT15/AHT20, address pin connected to GND
#define AHT10_ADDRESS_0X39         0x39  //chip I2C address no.2 for AHT10 only, address pin connected to Vcc

#define AHT10_INIT_CMD             0xE1  //initialization command for AHT10/AHT15
#define AHT20_INIT_CMD             0xBE  //initialization command for AHT20
#define AHT10_START_MEASURMENT_CMD 0xAC  //start measurment command
#define AHT10_NORMAL_CMD           0xA8  //normal cycle mode command, no info in datasheet!!!
#define AHT10_SOFT_RESET_CMD       0xBA  //soft reset command

#define AHT10_INIT_NORMAL_MODE     0x00  //enable normal mode
#define AHT10_INIT_CYCLE_MODE      0x20  //enable cycle mode
#define AHT10_INIT_CMD_MODE        0x40  //enable command mode
#define AHT10_INIT_CAL_ENABLE      0x08  //load factory calibration coeff


#define AHT10_DATA_MEASURMENT_CMD  0x33  //no info in datasheet!!! my guess it is DAC resolution, saw someone send 0x00 instead
#define AHT10_DATA_NOP             0x00  //no info in datasheet!!!


#define AHT10_MEASURMENT_DELAY     80    //at least 75 milliseconds
#define AHT10_POWER_ON_DELAY       40    //at least 20..40 milliseconds
#define AHT10_CMD_DELAY            350   //at least 300 milliseconds, no info in datasheet!!!
#define AHT10_SOFT_RESET_DELAY     20    //less than 20 milliseconds

#define AHT10_FORCE_READ_DATA      true  //force to read data
#define AHT10_USE_READ_DATA        false //force to use data from previous read
#define AHT10_ERROR                0xFF  //returns 255, if communication error is occurred

#Referencia https://esphome.io/api/aht10_8cpp_source.html