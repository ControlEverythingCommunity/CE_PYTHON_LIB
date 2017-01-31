# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MAG3110
# This code is designed to work with the MAG3110_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Compass?sku=MAG3110_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
MAG3110_DEFAULT_ADDRESS				= 0x0E

# MAG3110 Register Map
MAG3110_DR_STATUS					= 0x00 # Data ready status per axis
MAG3110_OUT_X_MSB					= 0x01 # X-Axis MSB Data
MAG3110_OUT_X_LSB					= 0x02 # X-Axis LSB Data
MAG3110_OUT_Y_MSB					= 0x03 # Y-Axis MSB Data
MAG3110_OUT_Y_LSB					= 0x04 # Y-Axis LSB Data
MAG3110_OUT_Z_MSB					= 0x05 # Z-Axis MSB Data
MAG3110_OUT_Z_LSB					= 0x06 # Z-Axis LSB Data
MAG3110_WHO_AM_I					= 0x07 # Device ID Number
MAG3110_SYSMOD						= 0x08 # Current System Mode
MAG3110_OFF_X_MSB					= 0x09 # X-Axis MSB Offset Data
MAG3110_OFF_X_LSB					= 0x0A # X-Axis LSB Offset Data
MAG3110_OFF_Y_MSB					= 0x0B # Y-Axis MSB Offset Data
MAG3110_OFF_Y_LSB					= 0x0C # Y-Axis LSB Offset Data
MAG3110_OFF_Z_MSB					= 0x0D # Z-Axis MSB Offset Data
MAG3110_OFF_Z_LSB					= 0x0E # Z-Axis LSB Offset Data
MAG3110_DIE_TEMP					= 0x0F # Temperature Register
MAG3110_CTRL_REG1					= 0x10 # Control Register 1
MAG3110_CTRL_REG2					= 0x11 # Control Register 2

# MAG3110 Control Register 1 Configuration
MAG3110_DR_OS_80_16					= 0x00 # Output Data Rate = 80Hz, Oversampling Ratio = 16
MAG3110_DR_OS_40_32					= 0x08 # Output Data Rate = 40Hz, Oversampling Ratio = 32
MAG3110_DR_OS_20_64					= 0x10 # Output Data Rate = 20Hz, Oversampling Ratio = 64
MAG3110_DR_OS_10_128				= 0x18 # Output Data Rate = 10Hz, Oversampling Ratio = 128
MAG3110_DR_OS_40_16					= 0x20 # Output Data Rate = 40Hz, Oversampling Ratio = 16
MAG3110_DR_OS_20_32					= 0x28 # Output Data Rate = 20Hz, Oversampling Ratio = 32
MAG3110_DR_OS_10_64					= 0x30 # Output Data Rate = 10Hz, Oversampling Ratio = 64
MAG3110_DR_OS_5_128					= 0x38 # Output Data Rate = 5Hz, Oversampling Ratio = 128
MAG3110_DR_OS_20_16					= 0x40 # Output Data Rate = 20Hz, Oversampling Ratio = 16
MAG3110_DR_OS_10_32					= 0x48 # Output Data Rate = 10Hz, Oversampling Ratio = 32
MAG3110_DR_OS_5_64					= 0x50 # Output Data Rate = 5Hz, Oversampling Ratio = 64
MAG3110_DR_OS_2_5_128				= 0x58 # Output Data Rate = 2.5Hz, Oversampling Ratio = 128
MAG3110_DR_OS_10_16					= 0x60 # Output Data Rate = 10Hz, Oversampling Ratio = 16
MAG3110_DR_OS_5_32					= 0x68 # Output Data Rate = 5Hz, Oversampling Ratio = 32
MAG3110_DR_OS_2_5_64				= 0x70 # Output Data Rate = 2.5Hz, Oversampling Ratio = 64
MAG3110_DR_OS_1_25_128				= 0x78 # Output Data Rate = 1.25Hz, Oversampling Ratio = 128
MAG3110_DR_OS_5_16					= 0x80 # Output Data Rate = 5Hz, Oversampling Ratio = 16
MAG3110_DR_OS_2_5_32				= 0x88 # Output Data Rate = 2.5Hz, Oversampling Ratio = 32
MAG3110_DR_OS_1_25_64				= 0x90 # Output Data Rate = 1.25Hz, Oversampling Ratio = 64
MAG3110_DR_OS_0_63_128				= 0x98 # Output Data Rate = 0.63Hz, Oversampling Ratio = 128
MAG3110_DR_OS_2_5_16				= 0xA0 # Output Data Rate = 2.5Hz, Oversampling Ratio = 16
MAG3110_DR_OS_1_25_32				= 0xA8 # Output Data Rate = 1.25Hz, Oversampling Ratio = 32
MAG3110_DR_OS_0_63_64				= 0xB0 # Output Data Rate = 0.63Hz, Oversampling Ratio = 64
MAG3110_DR_OS_0_31_128				= 0xB8 # Output Data Rate = 0.31Hz, Oversampling Ratio = 128
MAG3110_DR_OS_1_25_16				= 0xC0 # Output Data Rate = 1.25Hz, Oversampling Ratio = 16
MAG3110_DR_OS_0_63_32				= 0xC8 # Output Data Rate = 0.63Hz, Oversampling Ratio = 32
MAG3110_DR_OS_0_31_64				= 0xD0 # Output Data Rate = 0.31Hz, Oversampling Ratio = 64
MAG3110_DR_OS_0_16_128				= 0xD8 # Output Data Rate = 0.16Hz, Oversampling Ratio = 128
MAG3110_DR_OS_0_63_16				= 0xE0 # Output Data Rate = 0.63Hz, Oversampling Ratio = 16
MAG3110_DR_OS_0_31_32				= 0xE8 # Output Data Rate = 0.31Hz, Oversampling Ratio = 32
MAG3110_DR_OS_0_16_64				= 0xF0 # Output Data Rate = 0.16Hz, Oversampling Ratio = 64
MAG3110_DR_OS_0_08_128				= 0xF8 # Output Data Rate = 0.08Hz, Oversampling Ratio = 128
MAG3110_FAST_READ					= 0x04 # Fast Read enable
MAG3110_TRIGGER_MEASUREMENT			= 0x02 # Trigger Measurement enable
MAG3110_ACTIVE_MODE					= 0x01 # Active Mode
MAG3110_STANDBY_MODE				= 0x00 # Standby Mode

