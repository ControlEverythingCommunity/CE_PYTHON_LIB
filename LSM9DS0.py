# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# LSM9DS0
# This code is designed to work with the LSM9DS0_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Accelorometer?sku=LSM9DS0_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
LSM9DS0_MAG_ADDRESS				= 0x1E
LSM9DS0_ACCL_ADDRESS			= 0x1E
LSM9DS0_GYRO_ADDRESS			= 0x6A

# LSM9DS0 gyrometer registers
LSM9DS0_WHO_AM_I_G				= 0x0F
LSM9DS0_CTRL_REG1_G				= 0x20
LSM9DS0_CTRL_REG4_G				= 0x23
LSM9DS0_OUT_X_L_G				= 0x28
LSM9DS0_OUT_X_H_G				= 0x29
LSM9DS0_OUT_Y_L_G				= 0x2A
LSM9DS0_OUT_Y_H_G				= 0x2B
LSM9DS0_OUT_Z_L_G				= 0x2C
LSM9DS0_OUT_Z_H_G				= 0x2D

# Gyro Datarate & Bandwidth configuration
LSM9DS0_GYRO_DR_95				= 0x00 # ODR = 95 Hz
LSM9DS0_GYRO_DR_190				= 0x40 # ODR = 190 Hz
LSM9DS0_GYRO_DR_380				= 0x80 # ODR = 380 Hz
LSM9DS0_GYRO_DR_760				= 0xC0 # ODR = 760 Hz
LSM9DS0_GYRO_BW_12_5			= 0x00 # Cutoff = 12.5
LSM9DS0_GYRO_BW_25				= 0x10 # Cutoff = 25
LSM9DS0_GYRO_BW_50				= 0x20 # Cutoff = 50
LSM9DS0_GYRO_BW_70				= 0x30 # Cutoff = 70

# Gyro Power & Axis configuration
LSM9DS0_GYRO_PD					= 0x00 # Power down mode, Axis disabled
LSM9DS0_GYRO_ND					= 0x08 # Normal mode
LSM9DS0_GYRO_XAXIS				= 0x04 # X-Axis enabled
LSM9DS0_GYRO_YAXIS				= 0x02 # Y-Axis enabled
LSM9DS0_GYRO_ZAXIS				= 0x01 # Z-Axis enabled

# Gyro Full-scale selection & Mode configuration
LSM9DS0_GYRO_DEFAULT			= 0x00 # Continuous update, LSB first, Normal mode
LSM9DS0_GYRO_BDU				= 0x80 # Output registers not updated until MSB and LSB read
LSM9DS0_GYRO_BLE_MSB			= 0x40 # MSB first
LSM9DS0_GYRO_SCALE_245			= 0x00 # 245 dps
LSM9DS0_GYRO_SCALE_500			= 0x10 # 500 dps
LSM9DS0_GYRO_SCALE_2000			= 0x20 # 2000 dps
LSM9DS0_GYRO_ST_0				= 0x02 # Self-Test 0
LSM9DS0_GYRO_ST_1				= 0x06 # Self-Test 1

# Magnetometer addresses
LSM9DS0_STATUS_REG_M			= 0x07
LSM9DS0_OUT_X_L_M				= 0x08
LSM9DS0_OUT_X_H_M				= 0x09
LSM9DS0_OUT_Y_L_M				= 0x0A
LSM9DS0_OUT_Y_H_M				= 0x0B
LSM9DS0_OUT_Z_L_M				= 0x0C
LSM9DS0_OUT_Z_H_M				= 0x0D

# Shared addresses between Magnetometer & Accelerometer
LSM9DS0_WHO_AM_I_XM				= 0x0F
LSM9DS0_CTRL_REG1_XM			= 0x20
LSM9DS0_CTRL_REG2_XM			= 0x21
LSM9DS0_CTRL_REG5_XM			= 0x24
LSM9DS0_CTRL_REG6_XM			= 0x25
LSM9DS0_CTRL_REG7_XM			= 0x26

# Accelerometer addresses
LSM9DS0_OUT_X_L_A				= 0x28
LSM9DS0_OUT_X_H_A				= 0x29
LSM9DS0_OUT_Y_L_A				= 0x2A
LSM9DS0_OUT_Y_H_A				= 0x2B
LSM9DS0_OUT_Z_L_A				= 0x2C
LSM9DS0_OUT_Z_H_A				= 0x2D

