# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# LIS33DE
# This code is designed to work with the LIS33DE_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Accelorometer?sku=LIS33DE_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
LIS33DE_DEFAULT_ADDRESS			= 0x1C

# LIS33DE Register Map
LIS33DE_CTRL_REG1				= 0x20 # Accelerometer Control Register 1
LIS33DE_CTRL_REG2				= 0x21 # Accelerometer Control Register 2
LIS33DE_CTRL_REG3				= 0x22 # Accelerometer Control Register 3
LIS33DE_STATUS					= 0x27 # Status Register
LIS33DE_OUT_X					= 0x29 # X-Axis Acceleration Data Register
LIS33DE_OUT_Y					= 0x2B # Y-Axis Acceleration Data Register
LIS33DE_OUT_Z					= 0x2D # Z-Axis Acceleration Data Register
LIS33DE_FF_WU_CFG				= 0x30 # Free-Fall/Wake-Up Interrupt Configuration Register
LIS33DE_FF_WU_SRC				= 0x31 # Free-Fall/Wake-Up Interrupt Source Register
LIS33DE_FF_WU_THS				= 0x32 # Free-Fall/Wake-Up Interrupt Threshold Register
LIS33DE_FF_WU_DURATION			= 0x33 # Free-Fall/Wake-Up Interrupt Duration Register

# LIS33DE Control Register-1 Configuration
LIS33DE_CTRL_REG1_AODR_100		= 0x00 # ODR: 100 Hz
LIS33DE_CTRL_REG1_AODR_400		= 0x80 # ODR: 400 Hz
LIS33DE_CTRL_REG1_PD_PWRDWN		= 0x00 # Power-Down Mode
LIS33DE_CTRL_REG1_PD_ACTIVE		= 0x40 # Active Mode
LIS33DE_CTRL_REG1_FS_2G			= 0x00 # +/- 2G
LIS33DE_CTRL_REG1_FS_8G			= 0x20 # +/- 8G
LIS33DE_CTRL_REG1_ST_NORMAL		= 0x00 # Self Test Normal
LIS33DE_CTRL_REG1_STP_ENABLED	= 0x10 # Self-Test P Enabled
LIS33DE_CTRL_REG1_STM_ENABLED	= 0x08 # Self-Test M Enabled
LIS33DE_CTRL_REG1_AZEN_ENABLE	= 0x04 # Acceleration Z-Axis Enabled
LIS33DE_CTRL_REG1_AYEN_ENABLE	= 0x02 # Acceleration Y-Axis Enabled
LIS33DE_CTRL_REG1_AXEN_ENABLE	= 0x01 # Acceleration X-Axis Enabled

# LIS33DE Control Register-2 Configuration
LIS33DE_CTRL_REG2_SIM_4WIRE		= 0x00 # 4-Wire Interface
LIS33DE_CTRL_REG2_SIM_3WIRE		= 0x80 # 3-Wire Interface
LIS33DE_CTRL_REG2_BOOT_NORMAL	= 0x00 # Normal Mode
LIS33DE_CTRL_REG2_BOOT_REBOOT	= 0x40 # Reboot Memory Content

class LIS33DE():
	def __init__(self):
		self.datarate_config()
		self.mode_config()
	
	def datarate_config(self):
		""" Select the Control Register-1 Configuration from the given provided value above"""
		DATARATE_CONFIG = (LIS33DE_CTRL_REG1_PD_ACTIVE | LIS33DE_CTRL_REG1_AXEN_ENABLE | LIS33DE_CTRL_REG1_AYEN_ENABLE | LIS33DE_CTRL_REG1_AZEN_ENABLE)
		bus.write_byte_data(LIS33DE_DEFAULT_ADDRESS, LIS33DE_CTRL_REG1, DATARATE_CONFIG)
	
	def mode_config(self):
		""" Select the Control Register-2 Configuration from the given provided value above"""
		MODE_CONFIG = (LIS33DE_CTRL_REG2_SIM_4WIRE | LIS33DE_CTRL_REG2_BOOT_NORMAL)
		bus.write_byte_data(LIS33DE_DEFAULT_ADDRESS, LIS33DE_CTRL_REG2, MODE_CONFIG)
	
	def read_accl(self):
		"""Read data back from LIS33DE_OUT_X(0x29), 1 byte
		X-Axis Accl"""
		data = bus.read_byte_data(LIS33DE_DEFAULT_ADDRESS, LIS33DE_OUT_X)
		
		# Convert the data
		xAccl = data
		if xAccl > 127 :
			xAccl -= 256
		
		"""Read data back from LIS33DE_OUT_Y(0x2B), 1 byte
		Y-Axis Accl"""
		data = bus.read_byte_data(LIS33DE_DEFAULT_ADDRESS, LIS33DE_OUT_Y)
		
		# Convert the data
		yAccl = data
		if yAccl > 127 :
			yAccl -= 256
		
		"""Read data back from LIS33DE_OUT_Z(0x2D), 1 byte
		Z-Axis Accl"""
		data = bus.read_byte_data(LIS33DE_DEFAULT_ADDRESS, LIS33DE_OUT_Z)
		
		# Convert the data
		zAccl = data
		if zAccl > 127 :
			zAccl -= 256
		
		return {'x' : xAccl, 'y' : yAccl, 'z' : zAccl}

from LIS33DE import LIS33DE
lis33de = LIS33DE()

while True:
	accl = lis33de.read_accl()
	print "Acceleration in X-Axis : %d"%(accl['x'])
	print "Acceleration in Y-Axis : %d"%(accl['y'])
	print "Acceleration in Z-Axis : %d"%(accl['z'])
	print " ************************************* "
	time.sleep(1)
