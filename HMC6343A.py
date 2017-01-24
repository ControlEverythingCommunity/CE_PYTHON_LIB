# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# HMC6343A
# This code is designed to work with the HMC6343A_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Accelorometer?sku=HMC6343A_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
HMC6343A_DEFAULT_ADDRESS			= 0x19

# HMC6343A Register Map
HMC6343A_SW_VERSION					= 0x02 # Software Version Number
HMC6343A_OP_MODE1					= 0x04 # Operational Mode Register 1
HMC6343A_OP_MODE2					= 0x05 # Operational Mode Register 2
HMC6343A_SN_LSB						= 0x06 # Device Serial Number LSB
HMC6343A_SN_MSB						= 0x07 # Device Serial Number MSB
HMC6343A_DEVIATION_LSB				= 0x0A # Deviation Angle (+/-1800) in tenths of a degree LSB
HMC6343A_DEVIATION_MSB				= 0x0B # Deviation Angle (+/-1800) in tenths of a degree MSB
HMC6343A_VARIATION_LSB				= 0x0C # Variation Angle (+/-1800) in tenths of a degree LSB
HMC6343A_VARIATION_MSB				= 0x0D # Variation Angle (+/-1800) in tenths of a degree MSB
HMC6343A_XOFFSET_LSB				= 0x0E # Hard-Iron Calibration Offset for the X-axis LSB
HMC6343A_XOFFSET_MSB				= 0x0F # Hard-Iron Calibration Offset for the X-axis MSB
HMC6343A_YOFFSET_LSB				= 0x10 # Hard-Iron Calibration Offset for the Y-axis LSB
HMC6343A_YOFFSET_MSB				= 0x11 # Hard-Iron Calibration Offset for the Y-axis MSB
HMC6343A_ZOFFSET_LSB				= 0x12 # Hard-Iron Calibration Offset for the Z-axis LSB
HMC6343A_ZOFFSET_MSB				= 0x13 # Hard-Iron Calibration Offset for the Z-axis MSB
HMC6343A_FILTER_LSB					= 0x14 # Heading IIR Filter LSB
HMC6343A_FILTER_MSB					= 0x15 # Heading IIR Filter MSB
HMC6343A_POST_ACCEL					= 0x40 # Post Accel Data
HMC6343A_POST_MAG					= 0x45 # Post Mag Data

# HMC6343A Operational Mode Register-1 Configuration
HMC6343A_OM1_LEVEL					= 0x01 # Level Orientation Set
HMC6343A_OM1_UE						= 0x02 # Upright Edge Orientation Set
HMC6343A_OM1_UF						= 0x04 # Upright Front Orientation Set
HMC6343A_OM1_STDBY					= 0x08 # Stand-by Mode Set
HMC6343A_OM1_RUN					= 0x10 # Run Mode Set
HMC6343A_OM1_FILTER					= 0x20 # IIR Heading Filter Used
HMC6343A_OM1_CAL					= 0x40 # Calculating calibration offsets
HMC6343A_OM1_COMP					= 0x80 # Calculating compass data

# HMC6343A Operational Mode Register-2 Configuration
HMC6343A_MR_1						= 0x00 # Measurement Rate = 1Hz
HMC6343A_MR_5						= 0x01 # Measurement Rate = 5Hz
HMC6343A_MR_10						= 0x02 # Measurement Rate = 10Hz

class HMC6343A():
	def __init__(self):
		self.mode_config()
		self.measurement_rate_config()
	
	def mode_config(self):
		"""Select the Operational Mode Register-1 Configuration from the given provided values"""
		MODE_CONFIG = (HMC6343A_OM1_LEVEL | HMC6343A_OM1_RUN)
		bus.write_byte_data(HMC6343A_DEFAULT_ADDRESS, HMC6343A_OP_MODE1, MODE_CONFIG)
	
	def measurement_rate_config(self):
		"""Select the Operational Mode Register-2 Configuration from the given provided values"""
		bus.write_byte_data(HMC6343A_DEFAULT_ADDRESS, HMC6343A_OP_MODE2, HMC6343A_MR_5)
	
	def read_accl(self):
		"""Read data back from HMC6343A_POST_ACCEL(0x40), 6 bytes
		X-Axis Accl MSB, X-Axis Accl LSB, Y-Axis Accl MSB, Y-Axis Accl LSB, Z-Axis Accl MSB, Z-Axis Accl LSB"""
		data = bus.read_i2c_block_data(HMC6343A_DEFAULT_ADDRESS, HMC6343A_POST_ACCEL, 6)
		
		# Convert the data
		xAccl = data[0] * 256 + data[1]
		if xAccl > 32767 :
			xAccl -= 65536
		
		yAccl = data[2] * 256 + data[3]
		if yAccl > 32767 :
			yAccl -= 65536
		
		zAccl = data[4] * 256 + data[5]
		if zAccl > 32767 :
			zAccl -= 65536
		
		return {'x' : xAccl, 'y' : yAccl, 'z' : zAccl}
	
	def read_mag(self):
		"""Read data back from HMC6343A_POST_MAG(0x45), 6 bytes
		X-Axis Mag MSB, X-Axis Mag LSB, Y-Axis Mag MSB, Y-Axis Mag LSB, Z-Axis Mag MSB, Z-Axis Mag LSB"""
		data = bus.read_i2c_block_data(HMC6343A_DEFAULT_ADDRESS, HMC6343A_POST_MAG, 6)
		
		# Convert the data
		xMag = data[0] * 256 + data[1]
		if xMag > 32767 :
			xMag -= 65536
		
		yMag = data[2] * 256 + data[3]
		if yMag > 32767 :
			yMag -= 65536
		
		zMag = data[4] * 256 + data[5]
		if zMag > 32767 :
			zMag -= 65536
		
		return {'x' : xMag, 'y' : yMag, 'z' : zMag}

from HMC6343A import HMC6343A
hmc6343a = HMC6343A()

while True :
	hmc6343a.mode_config()
	hmc6343a.measurement_rate_config()
	time.sleep(0.1)
	accl = hmc6343a.read_accl()
	print "Acceleration in X-Axis : %d"%(accl['x'])
	print "Acceleration in Y-Axis : %d"%(accl['y'])
	print "Acceleration in Z-Axis : %d"%(accl['z'])
	
	mag = hmc6343a.read_mag()
	print "Magnetic field in X-Axis : %d"%(mag['x'])
	print "Magnetic field in Y-Axis : %d"%(mag['y'])
	print "Magnetic field in Z-Axis : %d"%(mag['z'])
	print " ************************************* "
	time.sleep(1)
