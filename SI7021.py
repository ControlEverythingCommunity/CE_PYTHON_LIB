# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# SI7021
# This code is designed to work with the SI7021_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Humidity?sku=SI7021_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
SI7021_DEFAULT_ADDRESS			= 0x40

# SI7021 Command Set
SI7021_MEASRH_HOLD_CMD			= 0xE5
SI7021_MEASRH_NOHOLD_CMD		= 0xF5
SI7021_MEASTEMP_HOLD_CMD		= 0xE3
SI7021_MEASTEMP_NOHOLD_CMD		= 0xF3
SI7021_READPREVTEMP_CMD			= 0xE0
SI7021_RESET_CMD				= 0xFE
SI7021_WRITERHT_REG_CMD			= 0xE6
SI7021_READRHT_REG_CMD			= 0xE7
SI7021_WRITEHEATER_REG_CMD		= 0x51
SI7021_READHEATER_REG_CMD		= 0x11

class SI7021():
	def __init__(self):
		self.writehumidity()
		time.sleep(0.3)
		self.writetemperature()
	
	def writehumidity(self):
		"""Select the relative humidity command from the given provided values"""
		bus.write_byte(SI7021_DEFAULT_ADDRESS, SI7021_MEASRH_NOHOLD_CMD)
	
	def readhumidity(self):
		"""Read data back from the device address, 2 bytes, humidity MSB, humidity LSB"""
		data0 = bus.read_byte(SI7021_DEFAULT_ADDRESS)
		data1 = bus.read_byte(SI7021_DEFAULT_ADDRESS)
		
		# Convert the data
		humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6
		
		return {'h' : humidity}
	
	time.sleep(1)
	
	def writetemperature(self):
		"""Select the temperature command from the given provided values"""
		bus.write_byte(SI7021_DEFAULT_ADDRESS, SI7021_MEASTEMP_NOHOLD_CMD)
	
	def readtemperature(self):
		"""Read data back from the device address, 2 bytes, temperature MSB, temperature LSB"""
		data0 = bus.read_byte(SI7021_DEFAULT_ADDRESS)
		data1 = bus.read_byte(SI7021_DEFAULT_ADDRESS)
		
		# Convert the data
		cTemp = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85
		fTemp = cTemp * 1.8 + 32
		
		return {'c' : cTemp, 'f' : fTemp}

from SI7021 import SI7021
si7021 = SI7021()

while True:
	time.sleep(0.3)
	si7021.writehumidity()
	time.sleep(0.3)
	si7021.writetemperature()
	time.sleep(0.3)
	hum = si7021.readhumidity()
	print "Relative Humidity : %.2f %%"%(hum['h'])
	temp = si7021.readtemperature()
	print "Temperature in Celsius : %.2f C"%(temp['c'])
	print "Temperature in Fahrenheit : %.2f F"%(temp['f'])
	print " ************************************* "
