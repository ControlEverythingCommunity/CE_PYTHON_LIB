# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# LSM330
# This code is designed to work with the LSM330_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Accelorometer?sku=LSM330_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
LSM330_ACCL_ADDRESS			= 0x1D
LSM330_GYRO_ADDRESS			= 0x6A

# LSM330 gyrometer registers
LSM330_WHO_AM_I_G				= 0x0F
LSM330_CTRL_REG1_G				= 0x20
LSM330_CTRL_REG4_G				= 0x23
LSM330_OUT_X_L_G				= 0x28
LSM330_OUT_X_H_G				= 0x29
LSM330_OUT_Y_L_G				= 0x2A
LSM330_OUT_Y_H_G				= 0x2B
LSM330_OUT_Z_L_G				= 0x2C
LSM330_OUT_Z_H_G				= 0x2D

# Gyro Datarate & Bandwidth configuration
LSM330_GYRO_DR_95				= 0x00 # ODR = 95 Hz
LSM330_GYRO_DR_190				= 0x40 # ODR = 190 Hz
LSM330_GYRO_DR_380				= 0x80 # ODR = 380 Hz
LSM330_GYRO_DR_760				= 0xC0 # ODR = 760 Hz
LSM330_GYRO_BW_12_5				= 0x00 # Cutoff = 12.5
LSM330_GYRO_BW_25				= 0x10 # Cutoff = 25
LSM330_GYRO_BW_50				= 0x20 # Cutoff = 50
LSM330_GYRO_BW_70				= 0x30 # Cutoff = 70

# Gyro Power & Axis configuration
LSM330_GYRO_PD					= 0x00 # Power down mode, Axis disabled
LSM330_GYRO_ND					= 0x08 # Normal mode
LSM330_GYRO_XAXIS				= 0x04 # X-Axis enabled
LSM330_GYRO_YAXIS				= 0x02 # Y-Axis enabled
LSM330_GYRO_ZAXIS				= 0x01 # Z-Axis enabled

# Gyro Full-scale selection & Mode configuration
LSM330_GYRO_DEFAULT				= 0x00 # Continuous update, LSB first, Normal mode
LSM330_GYRO_BDU					= 0x80 # Output registers not updated until MSB and LSB read
LSM330_GYRO_BLE_MSB				= 0x40 # MSB first
LSM330_GYRO_SCALE_245			= 0x00 # 245 dps
LSM330_GYRO_SCALE_500			= 0x10 # 500 dps
LSM330_GYRO_SCALE_2000			= 0x20 # 2000 dps
LSM330_GYRO_ST_0				= 0x02 # Self-Test 0
LSM330_GYRO_ST_1				= 0x06 # Self-Test 1

# LSM330 Accelerometer register
LSM330_WHO_AM_I_A				= 0x0F
LSM330_CTRL_REG4_A				= 0x23
LSM330_CTRL_REG5_A				= 0x20
LSM330_CTRL_REG6_A				= 0x24
LSM330_CTRL_REG7_A				= 0x25
LSM330_OUT_X_L_A				= 0x28
LSM330_OUT_X_H_A				= 0x29
LSM330_OUT_Y_L_A				= 0x2A
LSM330_OUT_Y_H_A				= 0x2B
LSM330_OUT_Z_L_A				= 0x2C
LSM330_OUT_Z_H_A				= 0x2D

# Accl Datarate configuration
LSM330_ACCL_DR_PD				= 0x00 # Power down mode
LSM330_ACCL_DR_3_125			= 0x10 # ODR = 3.125 Hz
LSM330_ACCL_DR_6_25				= 0x20 # ODR = 6.25 Hz
LSM330_ACCL_DR_12_5				= 0x30 # ODR = 12.5 Hz
LSM330_ACCL_DR_25				= 0x40 # ODR = 25 Hz
LSM330_ACCL_DR_50				= 0x50 # ODR = 50 Hz
LSM330_ACCL_DR_100				= 0x60 # ODR = 100 Hz
LSM330_ACCL_DR_200				= 0x70 # ODR = 200 Hz
LSM330_ACCL_DR_400				= 0x80 # ODR = 400 Hz
LSM330_ACCL_DR_800				= 0x90 # ODR = 800 Hz
LSM330_ACCL_DR_1600				= 0xA0 # ODR = 1600 Hz

# Accl Data update & Axis configuration
LSM330_ACCL_BDU					= 0x00 # Continuous update, Axis disabled
LSM330_ACCL_XAXIS				= 0x04 # X-Axis enabled
LSM330_ACCL_YAXIS				= 0x02 # Y-Axis enabled
LSM330_ACCL_ZAXIS				= 0x01 # Z-Axis enabled

# Acceleration Full-scale selection
LSM330_ACCL_RANGE_2G			= 0x00 # Full scale = +/-2g
LSM330_ACCL_RANGE_4G			= 0x08 # Full scale = +/-4g
LSM330_ACCL_RANGE_6G			= 0x10 # Full scale = +/-6g
LSM330_ACCL_RANGE_8G			= 0x18 # Full scale = +/-8g
LSM330_ACCL_RANGE_16G			= 0x20 # Full scale = +/-16g

