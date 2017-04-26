# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# L3DG20
# This code is designed to work with the L3DG20_I2CS I2C Mini Module available from ControlEverything.com.
# https://shop.controleverything.com/

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
L3DG20_DEFAULT_ADDRESS			= 0x6A

# L3DG20 Register Map
L3DG20_REG_WHOAMI					= 0x0F # Who Am I Register
L3DG20_REG_CTRL1					= 0x20 # Control Register-1
L3DG20_REG_CTRL2					= 0x21 # Control Register-2
L3DG20_REG_CTRL3					= 0x22 # Control Register-3
L3DG20_REG_CTRL4					= 0x23 # Control Register-4
L3DG20_REG_CTRL5					= 0x24 # Control Register-5
L3DG20_REG_REFERENCE				= 0x25 # Reference
L3DG20_OUT_TEMP					= 0x26 # Temperature Output
L3DG20_REG_STATUS					= 0x27 # Status Register
L3DG20_REG_OUT_X_L				= 0x28 # X-Axis LSB
L3DG20_REG_OUT_X_H				= 0x29 # X-Axis MSB
L3DG20_REG_OUT_Y_L				= 0x2A # Y-Axis LSB
L3DG20_REG_OUT_Y_H				= 0x2B # Y-Axis MSB
L3DG20_REG_OUT_Z_L				= 0x2C # Z-Axis LSB
L3DG20_REG_OUT_Z_H				= 0x2D # Z-Axis MSB

# L3DG20 Control Register-1 Configuration
L3DG20_DR_95_BW_12_5				= 0x00 # Datarate = 95 Hz, Cut-Off = 12.5
L3DG20_DR_95_BW_25				= 0x10 # Datarate = 95 Hz, Cut-Off = 25
L3DG20_DR_190_BW_12_5				= 0x40 # Datarate = 190 Hz, Cut-Off = 12.5
L3DG20_DR_190_BW_25				= 0x50 # Datarate = 190 Hz, Cut-Off = 25
L3DG20_DR_190_BW_50				= 0x60 # Datarate = 190 Hz, Cut-Off = 50
L3DG20_DR_190_BW_70				= 0x70 # Datarate = 190 Hz, Cut-Off = 70
L3DG20_DR_380_BW_20				= 0x80 # Datarate = 380 Hz, Cut-Off = 20
L3DG20_DR_380_BW_25				= 0x90 # Datarate = 380 Hz, Cut-Off = 25
L3DG20_DR_380_BW_50				= 0xA0 # Datarate = 380 Hz, Cut-Off = 50
L3DG20_DR_380_BW_110				= 0xB0 # Datarate = 380 Hz, Cut-Off = 110
L3DG20_DR_760_BW_30				= 0xC0 # Datarate = 760 Hz, Cut-Off = 30
L3DG20_DR_760_BW_35				= 0xD0 # Datarate = 760 Hz, Cut-Off = 35
L3DG20_DR_760_BW_50				= 0xE0 # Datarate = 760 Hz, Cut-Off = 50
L3DG20_DR_760_BW_110				= 0xF0 # Datarate = 760 Hz, Cut-Off = 110
L3DG20_MODE_PWRDWN				= 0x00 # Power-Down Mode, All axis disable
L3DG20_MODE_NRML					= 0x08 # Normal Mode
L3DG20_AXIS_Z_EN					= 0x04 # Z-Axis enable
L3DG20_AXIS_Y_EN					= 0x02 # Y-Axis enable
L3DG20_AXIS_X_EN					= 0x01 # X-Axis enable

# L3DG20 Control Register-4 Configuration
L3DG20_DEFAULT					= 0x00 # Continous Update, Data @ LSB, Normal Mode, 4-Wire Interface
L3DG20_BDU_READ_MSB_LSB			= 0x80 # Output Registers not updated until MSB and LSB reading
L3DG20_BLE_MSB					= 0x40 # Data @ MSB
L3DG20_FS_250						= 0x00 # Full Scale Selection = 250dps
L3DG20_FS_500						= 0x10 # Full Scale Selection = 500dps
L3DG20_FS_2000					= 0x20 # Full Scale Selection = 2000dps
L3DG20_FS_250						= 0x00 # Full Scale Selection = 250dps
L3DG20_SIM_4						= 0x00 # 4-Wire Interface
L3DG20_SIM_3						= 0x01 # 3-Wire Interface

class L3DG20():
	def __init__(self):
		self.select_datarate()
		self.select_data_config()
	
	def select_datarate(self):
		"""Select the Control Register-1 Configuration from the given provided value"""
		DATARATE = (L3DG20_DR_95_BW_12_5 | L3DG20_MODE_NRML | L3DG20_AXIS_Z_EN | L3DG20_AXIS_Y_EN | L3DG20_AXIS_X_EN)
		bus.write_byte_data(L3DG20_DEFAULT_ADDRESS, L3DG20_REG_CTRL1, DATARATE)
	
	def select_data_config(self):
		"""Select the Control Register-4 Configuration from the given provided value"""
		DATA_CONFIG = (L3DG20_DEFAULT | L3DG20_FS_2000)
		bus.write_byte_data(L3DG20_DEFAULT_ADDRESS, L3DG20_REG_CTRL4, DATA_CONFIG)
	
	def read_gyro(self):
		"""Read data back from L3DG20_REG_OUT_X_L(0x28), 2 bytes, X-Axis LSB first"""
		data0 = bus.read_byte_data(L3DG20_DEFAULT_ADDRESS, L3DG20_REG_OUT_X_L)
		data1 = bus.read_byte_data(L3DG20_DEFAULT_ADDRESS, L3DG20_REG_OUT_X_H)
		
		# Convert the data
		xGyro = data1 * 256 + data0
		if xGyro > 32767 :
			xGyro -= 65536
		
		"""Read data back from L3DG20_REG_OUT_Y_L(0x2A), 2 bytes, Y-Axis LSB first"""
		data0 = bus.read_byte_data(L3DG20_DEFAULT_ADDRESS, L3DG20_REG_OUT_Y_L)
		data1 = bus.read_byte_data(L3DG20_DEFAULT_ADDRESS, L3DG20_REG_OUT_Y_H)
		
		# Convert the data
		yGyro = data1 * 256 + data0
		if yGyro > 32767 :
			yGyro -= 65536
		
		"""Read data back from L3DG20_REG_OUT_Z_L(0x2C), 2 bytes, Z-Axis LSB first"""
		data0 = bus.read_byte_data(L3DG20_DEFAULT_ADDRESS, L3DG20_REG_OUT_Z_L)
		data1 = bus.read_byte_data(L3DG20_DEFAULT_ADDRESS, L3DG20_REG_OUT_Z_H)
		
		# Convert the data
		zGyro = data1 * 256 + data0
		if zGyro > 32767 :
			zGyro -= 65536
		
		return {'x' : xGyro, 'y' : yGyro, 'z' : zGyro}

from L3DG20 import L3DG20
l3dg20 = L3DG20()

while True :
	l3dg20.select_datarate()
	l3dg20.select_data_config()
	time.sleep(0.1)
	gyro = l3dg20.read_gyro()
	print "X-Axis of Rotation : %d" %(gyro['x'])
	print "Y-Axis of Rotation : %d" %(gyro['y'])
	print "Z-Axis of Rotation : %d" %(gyro['z'])
	print " ************************************ "
	time.sleep(1)
