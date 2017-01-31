# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MXC6226XU
# This code is designed to work with the MXC6226XU_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Accelorometer?sku=MXC6226XU_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
MXC6226XU_DEFAULT_ADDRESS			= 0x16

# MXC6226XU Register Map
MXC6226XU_REG_XOUT					= 0x00 # 8-bit x-axis acceleration output
MXC6226XU_REG_YOUT					= 0x01 # 8-bit y-axis acceleration output
MXC6226XU_REG_STATUS				= 0x02 # Orientation and Shake Status Register
MXC6226XU_REG_DETECTION				= 0x04 # Shake Detection Parameters Register

# MXC6226XU Detection Register
MXC6226XU_POWER_UP					= 0x00 # Power-Up
MXC6226XU_POWER_DOWN				= 0x80 # Power-Down
MXC6226XU_SHTH_0_5					= 0x00 # Shake Thershold = 0.5g
MXC6226XU_SHTH_1					= 0x10 # Shake Thershold = 1g
MXC6226XU_SHTH_1_5					= 0x20 # Shake Thershold = 1.5g
MXC6226XU_SHTH_2					= 0x30 # Shake Thershold = 2g
MXC6226XU_SHC_80					= 0x00 # Shake Event Time = 80ms
MXC6226XU_SHC_160					= 0x04 # Shake Event Time = 1600ms
MXC6226XU_SHC_320					= 0x08 # Shake Event Time = 320ms
MXC6226XU_SHC_640					= 0x0C # Shake Event Time = 640ms
MXC6226XU_ORC_160					= 0x00 # Orientation Time = 160ms
MXC6226XU_ORC_320					= 0x01 # Orientation Time = 320ms
MXC6226XU_ORC_640					= 0x02 # Orientation Time = 640ms
MXC6226XU_ORC_1280					= 0x03 # Orientation Time = 1280ms

class MXC6226XU():
	def __init__(self):
		self.detection_config()
	
	def detection_config(self):
		"""Select the Detection Register configuration from the given provided value above"""
		DETECTION_CONFIG = (MXC6226XU_POWER_UP | MXC6226XU_SHTH_0_5 | MXC6226XU_ORC_160 | MXC6226XU_SHC_80)
		bus.write_byte_data(MXC6226XU_DEFAULT_ADDRESS, MXC6226XU_REG_DETECTION, DETECTION_CONFIG)
	
	def read_accl(self):
		"""Read data back from MXC6226XU_REG_XOUT(0x00), 2 bytes
			X-Axis, Y-Axis"""
		data = bus.read_i2c_block_data(MXC6226XU_DEFAULT_ADDRESS, MXC6226XU_REG_XOUT, 2)
		
		# Convert the data
		xAccl = data[0]
		if xAccl > 127 :
			xAccl -= 256
		
		yAccl = data[1]
		if yAccl > 127 :
			yAccl -= 256
		
		return {'x' : xAccl, 'y' : yAccl}

from MXC6226XU import MXC6226XU
mxc6226xu = MXC6226XU()

while True :
	accl = mxc6226xu.read_accl()
	print "Acceleration in X-Axis : %d"%(accl['x'])
	print "Acceleration in Y-Axis : %d"%(accl['y'])
	print " ************************************* "
	time.sleep(1)
