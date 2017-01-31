# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# LSM303DLHC
# This code is designed to work with the LSM303DLHC_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/products

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
LSM303DHLC_MAG_ADDRESS				= 0x1E
LSM303DHLC_ACCL_ADDRESS				= 0x19

# LSM303DHLC Accelerometer register
LSM303DHLC_CTRL_REG1_A				= 0x20
LSM303DHLC_CTRL_REG4_A				= 0x23
LSM303DHLC_OUT_X_L_A				= 0x28
LSM303DHLC_OUT_X_H_A				= 0x29
LSM303DHLC_OUT_Y_L_A				= 0x2A
LSM303DHLC_OUT_Y_H_A				= 0x2B
LSM303DHLC_OUT_Z_L_A				= 0x2C
LSM303DHLC_OUT_Z_H_A				= 0x2D

# Accl Datarate configuration
LSM303DHLC_ACCL_DR_PD				= 0x00 # Power down mode
LSM303DHLC_ACCL_DR_1				= 0x10 # ODR = 1 Hz
LSM303DHLC_ACCL_DR_10				= 0x20 # ODR = 10 Hz
LSM303DHLC_ACCL_DR_25				= 0x30 # ODR = 25 Hz
LSM303DHLC_ACCL_DR_50				= 0x40 # ODR = 50 Hz
LSM303DHLC_ACCL_DR_100				= 0x50 # ODR = 100 Hz
LSM303DHLC_ACCL_DR_200				= 0x60 # ODR = 200 Hz
LSM303DHLC_ACCL_DR_400				= 0x70 # ODR = 400 Hz
LSM303DHLC_ACCL_DR_1620				= 0x80 # ODR = 1.620 KHz
LSM303DHLC_ACCL_DR_1344				= 0x90 # ODR = 1.344 KHz

# Accl Data update & Axis configuration
LSM303DHLC_ACCL_LPEN				= 0x00 # Normal Mode, Axis disabled
LSM303DHLC_ACCL_XAXIS				= 0x04 # X-Axis enabled
LSM303DHLC_ACCL_YAXIS				= 0x02 # Y-Axis enabled
LSM303DHLC_ACCL_ZAXIS				= 0x01 # Z-Axis enabled

# Acceleration Full-scale selection
LSM303DHLC_ACCL_RANGE_2G			= 0x00 # Full scale = +/-2g, LSB first
LSM303DHLC_ACCL_RANGE_4G			= 0x10 # Full scale = +/-4g
LSM303DHLC_ACCL_RANGE_8G			= 0x20 # Full scale = +/-8g
LSM303DHLC_ACCL_RANGE_16G			= 0x30 # Full scale = +/-16g
LSM303DHLC_GYRO_BLE_MSB				= 0x40 # MSB first

# LSM303DHLC Magnetometer addresses
LSM303DHLC_CRA_REG_M				= 0x00
LSM303DHLC_CRB_REG_M				= 0x01
LSM303DHLC_MR_REG_M					= 0x02
LSM303DHLC_OUT_X_H_M				= 0x03
LSM303DHLC_OUT_X_L_M				= 0x04
LSM303DHLC_OUT_Y_H_M				= 0x07
LSM303DHLC_OUT_Y_L_M				= 0x08
LSM303DHLC_OUT_Z_H_M				= 0x05
LSM303DHLC_OUT_Z_L_M				= 0x06

# Magnetic Datarate configuration
LSM303DHLC_MAG_TEMP_DS				= 0x00 # Temperature disabled, ODR = 0.75 Hz
LSM303DHLC_MAG_TEMP_EN				= 0x80 # Temperature enabled
LSM303DHLC_MAG_DR_1_5				= 0x04 # ODR = 1.5 Hz
LSM303DHLC_MAG_DR_3					= 0x08 # ODR = 3.0 hz
LSM303DHLC_MAG_DR_7_5				= 0x0C # ODR = 7.5 Hz
LSM303DHLC_MAG_DR_15				= 0x10 # ODR = 15 Hz
LSM303DHLC_MAG_DR_30				= 0x14 # ODR = 30 Hz
LSM303DHLC_MAG_DR_75				= 0x18 # ODR = 75 Hz
LSM303DHLC_MAG_DR_220				= 0x1C # ODR = 220 Hz

