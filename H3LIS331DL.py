# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# H3LIS331DL
# This code is designed to work with the H3LIS331DL_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Accelorometer?sku=H3LIS331DL_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
H3LIS331DL_DEFAULT_ADDRESS			= 0x18

# H3LIS331DL Register Map
H3LIS331DL_REG_WHOAMI					= 0x0F # Who Am I Register
H3LIS331DL_REG_CTRL1					= 0x20 # Control Register-1
H3LIS331DL_REG_CTRL2					= 0x21 # Control Register-2
H3LIS331DL_REG_CTRL3					= 0x22 # Control Register-3
H3LIS331DL_REG_CTRL4					= 0x23 # Control Register-4
H3LIS331DL_REG_CTRL5					= 0x24 # Control Register-5
H3LIS331DL_REG_REFERENCE				= 0x26 # Reference
H3LIS331DL_REG_STATUS					= 0x27 # Status Register
H3LIS331DL_REG_OUT_X_L					= 0x28 # X-Axis LSB
H3LIS331DL_REG_OUT_X_H					= 0x29 # X-Axis MSB
H3LIS331DL_REG_OUT_Y_L					= 0x2A # Y-Axis LSB
H3LIS331DL_REG_OUT_Y_H					= 0x2B # Y-Axis MSB
H3LIS331DL_REG_OUT_Z_L					= 0x2C # Z-Axis LSB
H3LIS331DL_REG_OUT_Z_H					= 0x2D # Z-Axis MSB

# Accl Datarate configuration
H3LIS331DL_ACCL_PM_PD					= 0x00 # Power down Mode
H3LIS331DL_ACCL_PM_NRMl					= 0x20 # Normal Mode
H3LIS331DL_ACCL_PM_0_5					= 0x40 # Low-Power Mode, ODR = 0.5Hz
H3LIS331DL_ACCL_PM_1					= 0x60 # Low-Power Mode, ODR = 1Hz
H3LIS331DL_ACCL_PM_2					= 0x80 # Low-Power Mode, ODR = 2Hz
H3LIS331DL_ACCL_PM_5					= 0xA0 # Low-Power Mode, ODR = 5Hz
H3LIS331DL_ACCL_PM_10					= 0xC0 # Low-Power Mode, ODR = 10Hz
H3LIS331DL_ACCL_DR_50					= 0x00 # ODR = 50Hz
H3LIS331DL_ACCL_DR_100					= 0x08 # ODR = 100Hz
H3LIS331DL_ACCL_DR_400					= 0x10 # ODR = 400Hz
H3LIS331DL_ACCL_DR_1000					= 0x18 # ODR = 1000Hz

# Accl Data update & Axis configuration
H3LIS331DL_ACCL_LPEN					= 0x00 # Normal Mode, Axis disabled
H3LIS331DL_ACCL_XAXIS					= 0x04 # X-Axis enabled
H3LIS331DL_ACCL_YAXIS					= 0x02 # Y-Axis enabled
H3LIS331DL_ACCL_ZAXIS					= 0x01 # Z-Axis enabled

# Acceleration Full-scale selection
H3LIS331DL_ACCL_BDU_CONT				= 0x00 # Continuous update, Normal Mode, 4-Wire Interface, LSB first
H3LIS331DL_ACCL_BDU_NOT_CONT			= 0x80 # Output registers not updated until MSB and LSB reading
H3LIS331DL_ACCL_BLE_MSB					= 0x40 # MSB first
H3LIS331DL_ACCL_RANGE_400G				= 0x30 # Full scale = +/-400g
H3LIS331DL_ACCL_RANGE_200G				= 0x10 # Full scale = +/-200g
H3LIS331DL_ACCL_RANGE_100G				= 0x00 # Full scale = +/-100g
H3LIS331DL_ACCL_SIM_3					= 0x01 # 3-Wire Interface

class H3LIS331DL():
	def __init__ (self):
		self.select_datarate()
		self.select_data_config()
	
	def select_datarate(self):
		"""Select the data rate of the accelerometer from the given provided values"""
		DATARATE_CONFIG = (H3LIS331DL_ACCL_PM_NRMl | H3LIS331DL_ACCL_DR_50 | H3LIS331DL_ACCL_XAXIS | H3LIS331DL_ACCL_YAXIS | H3LIS331DL_ACCL_ZAXIS)
		bus.write_byte_data(H3LIS331DL_DEFAULT_ADDRESS, H3LIS331DL_REG_CTRL1, DATARATE_CONFIG)
	
	def select_data_config(self):
		"""Select the data configuration of the accelerometer from the given provided values"""
		DATA_CONFIG = (H3LIS331DL_ACCL_RANGE_100G | H3LIS331DL_ACCL_BDU_CONT)
		bus.write_byte_data(H3LIS331DL_DEFAULT_ADDRESS, H3LIS331DL_REG_CTRL4, DATA_CONFIG)
	
	def read_accl(self):
		"""Read data back from H3LIS331DL_REG_OUT_X_L(0x28), 2 bytes
		X-Axis Accl LSB, X-Axis Accl MSB"""
		data0 = bus.read_byte_data(H3LIS331DL_DEFAULT_ADDRESS, H3LIS331DL_REG_OUT_X_L)
		data1 = bus.read_byte_data(H3LIS331DL_DEFAULT_ADDRESS, H3LIS331DL_REG_OUT_X_H)
		
		xAccl = data1 * 256 + data0
		if xAccl > 32767 :
			xAccl -= 65536
		
		"""Read data back from H3LIS331DL_REG_OUT_Y_L(0x2A), 2 bytes
		Y-Axis Accl LSB, Y-Axis Accl MSB"""
		data0 = bus.read_byte_data(H3LIS331DL_DEFAULT_ADDRESS, H3LIS331DL_REG_OUT_Y_L)
		data1 = bus.read_byte_data(H3LIS331DL_DEFAULT_ADDRESS, H3LIS331DL_REG_OUT_Y_H)
		
		yAccl = data1 * 256 + data0
		if yAccl > 32767 :
			yAccl -= 65536
		
		"""Read data back from H3LIS331DL_REG_OUT_Z_L(0x2C), 2 bytes
		Z-Axis Accl LSB, Z-Axis Accl MSB"""
		data0 = bus.read_byte_data(H3LIS331DL_DEFAULT_ADDRESS, H3LIS331DL_REG_OUT_Z_L)
		data1 = bus.read_byte_data(H3LIS331DL_DEFAULT_ADDRESS, H3LIS331DL_REG_OUT_Z_H)
		
		zAccl = data1 * 256 + data0
		if zAccl > 32767 :
			zAccl -= 65536
		
		return {'x' : xAccl, 'y' : yAccl, 'z' : zAccl}

from H3LIS331DL import H3LIS331DL
h3lis331dl = H3LIS331DL()

while True:
	h3lis331dl.select_datarate()
	h3lis331dl.select_data_config()
	time.sleep(0.2)
	accl = h3lis331dl.read_accl()
	print "Acceleration in X-Axis : %d" %(accl['x'])
	print "Acceleration in Y-Axis : %d" %(accl['y'])
	print "Acceleration in Z-Axis : %d" %(accl['z'])
	print " ************************************ "
	time.sleep(1)
