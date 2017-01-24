# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# AMS5915_0100_D
# This code is designed to work with the AMS5915_I2CS_0100-D I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Pressure?sku=AMS5915_I2CS_0100-D#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
AMS5915_0100_D_DEFAULT_ADDRESS			= 0x28

class AMS5915_0100_D():
	def __init__(self):
		self.read_data()
	
	def read_data(self):
		"""Read data back from the device address, 4 bytes
		pressure MSB, pressure LSB, temp MSB, temp LSB"""
		data = bus.read_i2c_block_data(AMS5915_0100_D_DEFAULT_ADDRESS, 4)
		
		# Convert the data
		pressure = ((data[0] & 0x3F) * 256) + data[1]
		pressure = (pressure - 1638.0) / (13107.0 / 100.0)
		psi = pressure * 0.0145038
		kPa = pressure / 10.0
		hg = pressure * 76.0 / 101.325
		
		temp = ((data[2] * 256) + (data[3] & 0xE0)) / 32
		cTemp = ((temp * 200.0) / 2048.0) - 50.0
		fTemp = (cTemp * 1.8 ) + 32
		
		return {'p' : pressure, 's' : psi, 'k' : kPa, 'h' : hg, 'c' : cTemp, 'f' : fTemp}

from AMS5915_0100_D import AMS5915_0100_D
ams5915_0100_d = AMS5915_0100_D()

while True :
	data = ams5915_0100_d.read_data()
	print "Pressure in mbar : %.2f mbar"%(data['p'])
	print "Pressure in PSI : %.2f PSI"%(data['s'])
	print "Pressure in kPa : %.2f kPa"%(data['k'])
	print "Pressure in mmHg : %.2f mmHg"%(data['h'])
	print "Temperature in Celsius : %.2f C"%(data['c'])
	print "Temperature in Fahrenheit : %.2f F"%(data['f'])
	print " ************************************* "
	time.sleep(1)
