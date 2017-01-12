# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# AT30TS74
# This code is designed to work with the AT30TS74_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/products

import smbus
import time

# I2C address of the device
AT30TS74_DEFAULT_ADDRESS			= 0x48

# AT30TS74 Register Map
AT30TS74_REG_TEMP					= 0x00 # Temperature Register
AT30TS74_REG_CONFIG					= 0x01 # Configuration Register
AT30TS74_REG_TLOW					= 0x02 # TLOW Limit Register
AT30TS74_REG_THIGH					= 0x03 # THIGH Limit Register

# AT30TS74 Temperature Configuration
AT30TS74_CONFIG_NORMAL				= 0x0000 # Normal Operation, Default Settings
AT30TS74_CONFIG_ONESHOT				= 0x8000 # Device perform One-Shot Measurement
AT30TS74_CONFIG_POL_HIGH			= 0x0400 # ALERT pin is Active High
AT30TS74_CONFIG_INT_MODE			= 0x0200 # Interrupt Mode
AT30TS74_CONFIG_SHUTDOWN			= 0x0100 # Shutdown Mode active

# AT30TS74 Resolution Configuration
AT30TS74_CONFIG_RES_9				= 0x0000 # Resolution = 9-bits
AT30TS74_CONFIG_RES_10				= 0x2000 # Resolution = 10-bits
AT30TS74_CONFIG_RES_11				= 0x4000 # Resolution = 11-bits
AT30TS74_CONFIG_RES_12				= 0x6000 # Resolution = 12-bits

class AT30TS74():
	def __init__(self):
		self.temp_config()
	
	def temp_config(self):
		"""Select the temperature configuration from the given provided values"""
		TEMP_RES_CONFIG = (AT30TS74_CONFIG_RES_12 | AT30TS74_CONFIG_NORMAL)
		bus.write_byte_data(AT30TS74_DEFAULT_ADDRESS, AT30TS74_REG_CONFIG, TEMP_RES_CONFIG)
	
	def readtemp(self):
		"""Read data back from AT30TS74_REG_TEMP(0x00), 2 bytes
		temp MSB, temp LSB"""
		data = bus.read_i2c_block_data(AT30TS74_DEFAULT_ADDRESS, AT30TS74_REG_TEMP, 2)
		
		# Convert the data to 12-bits
		temp = ((data[0] * 256) + (data[1] & 0xF0)) / 16
		if temp > 2047 :
			temp -= 4096
		cTemp = temp * 0.0625
		fTemp = (cTemp * 1.8) + 32
		
		return {'c' : cTemp, 'f' : fTemp}

from AT30TS74 import AT30TS74
at30ts74 = AT30TS74()

while True:
	temp = at30ts74.readtemp()
	print "Temperature in Celsius : %.2f C"%(temp['c'])
	print "Temperature in Fahrenheit : %.2f F"%(temp['f'])
	print " ************************************* "
	time.sleep(1)
