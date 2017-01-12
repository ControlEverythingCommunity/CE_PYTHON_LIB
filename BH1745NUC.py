# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# BH1745NUC
# This code is designed to work with the BH1745NUC_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Color?sku=BH1745NUC_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
BH1745NUC_DEFAULT_ADDRESS				= 0x38

# BH1745NUC Register Set
BH1745NUC_REG_SYSTEM					= 0x40 # System Control Register
BH1745NUC_REG_MODE_CONTROL1				= 0x41 # Mode Control 1 Register
BH1745NUC_REG_MODE_CONTROL2				= 0x42 # Mode Control 2 Register
BH1745NUC_REG_MODE_CONTROL3				= 0x44 # Mode Control 3 Register
BH1745NUC_REG_RED_DATA_LSB				= 0x50 # Red low data register
BH1745NUC_REG_RED_DATA_MSB				= 0x51 # Red high data register
BH1745NUC_REG_GREEN_DATA_LSB			= 0x52 # Green low data register
BH1745NUC_REG_GREEN_DATA_MSB			= 0x53 # Green high data register
BH1745NUC_REG_BLUE_DATA_LSB				= 0x54 # Blue low data register
BH1745NUC_REG_BLUE_DATA_MSB				= 0x55 # Blue high data register
BH1745NUC_REG_CLEAR_DATA_LSB			= 0x56 # Clear low data register
BH1745NUC_REG_CLEAR_DATA_MSB			= 0x56 # Clear high data register

# BH1745NUC Mode Control-1 Register Configuration
BH1745NUC_RGBC_MEASURE_TIME_160			= 0x00 # RGBC Measurement time = 160 ms
BH1745NUC_RGBC_MEASURE_TIME_320			= 0x01 # RGBC Measurement time = 320 ms
BH1745NUC_RGBC_MEASURE_TIME_640			= 0x02 # RGBC Measurement time = 640 ms
BH1745NUC_RGBC_MEASURE_TIME_1280		= 0x03 # RGBC Measurement time = 1280 ms
BH1745NUC_RGBC_MEASURE_TIME_2560		= 0x04 # RGBC Measurement time = 2560 ms
BH1745NUC_RGBC_MEASURE_TIME_5120		= 0x05 # RGBC Measurement time = 5120 ms

# BH1745NUC Mode Control-2 Register Configuration
BH1745NUC_VALID_NO_UPDATE				= 0x00 # RGBC data is not updated after last writing MODE_CONTROL-1,2,3 register or last reading MODE_CONTROL2 register
BH1745NUC_VALID_UPDATE					= 0x80 # RGBC data is updated after last writing MODE_CONTROL-1,2,3 register or last reading MODE_CONTROL2 register
BH1745NUC_RGBC_DS						= 0x00 # RGBC measurement is inactive and becomes power down
BH1745NUC_RGBC_EN						= 0x10 # RGBC measurement is active
BH1745NUC_ADC_GAIN_1					= 0x00 # Gain = 1x
BH1745NUC_ADC_GAIN_2					= 0x01 # Gain = 2x
BH1745NUC_ADC_GAIN_16					= 0x02 # Gain = 16x

# BH1745NUC Mode Control-3 Register Configuration
BH1745NUC_DEFAULT_RESERVED				= 0x02 # Default value

class BH1745NUC():
	def __init__(self):
		self.time_config()
		self.gain_config()
		self.write_default()
	
	def time_config(self):
		"""Select the mode control-1 register configuration from the given provided values"""
		TIME_CONFIG = (BH1745NUC_RGBC_MEASURE_TIME_160)
		bus.write_byte_data(BH1745NUC_DEFAULT_ADDRESS, BH1745NUC_REG_MODE_CONTROL1, TIME_CONFIG)
	
	def gain_config(self):
		"""Select the mode control-2 register configuration from the given provided values"""
		GAIN_CONFIG = (BH1745NUC_VALID_UPDATE | BH1745NUC_RGBC_EN | BH1745NUC_ADC_GAIN_1)
		bus.write_byte_data(BH1745NUC_DEFAULT_ADDRESS, BH1745NUC_REG_MODE_CONTROL2, GAIN_CONFIG)
	
	def write_default(self):
		"""Select the mode control-2 register configuration from the given provided values"""
		bus.write_byte_data(BH1745NUC_DEFAULT_ADDRESS, BH1745NUC_REG_MODE_CONTROL3, BH1745NUC_DEFAULT_RESERVED)
	
	time.sleep(0.5)
	
	def read_luminance(self):
		"""Read data back from BH1745NUC_REG_RED_DATA_LSB(0x50), 8 bytes
		Red LSB, Red MSB, Green LSB, Green MSB, Blue LSB, Blue MSB, cData LSB, cData MSB"""
		data = bus.read_i2c_block_data(BH1745NUC_DEFAULT_ADDRESS, BH1745NUC_REG_RED_DATA_LSB, 8)
		
		# Convert the data
		red = data[1] * 256 + data[0]
		green = data[3] * 256 + data[2]
		blue = data[5] * 256 + data[4]
		cData = data[7] * 256 + data[6]
		
		return {'c' :  cData, 'r' : red, 'g' : green, 'b' : blue}

from BH1745NUC import BH1745NUC
bh1745nuc = BH1745NUC()

while True:

	lum = bh1745nuc.read_luminance()
	print "Red Color Luminance : %d lux"%(lum['r'])
	print "Green Color Luminance : %d lux"%(lum['g'])
	print "Blue Color Luminance : %d lux"%(lum['b'])
	print "Clear Data Color Luminance : %d lux"%(lum['c'])
	print " ***************************************************** "
	time.sleep(1)
