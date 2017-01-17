# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# HIH6020
# This code is designed to work with the HIH6020_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Temperature?sku=HIH6020_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
HIH6020_DEFAULT_ADDRESS				= 0x27

# HIH6020 Read Register
HIH6020_HUM_MSB						= 0x00
HIH6020_HUM_LSB						= 0x01
HIH6020_TEMP_MSB					= 0x02
HIH6020_TEMP_LSB					= 0x03

class HIH6020():
	def __init__(self):
		self.read_hum_temp()
	
	def read_hum_temp(self):
		"""Read data back from HIH6020_HUM_MSB(0x00), 4 bytes, humidity MSB, humidity LSB, temp MSB, temp LSB"""
		data = bus.read_i2c_block_data(HIH6020_DEFAULT_ADDRESS, HIH6020_HUM_MSB, 4)
		
		# Convert the data to 14-bits
		humidity = ((((data[0] & 0x3F) * 256.0) + data[1]) * 100.0) / 16382.0
		temp = ((data[2] * 256) + (data[3] & 0xFC)) / 4
		cTemp = (temp / 16382.0) * 165.0 - 40.0
		fTemp = cTemp * 1.8 + 32
		
		return {'h' : humidity, 'c' : cTemp, 'f' : fTemp}

from HIH6020 import HIH6020
hih6020 = HIH6020()

while True:
	value = hih6020.read_hum_temp()
	print "Relative Humidity : %.2f %%RH"%(value['h'])
	print "Temperature in Celsius : %.2f C"%(value['c'])
	print "Temperature in Fahrenheit : %.2f F"%(value['f'])
	print " **************************************** "
	time.sleep(1)
