# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# TMP101NA
# This code is designed to work with the TMP101NA_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Temperature?sku=TMP101NA_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
TMP101NA_DEFAULT_ADDRESS		= 0x49

# TMP101NA Register Map
TMP101NA_REG_TEMP				= 0x00
TMP101NA_REG_CONFIG				= 0x01
TMP101NA_REG_THIGH				= 0x02
TMP101NA_REG_TLOW				= 0x03

# TMP101NA Configuration Register
TMP101NA_REG_CONFIG_SHUTDOWN	= 0x01
TMP101NA_REG_CONFIG_CONT		= 0x00
TMP101NA_REG_CONFIG_RES_9		= 0x00
TMP101NA_REG_CONFIG_RES_10		= 0x20
TMP101NA_REG_CONFIG_RES_11		= 0x40
TMP101NA_REG_CONFIG_RES_12		= 0x60
TMP101NA_REG_CONFIG_ONESHOT		= 0x80

class TMP101NA():
	def __init__(self):
		self.writetemperature()
	
	def writetemperature(self):
		"""Select the temperature configuration from the given provided values"""
		TEMP_CONFIG = (TMP101NA_REG_CONFIG_CONT | TMP101NA_REG_CONFIG_RES_12)
		bus.write_byte_data(TMP101NA_DEFAULT_ADDRESS, TMP101NA_REG_CONFIG, TEMP_CONFIG)
	
	def readtemperature(self):
		"""Read data back from TMP101NA_REG_TEMP(0x00), 2 bytes, ctemp MSB, ctemp LSB"""
		data = bus.read_i2c_block_data(TMP101NA_DEFAULT_ADDRESS, TMP101NA_REG_TEMP, 2)
		
		# Convert the data to 12-bits
		cTemp = (data[0] * 256 + (data[1] & 0xF0)) / 16
		if cTemp > 2047:
			cTemp -= 4096
		cTemp = cTemp * 0.0625
		fTemp = cTemp * 1.8 + 32
		
		return {'c' : cTemp, 'f' : fTemp}

from TMP101NA import TMP101NA
tmp101NA = TMP101NA()

while True:
	temp = tmp101NA.readtemperature()
	print "Temperature in Celsius : %.2f C"%(temp['c'])
	print "Temperature in Fahrenheit : %.2f F"%(temp['f'])
	time.sleep(1)
