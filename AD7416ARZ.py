# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# AD7416ARZ
# This code is designed to work with the AD7416ARZ_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Analog-Digital-Converters?sku=AD7416ARZ_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
AD7416ARZ_DEFAULT_ADDRESS		= 0x48

# AD7416ARZ Register Map
AD7416ARZ_REG_TEMP				= 0x00 # Temperature Value
AD7416ARZ_REG_CONFIG			= 0x01 # Configuration Register
AD7416ARZ_REG_THYST				= 0x02 # THYST setpoint
AD7416ARZ_REG_TOTI				= 0x03 # TOTI setpoint

# AD7416ARZ Configuration Register
AD7416ARZ_FAULTQUEUE_1			= 0x00 # Fault Queue = 1
AD7416ARZ_FAULTQUEUE_2			= 0x08 # Fault Queue = 2
AD7416ARZ_FAULTQUEUE_4			= 0x10 # Fault Queue = 4
AD7416ARZ_FAULTQUEUE_6			= 0x18 # Fault Queue = 6
AD7416ARZ_MODE_CMP				= 0x00 # Comparater Mode
AD7416ARZ_MODE_INT				= 0x02 # Interrupt Mode
AD7416ARZ_MODE_SHUTDOWN			= 0x01 # Shutdown Mode

class AD7416ARZ():
	def __init__(self):
		self.temp_configuration()
	
	def temp_configuration(self):
		"""Select the temperature configuration from the given provided values"""
		TEMP_CONFIG = (AD7416ARZ_FAULTQUEUE_1 | AD7416ARZ_MODE_CMP)
		bus.write_byte_data(AD7416ARZ_DEFAULT_ADDRESS, AD7416ARZ_REG_CONFIG, TEMP_CONFIG)
	
	def read_temp(self):
		"""Read data back from AD7416ARZ_REG_TEMP(0x00), 2 bytes, temp MSB, temp LSB"""
		data = bus.read_i2c_block_data(AD7416ARZ_DEFAULT_ADDRESS, AD7416ARZ_REG_TEMP, 2)
		
		# Convert the data to 10-bits
		temp = ((data[0] * 256) + (data[1] & 0xC0)) / 64
		if temp > 511 :
			temp -= 1024
		cTemp = temp * 0.25
		fTemp = cTemp * 1.8 + 32
		
		return {'c' : cTemp, 'f' : fTemp}

from AD7416ARZ import AD7416ARZ
ad7416arz = AD7416ARZ()

while True:
	temp = ad7416arz.read_temp()
	print "Temperature in Celsius : %.2f C"%(temp['c'])
	print "Temperature in Fahrenheit : %.2f F"%(temp['f'])
	print " ***************************************** "
	time.sleep(1)
