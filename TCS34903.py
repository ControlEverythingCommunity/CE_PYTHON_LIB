# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# TCS34903
# This code is designed to work with the TCS34903_IS2C I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Color?sku=TCS34903FN_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
TCS34903_DEFAULT_ADDRESS			= 0x39

# TCS34903 Register Set
TCS34903_REG_ENABLE					= 0x80 # Enables states and interrupts
TCS34903_REG_ATIME					= 0x81 # RGBC integration time
TCS34903_REG_WTIME					= 0x83 # Wait time
TCS34903_REG_CONFIG					= 0x8D # Configuration register
TCS34903_REG_CONTROL				= 0x8F # Control register
TCS34903_REG_CDATAL					= 0x94 # Clear/IR channel low data register
TCS34903_REG_CDATAH					= 0x95 # Clear/IR channel high data register
TCS34903_REG_RDATAL					= 0x96 # Red ADC low data register
TCS34903_REG_RDATAH					= 0x97 # Red ADC high data register
TCS34903_REG_GDATAL					= 0x98 # Green ADC low data register
TCS34903_REG_GDATAH					= 0x99 # Green ADC high data register
TCS34903_REG_BDATAL					= 0x9A # Blue ADC low data register
TCS34903_REG_BDATAH					= 0x9B # Blue ADC high data register

# TCS34903 Enable Register Configuration
TCS34903_REG_ENABLE_SAI				= 0x40 # Sleep After Interrupt
TCS34903_REG_ENABLE_AIEN			= 0x10 # ALS Interrupt Enable
TCS34903_REG_ENABLE_WEN				= 0x08 # Wait Enable
TCS34903_REG_ENABLE_AEN				= 0x02 # ADC Enable
TCS34903_REG_ENABLE_PON				= 0x01 # Power ON

# TCS34903 Time Register Configuration
TCS34903_REG_ATIME_2_78				= 0xFF # Atime = 2.78 ms, Cycles = 1
TCS34903_REG_ATIME_27_8				= 0xF6 # Atime = 27.8 ms, Cycles = 10
TCS34903_REG_ATIME_103				= 0xDB # Atime = 103 ms, Cycles = 37
TCS34903_REG_ATIME_178				= 0xC0 # Atime = 178 ms, Cycles = 64
TCS34903_REG_ATIME_712				= 0x00 # Atime = 712 ms, Cycles = 256
TCS34903_REG_WTIME_2_78				= 0xFF # Wtime = 2.78 ms
TCS34903_REG_WTIME_236				= 0xAB # Wtime = 236 ms
TCS34903_REG_WTIME_712				= 0x00 # Wtime = 712 ms

# TCS34903 Gain Configuration
TCS34903_REG_CONTROL_AGAIN_1		= 0x00 # 1x Gain
TCS34903_REG_CONTROL_AGAIN_4		= 0x01 # 4x Gain
TCS34903_REG_CONTROL_AGAIN_16		= 0x02 # 16x Gain
TCS34903_REG_CONTROL_AGAIN_64		= 0x03 # 64x Gain

class TCS34903():
	def __init__(self):
		self.enable_selection()
		self.time_selection()
		self.gain_selection()
	
	def enable_selection(self):
		"""Select the ENABLE register configuration from the given provided values"""
		ENABLE_CONFIGURATION = (TCS34903_REG_ENABLE_AEN | TCS34903_REG_ENABLE_PON)
		bus.write_byte_data(TCS34903_DEFAULT_ADDRESS, TCS34903_REG_ENABLE, ENABLE_CONFIGURATION)
	
	def time_selection(self):
		"""Select the ATIME register configuration from the given provided values"""
		bus.write_byte_data(TCS34903_DEFAULT_ADDRESS, TCS34903_REG_ATIME, TCS34903_REG_ATIME_712)
		
		"""Select the WTIME register configuration from the given provided values"""
		bus.write_byte_data(TCS34903_DEFAULT_ADDRESS, TCS34903_REG_WTIME, TCS34903_REG_WTIME_2_78)
	
	def gain_selection(self):
		"""Select the gain register configuration from the given provided values"""
		bus.write_byte_data(TCS34903_DEFAULT_ADDRESS, TCS34903_REG_CONTROL, TCS34903_REG_CONTROL_AGAIN_1)
	
	def readluminance(self):
		"""Read data back from TCS34903_REG_CDATAL(0x94), 8 bytes, with TCS34903_COMMAND_BIT, (0x80)
		Clear LSB, Clear MSB, Red LSB, Red MSB, Green LSB, Green MSB, Blue LSB, Blue MSB"""
		data = bus.read_i2c_block_data(TCS34903_DEFAULT_ADDRESS, TCS34903_REG_CDATAL, 8)
		
		# Convert the data
		clear = data[1] * 256 + data[0]
		red = data[3] * 256 + data[2]
		green = data[5] * 256 + data[4]
		blue = data[7] * 256 + data[6]
		
		return {'c' : clear, 'r' : red, 'g' : green, 'b' : blue}

from TCS34903 import TCS34903
tcs34903 = TCS34903()

while True:
	lum = tcs34903.readluminance()
	print "Clear Data Luminance : %d "%(lum['c'])
	print "Red Color Luminance : %d "%(lum['r'])
	print "Green Color Luminance : %d "%(lum['g'])
	print "Blue Color Luminance : %d "%(lum['b'])
	print " ************************************************ "
	time.sleep(1)
