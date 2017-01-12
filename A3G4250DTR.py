# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# A3G4250DTR
# This code is designed to work with the A3G4250DTR_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Gyro?sku=A3G4250DTR_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
A3G4250DTR_DEFAULT_ADDRESS			= 0x68

# A3G4250DTR Register Map
A3G4250DTR_REG_WHO_AM_I				= 0x0F # Device identification register
A3G4250DTR_REG_CTRL_1				= 0x20 # Control Register 1
A3G4250DTR_REG_CTRL_2				= 0x21 # Control Register 2
A3G4250DTR_REG_CTRL_3				= 0x22 # Control Register 3
A3G4250DTR_REG_CTRL_4				= 0x23 # Control Register 4
A3G4250DTR_REG_CTRL_5				= 0x24 # Control Register 5
A3G4250DTR_REG_STATUS				= 0x27 # Status Register
A3G4250DTR_REG_OUT_X_L				= 0x28 # X-Axis LSB Output
A3G4250DTR_REG_OUT_X_H				= 0x29 # X-Axis MSB Output
A3G4250DTR_REG_OUT_Y_L				= 0x2A # Y-Axis LSB Output
A3G4250DTR_REG_OUT_Y_H				= 0x2B # Y-Axis MSB Output
A3G4250DTR_REG_OUT_Z_L				= 0x2C # Z-Axis LSB Output
A3G4250DTR_REG_OUT_Z_H				= 0x2D # Z-Axis MSB Output

# A3G4250DTR Datarate & Bandwidth Configuration
A3G4250DTR_DR_100_BW_12_5			= 0x00 # Datarate = 100 Hz, Cut-Off = 12.5
A3G4250DTR_DR_100_BW_25				= 0x10 # Datarate = 100 Hz, Cut-Off = 25
A3G4250DTR_DR_200_BW_12_5			= 0x40 # Datarate = 200 Hz, Cut-Off = 12.5
A3G4250DTR_DR_200_BW_25				= 0x50 # Datarate = 200 Hz, Cut-Off = 25
A3G4250DTR_DR_200_BW_50				= 0x60 # Datarate = 200 Hz, Cut-Off = 50
A3G4250DTR_DR_200_BW_70				= 0x70 # Datarate = 200 Hz, Cut-Off = 70
A3G4250DTR_DR_400_BW_20				= 0x80 # Datarate = 400 Hz, Cut-Off = 20
A3G4250DTR_DR_400_BW_25				= 0x90 # Datarate = 400 Hz, Cut-Off = 25
A3G4250DTR_DR_400_BW_50				= 0xA0 # Datarate = 400 Hz, Cut-Off = 50
A3G4250DTR_DR_400_BW_110			= 0xB0 # Datarate = 400 Hz, Cut-Off = 110
A3G4250DTR_DR_800_BW_30				= 0xC0 # Datarate = 800 Hz, Cut-Off = 30
A3G4250DTR_DR_800_BW_35				= 0xD0 # Datarate = 800 Hz, Cut-Off = 35
A3G4250DTR_DR_800_BW_50				= 0xE0 # Datarate = 800 Hz, Cut-Off = 50
A3G4250DTR_DR_800_BW_110			= 0xF0 # Datarate = 800 Hz, Cut-Off = 110

# A3G4250DTR Mode & Axis Configuration
A3G4250DTR_MODE_PWRDWN				= 0x00 # Power-Down Mode, All axis disable
A3G4250DTR_MODE_NRML				= 0x08 # Normal Mode
A3G4250DTR_AXIS_Z_EN				= 0x04 # Z-Axis enable
A3G4250DTR_AXIS_Y_EN				= 0x02 # Y-Axis enable
A3G4250DTR_AXIS_X_EN				= 0x01 # X-Axis enable

# A3G4250DTR Data Output Configuration
A3G4250DTR_DEFAULT					= 0x00 # Data @ LSB, Self Test disabled, 4-Wire Interface
A3G4250DTR_BLE_MSB					= 0x40 # Data @ MSB
A3G4250DTR_ST_0						= 0x02 # Self Test 0
A3G4250DTR_ST_1						= 0x06 # Self Test 1
A3G4250DTR_SIM_3					= 0x01 # 3-Wire Interface

class A3G4250DTR():
	def __init__ (self):
		self.select_datarate()
		self.select_data_config()
	
	def select_datarate(self):
		"""Select the data rate of the gyroscope from the given provided values"""
		DATARATE_CONFIG = (A3G4250DTR_DR_100_BW_12_5 | A3G4250DTR_MODE_NRML | A3G4250DTR_AXIS_Z_EN | A3G4250DTR_AXIS_Y_EN | A3G4250DTR_AXIS_X_EN)
		bus.write_byte_data(A3G4250DTR_DEFAULT_ADDRESS, A3G4250DTR_REG_CTRL_1, DATARATE_CONFIG)
	
	def select_data_config(self):
		"""Select the data configuration of the gyroscope from the given provided values"""
		DATA_CONFIG = (A3G4250DTR_DEFAULT)
		bus.write_byte_data(A3G4250DTR_DEFAULT_ADDRESS, A3G4250DTR_REG_CTRL_4, DATA_CONFIG)
	
	def readgyro(self):
		"""Read data back from A3G4250DTR_REG_OUT_X_L(0x28), 2 bytes
		X-Axis Mag LSB, X-Axis Mag MSB"""
		data0 = bus.read_byte_data(A3G4250DTR_DEFAULT_ADDRESS, A3G4250DTR_REG_OUT_X_L)
		data1 = bus.read_byte_data(A3G4250DTR_DEFAULT_ADDRESS, A3G4250DTR_REG_OUT_X_H)
		
		xGyro = data1 * 256 + data0
		if xGyro > 32767 :
			xGyro -= 65536
		
		"""Read data back from A3G4250DTR_REG_OUT_Y_L(0x2A), 2 bytes
		Y-Axis Mag LSB, Y-Axis Mag MSB"""
		data0 = bus.read_byte_data(A3G4250DTR_DEFAULT_ADDRESS, A3G4250DTR_REG_OUT_Y_L)
		data1 = bus.read_byte_data(A3G4250DTR_DEFAULT_ADDRESS, A3G4250DTR_REG_OUT_Y_H)
		
		yGyro = data1 * 256 + data0
		if yGyro > 32767 :
			yGyro -= 65536
		
		"""Read data back from A3G4250DTR_REG_OUT_Z_L(0x2C), 2 bytes
		Z-Axis Mag LSB, Z-Axis Mag MSB"""
		data0 = bus.read_byte_data(A3G4250DTR_DEFAULT_ADDRESS, A3G4250DTR_REG_OUT_Z_L)
		data1 = bus.read_byte_data(A3G4250DTR_DEFAULT_ADDRESS, A3G4250DTR_REG_OUT_Z_H)
		
		zGyro = data1 * 256 + data0
		if zGyro > 32767 :
			zGyro -= 65536
		
		return {'x' : xGyro, 'y' : yGyro, 'z' : zGyro}

from A3G4250DTR import A3G4250DTR
a3g4250dtr = A3G4250DTR()

while True:
	gyro = a3g4250dtr.readgyro()
	print "X-Axis of Rotation : %d" %(gyro['x'])
	print "Y-Axis of Rotation : %d" %(gyro['y'])
	print "Z-Axis of Rotation : %d" %(gyro['z'])
	print " ************************************ "
	time.sleep(1)
