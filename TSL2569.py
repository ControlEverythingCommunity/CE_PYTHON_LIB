# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# TSL2569
# This code is designed to work with the TSL2569_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Light?sku=TSL2569_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
TSL2569_DEFAULT_ADDRESS				= 0x39

# TSL2569 Register Map
TSL2569_COMMAND_BIT					= 0x80
TSL2569_REG_CONTROL					= 0x00 # Control register
TSL2569_REG_TIMING					= 0x01 # Timing Register
TSL2569_REG_THRESLOW_LOW			= 0x02 # Low byte of low interrupt threshold
TSL2569_REG_THRESLOW_HIGH			= 0x03 # High byte of low interrupt threshold
TSL2569_REG_THRESHIGH_LOW			= 0x04 # Low byte of high interrupt threshold
TSL2569_REG_THRESHIGH_HIGH			= 0x05 # High byte of high interrupt threshold
TSL2569_REG_INTERRUPT				= 0x06 # Interrupt control
TSL2569_REG_DATA0LOW				= 0x0C # Low byte of ADC channel 0
TSL2569_REG_DATA0HIGH				= 0x0D # High byte of ADC channel 0
TSL2569_REG_DATA1LOW				= 0x0E # Low byte of ADC channel 1
TSL2569_REG_DATA1HIGH				= 0x0F # High byte of ADC channel 1

# TSL2569 Control Register
TSL2569_CONTROL_POWER_UP			= 0x03 # Power Up
TSL2569_CONTROL_POWER_DOWN			= 0x00 # Power Down

# TSL2569 Timing Register
TSL2569_GAIN_1X						= 0x00 # Gain = 1x
TSL2569_GAIN_16X					= 0x10 # Gain = 16x
TSL2569_MANUAL_START_CYCLE			= 0x08 # Begins an integration cycle
TSL2569_MANUAL_STOP_CYCLE			= 0x00 # Stops an integration cycle
TSL2569_INTEG_13_7					= 0x00 # Integration Time = 13.7 ms
TSL2569_INTEG_101					= 0x01 # Integration Time = 101 ms
TSL2569_INTEG_402					= 0x02 # Integration Time = 402 ms

class TSL2569():
	def __init__(self):
		self.power_config()
		self.time_config()
	
	def power_config(self):
		"""Select the Control Register configuration from the given provided value"""
		POWER_CONFIG = (TSL2569_CONTROL_POWER_UP)
		bus.write_byte_data(TSL2569_DEFAULT_ADDRESS, TSL2569_REG_CONTROL | TSL2569_COMMAND_BIT, POWER_CONFIG)
	
	def time_config(self):
		"""Select the Timing Register configuration from the given provided value"""
		TIME_CONFIG = (TSL2569_GAIN_1X | TSL2569_INTEG_402)
		bus.write_byte_data(TSL2569_DEFAULT_ADDRESS, TSL2569_REG_TIMING | TSL2569_COMMAND_BIT, TIME_CONFIG)
	
	def read_light(self):
		"""Read data back from TSL2569_REG_DATA0LOW(0x0C) with TSL2569_COMMAND_BIT(0x80), 4 bytes
		ch0 LSB, ch0 MSB, ch1 LSB, ch1 MSB"""
		data = bus.read_i2c_block_data(TSL2569_DEFAULT_ADDRESS, TSL2569_REG_DATA0LOW | TSL2569_COMMAND_BIT, 4)
		
		# Convert the data
		ch0 = data[1] * 256 + data[0]
		ch1 = data[3] * 256 + data[2]
		
		fullspectrum = ch0
		infrared = ch1
		visible = ch0 - ch1
		
		return {'f' : fullspectrum, 'i' : infrared, 'v' : visible}

from TSL2569 import TSL2569
tsl2569 = TSL2569()

while True :
	tsl2569.power_config()
	tsl2569.time_config()
	time.sleep(0.2)
	lux = tsl2569.read_light()
	print "Full Spectrum(IR + Visible) : %d "%(lux['f'])
	print "Infrared Value : %d "%(lux['i'])
	print "Visible Value : %d "%(lux['v'])
	print " ******************************************* "
	time.sleep(0.8)
