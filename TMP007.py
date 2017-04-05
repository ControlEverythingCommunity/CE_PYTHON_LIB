# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# TMP007
# This code is designed to work with the TMP007_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Temperature?sku=TMP007_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
TMP007_DEFAULT_ADDRESS		= 0x40

# TMP007 Register Map
TMP007_REG_VOBJ				= 0x00
TMP007_REG_TDIE				= 0x01
TMP007_REG_CONFIG			= 0x02
TMP007_REG_TOBJ				= 0x03
TMP007_REG_STATUS			= 0x04
TMP007_REG_STATMASK			= 0x05

# TMP007 Configuration Register
TMP007_CONFIG_RESET			= 0x8000
TMP007_CONFIG_MODEON		= 0x1000
TMP007_CONFIG_1SAMPLE		= 0x0000
TMP007_CONFIG_2SAMPLE		= 0x0200
TMP007_CONFIG_4SAMPLE		= 0x0400
TMP007_CONFIG_8SAMPLE		= 0x0600
TMP007_CONFIG_16SAMPLE		= 0x0800
TMP007_CONFIG_ALERTEN		= 0x0100
TMP007_CONFIG_ALERTF		= 0x0080
TMP007_CONFIG_TRANSC		= 0x0040

class TMP007():
	def __init__(self):
		self.writetemperature()
		time.sleep(0.5)
	
	def writetemperature(self):
		"""Select the temperature configuration from the given provided values"""
		TEMP_CONFIG = (TMP007_CONFIG_MODEON | TMP007_CONFIG_4SAMPLE | TMP007_CONFIG_ALERTEN | TMP007_CONFIG_TRANSC)
		bus.write_byte_data(TMP007_DEFAULT_ADDRESS, TMP007_REG_CONFIG, TEMP_CONFIG)
	
	def readtemperature(self):
		"""Read data back from TMP007_REG_TOBJ(0x03), 2 bytes, ctemp MSB, ctemp LSB"""
		data = bus.read_i2c_block_data(TMP007_DEFAULT_ADDRESS, TMP007_REG_TOBJ, 2)
		
		# Convert the data to 14-bits
		cTemp = ((data[0] * 256 + (data[1] & 0xFC)) / 4)
		if cTemp > 8191 :
			cTemp -= 16384
		cTemp = cTemp * 0.03125
		fTemp = cTemp * 1.8 + 32
		
		return {'c' : cTemp, 'f' : fTemp}

from TMP007 import TMP007
tmp007 = TMP007()

while True:
	temp = tmp007.readtemperature()
	print "Object Temperature in Celsius : %.2f C"(temp['c'])
	print "Object Temperature in Fahrenheit : %.2f F"(temp['f'])
	time.sleep(1)