# Accl Datarate configuration
LSM9DS0_ACCL_DR_PD				= 0x00 # Power down mode
LSM9DS0_ACCL_DR_3_125			= 0x10 # ODR = 3.125 Hz
LSM9DS0_ACCL_DR_6_25			= 0x20 # ODR = 6.25 Hz
LSM9DS0_ACCL_DR_12_5			= 0x30 # ODR = 12.5 Hz
LSM9DS0_ACCL_DR_25				= 0x40 # ODR = 25 Hz
LSM9DS0_ACCL_DR_50				= 0x50 # ODR = 50 Hz
LSM9DS0_ACCL_DR_100				= 0x60 # ODR = 100 Hz
LSM9DS0_ACCL_DR_200				= 0x70 # ODR = 200 Hz
LSM9DS0_ACCL_DR_400				= 0x80 # ODR = 400 Hz
LSM9DS0_ACCL_DR_800				= 0x90 # ODR = 800 Hz
LSM9DS0_ACCL_DR_1600			= 0xA0 # ODR = 1600 Hz

# Accl Data update & Axis configuration
LSM9DS0_ACCL_BDU				= 0x00 # Continuous update, Axis disabled
LSM9DS0_ACCL_XAXIS				= 0x04 # X-Axis enabled
LSM9DS0_ACCL_YAXIS				= 0x02 # Y-Axis enabled
LSM9DS0_ACCL_ZAXIS				= 0x01 # Z-Axis enabled

# Acceleration Full-scale selection
LSM9DS0_ACCL_RANGE_2G			= 0x00 # Full scale = +/-2g
LSM9DS0_ACCL_RANGE_4G			= 0x08 # Full scale = +/-4g
LSM9DS0_ACCL_RANGE_6G			= 0x10 # Full scale = +/-6g
LSM9DS0_ACCL_RANGE_8G			= 0x18 # Full scale = +/-8g
LSM9DS0_ACCL_RANGE_16G			= 0x20 # Full scale = +/-16g

# Magnetic Datarate configuration
LSM9DS0_MAG_DR_3_125			= 0x00 # ODR = 3.125 Hz
LSM9DS0_MAG_DR_6_25				= 0x04 # ODR = 6.25 hz
LSM9DS0_MAG_DR_12_5				= 0x08 # ODR = 12.5 Hz
LSM9DS0_MAG_DR_25				= 0x0C # ODR = 25 Hz
LSM9DS0_MAG_DR_50				= 0x10 # ODR = 50 Hz
LSM9DS0_MAG_DR_100				= 0x14 # ODR = 100 Hz

# Magnetic Temperature & Resolution configuration
LSM9DS0_MAG_TEMP_DEF			= 0x00 # Temperature disabled, Low Resolution
LSM9DS0_MAG_TEMP_EN				= 0x80 # Temperature enabled
LSM9DS0_MAG_RES_H				= 0x60 # High Resolution

# Magnetic Full-scale selection
LSM9DS0_MAG_GAIN_2				= 0x00 # +/- 2 gauss
LSM9DS0_MAG_GAIN_4				= 0x20 # +/- 4 gauss
LSM9DS0_MAG_GAIN_8				= 0x40 # +/- 8 gauss
LSM9DS0_MAG_GAIN_12				= 0x60 # +/- 12 gauss

# Magnetic Mode selection
LSM9DS0_MAG_FILTER_NRML			= 0x00 # Normal Mode
LSM9DS0_MAG_FILTER_REF			= 0x40 # Reference signal for filtering
LSM9DS0_MAG_FILTER_RST			= 0xC0 # Autoreset on interrupt event
LSM9DS0_MAG_MODE_CNTS			= 0x00 # Continuous-conversion mode
LSM9DS0_MAG_MODE_SNGL			= 0x01 # Single-conversion mode
LSM9DS0_MAG_MODE_PWR_DWN		= 0x02 # Power-down mode