# Magnetic Full-scale selection
LSM303DHLC_MAG_GAIN_1_3				= 0x20 # +/- 1.3 gauss
LSM303DHLC_MAG_GAIN_1_9				= 0x40 # +/- 1.9 gauss
LSM303DHLC_MAG_GAIN_2_5				= 0x60 # +/- 2.5 gauss
LSM303DHLC_MAG_GAIN_4				= 0x80 # +/- 4.0 gauss
LSM303DHLC_MAG_GAIN_4_7				= 0xA0 # +/- 4.7 gauss
LSM303DHLC_MAG_GAIN_5_6				= 0xC0 # +/- 5.6 gauss
LSM303DHLC_MAG_GAIN_8_1				= 0xE0 # +/- 8.1 gauss

# Magnetic Mode selection
LSM303DHLC_MAG_MODE_CNTS			= 0x00 # Continuous-conversion mode
LSM303DHLC_MAG_MODE_SNGL			= 0x01 # Single-conversion mode
LSM303DHLC_MAG_MODE_PWR_DWN			= 0x02 # Sleep mode

class LSM303DHLC():
	def accl_datarate(self):
		"""Select the data rate of the accelerometer from the given provided values"""
		ACCL_DATARATE = (LSM303DHLC_ACCL_DR_10 | LSM303DHLC_ACCL_XAXIS | LSM303DHLC_ACCL_YAXIS | LSM303DHLC_ACCL_ZAXIS)
		bus.write_byte_data(LSM303DHLC_ACCL_ADDRESS, LSM303DHLC_CTRL_REG1_A, ACCL_DATARATE)
	
	def accl_scale_selection(self):
		"""Select the full-scale values of the accelerometer from the given provided values"""
		ACCL_SCALE = (LSM303DHLC_ACCL_RANGE_2G)
		bus.write_byte_data(LSM303DHLC_ACCL_ADDRESS, LSM303DHLC_CTRL_REG4_A, ACCL_SCALE)
	
	def readaccl(self):
		"""Read data back from LSM303DHLC_OUT_X_L_A(0x28), 2 bytes
		X-Axis Mag LSB, X-Axis Mag MSB"""
		data0 = bus.read_byte_data(LSM303DHLC_ACCL_ADDRESS, LSM303DHLC_OUT_X_L_A)
		data1 = bus.read_byte_data(LSM303DHLC_ACCL_ADDRESS, LSM303DHLC_OUT_X_H_A)
		
		xAccl = data1 * 256 + data0
		if xAccl > 32767 :
			xAccl -= 65536
		
		"""Read data back from LSM303DHLC_OUT_Y_L_M(0x2A), 2 bytes
		Y-Axis Mag LSB, Y-Axis Mag MSB"""
		data0 = bus.read_byte_data(LSM303DHLC_ACCL_ADDRESS, LSM303DHLC_OUT_Y_L_A)
		data1 = bus.read_byte_data(LSM303DHLC_ACCL_ADDRESS, LSM303DHLC_OUT_Y_H_A)
		
		yAccl = data1 * 256 + data0
		if yAccl > 32767 :
			yAccl -= 65536
		
		"""Read data back from LSM303DHLC_OUT_Z_L_M(0x2C), 2 bytes
		Z-Axis Mag LSB, Z-Axis Mag MSB"""
		data0 = bus.read_byte_data(LSM303DHLC_ACCL_ADDRESS, LSM303DHLC_OUT_Z_L_A)
		data1 = bus.read_byte_data(LSM303DHLC_ACCL_ADDRESS, LSM303DHLC_OUT_Z_H_A)
		
		zAccl = data1 * 256 + data0
		if zAccl > 32767 :
			zAccl -= 65536
		
		return {'x' : xAccl, 'y' : yAccl, 'z' : zAccl}
	
	def mag_datarate(self):
		"""Select the data rate of the magnetometer from the given provided values"""
		MAG_DATARATE = (LSM303DHLC_MAG_DR_15)
		bus.write_byte_data(LSM303DHLC_MAG_ADDRESS, LSM303DHLC_CRA_REG_M, MAG_DATARATE)
	
	def mag_scale_selection(self):
		"""Select the full-scale values of the magnetometer from the given provided values"""
		bus.write_byte_data(LSM303DHLC_MAG_ADDRESS, LSM303DHLC_CRB_REG_M, LSM303DHLC_MAG_GAIN_1_3)
	
	def mag_mode_selection(self):
		"""Select the modes of the magnetometer from the given provided values"""
		bus.write_byte_data(LSM303DHLC_MAG_ADDRESS, LSM303DHLC_MR_REG_M, LSM303DHLC_MAG_MODE_CNTS)
	
	def readmag(self):
		"""Read data back from LSM303DHLC_OUT_X_L_M(0x03), 2 bytes
		X-Axis Mag LSB, X-Axis Mag MSB"""
		data0 = bus.read_byte_data(LSM303DHLC_MAG_ADDRESS, LSM303DHLC_OUT_X_H_M,)
		data1 = bus.read_byte_data(LSM303DHLC_MAG_ADDRESS, LSM303DHLC_OUT_X_L_M,)
		
		xMag = data0 * 256 + data1
		if xMag > 32767 :
			xMag -= 65536
		
		"""Read data back from LSM303DHLC_OUT_Z_L_M(0x05), 2 bytes
		Z-Axis Mag LSB, Z-Axis Mag MSB"""
		data0 = bus.read_byte_data(LSM303DHLC_MAG_ADDRESS, LSM303DHLC_OUT_Z_H_M,)
		data1 = bus.read_byte_data(LSM303DHLC_MAG_ADDRESS, LSM303DHLC_OUT_Z_L_M,)
		
		zMag = data0 * 256 + data1
		if zMag > 32767 :
			zMag -= 65536
		
		"""Read data back from LSM303DHLC_OUT_Y_L_M(0x06), 2 bytes
		Y-Axis Mag LSB, Y-Axis Mag MSB"""
		data0 = bus.read_byte_data(LSM303DHLC_MAG_ADDRESS, LSM303DHLC_OUT_Y_H_M,)
		data1 = bus.read_byte_data(LSM303DHLC_MAG_ADDRESS, LSM303DHLC_OUT_Y_L_M,)
		
		yMag = data0 * 256 + data1
		if yMag > 32767 :
			yMag -= 65536
		
		return {'x' : xMag, 'y' : yMag, 'z' : zMag}

from LSM303DHLC import LSM303DHLC
lsm303dhlc = LSM303DHLC()

while True:
	lsm303dhlc.accl_datarate()
	lsm303dhlc.accl_scale_selection()
	accl = lsm303dhlc.readaccl()
	print "Acceleration in X-Axis : %d"%(accl['x'])
	print "Acceleration in Y-Axis : %d"%(accl['y'])
	print "Acceleration in Z-Axis : %d"%(accl['z'])
	lsm303dhlc.mag_datarate()
	lsm303dhlc.mag_scale_selection()
	lsm303dhlc.mag_mode_selection()
	mag = lsm303dhlc.readmag()
	print "Magnetic field in X-Axis : %d"%(mag['x'])
	print "Magnetic field in Y-Axis : %d"%(mag['y'])
	print "Magnetic field in Z-Axis : %d"%(mag['z'])
	print " ************************************* "
	time.sleep(0.8)
