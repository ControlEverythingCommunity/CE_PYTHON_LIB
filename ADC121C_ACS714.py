# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# ADC121C_ACS714
# This code is designed to work with the ADC121C_I2CS_ACS714 I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Hall-Effect?sku=ADC121C_I2CS_ACS714#tabs-0-product_tabset-2
# NT

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
ADC121C_ACS714_DEFAULT_ADDRESS			= 0x50

class ADC121C_ACS714():
	def read_data(self):
		"""Read data back from the device, 2 bytes
		raw_adc MSB, raw_adc LSB"""
		data = bus.read_i2c_block_data(ADC121C_ACS714_DEFAULT_ADDRESS, 0x00, 2)
		
		# Convert the data to 12-bits
		current = (((data[0] & 0x0F) * 256) + data[1]) / 1000.0
		
		return {'c' : current}

from ADC121C_ACS714 import ADC121C_ACS714
adc121c_acs714 = ADC121C_ACS714()

while True :
	data = adc121c_acs714.read_data()
	print "Instantaneous Current value : %.6f A"%(data['c'])
	print " ******************************* "
	time.sleep(0.5)
