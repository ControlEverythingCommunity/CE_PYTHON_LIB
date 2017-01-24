# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# LIS331HH
# This code is designed to work with the LIS331HH_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Accelorometer?sku=LIS331HH_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
LIS331HH_DEFAULT_ADDRESS			= 0x18

# LIS331HH Register Map
LIS331HH_REG_CTRL1					= 0x20 # Control Register-1
LIS331HH_REG_CTRL2					= 0x21 # Control Register-2
LIS331HH_REG_CTRL3					= 0x22 # Control Register-3
LIS331HH_REG_CTRL4					= 0x23 # Control Register-4
LIS331HH_REG_CTRL5					= 0x24 # Control Register-5
LIS331HH_REG_REFERENCE				= 0x26 # Reference
LIS331HH_REG_STATUS					= 0x27 # Status Register
LIS331HH_REG_OUT_X_L				= 0x28 # X-Axis LSB
LIS331HH_REG_OUT_X_H				= 0x29 # X-Axis MSB
LIS331HH_REG_OUT_Y_L				= 0x2A # Y-Axis LSB
LIS331HH_REG_OUT_Y_H				= 0x2B # Y-Axis MSB
LIS331HH_REG_OUT_Z_L				= 0x2C # Z-Axis LSB
LIS331HH_REG_OUT_Z_H				= 0x2D # Z-Axis MSB

# Accl Datarate configuration
LIS331HH_ACCL_PM_PD					= 0x00 # Power down Mode
LIS331HH_ACCL_PM_NRMl				= 0x20 # Normal Mode
LIS331HH_ACCL_PM_0_5				= 0x40 # Low-Power Mode, ODR = 0.5Hz
LIS331HH_ACCL_PM_1					= 0x60 # Low-Power Mode, ODR = 1Hz
LIS331HH_ACCL_PM_2					= 0x80 # Low-Power Mode, ODR = 2Hz
LIS331HH_ACCL_PM_5					= 0xA0 # Low-Power Mode, ODR = 5Hz
LIS331HH_ACCL_PM_10					= 0xC0 # Low-Power Mode, ODR = 10Hz
LIS331HH_ACCL_DR_50					= 0x00 # ODR = 50Hz
LIS331HH_ACCL_DR_100				= 0x08 # ODR = 100Hz
LIS331HH_ACCL_DR_400				= 0x10 # ODR = 400Hz
LIS331HH_ACCL_DR_1000				= 0x18 # ODR = 1000Hz

# Accl Axis configuration
LIS331HH_ACCL_AXIS_DS				= 0x00 # Axis disabled
LIS331HH_ACCL_XAXIS					= 0x04 # X-Axis enabled
LIS331HH_ACCL_YAXIS					= 0x02 # Y-Axis enabled
LIS331HH_ACCL_ZAXIS					= 0x01 # Z-Axis enabled

# Acceleration Full-scale selection
LIS331HH_ACCL_BDU_CONT				= 0x00 # Continuous update, 4-Wire Interface
LIS331HH_ACCL_BDU_NOT_CONT			= 0x80 # Output registers not updated until MSB and LSB reading
LIS331HH_ACCL_BLE_MSB				= 0x40 # MSB first
LIS331HH_ACCL_RANGE_24G				= 0x30 # Full scale = +/-24g
LIS331HH_ACCL_RANGE_12G				= 0x10 # Full scale = +/-12g
LIS331HH_ACCL_RANGE_6G				= 0x00 # Full scale = +/-6g, LSB first
LIS331HH_ACCL_ST_SIGH_P				= 0x00 # Self Test Plus
LIS331HH_ACCL_ST_SIGH_M				= 0x08 # Self Test Minus
LIS331HH_ACCL_ST_EN					= 0x02 # Self Test enabled
LIS331HH_ACCL_ST_DS					= 0x00 # Self Test disabled
LIS331HH_ACCL_SIM_3					= 0x01 # 3-Wire Interface


class LIS331HH():
	def __init__ (self):
		self.select_datarate()
		self.select_data_config()
	
	def select_datarate(self):
		"""Select the data rate of the accelerometer from the given provided values"""
		DATARATE_CONFIG = (LIS331HH_ACCL_PM_NRMl | LIS331HH_ACCL_DR_50 | LIS331HH_ACCL_XAXIS | LIS331HH_ACCL_YAXIS | LIS331HH_ACCL_ZAXIS)
		bus.write_byte_data(LIS331HH_DEFAULT_ADDRESS, LIS331HH_REG_CTRL1, DATARATE_CONFIG)
	
	def select_data_config(self):
		"""Select the data configuration of the accelerometer from the given provided values"""
		DATA_CONFIG = (LIS331HH_ACCL_RANGE_6G | LIS331HH_ACCL_BDU_CONT | LIS331HH_ACCL_ST_DS)
		bus.write_byte_data(LIS331HH_DEFAULT_ADDRESS, LIS331HH_REG_CTRL4, DATA_CONFIG)
	
	def read_accl(self):
		"""Read data back from LIS331HH_REG_OUT_X_L(0x28), 2 bytes
		X-Axis Accl LSB, X-Axis Accl MSB"""
		data0 = bus.read_byte_data(LIS331HH_DEFAULT_ADDRESS, LIS331HH_REG_OUT_X_L)
		data1 = bus.read_byte_data(LIS331HH_DEFAULT_ADDRESS, LIS331HH_REG_OUT_X_H)
		
		xAccl = data1 * 256 + data0
		if xAccl > 32767 :
			xAccl -= 65536
		
		"""Read data back from LIS331HH_REG_OUT_Y_L(0x2A), 2 bytes
		Y-Axis Accl LSB, Y-Axis Accl MSB"""
		data0 = bus.read_byte_data(LIS331HH_DEFAULT_ADDRESS, LIS331HH_REG_OUT_Y_L)
		data1 = bus.read_byte_data(LIS331HH_DEFAULT_ADDRESS, LIS331HH_REG_OUT_Y_H)
		
		yAccl = data1 * 256 + data0
		if yAccl > 32767 :
			yAccl -= 65536
		
		"""Read data back from LIS331HH_REG_OUT_Z_L(0x2C), 2 bytes
		Z-Axis Accl LSB, Z-Axis Accl MSB"""
		data0 = bus.read_byte_data(LIS331HH_DEFAULT_ADDRESS, LIS331HH_REG_OUT_Z_L)
		data1 = bus.read_byte_data(LIS331HH_DEFAULT_ADDRESS, LIS331HH_REG_OUT_Z_H)
		
		zAccl = data1 * 256 + data0
		if zAccl > 32767 :
			zAccl -= 65536
		
		return {'x' : xAccl, 'y' : yAccl, 'z' : zAccl}

from LIS331HH import LIS331HH
lis331hh = LIS331HH()

while True:
	lis331hh.select_datarate()
	lis331hh.select_data_config()
	time.sleep(0.1)
	accl = lis331hh.read_accl()
	print "Acceleration in X-Axis : %d" %(accl['x'])
	print "Acceleration in Y-Axis : %d" %(accl['y'])
	print "Acceleration in Z-Axis : %d" %(accl['z'])
	print " ************************************ "
	time.sleep(1)
