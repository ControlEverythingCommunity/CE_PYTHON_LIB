# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# TSL2772
# This code is designed to work with the TSL2772_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/products

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
TSL27721_DEFAULT_ADDRESS				= 0x39

# TSL27721 Register Set
TSL27721_COMMAND_BIT					= 0x80
TSL27721_REG_ENABLE						= 0x00 # Enables states and interrupts
TSL27721_REG_ATIME						= 0x01 # ALS ADC time
TSL27721_REG_PTIME						= 0x02 # Proximity ADC time
TSL27721_REG_WTIME						= 0x03 # Wait time
TSL27721_REG_CONFIG						= 0x0D # Configuration register
TSL27721_REG_PPULSE						= 0x0E # Proximity pulse register
TSL27721_REG_CONTROL					= 0x0F # Control register
TSL27721_REG_DEVICE_ID					= 0x12 # Device ID register
TSL27721_REG_STATUS						= 0x13 # Device Status register
TSL27721_REG_C0DATAL					= 0x14 # Ch0 channel low data register
TSL27721_REG_C0DATAH					= 0x15 # Ch0 high data register
TSL27721_REG_C1DATAL					= 0x16 # Ch1 low data register
TSL27721_REG_C1DATAH					= 0x17 # Ch1 high data register
TSL27721_REG_PDATAL						= 0x18 # Proximity ADC low data register
TSL27721_REG_PDATAH						= 0x19 # Proximity ADC high data register

# TSL27721 Enable Register Configuration
TSL27721_REG_ENABLE_SAI					= 0x40 # Sleep After Interrupt Enable
TSL27721_REG_ENABLE_PIEN				= 0x20 # Proximity Interrupt Enable
TSL27721_REG_ENABLE_AIEN				= 0x10 # ALS Interrupt Enable
TSL27721_REG_ENABLE_WEN					= 0x08 # Wait Enable
TSL27721_REG_ENABLE_PEN					= 0x04 # Proximity Enable
TSL27721_REG_ENABLE_AEN					= 0x02 # ALS Enable
TSL27721_REG_ENABLE_PON					= 0x01 # Power ON

# TSL27721 ATime Register Configuration
TSL27721_REG_ATIME_2_73					= 0xFF # Atime = 2.73 ms, Cycles = 1
TSL27721_REG_ATIME_27_3					= 0xF6 # Atime = 27.3 ms, Cycles = 10
TSL27721_REG_ATIME_101					= 0xDB # Atime = 101 ms, Cycles = 37
TSL27721_REG_ATIME_175					= 0xC0 # Atime = 175 ms, Cycles = 64
TSL27721_REG_ATIME_699					= 0x00 # Atime = 699 ms, Cycles = 256

# TSL27721 PTime Register Configuration
TSL27721_REG_PTIME_2_73					= 0xFF # Ptime = 2.73 ms

# TSL27721 WTime Register Configuration
TSL27721_REG_WTIME_2_73					= 0xFF # Wtime = 2.73 ms
TSL27721_REG_WTIME_202					= 0xB6 # Wtime = 202 ms
TSL27721_REG_WTIME_699					= 0x00 # Wtime = 699 ms

# TSL27721 Proximity Pulse Register Configuration
TSL27721_REG_PPULSE_COUNT				= 0x20 # Pulse Count = 32 (Specifies the number of proximity pulses to be generated)

# TSL27721 Control Register Configuration
TSL27721_REG_CONTROL_LED_100			= 0x00 # LED Strength - 100%
TSL27721_REG_CONTROL_LED_50				= 0x40 # LED Strength - 50%
TSL27721_REG_CONTROL_LED_25				= 0x80 # LED Strength - 25%
TSL27721_REG_CONTROL_LED_12_5			= 0xC0 # LED Strength - 12.5%
TSL27721_REG_CONTROL_PDIODE_0			= 0x10 # Proximity uses the Channel 0 diode
TSL27721_REG_CONTROL_PDIODE_1			= 0x20 # Proximity uses the Channel 1 diode
TSL27721_REG_CONTROL_PDIODE_NONE		= 0x00 # Proximity uses the neither diodes
TSL27721_REG_CONTROL_PGAIN_1			= 0x00 # Proximity GAIN VALUE - 1x Gain
TSL27721_REG_CONTROL_PGAIN_2			= 0x04 # Proximity GAIN VALUE - 2x Gain
TSL27721_REG_CONTROL_PGAIN_4			= 0x08 # Proximity GAIN VALUE - 4x Gain
TSL27721_REG_CONTROL_PGAIN_8			= 0x0C # Proximity GAIN VALUE - 8x Gain
TSL27721_REG_CONTROL_AGAIN_1			= 0x00 # ALS GAIN VALUE - 1x Gain
TSL27721_REG_CONTROL_AGAIN_8			= 0x01 # ALS GAIN VALUE - 8x Gain
TSL27721_REG_CONTROL_AGAIN_16			= 0x02 # ALS GAIN VALUE - 16x Gain
TSL27721_REG_CONTROL_AGAIN_64			= 0x03 # ALS GAIN VALUE - 120x Gain

