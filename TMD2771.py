# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# TMD2771
# This code is designed to work with the TMD2771_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Light?sku=TMD2771_I2CS#tabs-0-product_tabset-2
# NT

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
TMD2771_DEFAULT_ADDRESS			= 0x39

# TMD2771 Register Set
TMD2771_COMMAND_BIT					= 0xA0 # Auto-increment protocol transaction
TMD2771_REG_ENABLE					= 0x00 # Enables states and interrupts
TMD2771_REG_ATIME					= 0x01 # ALS ADC time
TMD2771_REG_PTIME					= 0x02 # Proximity ADC time
TMD2771_REG_WTIME					= 0x03 # Wait time
TMD2771_REG_CONFIG					= 0x0D # Configuration register
TMD2771_REG_PPULSE					= 0x0E # Proximity pulse register
TMD2771_REG_CONTROL					= 0x0F # Control register
TMD2771_REG_DEVICE_ID				= 0x12 # Device ID register
TMD2771_REG_STATUS					= 0x13 # Device Status register
TMD2771_REG_C0DATAL					= 0x14 # Ch0 channel low data register
TMD2771_REG_C0DATAH					= 0x15 # Ch0 high data register
TMD2771_REG_C1DATAL					= 0x16 # Ch1 low data register
TMD2771_REG_C1DATAH					= 0x17 # Ch1 high data register
TMD2771_REG_PDATAL					= 0x18 # Proximity ADC low data register
TMD2771_REG_PDATAH					= 0x19 # Proximity ADC high data register

# TMD2771 Enable Register Configuration
TMD2771_REG_ENABLE_PIEN				= 0x20 # Proximity Interrupt Enable
TMD2771_REG_ENABLE_AIEN				= 0x10 # ALS Interrupt Enable
TMD2771_REG_ENABLE_WEN				= 0x08 # Wait Enable
TMD2771_REG_ENABLE_PEN				= 0x04 # Proximity Enable
TMD2771_REG_ENABLE_AEN				= 0x02 # ALS Enable
TMD2771_REG_ENABLE_PON				= 0x01 # Power ON

# TMD2771 ATime Register Configuration
TMD2771_REG_ATIME_2_72				= 0xFF # Atime = 2.72 ms, Cycles = 1
TMD2771_REG_ATIME_27_2				= 0xF6 # Atime = 27.2 ms, Cycles = 10
TMD2771_REG_ATIME_101				= 0xDB # Atime = 101 ms, Cycles = 37
TMD2771_REG_ATIME_174				= 0xC0 # Atime = 174 ms, Cycles = 64
TMD2771_REG_ATIME_696				= 0x00 # Atime = 696 ms, Cycles = 256

# TMD2771 PTime Register Configuration
TMD2771_REG_PTIME_2_72				= 0xFF # Ptime = 2.72 ms

# TMD2771 WTime Register Configuration
TMD2771_REG_WTIME_2_72				= 0xFF # Wtime = 2.72 ms
TMD2771_REG_WTIME_200				= 0xB6 # Wtime = 200 ms
TMD2771_REG_WTIME_700				= 0x00 # Wtime = 700 ms

# TMD2771 Proximity Pulse Register Configuration
TMD2771_REG_PPULSE_COUNT			= 0x0F # Pulse Count = 15 (Specifies the number of proximity pulses to be generated)

# TMD2771 Control Register Configuration
TMD2771_REG_CONTROL_LED_100			= 0x00 # LED Strength - 100%
TMD2771_REG_CONTROL_LED_50			= 0x40 # LED Strength - 50%
TMD2771_REG_CONTROL_LED_25			= 0x80 # LED Strength - 25%
TMD2771_REG_CONTROL_LED_12_5		= 0xC0 # LED Strength - 12.5%
TMD2771_REG_CONTROL_PDIODE_0		= 0x10 # Proximity uses the Channel 0 diode
TMD2771_REG_CONTROL_PDIODE_1		= 0x20 # Proximity uses the Channel 1 diode
TMD2771_REG_CONTROL_PDIODE_BOTH		= 0x30 # Proximity uses the both diodes
TMD2771_REG_CONTROL_AGAIN_1			= 0x00 # ALS GAIN VALUE - 1x Gain
TMD2771_REG_CONTROL_AGAIN_4			= 0x01 # ALS GAIN VALUE - 4x Gain
TMD2771_REG_CONTROL_AGAIN_16		= 0x02 # ALS GAIN VALUE - 16x Gain
TMD2771_REG_CONTROL_AGAIN_64		= 0x03 # ALS GAIN VALUE - 120x Gain