# MAG3110 Control Register 2 Configuration
MAG3110_AUTO_MRST_EN				= 0x80 # Automatic magnetic sensor resets enabled
MAG3110_RAW_MODE					= 0x20 # Raw Mode
MAG3110_NORMAL_MODE					= 0x00 # Normal Mode
MAG3110_MAG_RST						= 0x10 # Reset cycle initiate or Reset cycle busy/active

class MAG3110():
	def __init__(self):
		self.datarate_config()
		self.mode_config()
	
	def datarate_config(self):
		"""Select the Datarate Configuration of the magnetometer from the given provided values"""
		DATARATE_CONFIG = (MAG3110_DR_OS_80_16 | MAG3110_ACTIVE_MODE)
		bus.write_byte_data(MAG3110_DEFAULT_ADDRESS, MAG3110_CTRL_REG1, DATARATE_CONFIG)
	
	def mode_config(self):
		"""Select the Mode Configuration of the magnetometer from the given provided values"""
		MODE_CONFIG = (MAG3110_AUTO_MRST_EN | MAG3110_NORMAL_MODE)
		bus.write_byte_data(MAG3110_DEFAULT_ADDRESS, MAG3110_CTRL_REG2, MODE_CONFIG)
	
	def read_mag(self):
		"""Read data back from MAG3110_OUT_X_MSB(0x01), 6 bytes
		X-Axis MSB, X-Axis LSB, Y-Axis MSB, Y-Axis LSB, Z-Axis MSB, Z-Axis LSB"""
		data = bus.read_i2c_block_data(MAG3110_DEFAULT_ADDRESS, MAG3110_OUT_X_MSB, 6)
		
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

from MAG3110 import MAG3110
mag3110 = MAG3110()

while True:
	mag3110.datarate_config()
	mag3110.mode_config()
	mag = mag3110.read_mag()
	print "Magnetic field in X-Axis : %d"%(mag['x'])
	print "Magnetic field in Y-Axis : %d"%(mag['y'])
	print "Magnetic field in Z-Axis : %d"%(mag['z'])
	print " ************************************* "
	time.sleep(1)