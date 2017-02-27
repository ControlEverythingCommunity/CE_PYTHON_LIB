# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MMC3316xMT
# This code is designed to work with the MMC3316xMT_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Magnetic-Sensor?sku=MMC3316xMT_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
MMC3316xMT_DEFAULT_ADDRESS			= 0x30

# MMC3316xMT Register Map
MMC3316xMT_XOUTL					= 0x00 # Output Value X LSB
MMC3316xMT_XOUTH					= 0x01 # Output Value X MSB
MMC3316xMT_YOUTL					= 0x02 # Output Value Y LSB
MMC3316xMT_YOUTH					= 0x03 # Output Value Y MSB
MMC3316xMT_ZOUTL					= 0x04 # Output Value Z LSB
MMC3316xMT_ZOUTH					= 0x05 # Output Value Z MSB
MMC3316xMT_STATUS					= 0x06 # Device Status Register
MMC3316xMT_CNTRL_0					= 0x07 # Internal Control Register 0
MMC3316xMT_CNTRL_1					= 0x08 # Internal Control Register 1

# MMC3316xMT Control Register-0
MMC3316xMT_TM						= 0x01 # Take measurement
MMC3316xMT_CONT_MODE_ON				= 0x02 # Continuous Measurement Mode Enabled
MMC3316xMT_CONT_FREQ_50				= 0x00 # Frequency = 50Hz
MMC3316xMT_CONT_FREQ_20				= 0x04 # Frequency = 20Hz
MMC3316xMT_CONT_FREQ_20				= 0x08 # Frequency = 20Hz
MMC3316xMT_CONT_FREQ_1				= 0x0C # Frequency = 1Hz
MMC3316xMT_COIL_NOTSET				= 0x00 # Coil Not Set
MMC3316xMT_SET						= 0x20 # Sets the sensor by passing a large current through Set/Reset Coil
MMC3316xMT_RESET					= 0x40 # Resets the sensor by passing a large current through Set/Reset Coil at a reversed direction

class MMC3316xMT():
	def measurement_config(self):
		"""Select the Control Register-0 configuration from the given provided values above"""
		MEASURE_CONFIG = (MMC3316xMT_TM)
		bus.write_byte_data(MMC3316xMT_DEFAULT_ADDRESS, MMC3316xMT_CNTRL_0, MEASURE_CONFIG)
		time.sleep(0.1)
		
		MEASURE_CONFIG = (MMC3316xMT_SET)
		bus.write_byte_data(MMC3316xMT_DEFAULT_ADDRESS, MMC3316xMT_CNTRL_0, MEASURE_CONFIG)
		
		MEASURE_CONFIG = (MMC3316xMT_COIL_NOTSET)
		bus.write_byte_data(MMC3316xMT_DEFAULT_ADDRESS, MMC3316xMT_CNTRL_0, MEASURE_CONFIG)
		time.sleep(0.1)
		
		MEASURE_CONFIG = (MMC3316xMT_RESET)
		bus.write_byte_data(MMC3316xMT_DEFAULT_ADDRESS, MMC3316xMT_CNTRL_0, MEASURE_CONFIG)
		
		MEASURE_CONFIG = (MMC3316xMT_COIL_NOTSET)
		bus.write_byte_data(MMC3316xMT_DEFAULT_ADDRESS, MMC3316xMT_CNTRL_0, MEASURE_CONFIG)
		
		MEASURE_CONFIG = (MMC3316xMT_TM | MMC3316xMT_CONT_MODE_ON)
		bus.write_byte_data(MMC3316xMT_DEFAULT_ADDRESS, MMC3316xMT_CNTRL_0, MEASURE_CONFIG)
	
	def read_mag(self):
		"""Read data back from MMC3316xMT_XOUTL(0x00), 6 bytes
		X-Axis LSB, X-Axis MSB, Y-Axis LSB, Y-Axis MSB, Z-Axis LSB, Z-Axis MSB"""
		data = bus.read_i2c_block_data(MMC3316xMT_DEFAULT_ADDRESS, MMC3316xMT_XOUTL, 6)
		
		# Convert the data
		xMag = ((data[1] & 0x3F) * 256) + data[0]
		if xMag > 8191 :
			xMag -= 16384
		
		yMag = ((data[3] & 0x3F) * 256) + data[2]
		if yMag > 8191 :
			yMag -= 16384
		
		zMag = ((data[5] & 0x3F) * 256) + data[4]
		if zMag > 8191 :
			zMag -= 16384
		
		return {'x' : xMag, 'y' : yMag, 'z' : zMag}

from MMC3316xMT import MMC3316xMT
mmc3316xmt = MMC3316xMT()

while True :
	mmc3316xmt.measurement_config()
	mag = mmc3316xmt.read_mag()
	print "Magnetic field in X-Axis : %d"%(mag['x'])
	print "Magnetic field in Y-Axis : %d"%(mag['y'])
	print "Magnetic field in Z-Axis : %d"%(mag['z'])
	print " ************************************* "
	time.sleep(1)
