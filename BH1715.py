# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# BH1715
# This code is designed to work with the BH1715_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Light?sku=BH1715_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
BH1715_DEFAULT_ADDRESS					= 0x23

# BH1715 Command Set
BH1715_CMD_POWERDOWN					= 0x00 # Power Down
BH1715_CMD_POWERUP						= 0x01 # Power Up
BH1715_CMD_RESET						= 0x07 # Reset Data register values
BH1715_CMD_H_RES_CONT					= 0x10 # Start measurement at 1 lux resolution
BH1715_CMD_L_RES_CONT					= 0x13 # Start measurement at 4 lux resolution
BH1715_CMD_H_RES_ONE					= 0x20 # Start measurement at 1 lux resolution. It is automatically set to Power Down mode after measurement
BH1715_CMD_L_RES_ONE					= 0x23 # Start measurement at 4 lux resolution. It is automatically set to Power Down mode after measurement

class BH1715():
	def __init__(self):
		self.power_command()
		self.resolution_command()
	
	def power_command(self):
		"""Select the power command from the given provided values"""
		bus.write_byte(BH1715_DEFAULT_ADDRESS, BH1715_CMD_POWERUP)
	
	def resolution_command(self):
		"""Select the continuous resolution command from the given provided values"""
		bus.write_byte(BH1715_DEFAULT_ADDRESS, BH1715_CMD_H_RES_CONT)
	
	def read_luminance(self):
		"""Read data back, 2 bytes using General Calling, luminance MSB, luminance LSB"""
		data = bus.read_i2c_block_data(BH1715_DEFAULT_ADDRESS, 2)
		
		# Convert the data
		luminance = (data[0] * 256 + data[1]) / 1.2
		
		return {'l' : luminance}

from BH1715 import BH1715
bh1715 = BH1715()

while True:
	bh1715.power_command()
	time.sleep(0.3)
	bh1715.resolution_command()
	time.sleep(0.3)
	lum = bh1715.read_luminance()
	print "Ambient Light luminance : %d lux" %(lum['l'])
	print " ***************************************** "
	time.sleep(0.5)
