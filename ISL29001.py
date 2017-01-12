# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# ISL29001
# This code is designed to work with the ISL29001_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/products

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
ISL29001_DEFAULT_ADDRESS			= 0x44

# ISL29001 Command Set
ISL29001_ADC_POWERDOWN				= 0x8C # ADC is powered-down
ISL29001_ADC_RESET					= 0x0C # ADC is reset
ISL29001_ADC_DIODE_1_INT			= 0x00 # ADC converts Diode 1's current into unsigned-magnitude 16-bit data. Internally timed at 100ms per integration
ISL29001_ADC_DIODE_2_INT			= 0x04 # ADC converts Diode 2's current into unsigned-magnitude 16-bit data. Internally timed at 100ms per integration
ISL29001_ADC_DIODE_DIFF_INT			= 0x08 # ADC converts DIODE-1-DIODE-2 into 2's-complement 16-bit data. Internally timed at 200ms per integration
ISL29001_ADC_DIODE_1_EXT			= 0x30 # ADC converts Diode 1's current into unsigned-magnitude 16-bit data. The integration is externally timed
ISL29001_ADC_DIODE_2_EXT			= 0x34 # ADC converts Diode 2's current into unsigned-magnitude 16-bit data. The integration is externally timed
ISL29001_ADC_DIODE_DIFF_EXT			= 0x38 # ADC converts DIODE-1-DIODE-2 into 2's-complement 16-bit data. The integration is externally timed

class ISL29001():
	def __init__(self):
		self.luminance_command()
	
	def luminance_command(self):
		"""Select the luminance command from the given provided values"""
		bus.write_byte(ISL29001_DEFAULT_ADDRESS, ISL29001_ADC_DIODE_DIFF_INT)
	
	def read_luminance(self):
		"""Read data back from the device address, 2 bytes, luminance LSB, luminance MSB"""
		data = bus.read_i2c_block_data(ISL29001_DEFAULT_ADDRESS, 2)
		
		# Convert the data
		luminance = (((data[1] * 256) + data[0]) * 10000) / 32768
		
		return {'l' : luminance}

from ISL29001 import ISL29001
isl29001 = ISL29001()

while True:
	time.sleep(0.3)
	isl29001.luminance_command()
	time.sleep(0.3)
	lum = isl29001.read_luminance()
	print "Ambient Light luminance : %d lux" %(lum['l'])
	print " ******************************************* "
	time.sleep(0.5)