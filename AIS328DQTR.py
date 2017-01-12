# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# AIS328DQTR
# This code is designed to work with the AIS328DQTR_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Accelorometer?sku=AIS328DQTR_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
AIS328DQTR_DEFAULT_ADDRESS			= 0x18

# AIS328DQTR Register Map
AIS328DQTR_REG_WHO_AM_I				= 0x0F # Device identification register
AIS328DQTR_REG_CTRL_1				= 0x20 # Control Register 1
AIS328DQTR_REG_CTRL_2				= 0x21 # Control Register 2
AIS328DQTR_REG_CTRL_3				= 0x22 # Control Register 3
AIS328DQTR_REG_CTRL_4				= 0x23 # Control Register 4
AIS328DQTR_REG_CTRL_5				= 0x24 # Control Register 5
AIS328DQTR_REG_STATUS				= 0x27 # Status Register
AIS328DQTR_REG_OUT_X_L				= 0x28 # X-Axis LSB Output
AIS328DQTR_REG_OUT_X_H				= 0x29 # X-Axis MSB Output
AIS328DQTR_REG_OUT_Y_L				= 0x2A # Y-Axis LSB Output
AIS328DQTR_REG_OUT_Y_H				= 0x2B # Y-Axis MSB Output
AIS328DQTR_REG_OUT_Z_L				= 0x2C # Z-Axis LSB Output
AIS328DQTR_REG_OUT_Z_H				= 0x2D # Z-Axis MSB Output

# AIS328DQTR Mode & Axis Configuration
AIS328DQTR_MODE_POWERDOWN			= 0x00 # Power down Mode, All axis disabled
AIS328DQTR_MODE_NORMAL				= 0x20 # Normal Mode
AIS328DQTR_MODE_LOWPOWER_0_5		= 0x40 # Low Power Mode, ODR = 0.5 Hz
AIS328DQTR_MODE_LOWPOWER_1			= 0x60 # Low Power Mode, ODR = 1 Hz
AIS328DQTR_MODE_LOWPOWER_2			= 0x80 # Low Power Mode, ODR = 2 Hz
AIS328DQTR_MODE_LOWPOWER_5			= 0xA0 # Low Power Mode, ODR = 5 Hz
AIS328DQTR_MODE_LOWPOWER_10			= 0xC0 # Low Power Mode, ODR = 10 Hz
AIS328DQTR_AXIS_Z_EN				= 0x04 # Z-Axis enabled
AIS328DQTR_AXIS_Y_EN				= 0x02 # Y-Axis enabled
AIS328DQTR_AXIS_X_EN				= 0x01 # X-Axis enabled

# AIS328DQTR Datarate Configuration
AIS328DQTR_DATARATE_50				= 0x00 # ODR = 50 Hz
AIS328DQTR_DATARATE_100				= 0x08 # ODR = 100 Hz
AIS328DQTR_DATARATE_400				= 0x10 # ODR = 400 Hz
AIS328DQTR_DATARATE_1000			= 0x18 # ODR = 1000 Hz

# AIS328DQTR Data Output Configuration
AIS328DQTR_BDU_CONTINUOUS			= 0x00 # Continuous Update, Data @ LSB, Self Test disabled, 4-Wire Interface
AIS328DQTR_BLE_MSB					= 0x40 # Data @ MSB
AIS328DQTR_SELFTEST_EN				= 0x02 # Self Test enabled
AIS328DQTR_SIM_3					= 0x01 # 3-Wire Interface

# AIS328DQTR Range Configuration
AIS328DQTR_RANGE_2					= 0x00 # Full-Scale Selection = +/-2g
AIS328DQTR_RANGE_4					= 0x10 # Full-Scale Selection = +/-4g
AIS328DQTR_RANGE_8					= 0x30 # Full-Scale Selection = +/-8g

class AIS328DQTR():
	def __init__ (self):
		self.select_datarate()
		self.select_data_config()
	
	def select_datarate(self):
		"""Select the data rate & mode of the accelerometer from the given provided values"""
		DATARATE_MODE_CONFIG = (AIS328DQTR_DATARATE_50 | AIS328DQTR_MODE_NORMAL | AIS328DQTR_AXIS_Z_EN | AIS328DQTR_AXIS_Y_EN | AIS328DQTR_AXIS_X_EN)
		bus.write_byte_data(AIS328DQTR_DEFAULT_ADDRESS, AIS328DQTR_REG_CTRL_1, DATARATE_MODE_CONFIG)
	
	def select_data_config(self):
		"""Select the data configuration of the accelerometer from the given provided values"""
		DATA_RANGE_CONFIG = (AIS328DQTR_BDU_CONTINUOUS | AIS328DQTR_RANGE_8)
		bus.write_byte_data(AIS328DQTR_DEFAULT_ADDRESS, AIS328DQTR_REG_CTRL_4, DATA_RANGE_CONFIG)
	
	def readaccl(self):
		"""Read data back from AIS328DQTR_REG_OUT_X_L(0x28), 2 bytes
		X-Axis Accl LSB, X-Axis Accl MSB"""
		data0 = bus.read_byte_data(AIS328DQTR_DEFAULT_ADDRESS, AIS328DQTR_REG_OUT_X_L)
		data1 = bus.read_byte_data(AIS328DQTR_DEFAULT_ADDRESS, AIS328DQTR_REG_OUT_X_H)
		
		xAccl = data1 * 256 + data0
		if xAccl > 32767 :
			xAccl -= 65536
		
		"""Read data back from AIS328DQTR_REG_OUT_Y_L(0x2A), 2 bytes
		Y-Axis Accl LSB, Y-Axis Accl MSB"""
		data0 = bus.read_byte_data(AIS328DQTR_DEFAULT_ADDRESS, AIS328DQTR_REG_OUT_Y_L)
		data1 = bus.read_byte_data(AIS328DQTR_DEFAULT_ADDRESS, AIS328DQTR_REG_OUT_Y_H)
		
		yAccl = data1 * 256 + data0
		if yAccl > 32767 :
			yAccl -= 65536
		
		"""Read data back from AIS328DQTR_REG_OUT_Z_L(0x2C), 2 bytes
		Z-Axis Accl LSB, Z-Axis Accl MSB"""
		data0 = bus.read_byte_data(AIS328DQTR_DEFAULT_ADDRESS, AIS328DQTR_REG_OUT_Z_L)
		data1 = bus.read_byte_data(AIS328DQTR_DEFAULT_ADDRESS, AIS328DQTR_REG_OUT_Z_H)
		
		zAccl = data1 * 256 + data0
		if zAccl > 32767 :
			zAccl -= 65536
		
		return {'x' : xAccl, 'y' : yAccl, 'z' : zAccl}

from AIS328DQTR import AIS328DQTR
ais328dqtr = AIS328DQTR()

while True:
	accl = ais328dqtr.readaccl()
	print "Acceleration in X-Axis : %d"%(accl['x'])
	print "Acceleration in Y-Axis : %d"%(accl['y'])
	print "Acceleration in Z-Axis : %d"%(accl['z'])
	print " ************************************* "
	time.sleep(1)