class LSM330():
	def gyro_datarate(self):
		"""Select the data rate of the gyroscope from the given provided values"""
		GYRO_DATARATE = (LSM330_GYRO_DR_95 | LSM330_GYRO_BW_12_5 | LSM330_GYRO_ND | LSM330_GYRO_XAXIS | LSM330_GYRO_YAXIS | LSM330_GYRO_ZAXIS)
		bus.write_byte_data(LSM330_GYRO_ADDRESS, LSM330_CTRL_REG1_G, GYRO_DATARATE)
	
	def gyro_scale_selection(self):
		"""Select the full-scale values of the gyroscope from the given provided values"""
		GYRO_SCALE = (LSM330_GYRO_DEFAULT | LSM330_GYRO_SCALE_2000)
		bus.write_byte_data(LSM330_GYRO_ADDRESS, LSM330_CTRL_REG4_G, GYRO_SCALE)
	
	def readgyro(self):
		"""Read data back from LSM330_OUT_X_L_G(0x28), 2 bytes
		X-Axis Mag LSB, X-Axis Mag MSB"""
		data0 = bus.read_byte_data(LSM330_GYRO_ADDRESS, LSM330_OUT_X_L_G)
		data1 = bus.read_byte_data(LSM330_GYRO_ADDRESS, LSM330_OUT_X_H_G)
		
		xGyro = data1 * 256 + data0
		if xGyro > 32767 :
			xGyro -= 65536
		
		"""Read data back from LSM330_OUT_Y_L_G(0x2A), 2 bytes
		Y-Axis Mag LSB, Y-Axis Mag MSB"""
		data0 = bus.read_byte_data(LSM330_GYRO_ADDRESS, LSM330_OUT_Y_L_G)
		data1 = bus.read_byte_data(LSM330_GYRO_ADDRESS, LSM330_OUT_Y_H_G)
		
		yGyro = data1 * 256 + data0
		if yGyro > 32767 :
			yGyro -= 65536
		
		"""Read data back from LSM330_OUT_Z_L_G(0x2C), 2 bytes
		Z-Axis Mag LSB, Z-Axis Mag MSB"""
		data0 = bus.read_byte_data(LSM330_GYRO_ADDRESS, LSM330_OUT_Z_L_G)
		data1 = bus.read_byte_data(LSM330_GYRO_ADDRESS, LSM330_OUT_Z_H_G)
		
		zGyro = data1 * 256 + data0
		if zGyro > 32767 :
			zGyro -= 65536
		
		return {'x' : xGyro, 'y' : yGyro, 'z' : zGyro}
	
	def accl_datarate(self):
		"""Select the data rate of the accelerometer from the given provided values"""
		ACCL_DATARATE = (LSM330_ACCL_DR_100 | LSM330_ACCL_XAXIS | LSM330_ACCL_YAXIS | LSM330_ACCL_ZAXIS)
		bus.write_byte_data(LSM330_ACCL_ADDRESS, LSM330_CTRL_REG5_A, ACCL_DATARATE)
	
	def accl_scale_selection(self):
		"""Select the full-scale values of the accelerometer from the given provided values"""
		bus.write_byte_data(LSM330_ACCL_ADDRESS, LSM330_CTRL_REG4_A, LSM330_ACCL_RANGE_2G)
	
	def readaccl(self):
		"""Read data back from LSM330_OUT_X_L_A(0x28), 2 bytes
		X-Axis Mag LSB, X-Axis Mag MSB"""
		data0 = bus.read_byte_data(LSM330_ACCL_ADDRESS, LSM330_OUT_X_L_A)
		data1 = bus.read_byte_data(LSM330_ACCL_ADDRESS, LSM330_OUT_X_H_A)
		
		xAccl = data1 * 256 + data0
		if xAccl > 32767 :
			xAccl -= 65536
		
		"""Read data back from LSM330_OUT_Y_L_M(0x2A), 2 bytes
		Y-Axis Mag LSB, Y-Axis Mag MSB"""
		data0 = bus.read_byte_data(LSM330_ACCL_ADDRESS, LSM330_OUT_Y_L_A)
		data1 = bus.read_byte_data(LSM330_ACCL_ADDRESS, LSM330_OUT_Y_H_A)
		
		yAccl = data1 * 256 + data0
		if yAccl > 32767 :
			yAccl -= 65536
		
		"""Read data back from LSM330_OUT_Z_L_M(0x2C), 2 bytes
		Z-Axis Mag LSB, Z-Axis Mag MSB"""
		data0 = bus.read_byte_data(LSM330_ACCL_ADDRESS, LSM330_OUT_Z_L_A)
		data1 = bus.read_byte_data(LSM330_ACCL_ADDRESS, LSM330_OUT_Z_H_A)
		
		zAccl = data1 * 256 + data0
		if zAccl > 32767 :
			zAccl -= 65536
		
		return {'x' : xAccl, 'y' : yAccl, 'z' : zAccl}

from LSM330 import LSM330
lsm330 = LSM330()

while True:
	lsm330.gyro_datarate()
	lsm330.gyro_scale_selection()
	gyro = lsm330.readgyro()
	print "X-Axis of Rotation : %d"%(gyro['x'])
	print "Y-Axis of Rotation : %d"%(gyro['y'])
	print "Z-Axis of Rotation : %d"%(gyro['z'])
	lsm330.accl_datarate()
	lsm330.accl_scale_selection()
	accl = lsm330.readaccl()
	print "Acceleration in X-Axis : %d"%(accl['x'])
	print "Acceleration in Y-Axis : %d"%(accl['y'])
	print "Acceleration in Z-Axis : %d"%(accl['z'])
	print " ************************************* "
	time.sleep(1)
