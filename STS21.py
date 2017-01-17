# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# STS21
# This code is designed to work with the STS21_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Temperature?sku=STS21_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
STS21_DEFAULT_ADDRESS			= 0x4A

# STS21 Command Set
STS21_MEASTEMP_HOLD_CMD			= 0xE3 # Hold master
STS21_MEASTEMP_NOHOLD_CMD		= 0xF3 # No-Hold master 
STS21_RESET_CMD					= 0xFE # Reset Command
STS21_WRITE_REG_CMD				= 0xE6 # Write User Register
STS21_READ_REG_CMD				= 0xE7 # Read User Register

class STS21():
	def __init__(self):
		self.writetemperature()
		time.sleep(0.3)
		
	
	def writetemperature(self):
		"""Select the temperature command from the given provided values"""
		bus.write_byte(STS21_DEFAULT_ADDRESS, STS21_MEASTEMP_NOHOLD_CMD)
	
	def readtemperature(self):
		"""Read data back from the device address, 2 bytes, temperature MSB, temperature LSB"""
		data0 = bus.read_byte(STS21_DEFAULT_ADDRESS)
		data1 = bus.read_byte(STS21_DEFAULT_ADDRESS)
		
		# Convert the data
		cTemp = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85
		fTemp = cTemp * 1.8 + 32
		
		return {'c' : cTemp, 'f' : fTemp}

from STS21 import STS21
sts21 = STS21()

while True:
	sts21.writetemperature()
	time.sleep(0.3)
	temp = sts21.readtemperature()
	print "Temperature in Celsius : %.2f C"%(temp['c'])
	print "Temperature in Fahrenheit : %.2f F"%(temp['f'])
	print " ************************************* "
	time.sleep(0.5)
