# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# ADT75
# This code is designed to work with the ADT75_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Temperature?sku=ADT75_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
ADT75_DEFAULT_ADDRESS		= 0x48

# ADT75 Register Map
ADT75_REG_TEMP				= 0x00 # Temperature Value
ADT75_REG_CONFIG			= 0x01 # Configuration Register
ADT75_REG_THYST				= 0x02 # THYST setpoint
ADT75_REG_TOS				= 0x03 # TOS setpoint

# ADT75 Configuration Register
ADT75_MODE_NORMAL			= 0x00 # Normal Mode
ADT75_MODE_ONESHOT			= 0x20 # One-Shot Mode
ADT75_FAULTQUEUE_1			= 0x00 # Fault Queue = 1
ADT75_FAULTQUEUE_2			= 0x08 # Fault Queue = 2
ADT75_FAULTQUEUE_4			= 0x10 # Fault Queue = 4
ADT75_FAULTQUEUE_6			= 0x18 # Fault Queue = 6
ADT75_MODE_CMP				= 0x00 # Comparater Mode
ADT75_MODE_INT				= 0x02 # Interrupt Mode
ADT75_MODE_SHUTDOWN			= 0x01 # Shutdown Mode

class ADT75():
	def __init__(self):
		self.temp_configuration()
	
	def temp_configuration(self):
		"""Select the temperature configuration from the given provided values"""
		TEMP_CONFIG = (ADT75_MODE_NORMAL | ADT75_FAULTQUEUE_1 | ADT75_MODE_CMP)
		bus.write_byte_data(ADT75_DEFAULT_ADDRESS, ADT75_REG_CONFIG, TEMP_CONFIG)
	
	def read_temp(self):
		"""Read data back from ADT75_REG_TEMP(0x00), 2 bytes, temp MSB, temp LSB"""
		data = bus.read_i2c_block_data(ADT75_DEFAULT_ADDRESS, ADT75_REG_TEMP, 2)
		
		# Convert the data to 12-bits
		temp = ((data[0] * 256) + data[1]) / 16
		if temp > 2047 :
			temp -= 4096
		cTemp = temp * 0.0625
		fTemp = (cTemp * 1.8) + 32
		
		return {'c' : cTemp, 'f' : fTemp}

from ADT75 import ADT75
adt75 = ADT75()

while True:
	temp = adt75.read_temp()
	print "Temperature in Celsius : %.2f C"%(temp['c'])
	print "Temperature in Fahrenheit : %.2f F"%(temp['f'])
	print " ***************************************** "
	time.sleep(1)
