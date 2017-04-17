# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# LIS302DLTR
# This code is designed to work with the LIS302DLTR_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Accelorometer?sku=LIS302DLTR_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
LIS302DLTR_DEFAULT_ADDRESS			= 0x1C

# LIS302DLTR Register Map
LIS302DLTR_REG_WHOAMI               = 0x0F # Who Am I Register
LIS302DLTR_REG_CTRL1                = 0x20 # Control Register-1
LIS302DLTR_REG_CTRL2                = 0x21 # Control Register-2
LIS302DLTR_REG_CTRL3                = 0x22 # Control Register-3
LIS302DLTR_REG_STATUS               = 0x27 # Status Register
LIS302DLTR_REG_OUT_X				= 0x29 # X-Axis
LIS302DLTR_REG_OUT_Y				= 0x2B # Y-Axis
LIS302DLTR_REG_OUT_Z_H				= 0x2D # Z-Axis

# Accl Data Rate
LIS302DLTR_ACCL_DR_100              = 0x00 # ODR: 100 Hz
LIS302DLTR_ACCL_DR_400              = 0x80 # ODR: 400 Hz

# Accl Data update
LIS302DLTR_ACCL_PD_ACTIVE           = 0x40 # Active Mode
# Acceleration Full-scale selection and Axis configuration
LIS302DLTR_ACCL_RANGE_2G            = 0x00 # Full scale = +/-2g
LIS302DLTR_ACCL_RANGE_8G            = 0x20 # Full scale = +/-8g
LIS302DLTR_ACCL_STP_NORMAL          = 0x00 # Self Test P Normal
LIS302DLTR_ACCL_STM_NORMAL          = 0x00 # Self Test M Normal
LIS302DLTR_ACCL_XAXIS               = 0x04 # X-Axis enabled
LIS302DLTR_ACCL_YAXIS               = 0x02 # Y-Axis enabled
LIS302DLTR_ACCL_ZAXIS               = 0x01 # Z-Axis enabled

# Acceleration Serial Interface
LIS302DLTR_SIM_3                    = 0x80 # 3-Wire Interface
LIS302DLTR_BOOT_NORMAL              = 0x00 # Normal Mode


class LIS302DLTR():
	def __init__ (self):
		self.select_datarate()
		self.select_data_config()
	
	def select_datarate(self):
		"""Select the data rate of the accelerometer from the given provided values"""
		DATARATE_CONFIG = (LIS302DLTR_ACCL_DR_100 | LIS302DLTR_ACCL_XAXIS | LIS302DLTR_ACCL_YAXIS | LIS302DLTR_ACCL_ZAXIS)
		bus.write_byte_data(LIS302DLTR_DEFAULT_ADDRESS, LIS302DLTR_REG_CTRL1, DATARATE_CONFIG)
	
	def select_data_config(self):
		"""Select the data configuration of the accelerometer from the given provided values"""
		DATA_CONFIG = (LIS302DLTR_ACCL_RANGE_2G | LIS302DLTR_ACCL_STP_NORMAL | LIS302DLTR_ACCL_STM_NORMAL)
		bus.write_byte_data(LIS302DLTR_DEFAULT_ADDRESS, LIS302DLTR_REG_CTRL4, DATA_CONFIG)
	
	def read_accl(self):
		"""Read data back from LIS302DLTR_REG_OUT_X(0x29), 1 byte
		X-Axis Accl"""
		data0 = bus.read_byte_data(LIS302DLTR_DEFAULT_ADDRESS, LIS302DLTR_REG_OUT_X)
		
        xAccl = data0
        if xAccl > 127 :
            xAccl -= 256
		
		"""Read data back from LIS302DLTR_REG_OUT_Y(0x2B), 1 byte
		Y-Axis Accl"""
		data0 = bus.read_byte_data(LIS302DLTR_DEFAULT_ADDRESS, LIS302DLTR_REG_OUT_Y)
		
		yAccl = data0
        if yAccl > 127
            yAccl -= 256
		
		"""Read data back from LIS302DLTR_REG_OUT_Z(0x2D), 1 byte
		Z-Axis Accl"""
		data0 = bus.read_byte_data(LIS302DLTR_DEFAULT_ADDRESS, LIS302DLTR_REG_OUT_Z)
		
		zAccl = data0
		if zAccl > 127 :
			zAccl -= 256
		
		return {'x' : xAccl, 'y' : yAccl, 'z' : zAccl}

from LIS302DLTR import LIS302DLTR
lis302dltr = LIS302DLTR()

while True:
	lis302dltr.select_datarate()
	lis302dltr.select_data_config()
	time.sleep(0.1)
	accl = lis302dltr.read_accl()
	print "Acceleration in X-Axis : %d" %(accl['x'])
	print "Acceleration in Y-Axis : %d" %(accl['y'])
	print "Acceleration in Z-Axis : %d" %(accl['z'])
	print " ************************************ "
	time.sleep(1)
