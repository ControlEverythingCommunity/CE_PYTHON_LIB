# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# LM75BIMM
# This code is designed to work with the LM75BIMM_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Temperature?sku=LM75BIMM_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
LM75BIMM_DEFAULT_ADDRESS		= 0x49

# LM75BIMM Register Map
LM75BIMM_REG_TEMP					= 0x00 # Temperature Register
LM75BIMM_REG_CONFIG					= 0x01 # Configuration Register
LM75BIMM_REG_THYST					= 0x02 # Temperature Hysteresis Register
LM75BIMM_REG_TOS					= 0x03 # Over Temperature Shutdown Register

# LM75BIMM Configuration Register
LM75BIMM_FAULTQUEUE_1				= 0x00 # Fault Queue = 1
LM75BIMM_FAULTQUEUE_2				= 0x08 # Fault Queue = 2
LM75BIMM_FAULTQUEUE_4				= 0x10 # Fault Queue = 4
LM75BIMM_FAULTQUEUE_6				= 0x18 # Fault Queue = 6
LM75BIMM_POLARITY_LOW				= 0x00 # Active Polarity LOW
LM75BIMM_POLARITY_HIGH				= 0x04 # Active Polarity HIGH
LM75BIMM_MODE_CMP					= 0x00 # Comparater Mode
LM75BIMM_MODE_INT					= 0x02 # Interrupt Mode
LM75BIMM_MODE_SHUTDOWN				= 0x01 # Shutdown Mode

class LM75BIMM():
	def __init__(self):
		self.temp_configuration()
	
	def temp_configuration(self):
		"""Select the temperature configuration from the given provided values"""
		TEMP_CONFIG = (LM75BIMM_FAULTQUEUE_1 | LM75BIMM_POLARITY_LOW | LM75BIMM_MODE_CMP)
		bus.write_byte_data(LM75BIMM_DEFAULT_ADDRESS, LM75BIMM_REG_CONFIG, TEMP_CONFIG)
	
	def read_temp(self):
		"""Read data back from LM75BIMM_REG_TEMP(0x00), 2 bytes, temp MSB, temp LSB"""
		data = bus.read_i2c_block_data(LM75BIMM_DEFAULT_ADDRESS, LM75BIMM_REG_TEMP, 2)
		
		# Convert the data to 9-bits
		temp = (data[0] * 256 + (data[1] & 0x80)) / 128
		if temp > 255 :
			temp -= 512
		cTemp = temp * 0.5
		fTemp = cTemp * 1.8 + 32
		
		return {'c' : cTemp, 'f' : fTemp}

from LM75BIMM import LM75BIMM
lm75bimm = LM75BIMM()

while True:
	temp = lm75bimm.read_temp()
	print "Temperature in Celsius : %.2f C"%(temp['c'])
	print "Temperature in Fahrenheit : %.2f F"%(temp['f'])
	print " ***************************************** "
	time.sleep(1)
