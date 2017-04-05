# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# HIH9130
# This code is designed to work with the HIH9130_I2CS I2C Mini Module available from ControlEverything.com.
# https://shop.controleverything.com/products/humidity-and-temperature-sensor-1-7-rh-0-6-c#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
HIH9130_DEFAULT_ADDRESS				= 0x27

class HIH9130():
	def read_hum_temp(self):
		"""Read data back from device address, 4 bytes, humidity MSB, humidity LSB, temp MSB, temp LSB"""
		data = bus.read_i2c_block_data(HIH9130_DEFAULT_ADDRESS, 4)
		time.sleep(0.2)
		data = bus.read_i2c_block_data(HIH9130_DEFAULT_ADDRESS, 4)
		
		# Convert the data to 14-bits
		humidity = ((((data[0] & 0x3F) * 256.0) + data[1]) / 16382.0) * 100.0
		temp = ((data[2] * 256) + (data[3] & 0xFC)) / 4
		cTemp = (temp / 16382.0) * 165.0 - 40.0
		fTemp = cTemp * 1.8 + 32
		
		return {'h' : humidity, 'c' : cTemp, 'f' : fTemp}

from HIH9130 import *
hih9130 = HIH9130()

while True:
	result = hih9130.read_hum_temp()
	print "Relative Humidity : %.2f %%RH"%(result['h'])
	print "Temperature in Celsius : %.2f C"%(result['c'])
	print "Temperature in Fahrenheit : %.2f F"%(result['f'])
	print " **************************************** "
	time.sleep(1)
