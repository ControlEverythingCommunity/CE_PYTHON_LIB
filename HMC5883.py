# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# HMC5883
# This code is designed to work with the HMC5883_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Compass?sku=HMC5883_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
HMC5883_DEFAULT_ADDRESS			= 0x1E

# HMC5883 Register Map
HMC5883_REG_CRA					= 0x00 # Configuration Register-A
HMC5883_REG_CRB					= 0x01 # Configuration Register-B
HMC5883_REG_MODE				= 0x02 # Mode Register
HMC5883_REG_OUT_X_H				= 0x03 # Data Output X MSB Register
HMC5883_REG_OUT_X_L				= 0x04 # Data Output X LSB Register
HMC5883_REG_OUT_Z_H				= 0x05 # Data Output Z MSB Register
HMC5883_REG_OUT_Z_L				= 0x06 # Data Output Z LSB Register
HMC5883_REG_OUT_Y_H				= 0x07 # Data Output Y MSB Register
HMC5883_REG_OUT_Y_L				= 0x08 # Data Output Y LSB Register
HMC5883_REG_STATUS				= 0x09 # Status Register
HMC5883_REG_IRA					= 0x0A # Identification Register-A
HMC5883_REG_IRB					= 0x0B # Identification Register-B
HMC5883_REG_IRC					= 0x0C # Identification Register-C

# HMC5883 Configuration Register-A
HMC5883_MA_1					= 0x00 # Samples per measurement = 1
HMC5883_MA_2					= 0x20 # Samples per measurement = 2
HMC5883_MA_4					= 0x40 # Samples per measurement = 4
HMC5883_MA_8					= 0x60 # Samples per measurement = 6
HMC5883_DR_0_75					= 0x00 # Output Data Rate = 0.75Hz
HMC5883_DR_1_5					= 0x04 # Output Data Rate = 1.5Hz
HMC5883_DR_3					= 0x08 # Output Data Rate = 3Hz
HMC5883_DR_7_5					= 0x0C # Output Data Rate = 7.5Hz
HMC5883_DR_15					= 0x10 # Output Data Rate = 15Hz
HMC5883_DR_30					= 0x14 # Output Data Rate = 30Hz
HMC5883_DR_75					= 0x18 # Output Data Rate = 75Hz
HMC5883_MS_NORMAL				= 0x00 # Normal Measurement Configuration
HMC5883_MS_POSITIVE				= 0x01 # Positive bias configuration for X, Y and Z-axes
HMC5883_MS_NEGATIVE				= 0x02 # Negative bias configuration for X, Y and Z-axes

# HMC5883 Configuration Register-B
HMC5883_GAIN_0_88				= 0x00 # Gain = +/- 0.88
HMC5883_GAIN_1_3				= 0x20 # Gain = +/- 1.3
HMC5883_GAIN_1_9				= 0x40 # Gain = +/- 1.9
HMC5883_GAIN_2_5				= 0x60 # Gain = +/- 2.5
HMC5883_GAIN_4_0				= 0x80 # Gain = +/- 4.0
HMC5883_GAIN_4_7				= 0xA0 # Gain = +/- 4.7
HMC5883_GAIN_5_6				= 0xC0 # Gain = +/- 5.6
HMC5883_GAIN_8_1				= 0xE0 # Gain = +/- 8.1

# HMC5883 Mode Register
HMC5883_MODE_CONT				= 0x00 # Continuous-Measurement Mode
HMC5883_MODE_SNGL				= 0x01 # Single-Measurement Mode
HMC5883_MODE_IDLE				= 0x02 # Idle Mode

class HMC5883():
	def __init__(self):
		self.measurement_config()
		self.gain_config()
		self.mode_config()
	
	def measurement_config(self):
		"""Select the Configuration Register-A data from the given provided values"""
		MEASURE_CONFIG = (HMC5883_MS_NORMAL | HMC5883_DR_0_75 | HMC5883_MA_8)
		bus.write_byte_data(HMC5883_DEFAULT_ADDRESS, HMC5883_REG_CRA, MEASURE_CONFIG)
	
	def gain_config(self):
		"""Select the Configuration Register-B data from the given provided values"""
		bus.write_byte_data(HMC5883_DEFAULT_ADDRESS, HMC5883_REG_CRB, HMC5883_GAIN_0_88)
	
	def mode_config(self):
		"""Select the Mode Register configuration from the given provided values"""
		bus.write_byte_data(HMC5883_DEFAULT_ADDRESS, HMC5883_REG_MODE, HMC5883_MODE_CONT)
	
	def read_mag(self):
		"""Read data back from HMC5883_REG_OUT_X_H(0x03), 6 bytes
		X-Axis MSB, X-Axis LSB, Z-Axis MSB, Z-Axis LSB, Y-Axis MSB, Y-Axis LSB"""
		data = bus.read_i2c_block_data(HMC5883_DEFAULT_ADDRESS, HMC5883_REG_OUT_X_H, 6)
		
		# Convert the data
		xMag = data[0] * 256 + data[1]
		if xMag > 32767 :
			xMag -= 65536
		
		zMag = data[2] * 256 + data[3]
		if zMag > 32767 :
			zMag -= 65536
		
		yMag = data[4] * 256 + data[5]
		if yMag > 32767 :
			yMag -= 65536
		
		return {'x' : xMag, 'y' : yMag, 'z' : zMag}

from HMC5883 import HMC5883
hmc5883 = HMC5883()

while True :
	hmc5883.measurement_config()
	hmc5883.gain_config()
	hmc5883.mode_config()
	time.sleep(0.1)
	mag = hmc5883.read_mag()
	print "Magnetic field in X-Axis : %d"%(mag['x'])
	print "Magnetic field in Y-Axis : %d"%(mag['y'])
	print "Magnetic field in Z-Axis : %d"%(mag['z'])
	print " ************************************* "
	time.sleep(1)
