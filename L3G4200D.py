# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# L3G4200D
# This code is designed to work with the L3G4200D_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Gyro?sku=L3G4200D_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
L3G4200D_DEFAULT_ADDRESS			= 0x68

# L3G4200D Register Map
L3G4200D_REG_WHOAMI					= 0x0F # Who Am I Register
L3G4200D_REG_CTRL1					= 0x20 # Control Register-1
L3G4200D_REG_CTRL2					= 0x21 # Control Register-2
L3G4200D_REG_CTRL3					= 0x22 # Control Register-3
L3G4200D_REG_CTRL4					= 0x23 # Control Register-4
L3G4200D_REG_CTRL5					= 0x24 # Control Register-5
L3G4200D_REG_REFERENCE				= 0x25 # Reference
L3G4200D_OUT_TEMP					= 0x26 # Temperature Output
L3G4200D_REG_STATUS					= 0x27 # Status Register
L3G4200D_REG_OUT_X_L				= 0x28 # X-Axis LSB
L3G4200D_REG_OUT_X_H				= 0x29 # X-Axis MSB
L3G4200D_REG_OUT_Y_L				= 0x2A # Y-Axis LSB
L3G4200D_REG_OUT_Y_H				= 0x2B # Y-Axis MSB
L3G4200D_REG_OUT_Z_L				= 0x2C # Z-Axis LSB
L3G4200D_REG_OUT_Z_H				= 0x2D # Z-Axis MSB

# L3G4200D Control Register-1 Configuration
L3G4200D_DR_100_BW_12_5				= 0x00 # Datarate = 100 Hz, Cut-Off = 12.5
L3G4200D_DR_100_BW_25				= 0x10 # Datarate = 100 Hz, Cut-Off = 25
L3G4200D_DR_200_BW_12_5				= 0x40 # Datarate = 200 Hz, Cut-Off = 12.5
L3G4200D_DR_200_BW_25				= 0x50 # Datarate = 200 Hz, Cut-Off = 25
L3G4200D_DR_200_BW_50				= 0x60 # Datarate = 200 Hz, Cut-Off = 50
L3G4200D_DR_200_BW_70				= 0x70 # Datarate = 200 Hz, Cut-Off = 70
L3G4200D_DR_400_BW_20				= 0x80 # Datarate = 400 Hz, Cut-Off = 20
L3G4200D_DR_400_BW_25				= 0x90 # Datarate = 400 Hz, Cut-Off = 25
L3G4200D_DR_400_BW_50				= 0xA0 # Datarate = 400 Hz, Cut-Off = 50
L3G4200D_DR_400_BW_110				= 0xB0 # Datarate = 400 Hz, Cut-Off = 110
L3G4200D_DR_800_BW_30				= 0xC0 # Datarate = 800 Hz, Cut-Off = 30
L3G4200D_DR_800_BW_35				= 0xD0 # Datarate = 800 Hz, Cut-Off = 35
L3G4200D_DR_800_BW_50				= 0xE0 # Datarate = 800 Hz, Cut-Off = 50
L3G4200D_DR_800_BW_110				= 0xF0 # Datarate = 800 Hz, Cut-Off = 110
L3G4200D_MODE_PWRDWN				= 0x00 # Power-Down Mode, All axis disable
L3G4200D_MODE_NRML					= 0x08 # Normal Mode
L3G4200D_AXIS_Z_EN					= 0x04 # Z-Axis enable
L3G4200D_AXIS_Y_EN					= 0x02 # Y-Axis enable
L3G4200D_AXIS_X_EN					= 0x01 # X-Axis enable

# L3G4200D Control Register-4 Configuration
L3G4200D_DEFAULT					= 0x00 # Continous Update, Data @ LSB, Normal Mode, 4-Wire Interface
L3G4200D_BDU_READ_MSB_LSB			= 0x80 # Output Registers not updated until MSB and LSB reading
L3G4200D_BLE_MSB					= 0x40 # Data @ MSB
L3G4200D_FS_250						= 0x00 # Full Scale Selection = 250dps
L3G4200D_FS_500						= 0x10 # Full Scale Selection = 500dps
L3G4200D_FS_2000					= 0x20 # Full Scale Selection = 2000dps
L3G4200D_FS_250						= 0x00 # Full Scale Selection = 250dps
L3G4200D_ST_0						= 0x02 # Self Test-0
L3G4200D_ST_1						= 0x06 # Self Test-1
L3G4200D_SIM_3						= 0x01 # 3-Wire Interface

class L3G4200D():
	def __init__(self):
		self.select_datarate()
		self.select_data_config()
	
	def select_datarate(self):
		"""Select the Control Register-1 Configuration from the given provided value"""
		DATARATE = (L3G4200D_DR_100_BW_12_5 | L3G4200D_MODE_NRML | L3G4200D_AXIS_Z_EN | L3G4200D_AXIS_Y_EN | L3G4200D_AXIS_X_EN)
		bus.write_byte_data(L3G4200D_DEFAULT_ADDRESS, L3G4200D_REG_CTRL1, DATARATE)
	
	def select_data_config(self):
		"""Select the Control Register-4 Configuration from the given provided value"""
		DATA_CONFIG = (L3G4200D_DEFAULT | L3G4200D_FS_2000)
		bus.write_byte_data(L3G4200D_DEFAULT_ADDRESS, L3G4200D_REG_CTRL4, DATA_CONFIG)
	
	def read_gyro(self):
		"""Read data back from L3G4200D_REG_OUT_X_L(0x28), 2 bytes, X-Axis LSB first"""
		data0 = bus.read_byte_data(L3G4200D_DEFAULT_ADDRESS, L3G4200D_REG_OUT_X_L)
		data1 = bus.read_byte_data(L3G4200D_DEFAULT_ADDRESS, L3G4200D_REG_OUT_X_H)
		
		# Convert the data
		xGyro = data1 * 256 + data0
		if xGyro > 32767 :
			xGyro -= 65536
		
		"""Read data back from L3G4200D_REG_OUT_Y_L(0x2A), 2 bytes, Y-Axis LSB first"""
		data0 = bus.read_byte_data(L3G4200D_DEFAULT_ADDRESS, L3G4200D_REG_OUT_Y_L)
		data1 = bus.read_byte_data(L3G4200D_DEFAULT_ADDRESS, L3G4200D_REG_OUT_Y_H)
		
		# Convert the data
		yGyro = data1 * 256 + data0
		if yGyro > 32767 :
			yGyro -= 65536
		
		"""Read data back from L3G4200D_REG_OUT_Z_L(0x2C), 2 bytes, Z-Axis LSB first"""
		data0 = bus.read_byte_data(L3G4200D_DEFAULT_ADDRESS, L3G4200D_REG_OUT_Z_L)
		data1 = bus.read_byte_data(L3G4200D_DEFAULT_ADDRESS, L3G4200D_REG_OUT_Z_H)
		
		# Convert the data
		zGyro = data1 * 256 + data0
		if zGyro > 32767 :
			zGyro -= 65536
		
		return {'x' : xGyro, 'y' : yGyro, 'z' : zGyro}

from L3G4200D import L3G4200D
l3g4200d = L3G4200D()

while True :
	l3g4200d.select_datarate()
	l3g4200d.select_data_config()
	time.sleep(0.1)
	gyro = l3g4200d.read_gyro()
	print "X-Axis of Rotation : %d" %(gyro['x'])
	print "Y-Axis of Rotation : %d" %(gyro['y'])
	print "Z-Axis of Rotation : %d" %(gyro['z'])
	print " ************************************ "
	time.sleep(1)
