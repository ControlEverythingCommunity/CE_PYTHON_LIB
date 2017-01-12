# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# SI7050
# This code is designed to work with the SI7050_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Temperature?sku=SI7050_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
SI7050_DEFAULT_ADDRESS			= 0x40

# SI7050 Command Set
SI7050_MEASTEMP_HOLD_CMD		= 0xE3
SI7050_MEASTEMP_NOHOLD_CMD		= 0xF3
SI7050_RESET_CMD				= 0xFE
SI7050_WRITERHT_REG_CMD			= 0xE6
SI7050_READRHT_REG_CMD			= 0xE7

class SI7050():
	def __init__(self):
		self.writetemperature()
		time.sleep(0.3)
		
	
	def writetemperature(self):
		"""Select the temperature command from the given provided values"""
		bus.write_byte(SI7050_DEFAULT_ADDRESS, SI7050_MEASTEMP_NOHOLD_CMD)
	
	def readtemperature(self):
		"""Read data back from the device address, 2 bytes, temperature MSB, temperature LSB"""
		data0 = bus.read_byte(SI7050_DEFAULT_ADDRESS)
		data1 = bus.read_byte(SI7050_DEFAULT_ADDRESS)
		
		# Convert the data
		cTemp = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85
		fTemp = cTemp * 1.8 + 32
		
		return {'c' : cTemp, 'f' : fTemp}

from SI7050 import SI7050
si7050 = SI7050()

while True:
	time.sleep(0.3)
	si7050.writetemperature()
	time.sleep(0.3)
	temp = si7050.readtemperature()
	print "Temperature in Celsius : %.2f C"%(temp['c'])
	print "Temperature in Fahrenheit : %.2f F"%(temp['f'])
	print " ************************************* "
