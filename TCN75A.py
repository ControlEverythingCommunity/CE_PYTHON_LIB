# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# TCN75A
# This code is designed to work with the TCN75A_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Temperature?sku=TCN75A_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
TCN75A_DEFAULT_ADDRESS			= 0x48

# TCN75A Register Map
TCN75A_REG_TEMP					= 0x00 # Temperature Register
TCN75A_REG_CONFIG				= 0x01 # Configuration Register
TCN75A_REG_THYST				= 0x02 # Temperature Hysteresis Register
TCN75A_REG_TSET					= 0x03 # Temperature Limit-set Register

# TCN75A Configuration Register
TCN75A_MODE_ONESHOT_DS			= 0x00 # One-Shot Mode disabled
TCN75A_MODE_ONESHOT_EN			= 0x80 # One-Shot Mode enabled
TCN75A_RESOLUTION_9				= 0x00 # Resolution = 9-bits
TCN75A_RESOLUTION_10			= 0x20 # Resolution = 10-bits
TCN75A_RESOLUTION_11			= 0x40 # Resolution = 11-bits
TCN75A_RESOLUTION_12			= 0x60 # Resolution = 12-bits
TCN75A_FAULTQUEUE_1				= 0x00 # Fault Queue = 1
TCN75A_FAULTQUEUE_2				= 0x08 # Fault Queue = 2
TCN75A_FAULTQUEUE_4				= 0x10 # Fault Queue = 4
TCN75A_FAULTQUEUE_6				= 0x18 # Fault Queue = 6
TCN75A_POLARITY_LOW				= 0x00 # Active Polarity LOW
TCN75A_POLARITY_HIGH			= 0x04 # Active Polarity HIGH
TCN75A_MODE_CMP					= 0x00 # Comparater Mode
TCN75A_MODE_INT					= 0x02 # Interrupt Mode
TCN75A_MODE_SHUTDOWN			= 0x01 # Shutdown Mode

class TCN75A():
	def __init__(self):
		self.temp_configuration()
	
	def temp_configuration(self):
		"""Select the temperature configuration from the given provided values"""
		TEMP_CONFIG = (TCN75A_MODE_ONESHOT_DS | TCN75A_RESOLUTION_12 | TCN75A_FAULTQUEUE_1 | TCN75A_POLARITY_LOW | TCN75A_MODE_CMP)
		bus.write_byte_data(TCN75A_DEFAULT_ADDRESS, TCN75A_REG_CONFIG, TEMP_CONFIG)
	
	def read_temp(self):
		"""Read data back from TCN75A_REG_TEMP(0x00), 2 bytes, temp MSB, temp LSB"""
		data = bus.read_i2c_block_data(TCN75A_DEFAULT_ADDRESS, TCN75A_REG_TEMP, 2)
		
		# Convert the data to 12-bits
		temp = ((data[0] * 256) + (data[1] & 0xF0)) / 16
		if temp > 2047 :
			temp -= 4096
		cTemp = temp  * 0.0625
		fTemp = (cTemp * 1.8) + 32
		
		return {'c' : cTemp, 'f' : fTemp}

from TCN75A import TCN75A
tcn75a = TCN75A()

while True:
	temp = tcn75a.read_temp()
	print "Temperature in Celsius : %.2f C"%(temp['c'])
	print "Temperature in Fahrenheit : %.2f F"%(temp['f'])
	print " ***************************************** "
	time.sleep(1)