class TSL27721():
	def __init__(self):
		self.enable_selection()
		self.time_selection()
		self.pulse_selection()
		self.gain_selection()
	
	def enable_selection(self):
		"""Select the ENABLE register configuration from the given provided values"""
		ENABLE_CONFIGURATION = (TSL27721_REG_ENABLE_WEN | TSL27721_REG_ENABLE_PEN | TSL27721_REG_ENABLE_AEN | TSL27721_REG_ENABLE_PON)
		bus.write_byte_data(TSL27721_DEFAULT_ADDRESS, TSL27721_REG_ENABLE | TSL27721_COMMAND_BIT, ENABLE_CONFIGURATION)
	
	def time_selection(self):
		"""Select the ATIME register configuration from the given provided values"""
		bus.write_byte_data(TSL27721_DEFAULT_ADDRESS, TSL27721_REG_ATIME | TSL27721_COMMAND_BIT, TSL27721_REG_ATIME_2_73)
		
		"""Select the PTIME register configuration from the given provided values"""
		bus.write_byte_data(TSL27721_DEFAULT_ADDRESS, TSL27721_REG_PTIME | TSL27721_COMMAND_BIT, TSL27721_REG_PTIME_2_73)
		
		"""Select the WTIME register configuration from the given provided values"""
		bus.write_byte_data(TSL27721_DEFAULT_ADDRESS, TSL27721_REG_WTIME | TSL27721_COMMAND_BIT, TSL27721_REG_WTIME_2_73)
	
	def pulse_selection(self):
		"""Select the PPULSE register configuration from the given provided values"""
		bus.write_byte_data(TSL27721_DEFAULT_ADDRESS, TSL27721_REG_PPULSE, TSL27721_REG_PPULSE_COUNT)
	
	def gain_selection(self):
		"""Select the CONTROL register configuration from the given provided values"""
		GAIN_CONFIGURATION = (TSL27721_REG_CONTROL_LED_100 | TSL27721_REG_CONTROL_PDIODE_1 | TSL27721_REG_CONTROL_PGAIN_1 | TSL27721_REG_CONTROL_AGAIN_1)
		bus.write_byte_data(TSL27721_DEFAULT_ADDRESS, TSL27721_REG_CONTROL | TSL27721_COMMAND_BIT, GAIN_CONFIGURATION)

	def readluminance(self):
		"""Read data back from TSL27721_REG_C0DATAL(0x14), 6 bytes, with TSL27721_COMMAND_BIT, (0x80)
		c0Data LSB, c0Data MSB, c1Data LSB, c1Data MSB, Proximity LSB, Proximity MSB"""
		data = bus.read_i2c_block_data(TSL27721_DEFAULT_ADDRESS, TSL27721_REG_C0DATAL | TSL27721_COMMAND_BIT, 6)
		
		# Convert the data
		c0Data = data[1] * 256 + data[0]
		c1Data = data[3] * 256 + data[2]
		proximity = data[5] * 256 + data[4]
		luminance = 0.0
		CPL = 2.73 / 60.0
		luminance1 = (1.00 *  c0Data - (1.87 * c1Data)) / CPL
		luminance2 = ((0.63 * c0Data) - (1.00 * c1Data)) / CPL
		if luminance1 > 0 and luminance2 > 0 :
			if luminance1 > luminance2 :
				luminance = luminance1
			else :
				luminance = luminance2
		
		return {'l' : luminance, 'p' : proximity}

from TSL27721 import TSL27721
tsl27721 = TSL27721()

while True:
	lum = tsl27721.readluminance()
	print "Ambient Light Luminance : %.2f lux"%(lum['l'])
	print "Proximity of the Device : %d " %(lum['p'])
	print " ************************************************ "
	time.sleep(1)
