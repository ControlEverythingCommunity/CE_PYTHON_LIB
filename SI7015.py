# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# SI7015
# This code is designed to work with the SI7015_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Temperature?sku=SI7015_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
SI7015_DEFAULT_ADDRESS			= 0x40

# SI7015 Register Set
SI7015_REG_STATUS				= 0x00 # Status Register
SI7015_REG_DATAH				= 0x01 # Relative Humidity or Temperature, High Byte
SI7015_REG_DATAL				= 0x02 # Relative Humidity or Temperature, Low Byte
SI7015_REG_CONFIG				= 0x03 # Configuration Register
SI7015_REG_ID					= 0x11 # ID Register

# SI7015 Configuration Register
SI7015_REG_CONFIG_FS_			= 0x20 # Fast Mode Enable, 2.6ms
SI7015_REG_CONFIG_TEMP			= 0x10 # Temperature Enable
SI7015_REG_CONFIG_HEATER_OFF	= 0x02 # Heater ON
SI7015_REG_CONFIG_CNVRSN_ON		= 0x01 # Start A Conversion
SI7015_REG_CONFIG_DEFAULT		= 0x00 # Relative Humidity Enable, Heater OFF

class SI7015():
	def __init__(self):
		self.writetemperature()
		self.writehumidity()
	
	def writetemperature(self):
		"""Select the temperature configuration from the given provided values"""
		TEMP_CONFIG = (SI7015_REG_CONFIG_CNVRSN_ON | SI7015_REG_CONFIG_TEMP)
		bus.write_byte_data(SI7015_DEFAULT_ADDRESS, SI7015_REG_CONFIG, TEMP_CONFIG)
	
	def readtemperature(self, cTemp):
		"""Read data back from SI7015_REG_STATUS(0x00), 3 bytes, Status register, ctemp MSB, ctemp LSB"""
		data = bus.read_byte_data(SI7015_DEFAULT_ADDRESS, SI7015_REG_STATUS)
		while (data & 0x01) != 0 :
			data = bus.read_byte_data(SI7015_DEFAULT_ADDRESS, SI7015_REG_STATUS)
		data1 = bus.read_byte_data(SI7015_DEFAULT_ADDRESS, SI7015_REG_DATAH)
		data2 = bus.read_byte_data(SI7015_DEFAULT_ADDRESS, SI7015_REG_DATAH)
		
		# Convert the data to 14-bits
		cTemp = (((data1 * 256.0) + data2) / 4.0)
		
		if cTemp < 0x0140 :
			cTemp = 0x0140
		elif cTemp > 0x12C0 :
			cTemp = 0x12C0
		else :
			cTemp = cTemp
		
		cTemp = (cTemp / 32.0) - 50.0
		fTemp = cTemp * 1.8 + 32
		
		return {'c' : cTemp, 'f' : fTemp}
	
	def writehumidity(self):
		"""Select the relative humidity configuration from the given provided values"""
		HUMIDITY_CONFIG = (SI7015_REG_CONFIG_CNVRSN_ON | SI7015_REG_CONFIG_DEFAULT)
		bus.write_byte_data(SI7015_DEFAULT_ADDRESS, SI7015_REG_CONFIG, HUMIDITY_CONFIG)
	
	def readhumidity(self, cTemp):
		"""Read data back from SI7015_REG_STATUS(0x00), 3 bytes, Status register, humidity MSB, humidity LSB"""
		data = bus.read_byte_data(SI7015_DEFAULT_ADDRESS, SI7015_REG_STATUS)
		while (data & 0x01) != 0 :
			data = bus.read_byte_data(SI7015_DEFAULT_ADDRESS, SI7015_REG_STATUS)
		data1 = bus.read_byte_data(SI7015_DEFAULT_ADDRESS, SI7015_REG_DATAH)
		data2 = bus.read_byte_data(SI7015_DEFAULT_ADDRESS, SI7015_REG_DATAH)
		
		# Convert the data to 12-bits
		humidity = ((data1 * 256 + (data2 & 0xF0)) / 16.0)
		
		if humidity < 0x180 :
			humidity = 0x180
		elif humidity > 0x7C0 :
			humidity = 0x7C0
		else :
			humidity = humidity
		
		humidity =  (humidity / 16.0) - 24.0
		linearhumidity = humidity - (((humidity * humidity) * (-0.00393)) + (humidity * 0.4008) - 4.7844)
		tempcomphumidity = linearhumidity + ((cTemp - 30.00) * (linearhumidity * 0.00237 + 0.1973))
		
		return {'h' : humidity, 'l' : linearhumidity, 't' : tempcomphumidity}

from SI7015 import SI7015
si7015 = SI7015()

while True:
	si7015.writehumidity()
	time.sleep(0.1)
	hum = si7015.readhumidity(2)
	print "Relative Humidity : %.2f %%"%(hum['h'])
	print "Linear Relative Humidity : %.2f %%"%(hum['l'])
	print "Temperature Compensated Relative Humidity : %.2f %%"%(hum['t'])
	si7015.writetemperature()
	time.sleep(0.1)
	temp = si7015.readtemperature(2)
	print "Temperature in Celsius : %.2f C"%(temp['c'])
	print "Temperature in Fahrenheit : %.2f F"%(temp['f'])
	print " ************************************* "
	time.sleep(1)
