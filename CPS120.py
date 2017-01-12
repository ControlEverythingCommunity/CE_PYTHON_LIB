# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# CPS120
# This code is designed to work with the CPS120_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Barometer?sku=CPS120_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
CPS120_DEFAULT_ADDRESS			= 0x28

# CPS120 Command Set
CPS120_START_MODE				= 0x80 # Select Start mode
CPS120_READ_DATA				= 0x00 # Read data

class CPS120():
	def __init__(self):
		self.writeCommand()
		time.sleep(0.5)
		self.readData()
	
	def writeCommand(self):
		"""Select the command from the given provided values"""
		bus.write_byte(CPS120_DEFAULT_ADDRESS, CPS120_START_MODE)
	
	def readData(self):
		"""Read data back from CPS120_READ_DATA(0x00), 2 bytes
		pressure MSB, pressure LSB"""
		data = bus.read_i2c_block_data(CPS120_DEFAULT_ADDRESS, CPS120_READ_DATA, 2)
		
		# Convert the data to 14-bits
		pressure = ((((data[0] & 0X3F) * 256.00 + data[1]) * 90.00) / 16384.00) + 30.00
		mbar = pressure * 10
		hg = pressure * 760.0 / 101.325
		
		return {'p' : pressure, 'm' : mbar, 'h' : hg}

from CPS120 import CPS120
cps120 = CPS120()

while True:
	value = cps120.readData()
	print "Pressure in kPa : %.2f"%(value['p'])
	print "Pressure in mbar : %.2f"%(value['m'])
	print "Pressure in mmHg : %.2f"%(value['h'])
	print " ***************************************** "
	time.sleep(0.5)
