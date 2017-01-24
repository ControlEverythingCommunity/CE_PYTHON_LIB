# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# BMA250
# This code is designed to work with the BMA250_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Accelorometer?sku=BMA250_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
BMA250_DEFAULT_ADDRESS				= 0x18

# BMA250 Register Map
BMA250_CHIP_ID_REG					= 0x00 # Chip ID Register
BMA250_X_AXIS_LSB_REG				= 0x02 # X-Axis Data LSB
BMA250_X_AXIS_MSB_REG				= 0x03 # X-Axis Data MSB
BMA250_Y_AXIS_LSB_REG				= 0x04 # Y-Axis Data LSB
BMA250_Y_AXIS_MSB_REG				= 0x05 # Y-Axis Data MSB
BMA250_Z_AXIS_LSB_REG				= 0x06 # Z-Axis Data LSB
BMA250_Z_AXIS_MSB_REG				= 0x07 # Z-Axis Data MSB
BMA250_TEMP_RD_REG					= 0x08 # Temperature Data
BMA250_STATUS1_REG					= 0x09 # Interrupt Status Register
BMA250_STATUS2_REG					= 0x0A # New Data Status Register
BMA250_STATUS_TAP_SLOPE_REG			= 0x0B # Tap and Hold Interrupt Status Register
BMA250_STATUS_ORIENT_HIGH_REG		= 0x0C # Flat and Orientation Status Register
BMA250_RANGE_SEL_REG				= 0x0F # Range Selection Register
BMA250_BW_SEL_REG					= 0x10 # Bandwidth Register
BMA250_MODE_CTRL_REG				= 0x11 # Mode Control Register
BMA250_DATA_CTRL_REG				= 0x13 # Data Control Register
BMA250_RESET_REG					= 0x14 # Reset Register

# BMA250 Range Selection Register Configuration
BMA250_RANGE_SEL_2G					= 0x03 # Range = +/-2G
BMA250_RANGE_SEL_4G					= 0x05 # Range = +/-4G
BMA250_RANGE_SEL_8G					= 0x08 # Range = +/-8G
BMA250_RANGE_SEL_16G				= 0x0C # Range = +/-16G

# BMA250 Bandwidth Register Configuration
BMA250_BW_SEL_7_81					= 0x08 # Bandwidth = 7.81Hz
BMA250_BW_SEL_15_63					= 0x09 # Bandwidth = 15.63Hz
BMA250_BW_SEL_31_25					= 0x0A # Bandwidth = 31.25Hz
BMA250_BW_SEL_62_5					= 0x0B # Bandwidth = 62.5Hz
BMA250_BW_SEL_125					= 0x0C # Bandwidth = 125Hz
BMA250_BW_SEL_250					= 0x0D # Bandwidth = 250Hz
BMA250_BW_SEL_500					= 0x0E # Bandwidth = 500Hz
BMA250_BW_SEL_1000					= 0x0F # Bandwidth = 1000Hz

class BMA250():
	def __init__(self):
		self.range_selection()
		self.bandwidth_selection()
	
	def range_selection(self):
		"""Select the Range Selection Register Configuration from the given provided values"""
		bus.write_byte_data(BMA250_DEFAULT_ADDRESS, BMA250_RANGE_SEL_REG, BMA250_RANGE_SEL_2G)
	
	def bandwidth_selection(self):
		"""Select the Bandwidth Register Configuration from the given provided values"""
		bus.write_byte_data(BMA250_DEFAULT_ADDRESS, BMA250_BW_SEL_REG, BMA250_BW_SEL_7_81)
	
	def read_accl(self):
		"""Read data back from BMA250_X_AXIS_LSB_REG(0x02), 6 bytes
		X-Axis LSB, X-Axis MSB, Y-Axis LSB, Y-Axis MSB, Z-Axis LSB, Z-Axis MSB"""
		data = bus.read_i2c_block_data(BMA250_DEFAULT_ADDRESS, BMA250_X_AXIS_LSB_REG, 6)
		
		# Convert the data to 10 bits
		xAccl = (data[1] * 256 + (data[0] & 0xC0)) / 64
		if xAccl > 511 :
			xAccl -= 1024
		
		yAccl = (data[3] * 256 + (data[2] & 0xC0)) / 64
		if yAccl > 511 :
			yAccl -= 1024
		
		zAccl = (data[5] * 256 + (data[4] & 0xC0)) / 64
		if zAccl > 511 :
			zAccl -= 1024
		
		return {'x' : xAccl, 'y' : yAccl, 'z' : zAccl}

from BMA250 import BMA250
bma250 = BMA250()

while True :
	bma250.range_selection()
	bma250.bandwidth_selection()
	time.sleep(0.1)
	accl = bma250.read_accl()
	print "Acceleration in X-Axis : %d"%(accl['x'])
	print "Acceleration in Y-Axis : %d"%(accl['y'])
	print "Acceleration in Z-Axis : %d"%(accl['z'])
	print " ************************************* "
	time.sleep(1)
	