class LSM9DS0():
	def __init__(self):
		self.gyro_datarate()
		self.gyro_scale_selection()
		self.accl_datarate()
		self.accl_scale_selection()
		self.mag_datarate()
		self.mag_scale_selection()
		self.mag_mode_selection()
	
	def gyro_datarate(self):
		"""Select the data rate of the gyroscope from the given provided values"""
		GYRO_DATARATE = (LSM9DS0_GYRO_DR_95 | LSM9DS0_GYRO_BW_12_5 | LSM9DS0_GYRO_ND | LSM9DS0_GYRO_XAXIS | LSM9DS0_GYRO_YAXIS | LSM9DS0_GYRO_ZAXIS)
		bus.write_byte_data(LSM9DS0_GYRO_ADDRESS, LSM9DS0_CTRL_REG1_G, GYRO_DATARATE)
	
	def gyro_scale_selection(self):
		"""Select the full-scale values of the gyroscope from the given provided values"""
		GYRO_SCALE = (LSM9DS0_GYRO_DEFAULT | LSM9DS0_GYRO_SCALE_2000)
		bus.write_byte_data(LSM9DS0_GYRO_ADDRESS, LSM9DS0_CTRL_REG4_G, GYRO_SCALE)
	
	time.sleep(0.5)
	
	def readgyro(self):
		"""Read data back from LSM9DS0_OUT_X_L_G(0x28), 2 bytes
		X-Axis Mag LSB, X-Axis Mag MSB"""
		data0 = bus.read_byte_data(LSM9DS0_GYRO_ADDRESS, LSM9DS0_OUT_X_L_G)
		data1 = bus.read_byte_data(LSM9DS0_GYRO_ADDRESS, LSM9DS0_OUT_X_H_G)
		
		xGyro = data1 * 256 + data0
		if xGyro > 32767 :
			xGyro -= 65536
		
		"""Read data back from LSM9DS0_OUT_Y_L_G(0x2A), 2 bytes
		Y-Axis Mag LSB, Y-Axis Mag MSB"""
		data0 = bus.read_byte_data(LSM9DS0_GYRO_ADDRESS, LSM9DS0_OUT_Y_L_G)
		data1 = bus.read_byte_data(LSM9DS0_GYRO_ADDRESS, LSM9DS0_OUT_Y_H_G)
		
		yGyro = data1 * 256 + data0
		if yGyro > 32767 :
			yGyro -= 65536
		
		"""Read data back from LSM9DS0_OUT_Z_L_G(0x2C), 2 bytes
		Z-Axis Mag LSB, Z-Axis Mag MSB"""
		data0 = bus.read_byte_data(LSM9DS0_GYRO_ADDRESS, LSM9DS0_OUT_Z_L_G)
		data1 = bus.read_byte_data(LSM9DS0_GYRO_ADDRESS, LSM9DS0_OUT_Z_H_G)
		
		zGyro = data1 * 256 + data0
		if zGyro > 32767 :
			zGyro -= 65536
		
		return {'x' : xGyro, 'y' : yGyro, 'z' : zGyro}
	
	def accl_datarate(self):
		"""Select the data rate of the accelerometer from the given provided values"""
		ACCL_DATARATE = (LSM9DS0_ACCL_DR_100 | LSM9DS0_ACCL_XAXIS | LSM9DS0_ACCL_YAXIS | LSM9DS0_ACCL_ZAXIS)
		bus.write_byte_data(LSM9DS0_ACCL_ADDRESS, LSM9DS0_CTRL_REG1_XM, ACCL_DATARATE)
	
	def accl_scale_selection(self):
		"""Select the full-scale values of the accelerometer from the given provided values"""
		ACCL_SCALE = (LSM9DS0_ACCL_RANGE_2G)
		bus.write_byte_data(LSM9DS0_ACCL_ADDRESS, LSM9DS0_CTRL_REG2_XM, ACCL_SCALE)
	
	def mag_datarate(self):
		"""Select the data rate of the magnetometer from the given provided values"""
		MAG_DATARATE = (LSM9DS0_MAG_DR_50 | LSM9DS0_MAG_RES_H)
		bus.write_byte_data(LSM9DS0_MAG_ADDRESS, LSM9DS0_CTRL_REG5_XM, MAG_DATARATE)
	
	def mag_scale_selection(self):
		"""Select the full-scale values of the magnetometer from the given provided values"""
		MAG_SCALE = (LSM9DS0_MAG_GAIN_12)
		bus.write_byte_data(LSM9DS0_MAG_ADDRESS, LSM9DS0_CTRL_REG6_XM, MAG_SCALE)
	
	def mag_mode_selection(self):
		"""Select the modes of the magnetometer from the given provided values"""
		MAG_MODE = (LSM9DS0_MAG_FILTER_NRML | LSM9DS0_MAG_MODE_CNTS)
		bus.write_byte_data(LSM9DS0_MAG_ADDRESS, LSM9DS0_CTRL_REG7_XM, MAG_MODE)
	
	time.sleep(0.5)
	
	def readaccl(self):
		"""Read data back from LSM9DS0_OUT_X_L_A(0x28), 2 bytes
		X-Axis Mag LSB, X-Axis Mag MSB"""
		data0 = bus.read_byte_data(LSM9DS0_ACCL_ADDRESS, LSM9DS0_OUT_X_L_A)
		data1 = bus.read_byte_data(LSM9DS0_ACCL_ADDRESS, LSM9DS0_OUT_X_H_A)
		
		xAccl = data1 * 256 + data0
		if xAccl > 32767 :
			xAccl -= 65536
		
		"""Read data back from LSM9DS0_OUT_Y_L_M(0x2A), 2 bytes
		Y-Axis Mag LSB, Y-Axis Mag MSB"""
		data0 = bus.read_byte_data(LSM9DS0_ACCL_ADDRESS, LSM9DS0_OUT_Y_L_A)
		data1 = bus.read_byte_data(LSM9DS0_ACCL_ADDRESS, LSM9DS0_OUT_Y_H_A)
		
		yAccl = data1 * 256 + data0
		if yAccl > 32767 :
			yAccl -= 65536
		
		"""Read data back from LSM9DS0_OUT_Z_L_M(0x2C), 2 bytes
		Z-Axis Mag LSB, Z-Axis Mag MSB"""
		data0 = bus.read_byte_data(LSM9DS0_ACCL_ADDRESS, LSM9DS0_OUT_Z_L_A)
		data1 = bus.read_byte_data(LSM9DS0_ACCL_ADDRESS, LSM9DS0_OUT_Z_H_A)
		
		zAccl = data1 * 256 + data0
		if zAccl > 32767 :
			zAccl -= 65536
		
		return {'x' : xAccl, 'y' : yAccl, 'z' : zAccl}
	
	def readmag(self):
		"""Read data back from LSM9DS0_OUT_X_L_M(0x08), 2 bytes
		X-Axis Mag LSB, X-Axis Mag MSB"""
		data0 = bus.read_byte_data(LSM9DS0_MAG_ADDRESS, LSM9DS0_OUT_X_L_M)
		data1 = bus.read_byte_data(LSM9DS0_MAG_ADDRESS, LSM9DS0_OUT_X_H_M)
		
		xMag = data1 * 256 + data0
		if xMag > 32767 :
			xMag -= 65536
		
		"""Read data back from LSM9DS0_OUT_Y_L_M(0x0A), 2 bytes
		Y-Axis Mag LSB, Y-Axis Mag MSB"""
		data0 = bus.read_byte_data(LSM9DS0_MAG_ADDRESS, LSM9DS0_OUT_Y_L_M)
		data1 = bus.read_byte_data(LSM9DS0_MAG_ADDRESS, LSM9DS0_OUT_Y_H_M)
		
		yMag = data1 * 256 + data0
		if yMag > 32767 :
			yMag -= 65536
		
		"""Read data back from LSM9DS0_OUT_Z_L_M(0x0C), 2 bytes
		Z-Axis Mag LSB, Z-Axis Mag MSB"""
		data0 = bus.read_byte_data(LSM9DS0_MAG_ADDRESS, LSM9DS0_OUT_Z_L_M)
		data1 = bus.read_byte_data(LSM9DS0_MAG_ADDRESS, LSM9DS0_OUT_Z_H_M)
		
		zMag = data1 * 256 + data0
		if zMag > 32767 :
			zMag -= 65536
		
		return {'x' : xMag, 'y' : yMag, 'z' : zMag}

from LSM9DS0 import LSM9DS0
lsm9ds0 = LSM9DS0()

while True:
	lsm9ds0.gyro_datarate()
	lsm9ds0.gyro_scale_selection()
	gyro = lsm9ds0.readgyro()
	print "X-Axis of Rotation : %d" %(gyro['x'])
	print "Y-Axis of Rotation : %d" %(gyro['y'])
	print "Z-Axis of Rotation : %d" %(gyro['z'])
	lsm9ds0.accl_datarate()
	lsm9ds0.accl_scale_selection()
	accl = lsm9ds0.readaccl()
	print "Acceleration in X-Axis : %d"%(accl['x'])
	print "Acceleration in Y-Axis : %d"%(accl['y'])
	print "Acceleration in Z-Axis : %d"%(accl['z'])
	lsm9ds0.mag_datarate()
	lsm9ds0.mag_scale_selection()
	lsm9ds0.mag_mode_selection()
	mag = lsm9ds0.readmag()
	print "Magnetic field in X-Axis : %d"%(mag['x'])
	print "Magnetic field in Y-Axis : %d"%(mag['y'])
	print "Magnetic field in Z-Axis : %d"%(mag['z'])
	print " ************************************* "
	time.sleep(1)
