# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# BMG160
# This code is designed to work with the BMG160_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Gyro?sku=BMG160_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
BMG160_DEFAULT_ADDRESS			= 0x68

# BMG160 Register Map
BMG160_REG_CHIPID				= 0x00 # Chip ID Register
BMG160_REG_X_LSB				= 0x02 # X-axis Data LSB
BMG160_REG_X_MSB				= 0x03 # X-axis Data MSB
BMG160_REG_Y_LSB				= 0x04 # Y-axis Data LSB
BMG160_REG_Y_MSB				= 0x05 # Y-axis Data MSB
BMG160_REG_Z_LSB				= 0x06 # Z-axis Data LSB
BMG160_REG_Z_MSB				= 0x07 # Z-axis Data MSB
BMG160_REG_TEMP					= 0x08 # Temperature Register
BMG160_REG_INT_STATUS_0			= 0x09 # Interrupt Status-0
BMG160_REG_INT_STATUS_1			= 0x0A # Interrupt Status-1
BMG160_REG_INT_STATUS_2			= 0x0B # Interrupt Status-2
BMG160_REG_INT_STATUS_3			= 0x0C # Interrupt Status-3
BMG160_REG_FIFO_STATUS			= 0x0D # FIFO Status
BMG160_REG_RANGE				= 0x0F # Range Register
BMG160_REG_BW					= 0x10 # Bandwidth Register

# BMG160 Range Register Configuration
BMG160_RANGE_2000				= 0x00 # Full Scale = +/-2000dps
BMG160_RANGE_1000				= 0x01 # Full Scale = +/-1000dps
BMG160_RANGE_500				= 0x02 # Full Scale = +/-500dps
BMG160_RANGE_250				= 0x03 # Full Scale = +/-250dps
BMG160_RANGE_125				= 0x04 # Full Scale = +/-125dps

# BMG160 Bandwidth Register Configuration
BMG160_BW_UNFILTER				= 0x00 # Unfilter Bandwidth
BMG160_BW_230					= 0x01 # Filter Bandwidth = 230Hz
BMG160_BW_116					= 0x02 # Filter Bandwidth = 116Hz
BMG160_BW_47					= 0x03 # Filter Bandwidth = 47Hz
BMG160_BW_23					= 0x04 # Filter Bandwidth = 23Hz
BMG160_BW_12					= 0x05 # Filter Bandwidth = 12Hz
BMG160_BW_64					= 0x06 # Filter Bandwidth = 64Hz
BMG160_BW_32					= 0x07 # Filter Bandwidth = 32Hz

class BMG160():
	def __init__(self):
		self.range_configuration()
		self.bandwidth_configuration()
	
	def range_configuration(self):
		"""Select the Range Register Configuration from the given provided value"""
		RANGE_CONFIG = (BMG160_RANGE_2000)
		bus.write_byte_data(BMG160_DEFAULT_ADDRESS, BMG160_REG_RANGE, RANGE_CONFIG)
	
	def bandwidth_configuration(self):
		"""Select the Bandwidth Register Configuration from the given provided value"""
		BANDWIDTH_CONFIG = (BMG160_BW_23)
		bus.write_byte_data(BMG160_DEFAULT_ADDRESS, BMG160_REG_BW, BANDWIDTH_CONFIG)
	
	def read_gyro(self):
		"""Read data back from BMG160_REG_X_LSB(ox02), 6 bytes
		X-Axis LSB, X-Axis MSB, Y-Axis LSB, Y-Axis MSB, Z-Axis LSB, Z-Axis MSB"""
		data = bus.read_i2c_block_data(BMG160_DEFAULT_ADDRESS, BMG160_REG_X_LSB, 6)
		
		# Convert the data
		xGyro = data[1] * 256 + data[0]
		if xGyro > 32767 :
			xGyro -= 65536
		
		yGyro = data[3] * 256 + data[2]
		if yGyro > 32767 :
			yGyro -= 65536
		
		zGyro = data[5] * 256 + data[4]
		if zGyro > 32767 :
			zGyro -= 65536
		
		return {'x' : xGyro, 'y' : yGyro, 'z' : zGyro}

from BMG160 import BMG160
bmg160 = BMG160()

while True :
	bmg160.range_configuration()
	bmg160.bandwidth_configuration()
	time.sleep(0.1)
	gyro = bmg160.read_gyro()
	print "X-Axis of Rotation : %d" %(gyro['x'])
	print "Y-Axis of Rotation : %d" %(gyro['y'])
	print "Z-Axis of Rotation : %d" %(gyro['z'])
	print " ************************************ "
	time.sleep(1)
