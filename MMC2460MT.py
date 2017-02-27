# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MMC2460MT
# This code is designed to work with the MMC2460MT_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Magnetic-Sensor?sku=MMC2460MT_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
MMC2460MT_DEFAULT_ADDRESS			= 0x30

# MMC2460MT Register Map
MMC2460MT_XOUTL						= 0x00 # Output Value X LSB
MMC2460MT_XOUTH						= 0x01 # Output Value X MSB
MMC2460MT_YOUTL						= 0x02 # Output Value Y LSB
MMC2460MT_YOUTH						= 0x03 # Output Value Y MSB
MMC2460MT_STATUS					= 0x06 # Device Status Register
MMC2460MT_CNTRL_0					= 0x07 # Internal Control Register 0
MMC2460MT_CNTRL_1					= 0x08 # Internal Control Register 1

# MMC2460MT Control Register-0
MMC2460MT_TM						= 0x01 # Take measurement
MMC2460MT_CONT_MODE_ON				= 0x02 # Continuous Measurement Mode Enabled
MMC2460MT_CONT_FREQ_1_5				= 0x00 # Frequency = 1.5Hz
MMC2460MT_CONT_FREQ_12				= 0x04 # Frequency = 12Hz
MMC2460MT_CONT_FREQ_25				= 0x08 # Frequency = 25Hz
MMC2460MT_CONT_FREQ_50				= 0x0C # Frequency = 50Hz
MMC2460MT_NO_BOOST_DS				= 0x00 # Charge pump enabled
MMC2460MT_NO_BOOST_EN				= 0x10 # Charge pump disabled
MMC2460MT_SET						= 0x20 # Sets the sensor by passing a large current through Set/Reset Coil
MMC2460MT_RESET						= 0x40 # Resets the sensor by passing a large current through Set/Reset Coil at a reversed direction
MMC2460MT_REFILL_CAP				= 0x80 # Recharge the capacitor at CAP pin

# MMC2460MT Control Register-1
MMC2460MT_BW_7_92					= 0x00 # Measurement Time = 7.82ms
MMC2460MT_BW_4_08					= 0x01 # Measurement Time = 4.08ms
MMC2460MT_BW_2_16					= 0x02 # Measurement Time = 2.16ms
MMC2460MT_ST_XY						= 0x20 # Self Test Check
MMC2460MT_ST_NRML					= 0x00 # Normal Operation
MMC2460MT_SW_RST					= 0x80 # Reset, similar to power-up
MMC2460MT_RESERVED					= 0x10 # Factory-use Register

class MMC2460MT():
	def measurement_config(self):
		"""Select the Control Register-0 configuration from the given provided values above"""
		MEASURE_CONFIG = (MMC2460MT_TM | MMC2460MT_CONT_MODE_ON | MMC2460MT_CONT_FREQ_1_5)
		bus.write_byte_data(MMC2460MT_DEFAULT_ADDRESS, MMC2460MT_CNTRL_0, MEASURE_CONFIG)
	
	def time_config(self):
		"""Select the Control Register-1 configuration from the givn provided values above"""
		TIME_CONFIG = (MMC2460MT_BW_7_92 | MMC2460MT_ST_NRML | MMC2460MT_RESERVED)
		bus.write_byte_data(MMC2460MT_DEFAULT_ADDRESS, MMC2460MT_CNTRL_1, TIME_CONFIG)
	
	def read_mag(self):
		"""Read data back from MMC2460MT_XOUTL(0x00), 4 bytes
		X-Axis LSB, X-Axis MSB, Y-Axis LSB, Y-Axis MSB"""
		data = bus.read_i2c_block_data(MMC2460MT_DEFAULT_ADDRESS, MMC2460MT_XOUTL, 4)
		
		# Convert the data
		xMag = data[1] * 256 + data[0]
		if xMag > 32767 :
			xMag -= 65536
		
		yMag = data[3] * 256 + data[2]
		if yMag > 32767 :
			yMag -= 65536
		
		return {'x' : xMag, 'y' : yMag}

from MMC2460MT import MMC2460MT
mmc2460mt = MMC2460MT()

while True :
	mmc2460mt.measurement_config()
	mmc2460mt.time_config()
	mag = mmc2460mt.read_mag()
	print "Magnetic field in X-Axis : %d"%(mag['x'])
	print "Magnetic field in Y-Axis : %d"%(mag['y'])
	print " ************************************* "
	time.sleep(1)
