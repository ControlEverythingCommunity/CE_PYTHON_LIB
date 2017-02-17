# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# A1332
# This code is designed to work with the A1332_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Hall-Effect?sku=A1332_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
A1332_DEFAULT_ADDRESS			 =0x0C

class A1332():
	def read_data(self):
		"""Read data back from the device address, 2 bytes
		raw_adc MSB, raw_adc LSB"""
		data0 = bus.read_byte(A1332_DEFAULT_ADDRESS)
		data1 = bus.read_byte(A1332_DEFAULT_ADDRESS)
		
		time.sleep(0.5)
		
		# Checking valid data
		while (data0 == 0) and (data1 == 0) :
			data0 = bus.read_byte(A1332_DEFAULT_ADDRESS)
			data1 = bus.read_byte(A1332_DEFAULT_ADDRESS)
		
		# Convert the data to 12-bits
		raw_adc = ((data0 & 0x0F) * 256.0) + data1
		angle = (raw_adc / 4096.0) * 360.0
		
		return {'a' : angle}

from A1332 import A1332
a1332 = A1332()

while True :
	data = a1332.read_data()
	print "Magnetic Angle : %.2f"%(data['a'])
	print " ******************************* "
	time.sleep(0.5)
