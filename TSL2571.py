# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# TSL2571
# This code is designed to work with the TSL2571_I2CS I2C Mini Module available from ControlEverything.com.
# https://shop.controleverything.com/products/light-sensor-with-programmable-analog-gain

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
TSL2571_DEFAULT_ADDRESS			= 0x39

# TSL2571 Register Set
TSL2571_COMMAND_BIT					= 0xA0 # Auto-increment protocol transaction
TSL2571_REG_ENABLE					= 0x00 # Enables states and interrupts
TSL2571_REG_ATIME					= 0x01 # ALS ADC time
TSL2571_REG_WTIME					= 0x03 # Wait time
TSL2571_REG_CONFIG					= 0x0D # Configuration register
TSL2571_REG_CONTROL					= 0x0F # Control register
TSL2571_REG_DEVICE_ID				= 0x12 # Device ID register
TSL2571_REG_STATUS					= 0x13 # Device Status register
TSL2571_REG_C0DATAL					= 0x14 # Ch0 channel low data register
TSL2571_REG_C0DATAH					= 0x15 # Ch0 high data register
TSL2571_REG_C1DATAL					= 0x16 # Ch1 low data register
TSL2571_REG_C1DATAH					= 0x17 # Ch1 high data register

# TSL2571 Enable Register Configuration
TSL2571_REG_ENABLE_AIEN				= 0x10 # ALS Interrupt Enable
TSL2571_REG_ENABLE_WEN				= 0x08 # Wait Enable
TSL2571_REG_ENABLE_AEN				= 0x02 # ALS Enable
TSL2571_REG_ENABLE_PON				= 0x01 # Power ON

# TSL2571 ATime Register Configuration
TSL2571_REG_ATIME_2_72				= 0xFF # Atime = 2.72 ms, Cycles = 1
TSL2571_REG_ATIME_27_2				= 0xF6 # Atime = 27.2 ms, Cycles = 10
TSL2571_REG_ATIME_101				= 0xDB # Atime = 101 ms, Cycles = 37
TSL2571_REG_ATIME_174				= 0xC0 # Atime = 174 ms, Cycles = 64
TSL2571_REG_ATIME_696				= 0x00 # Atime = 696 ms, Cycles = 256

# TSL2571 WTime Register Configuration
TSL2571_REG_WTIME_2_72				= 0xFF # Wtime = 2.72 ms
TSL2571_REG_WTIME_201				= 0xB6 # Wtime = 201 ms
TSL2571_REG_WTIME_696				= 0x00 # Wtime = 696 ms

# TSL2571 Control Register Configuration
TSL2571_REG_CONTROL_AGAIN_1			= 0x00 # ALS GAIN VALUE - 1x Gain
TSL2571_REG_CONTROL_AGAIN_4			= 0x01 # ALS GAIN VALUE - 4x Gain
TSL2571_REG_CONTROL_AGAIN_16		= 0x02 # ALS GAIN VALUE - 16x Gain
TSL2571_REG_CONTROL_AGAIN_120		= 0x03 # ALS GAIN VALUE - 120x Gain

class TSL2571():
	def __init__(self):
		self.enable_selection()
		self.time_selection()
		self.gain_selection()
	
	def enable_selection(self):
		"""Select the ENABLE register configuration from the given provided values"""
		ENABLE_CONFIGURATION = (TSL2571_REG_ENABLE_WEN | TSL2571_REG_ENABLE_AEN | TSL2571_REG_ENABLE_PON)
		bus.write_byte_data(TSL2571_DEFAULT_ADDRESS, TSL2571_REG_ENABLE | TSL2571_COMMAND_BIT, ENABLE_CONFIGURATION)
	
	time.sleep(0.3)
	
	def time_selection(self):
		"""Select the ATIME register configuration from the given provided values"""
		bus.write_byte_data(TSL2571_DEFAULT_ADDRESS, TSL2571_REG_ATIME | TSL2571_COMMAND_BIT, TSL2571_REG_ATIME_101)
		
		"""Select the WTIME register configuration from the given provided values"""
		bus.write_byte_data(TSL2571_DEFAULT_ADDRESS, TSL2571_REG_WTIME | TSL2571_COMMAND_BIT, TSL2571_REG_WTIME_2_72)
	
	def gain_selection(self):
		"""Select the CONTROL register configuration from the given provided values"""
		GAIN_CONFIGURATION = TSL2571_REG_CONTROL_AGAIN_1
		bus.write_byte_data(TSL2571_DEFAULT_ADDRESS, TSL2571_REG_CONTROL | TSL2571_COMMAND_BIT, GAIN_CONFIGURATION)

	def readluminance(self):
		"""Read data back from TSL2571_REG_C0DATAL(0x14), 4 bytes, with TSL2571_COMMAND_BIT, (0xA0)
		c0Data LSB, c0Data MSB, c1Data LSB, c1Data MSB"""
		data = bus.read_i2c_block_data(TSL2571_DEFAULT_ADDRESS, TSL2571_REG_C0DATAL | TSL2571_COMMAND_BIT, 4)
		
		# Convert the data
		c0Data = (data[1] * 256) + data[0]
		c1Data = (data[3] * 256) + data[2]
		luminance = 0.0
		CPL = (101.0) / 23.0
		luminance1 = ((1.00 *  c0Data) - (2.00 * c1Data)) / CPL
		luminance2 = ((0.6 * c0Data) - (1.00 * c1Data)) / CPL
		if luminance1 > 0 and luminance2 > 0 :
			if luminance1 > luminance2 :
				luminance = luminance1
			else :
				luminance = luminance2
		
		return {'l' : luminance}

from TSL2571 import TSL2571
tsl2571 = TSL2571()

while True:
	lum = tsl2571.readluminance()
	print "Ambient Light Luminance : %.2f lux"%(lum['l'])
	print " ************************************************ "
	time.sleep(1)