class TMD2771():
	def __init__(self):
		self.enable_selection()
		self.time_selection()
		self.pulse_selection()
		self.gain_selection()
	
	def enable_selection(self):
		"""Select the ENABLE register configuration from the given provided values"""
		ENABLE_CONFIGURATION = (TMD2771_REG_ENABLE_WEN | TMD2771_REG_ENABLE_PEN | TMD2771_REG_ENABLE_AEN | TMD2771_REG_ENABLE_PON)
		bus.write_byte_data(TMD2771_DEFAULT_ADDRESS, TMD2771_REG_ENABLE | TMD2771_COMMAND_BIT, ENABLE_CONFIGURATION)
	
	time.sleep(0.3)
	
	def time_selection(self):
		"""Select the ATIME register configuration from the given provided values"""
		bus.write_byte_data(TMD2771_DEFAULT_ADDRESS, TMD2771_REG_ATIME | TMD2771_COMMAND_BIT, TMD2771_REG_ATIME_101)
		
		"""Select the PTIME register configuration from the given provided values"""
		bus.write_byte_data(TMD2771_DEFAULT_ADDRESS, TMD2771_REG_PTIME | TMD2771_COMMAND_BIT, TMD2771_REG_PTIME_2_72)
		
		"""Select the WTIME register configuration from the given provided values"""
		bus.write_byte_data(TMD2771_DEFAULT_ADDRESS, TMD2771_REG_WTIME | TMD2771_COMMAND_BIT, TMD2771_REG_WTIME_2_72)
	
	def pulse_selection(self):
		"""Select the PPULSE register configuration from the given provided values"""
		bus.write_byte_data(TMD2771_DEFAULT_ADDRESS, TMD2771_REG_PPULSE, TMD2771_REG_PPULSE_COUNT)
	
	def gain_selection(self):
		"""Select the CONTROL register configuration from the given provided values"""
		GAIN_CONFIGURATION = (TMD2771_REG_CONTROL_LED_100 | TMD2771_REG_CONTROL_PDIODE_BOTH | TMD2771_REG_CONTROL_AGAIN_1)
		bus.write_byte_data(TMD2771_DEFAULT_ADDRESS, TMD2771_REG_CONTROL | TMD2771_COMMAND_BIT, GAIN_CONFIGURATION)

	def readluminance(self):
		"""Read data back from TMD2771_REG_C0DATAL(0x14), 6 bytes, with TMD2771_COMMAND_BIT, (0xA0)
		c0Data LSB, c0Data MSB, c1Data LSB, c1Data MSB, Proximity LSB, Proximity MSB"""
		data = bus.read_i2c_block_data(TMD2771_DEFAULT_ADDRESS, TMD2771_REG_C0DATAL | TMD2771_COMMAND_BIT, 6)
		
		# Convert the data
		c0Data = (data[1] * 256) + data[0]
		c1Data = (data[3] * 256) + data[2]
		proximity = (data[5] * 256) + data[4]
		luminance = 0.0
		CPL = (101.0) / 24.0
		luminance1 = ((1.00 *  c0Data) - (2 * c1Data)) / CPL
		luminance2 = ((0.6 * c0Data) - (1.00 * c1Data)) / CPL
		if luminance1 > 0 and luminance2 > 0 :
			if luminance1 > luminance2 :
				luminance = luminance1
			else :
				luminance = luminance2
		
		return {'l' : luminance, 'p' : proximity}

from TMD2771 import TMD2771
tmd2771 = TMD2771()

while True:
	lum = tmd2771.readluminance()
	print "Ambient Light Luminance : %.2f lux"%(lum['l'])
	print "Proximity of the Device : %d " %(lum['p'])
	print " ************************************************ "
	time.sleep(1)
