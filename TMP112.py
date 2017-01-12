# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# TMP112
# This code is designed to work with the TMP112_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Temperature?sku=TMP112_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
TMP112_DEFAULT_ADDRESS			= 0x48

# TMP112 Register Map
TMP112_REG_TEMP					= 0x00
TMP112_REG_CONFIG				= 0x01
TMP112_REG_THIGH				= 0x02
TMP112_REG_TLOW					= 0x03

# TMP112 Configuration Register
TMP112_REG_CONFIG_CONTINOUS		= 0x0000 # Continuous Conversion Mode, Comparator Mode, Polarity Active LOW
TMP112_REG_CONFIG_SHUTDOWN		= 0x0100 # Shutdown Mode enabled
TMP112_REG_CONFIG_INTERRUPT		= 0x0200 # Interrupt Mode enabled
TMP112_REG_CONFIG_POL_H			= 0x0400 # Polarity Active HIGH
TMP112_REG_CONFIG_FQ_1			= 0x0000 # Fault Queue = 1
TMP112_REG_CONFIG_FQ_2			= 0x0800 # Fault Queue = 2
TMP112_REG_CONFIG_FQ_4			= 0x1000 # Fault Queue = 4
TMP112_REG_CONFIG_FQ_6			= 0x1800 # Fault Queue = 6
TMP112_REG_CONFIG_RES			= 0x6000 # 12-bits Resolution
TMP112_REG_CONFIG_OS			= 0x8000 # One-shot enabled
TMP112_REG_CONFIG_CR_0_25		= 0x0000 # Conversion Rate = 0.25 Hz
TMP112_REG_CONFIG_CR_1			= 0x0040 # Conversion Rate = 1 Hz
TMP112_REG_CONFIG_CR_4			= 0x0080 # Conversion Rate = 4 Hz
TMP112_REG_CONFIG_CR_8			= 0x00C0 # Conversion Rate = 8 Hz
TMP112_REG_CONFIG_AL_H			= 0x0020 # When the POL bit equals 0, AL is HIGH

class TMP112():
	def __init__(self):
		self.temp_config()
	
	def temp_config(self):
		"""Select the temperature configuration from the given provided values"""
		TEMP_CONFIG = (TMP112_REG_CONFIG_CONTINOUS | TMP112_REG_CONFIG_FQ_1 | TMP112_REG_CONFIG_RES | TMP112_REG_CONFIG_FQ_1 | TMP112_REG_CONFIG_CR_4 | TMP112_REG_CONFIG_AL_H)
		bus.write_byte_data(TMP112_DEFAULT_ADDRESS, TMP112_REG_CONFIG, TEMP_CONFIG)
	
	def read_temp(self):
		"""Read data back from the TMP112_REG_TEMP(0x00), 2 bytes, temperature MSB, temperature LSB"""
		data = bus.read_i2c_block_data(TMP112_DEFAULT_ADDRESS, TMP112_REG_TEMP, 2)
		
		# Convert the data to 12-bits
		temp =(data[0] * 256 + data[1]) / 16
		if temp > 2047 :
			temp -= 4096
		cTemp = temp * 0.0625
		fTemp = cTemp * 1.8 + 32
		
		return {'c' : cTemp, 'f' : fTemp}

from TMP112 import TMP112
tmp112 = TMP112()

while True:
	temp = tmp112.read_temp()
	print "Temperature in Celsius : %.2f C"%(temp['c'])
	print "Temperature in Fahrenheit : %.2f F"%(temp['f'])
	print " ************************************* "
	time.sleep(1)
