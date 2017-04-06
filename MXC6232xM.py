# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MXC6232xM
# This code is designed to work with the MXC6232xM_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Accelorometer?sku=MXC6232xM_I2CS#tabs-0-product_tabset-2
# NT

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
MXC6232xM_DEFAULT_ADDRESS	= 0x10

# MXC6232xM Command Map
MXC6232xM_POWER_O			= 0x00 # Power ON
MXC6232xM_POWER_D			= 0x01 # Power Down
MXC6232xM_SELFTEST_O		= 0x02 # Self Test ON
MXC6232xM_SELFTEST_F		= 0x00 # Self Test OFF
MXC6232xM_BGTST				= 0x04 # Band Gap Test
MXC6232xM_NRML				= 0x00 # Normal
MXC6232xM_TOEN_EN			= 0x08 # Temperature Enable
MXC6232xM_TOEN_DS			= 0x00 # Temperature Disable
MXC6232xM_INTRL_REG			= 0x00 # Internal Register
MXC6232xM_MSB_X				= 0x01 # X-Axis MSB
MXC6232xM_LSB_X				= 0x02 # X-Axis LSB
MXC6232xM_MSB_Y				= 0x03 # Y-Axis MSB
MXC6232xM_LSB_Y				= 0x04 # Y-Axis LSB

class MXC6232xM():
	def configuration(self):
		"""Select the configuration of the aceelerometer from the given provided values above"""
		CONFIG = (MXC6232xM_POWER_O | MXC6232xM_SELFTEST_F | MXC6232xM_NRML | MXC6232xM_TOEN_DS)
		bus.write_byte(MXC6232xM_DEFAULT_ADDRESS, CONFIG)
	
	def readAccl(self):
		"""Read data back from INTRL_REG(0x00), 5 bytes
		Internal register, X-Axis MSB, X-Axis LSB, Y-Axis MSB, Y-Axis LSB"""
		data = bus.read_i2c_block_data(MXC6232xM_DEFAULT_ADDRESS, MXC6232xM_MSB_X, 4)
		
		# Convert the data
		xAccl = ((data[0] & 0x0F) * 256) + data[1]
		if xAccl > 2047 :
			xAccl -= 4096
		
		yAccl = ((data[2] & 0x0F) * 256) + data[3]
		if yAccl > 2047 :
			yAccl -= 4096
		
		return {"x": xAccl, "y": yAccl}

from MXC6232xM import MXC6232xM
mxc6232xm = MXC6232xM()

while True:
	mxc6232xm.configuration()
	time.sleep(0.3)
	axes = mxc6232xm.readAccl()
	print "Acceleration in X-Axis : %d" %(axes['x'])
	print "Acceleration in Y-Axis : %d" %(axes['y'])
	print " ************************************* "
	time.sleep(0.5)
