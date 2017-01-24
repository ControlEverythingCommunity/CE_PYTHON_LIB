# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# TMG39931
# This code is designed to work with the TMG39931_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Color?sku=TMG39931_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
TMG39931_DEFAULT_ADDRESS			= 0x39

# TMG39931 Register Set
TMG39931_REG_ENABLE					= 0x80 # Enables states and interrupts
TMG39931_REG_ATIME					= 0x81 # ADC integration time
TMG39931_REG_WTIME					= 0x83 # Wait time
TMG39931_REG_CONFIG1				= 0x8D # Configuration register 1
TMG39931_REG_PPULSE					= 0x8E # Proximity pulse count and length
TMG39931_REG_CONTROL				= 0x8F # Control register
TMG39931_REG_CONFIG2				= 0x90 # Configuration register 2
TMG39931_REG_CDATAL					= 0x94 # Clear ADC low data register
TMG39931_REG_CDATAH					= 0x95 # Clear ADC high data register
TMG39931_REG_RDATAL					= 0x96 # Red ADC low data register
TMG39931_REG_RDATAH					= 0x97 # Red ADC high data register
TMG39931_REG_GDATAL					= 0x98 # Green ADC low data register
TMG39931_REG_GDATAH					= 0x99 # Green ADC high data register
TMG39931_REG_BDATAL					= 0x9A # Blue ADC low data register
TMG39931_REG_BDATAH					= 0x9B # Blue ADC high data register
TMG39931_REG_PDATA					= 0x9C # Proximity ADC data register

# TMG39931 Enable Register Configuration
TMG39931_REG_ENABLE_PBEN			= 0x80 # Pattern Burst Enable
TMG39931_REG_ENABLE_GEN				= 0x40 # Gesture Enable
TMG39931_REG_ENABLE_PIEN			= 0x20 # Proximity Interrupt Enable
TMG39931_REG_ENABLE_AIEN			= 0x10 # ALS Interrupt Enable
TMG39931_REG_ENABLE_WEN				= 0x08 # Wait Enable
TMG39931_REG_ENABLE_PEN				= 0x04 # Proximity Enable
TMG39931_REG_ENABLE_AEN				= 0x02 # ALS Enable
TMG39931_REG_ENABLE_PON				= 0x01 # Power ON

# TMG39931 ATime Register Configuration
TMG39931_REG_ATIME_2_78				= 0xFF # Atime = 2.78 ms, Cycles = 1
TMG39931_REG_ATIME_27_8				= 0xF6 # Atime = 27.8 ms, Cycles = 10
TMG39931_REG_ATIME_103				= 0xDB # Atime = 103 ms, Cycles = 37
TMG39931_REG_ATIME_178				= 0xC0 # Atime = 178 ms, Cycles = 64
TMG39931_REG_ATIME_712				= 0x00 # Atime = 712 ms, Cycles = 256

# TMG39931 WTime Register Configuration
TMG39931_REG_WTIME_2_78				= 0xFF # Wtime = 2.78 ms
TMG39931_REG_WTIME_236				= 0xAB # Wtime = 236 ms
TMG39931_REG_WTIME_712				= 0x00 # Wtime = 712 ms

# TMG39931 Control Register Configuration
TMG39931_REG_CONTROL_LED_100		= 0x00 # LED Strength - 100%
TMG39931_REG_CONTROL_LED_50			= 0x40 # LED Strength - 50%
TMG39931_REG_CONTROL_LED_25			= 0x80 # LED Strength - 25%
TMG39931_REG_CONTROL_LED_12_5		= 0xC0 # LED Strength - 12.5%
TMG39931_REG_CONTROL_PGAIN_1		= 0x00 # Proximity GAIN VALUE - 1x Gain
TMG39931_REG_CONTROL_PGAIN_2		= 0x04 # Proximity GAIN VALUE - 2x Gain
TMG39931_REG_CONTROL_PGAIN_4		= 0x08 # Proximity GAIN VALUE - 4x Gain
TMG39931_REG_CONTROL_PGAIN_8		= 0x0C # Proximity GAIN VALUE - 8x Gain
TMG39931_REG_CONTROL_AGAIN_1		= 0x00 # RGBC GAIN VALUE - 1x Gain
TMG39931_REG_CONTROL_AGAIN_4		= 0x01 # RGBC GAIN VALUE - 4x Gain
TMG39931_REG_CONTROL_AGAIN_16		= 0x02 # RGBC GAIN VALUE - 16x Gain
TMG39931_REG_CONTROL_AGAIN_64		= 0x03 # RGBC GAIN VALUE - 64x Gain

class TMG39931():
	def __init__(self):
		self.enable_selection()
		self.time_selection()
		self.gain_selection()
	
	def enable_selection(self):
		"""Select the ENABLE register configuration from the given provided values"""
		ENABLE_CONFIGURATION = (TMG39931_REG_ENABLE_WEN | TMG39931_REG_ENABLE_PEN | TMG39931_REG_ENABLE_AEN | TMG39931_REG_ENABLE_PON)
		bus.write_byte_data(TMG39931_DEFAULT_ADDRESS, TMG39931_REG_ENABLE, ENABLE_CONFIGURATION)
	
	def time_selection(self):
		"""Select the ATIME register configuration from the given provided values"""
		bus.write_byte_data(TMG39931_DEFAULT_ADDRESS, TMG39931_REG_ATIME, TMG39931_REG_ATIME_712)
		
		"""Select the WTIME register configuration from the given provided values"""
		bus.write_byte_data(TMG39931_DEFAULT_ADDRESS, TMG39931_REG_WTIME, TMG39931_REG_WTIME_2_78)
	
	def gain_selection(self):
		"""Select the CONTROL register configuration from the given provided values"""
		GAIN_CONFIGURATION = (TMG39931_REG_CONTROL_LED_100 | TMG39931_REG_CONTROL_PGAIN_1 | TMG39931_REG_CONTROL_AGAIN_1)
		bus.write_byte_data(TMG39931_DEFAULT_ADDRESS, TMG39931_REG_CONTROL, GAIN_CONFIGURATION)
	
	def readluminance(self):
		"""Read data back from TMG39931_REG_CDATAL(0x94), 9 bytes
		cData LSB, cData MSB, red LSB, red MSB, green LSB, green MSB, blue LSB, blue MSB, proximity"""
		data = bus.read_i2c_block_data(TMG39931_DEFAULT_ADDRESS, TMG39931_REG_CDATAL, 9)
		
		# Convert the data
		cData = data[1] * 256.0 + data[0]
		red = data[3] * 256.0 + data[2]
		green = data[5] * 256.0 + data[4]
		blue = data[7] * 256.0 + data[6]
		proximity = data[8]
		
		return {'i' : cData, 'r' : red, 'g' : green, 'b' : blue, 'p' : proximity}

from TMG39931 import TMG39931
tmg39931 = TMG39931()

while True:
	lum = tmg39931.readluminance()
	print "InfraRed Luminance : %d lux"%(lum['i'])
	print "Red Color Luminance : %d lux"%(lum['r'])
	print "Green Color Luminance : %d lux"%(lum['g'])
	print "Blue Color Luminance : %d lux"%(lum['b'])
	print "Proximity of the device : %d " %(lum['p'])
	print " ***************************************************** "
	time.sleep(1)
