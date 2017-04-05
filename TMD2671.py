# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# TMD2671
# This code is designed to work with the TMD2671_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/products

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)


# I2C Address of the device
TMD2671_DEFAULT_ADDRESS				= 0x39

# TMD2671 Register Set
TMD2671_COMMAND_BIT					= 0x80
TMD2671_REG_ENABLE					= 0x00 # Enables states and interrupts
TMD2671_REG_PTIME					= 0x02 # Proximity ADC time
TMD2671_REG_WTIME					= 0x03 # Wait time
TMD2671_REG_CONFIG					= 0x0D # Configuration register
TMD2671_REG_PPULSE					= 0x0E # Proximity pulse register
TMD2671_REG_CONTROL					= 0x0F # Control register
TMD2671_REG_DEVICE_ID				= 0x12 # Device ID register
TMD2671_REG_STATUS					= 0x13 # Device Status register
TMD2671_REG_PDATAL					= 0x18 # Proximity ADC low data register
TMD2671_REG_PDATAH					= 0x19 # Proximity ADC high data register

# TMD2671 Enable Register Configuration
TMD2671_REG_ENABLE_SAI				= 0x40 # Sleep After Interrupt Enable
TMD2671_REG_ENABLE_PIEN				= 0x20 # Proximity Interrupt Enable
TMD2671_REG_ENABLE_WEN				= 0x08 # Wait Enable
TMD2671_REG_ENABLE_PEN				= 0x06 # Proximity Enable
TMD2671_REG_ENABLE_PON				= 0x01 # Power ON

# TMD2671 PTime Register Configuration
TMD2671_REG_PTIME_2_72				= 0xFF # Ptime = 2.72 ms

# TMD2671 WTime Register Configuration
TMD2671_REG_WTIME_2_72				= 0xFF # Wtime = 2.72 ms
TMD2671_REG_WTIME_200				= 0xB6 # Wtime = 200 ms
TMD2671_REG_WTIME_700				= 0x00 # Wtime = 700 ms

# TMD2671 Proximity Pulse Register Configuration
TMD2671_REG_PPULSE_COUNT			= 0x20 # Pulse Count = 32 (Specifies the number of proximity pulses to be generated)

# TMD2671 Control Register Configuration
TMD2671_REG_CONTROL_LED_100			= 0x00 # LED Strength - 100%
TMD2671_REG_CONTROL_LED_50			= 0x40 # LED Strength - 50%
TMD2671_REG_CONTROL_LED_25			= 0x80 # LED Strength - 25%
TMD2671_REG_CONTROL_LED_12_5		= 0xC0 # LED Strength - 12.5%
TMD2671_REG_CONTROL_PDIODE_0		= 0x10 # Proximity uses the Channel 0 diode
TMD2671_REG_CONTROL_PDIODE_1		= 0x20 # Proximity uses the Channel 1 diode
TMD2671_REG_CONTROL_PDIODE_BOTH		= 0x30 # Proximity uses the both diodes

class TMD2671():
	def power_enable(self):
		"""Select the ENABLE register configuration from the given provided values"""
		ENABLE_CONFIGURATION = (TMD2671_REG_ENABLE_PON)
		bus.write_byte_data(TMD2671_DEFAULT_ADDRESS, TMD2671_REG_ENABLE | TMD2671_COMMAND_BIT, ENABLE_CONFIGURATION)
	
	def enable_selection(self):
		"""Select the ENABLE register configuration from the given provided values"""
		ENABLE_CONFIGURATION = (TMD2671_REG_ENABLE_WEN | TMD2671_REG_ENABLE_PEN)
		bus.write_byte_data(TMD2671_DEFAULT_ADDRESS, TMD2671_REG_ENABLE | TMD2671_COMMAND_BIT, ENABLE_CONFIGURATION)
	
	def time_selection(self):
		"""Select the PTIME register configuration from the given provided values"""
		bus.write_byte_data(TMD2671_DEFAULT_ADDRESS, TMD2671_REG_PTIME | TMD2671_COMMAND_BIT, TMD2671_REG_PTIME_2_72)
		
		"""Select the WTIME register configuration from the given provided values"""
		bus.write_byte_data(TMD2671_DEFAULT_ADDRESS, TMD2671_REG_WTIME | TMD2671_COMMAND_BIT, TMD2671_REG_WTIME_2_72)
	
	def pulse_selection(self):
		"""Select the PPULSE register configuration from the given provided values"""
		bus.write_byte_data(TMD2671_DEFAULT_ADDRESS, TMD2671_REG_PPULSE, TMD2671_REG_PPULSE_COUNT)
	
	def gain_selection(self):
		"""Select the CONTROL register configuration from the given provided values"""
		GAIN_CONFIGURATION = (TMD2671_REG_CONTROL_LED_100 | TMD2671_REG_CONTROL_PDIODE_BOTH)
		bus.write_byte_data(TMD2671_DEFAULT_ADDRESS, TMD2671_REG_CONTROL | TMD2671_COMMAND_BIT, GAIN_CONFIGURATION)

	def read_prox(self):
		"""Read data back from TMD2671_REG_PDATAL(0x18), 2 bytes, with TMD2671_COMMAND_BIT,(0x80)
		Proximity LSB, Proximity MSB"""
		data = bus.read_i2c_block_data(TMD2671_DEFAULT_ADDRESS, TMD2671_REG_PDATAL | TMD2671_COMMAND_BIT, 2)
		
		# Convert the data
		proximity = data[1] * 256 + data[0]
		
		return {'p' : proximity}

from TMD2671 import TMD2671
tmd2671 = TMD2671()

while True:
	tmd2671.power_enable()
	time.sleep(0.3)
	tmd2671.enable_selection()
	tmd2671.pulse_selection()
	tmd2671.gain_selection()
	tmd2671.time_selection()
	time.sleep(0.3)
	prox = tmd2671.read_prox()
	print "Proximity of the Device : %d " %(prox['p'])
	print " ***************************************** "
	time.sleep(1)
