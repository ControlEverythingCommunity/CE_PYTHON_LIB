# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# TSL45315
# This code is designed to work with the TSL45315_IS2C I2C Mini Module available from ControlEverything.com.
# https:#www.controleverything.com/content/Light?sku=TSL45315_I2CS#tabs-0-product_tabset-2
# NT

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
TSL45315_DEFAULT_ADDRESS			= 0x29

# TSL45315 Register Set
TSL45315_COMMAND_BIT				= 0x80
TSL45315_REG_CONTROL				= 0x00 # Control Register
TSL45315_REG_CONFIG					= 0x01 # Configuration register
TSL45315_REG_DATALOW				= 0x04 # ALS Data LOW Register
TSL45315_REG_DATAHIGH				= 0x05 # ALS Data HIGH Register

# TSL45315 Mode Configuration
TSL45315_REG_CONTROL_PD				= 0x00 # Power down
TSL45315_REG_CONTROL_ADC			= 0x02 # Run a single ADC cycle and return to PowerDown
TSL45315_REG_CONTROL_NRML			= 0x03 # Normal Operation

# TSL45315 Multiplier Configuration
TSL45315_REG_CONFIG_TCNTRL_1		= 0x00 # Multiplier 1x, Tint : 400ms
TSL45315_REG_CONFIG_TCNTRL_2		= 0x01 # Multiplier 2x, Tint : 200ms
TSL45315_REG_CONFIG_TCNTRL_4		= 0x02 # Multiplier 4x, Tint : 100ms
TSL45315_REG_CONFIG_PSAVESKIP		= 0x08 # Power save Mode

class TSL45315():
	def __init__(self):
		self.mode_selection()
		self.multipler_selection()
	
	def mode_selection(self):
		"""Select the mode configuration from the given provided values"""
		bus.write_byte_data(TSL45315_DEFAULT_ADDRESS, TSL45315_REG_CONTROL | TSL45315_COMMAND_BIT, TSL45315_REG_CONTROL_NRML)
	
	def multipler_selection(self):
		"""Select the multiplier configuration from the given provided values"""
		bus.write_byte_data(TSL45315_DEFAULT_ADDRESS, TSL45315_REG_CONFIG | TSL45315_COMMAND_BIT, TSL45315_REG_CONFIG_TCNTRL_1)
	
	def readluminance(self):
		"""Read data back from TSL45315_REG_DATALOW(0x04), 2 bytes, with TSL45315_COMMAND_BIT, (0x80)
		luminance LSB, luminance MSB"""
		data = bus.read_i2c_block_data(TSL45315_DEFAULT_ADDRESS, TSL45315_REG_DATALOW | TSL45315_COMMAND_BIT, 2)
		
		# Convert the data to lux
		luminance = data[1] * 256 + data[0]
		
		return luminance

from TSL45315 import TSL45315
tsl45315 = TSL45315()

while True:
	tsl45315.readluminance()
	print "Ambient Light Luminance : %.2f lux"%luminance
	print " ***************************************************** "
	time.sleep(1)
