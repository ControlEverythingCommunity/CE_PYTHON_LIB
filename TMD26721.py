# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# TMD26721
# This code is designed to work with the TMD26721_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Proximity?sku=TMD26721_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
TMD26721_DEFAULT_ADDRESS			= 0x39

# TMD26721 Register Set
TMD26721_COMMAND_BIT				= 0x80
TMD26721_REG_ENABLE					= 0x00 # Enables states and interrupts
TMD26721_REG_PTIME					= 0x02 # Proximity ADC time
TMD26721_REG_WTIME					= 0x03 # Wait time
TMD26721_REG_CONFIG					= 0x0D # Configuration register
TMD26721_REG_PPULSE					= 0x0E # Proximity pulse register
TMD26721_REG_CONTROL				= 0x0F # Control register
TMD26721_REG_DEVICE_ID				= 0x12 # Device ID register
TMD26721_REG_STATUS					= 0x13 # Device Status register
TMD26721_REG_PDATAL					= 0x18 # Proximity ADC low data register
TMD26721_REG_PDATAH					= 0x19 # Proximity ADC high data register

# TMD26721 Enable Register Configuration
TMD26721_REG_ENABLE_SAI				= 0x40 # Sleep After Interrupt Enable
TMD26721_REG_ENABLE_PIEN			= 0x20 # Proximity Interrupt Enable
TMD26721_REG_ENABLE_WEN				= 0x08 # Wait Enable
TMD26721_REG_ENABLE_PEN				= 0x04 # Proximity Enable
TMD26721_REG_ENABLE_PON				= 0x01 # Power ON

# TMD26721 PTime Register Configuration
TMD26721_REG_PTIME_2_73				= 0xFF # Ptime = 2.73 ms

# TMD26721 WTime Register Configuration
TMD26721_REG_WTIME_2_72				= 0xFF # Wtime = 2.72 ms
TMD26721_REG_WTIME_200				= 0xB6 # Wtime = 200 ms
TMD26721_REG_WTIME_700				= 0x00 # Wtime = 700 ms

# TMD26721 Proximity Pulse Register Configuration
TMD26721_REG_PPULSE_COUNT			= 0x20 # Pulse Count = 32 (Specifies the number of proximity pulses to be generated)

# TMD26721 Control Register Configuration
TMD26721_REG_CONTROL_LED_100		= 0x00 # LED Strength - 100%
TMD26721_REG_CONTROL_LED_50			= 0x40 # LED Strength - 50%
TMD26721_REG_CONTROL_LED_25			= 0x80 # LED Strength - 25%
TMD26721_REG_CONTROL_LED_12_5		= 0xC0 # LED Strength - 12.5%
TMD26721_REG_CONTROL_PDIODE_0		= 0x10 # Proximity uses the Channel 0 diode
TMD26721_REG_CONTROL_PDIODE_1		= 0x20 # Proximity uses the Channel 1 diode
TMD26721_REG_CONTROL_PDIODE_NONE	= 0x00 # Proximity uses the neither diodes
TMD26721_REG_CONTROL_PGAIN_1		= 0x00 # Proximity GAIN VALUE - 1x Gain
TMD26721_REG_CONTROL_PGAIN_2		= 0x04 # Proximity GAIN VALUE - 2x Gain
TMD26721_REG_CONTROL_PGAIN_4		= 0x08 # Proximity GAIN VALUE - 4x Gain
TMD26721_REG_CONTROL_PGAIN_8		= 0x0C # Proximity GAIN VALUE - 8x Gain

class TMD26721():
	def __init__(self):
		self.enable_selection()
		self.time_selection()
		self.pulse_selection()
		self.gain_selection()
	
	def enable_selection(self):
		"""Select the ENABLE register configuration from the given provided values"""
		ENABLE_CONFIGURATION = (TMD26721_REG_ENABLE_WEN | TMD26721_REG_ENABLE_PEN | TMD26721_REG_ENABLE_PON)
		bus.write_byte_data(TMD26721_DEFAULT_ADDRESS, TMD26721_REG_ENABLE | TMD26721_COMMAND_BIT, ENABLE_CONFIGURATION)
	
	def time_selection(self):
		"""Select the PTIME register configuration from the given provided values"""
		bus.write_byte_data(TMD26721_DEFAULT_ADDRESS, TMD26721_REG_PTIME | TMD26721_COMMAND_BIT, TMD26721_REG_PTIME_2_73)
		
		"""Select the WTIME register configuration from the given provided values"""
		bus.write_byte_data(TMD26721_DEFAULT_ADDRESS, TMD26721_REG_WTIME | TMD26721_COMMAND_BIT, TMD26721_REG_WTIME_2_72)
	
	def pulse_selection(self):
		"""Select the PPULSE register configuration from the given provided values"""
		bus.write_byte_data(TMD26721_DEFAULT_ADDRESS, TMD26721_REG_PPULSE, TMD26721_REG_PPULSE_COUNT)
	
	def gain_selection(self):
		"""Select the CONTROL register configuration from the given provided values"""
		GAIN_CONFIGURATION = (TMD26721_REG_CONTROL_LED_100 | TMD26721_REG_CONTROL_PDIODE_1 | TMD26721_REG_CONTROL_PGAIN_1)
		bus.write_byte_data(TMD26721_DEFAULT_ADDRESS, TMD26721_REG_CONTROL | TMD26721_COMMAND_BIT, GAIN_CONFIGURATION)

	def read_prox(self):
		"""Read data back from TMD26721_REG_PDATAL(0x18), 2 bytes, with TMD26721_COMMAND_BIT,(0x80)
		Proximity LSB, Proximity MSB"""
		data = bus.read_i2c_block_data(TMD26721_DEFAULT_ADDRESS, TMD26721_REG_PDATAL | TMD26721_COMMAND_BIT, 2)
		
		# Convert the data
		proximity = data[1] * 256 + data[0]
		
		return {'p' : proximity}

from TMD26721 import TMD26721
tmd26721 = TMD26721()

while True:
	prox = tmd26721.read_prox()
	print "Proximity of the Device : %d " %(prox['p'])
	print " ***************************************** "
	time.sleep(1)
