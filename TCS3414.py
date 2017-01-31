# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# TCS3414
# This code is designed to work with the TCS3414_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Color?sku=TCS3414_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
TCS3414_DEFAULT_ADDRESS			= 0x39

# TCS3414 Register Set
TCS3414_COMMAND_BIT				= 0x80
TCS3414_REG_CONTROL				= 0x00 # Control of basic functions
TCS3414_REG_TIMING				= 0x01 # Integration time/gain control
TCS3414_REG_GAIN				= 0x07 # ADC gain control
TCS3414_REG_DATA1LOW			= 0x10 # Low byte of ADC green channel
TCS3414_REG_DATA1HIGH			= 0x11 # High byte of ADC green channel
TCS3414_REG_DATA2LOW			= 0x12 # Low byte of ADC red channel
TCS3414_REG_DATA2HIGH			= 0x13 # High byte of ADC red channel
TCS3414_REG_DATA3LOW			= 0x14 # Low byte of ADC blue channel
TCS3414_REG_DATA3HIGH			= 0x15 # High byte of ADC blue channel
TCS3414_REG_DATA4LOW			= 0x16 # Low byte of ADC clear channel
TCS3414_REG_DATA4HIGH			= 0x17 # Low byte of ADC clear channel

# Control register configuration
TCS3414_REG_CONTROL_POWEROFF	= 0x00 # Power Off, ADC disable
TCS3414_REG_CONTROL_POWERON		= 0x01 # Power On
TCS3414_REG_CONTROL_ADC_EN		= 0x02 # ADC enable

# Gain register configuration
TCS3414_REG_GAIN_PRESCALAR_1	= 0x00 # Gain = 1x, PRESCALAR Mode divide by 1
TCS3414_REG_GAIN_4				= 0x10 # Gain = 4x
TCS3414_REG_GAIN_16				= 0x20 # Gain = 16x
TCS3414_REG_GAIN_64				= 0x30 # Gain = 64x
TCS3414_REG_PRESCALAR_2			= 0x01 # PRESCALAR Mode divide by 2
TCS3414_REG_PRESCALAR_4			= 0x02 # PRESCALAR Mode divide by 4
TCS3414_REG_PRESCALAR_8			= 0x03 # PRESCALAR Mode divide by 8
TCS3414_REG_PRESCALAR_16		= 0x04 # PRESCALAR Mode divide by 16
TCS3414_REG_PRESCALAR_32		= 0x05 # PRESCALAR Mode divide by 32
TCS3414_REG_PRESCALAR_64		= 0x06 # PRESCALAR Mode divide by 64

class TCS3414():
	def __init__(self):
		self.power_selection()
		self.gain_selection()
	
	def power_selection(self):
		"""Select the power configuration from the given provided values"""
		POWER_CONFIGURATION = (TCS3414_REG_CONTROL_POWERON | TCS3414_REG_CONTROL_ADC_EN)
		bus.write_byte_data(TCS3414_DEFAULT_ADDRESS, TCS3414_REG_CONTROL | TCS3414_COMMAND_BIT, POWER_CONFIGURATION)
	
	def gain_selection(self):
		"""Select the gain configuration from the given provided values"""
		GAIN_CONFIGURATION = (TCS3414_REG_GAIN_PRESCALAR_1)
		bus.write_byte_data(TCS3414_DEFAULT_ADDRESS, TCS3414_REG_GAIN | TCS3414_COMMAND_BIT, GAIN_CONFIGURATION)
	
	def readluminance(self):
		"""Read data back from TCS3414_REG_DATA1LOW(0x10), 8 bytes, with TCS3414_COMMAND_BIT, (0x80)
		Green LSB, Green MSB, Red LSB, Red MSB, Blue LSB, Blue MSB, cData LSB, cData MSB"""
		data = bus.read_i2c_block_data(TCS3414_DEFAULT_ADDRESS, TCS3414_REG_DATA1LOW | TCS3414_COMMAND_BIT, 8)
		
		# Convert the data
		green	= data[1] * 256 + data[0]
		red		= data[3] * 256 + data[2]
		blue	= data[5] * 256 + data[4]
		cData	= data[7] * 256 + data[6]
		
		return {'g' : green, 'r' : red, 'b' : blue, 'c' : cData,}

from TCS3414 import TCS3414
tcs3414 = TCS3414()

while True:
	lum = tcs3414.readluminance()
	print "Green Color Luminance : %d "%(lum['g'])
	print "Red Color Luminance : %d "%(lum['r'])
	print "Blue Color Luminance : %d "%(lum['b'])
	print "Clear Data Luminance : %d "%(lum['c'])
	print " ***************************************************** "
	time.sleep(1)
