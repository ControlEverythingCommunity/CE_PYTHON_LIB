# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# TMD37821
# This code is designed to work with the TMD37821_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Light?sku=TMD37821_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
TMD37821_DEFAULT_ADDRESS			= 0x39

# TMD37821 Register Set
TMD37821_COMMAND_BIT                = 0xA0 # Auto-increment protocol transaction
TMD37821_REG_ENABLE					= 0x00 # Enables states and interrupts
TMD37821_REG_ATIME					= 0x01 # ALS ADC time
TMD37821_REG_WTIME					= 0x03 # Wait time
TMD37821_REG_CONFIG					= 0x0D # Configuration register
TMD37821_REG_PPULSE					= 0x0E # Proximity pulse register
TMD37821_REG_CONTROL                = 0x0F # Control register
TMD37821_REG_DEVICE_ID				= 0x12 # Device ID register
TMD37821_REG_STATUS					= 0x13 # Device Status register
TMD37821_REG_CDATAL					= 0x14 # Clear ADC low data register
TMD37821_REG_CDATAH					= 0x15 # Clear ADC high data register
TMD37821_REG_RDATAL					= 0x16 # Red ADC low data register
TMD37821_REG_RDATAH					= 0x17 # Red ADC high data register
TMD37821_REG_GDATAL					= 0x18 # Green ADC low data register
TMD37821_REG_GDATAH					= 0x19 # Green ADC high data register
TMD37821_REG_BDATAL					= 0x1A # Blue ADC low data register
TMD37821_REG_BDATAH					= 0x1B # Blue ADC high data register
TMD37821_REG_PDATAL					= 0x1C # Proximity ADC low data register
TMD37821_REG_PDATAH					= 0x1D # Proximity ADC high data register

# TMD37821 Enable Register Configuration
TMD37821_REG_ENABLE_PIEN            = 0x20 # Proximity Interrupt Enable
TMD37821_REG_ENABLE_AIEN            = 0x10 # ALS Interrupt Enable
TMD37821_REG_ENABLE_WEN				= 0x08 # Wait Enable
TMD37821_REG_ENABLE_PEN				= 0x04 # Proximity Enable
TMD37821_REG_ENABLE_AEN				= 0x02 # RGBC ADC Enable
TMD37821_REG_ENABLE_PON				= 0x01 # Power ON

# TMD37821 ATime Register Configuration
TMD37821_REG_ATIME_2_38				= 0xFF # Atime = 2.38 ms, Cycles = 1
TMD37821_REG_ATIME_24				= 0xF6 # Atime = 24 ms, Cycles = 10
TMD37821_REG_ATIME_100				= 0xDB # Atime = 100 ms, Cycles = 37
TMD37821_REG_ATIME_152				= 0xC0 # Atime = 152 ms, Cycles = 64
TMD37821_REG_ATIME_609				= 0x00 # Atime = 609 ms, Cycles = 256

# TMD37821 WTime Register Configuration
TMD37821_REG_WTIME_2_38				= 0xFF # Wtime = 2.38 ms
TMD37821_REG_WTIME_202				= 0xB6 # Wtime = 202 ms
TMD37821_REG_WTIME_609				= 0x00 # Wtime = 609 ms

# TMD37821 Proximity Pulse Register Configuration
TMD37821_REG_PPULSE_COUNT			= 0x0F # Pulse Count = 15 (Specifies the number of proximity pulses to be generated)

# TMD37821 Control Register Configuration
TMD37821_REG_CONTROL_PDRIVE_100     = 0x00 # LED Strength - 100%
TMD37821_REG_CONTROL_PDRIVE_50      = 0x40 # LED Strength - 50%
TMD37821_REG_CONTROL_PDRIVE_25      = 0x80 # LED Strength - 25%
TMD37821_REG_CONTROL_PDRIVE_12_5    = 0xC0 # LED Strength - 12.5%
TMD37821_REG_CONTROL_PSAT_0         = 0x10 # PDATA output regardless of ambient light level
TMD37821_REG_CONTROL_PSAT_1         = 0x20 # PDATA output equal to dark current value if saturated
TMD37821_REG_CONTROL_AGAIN_1        = 0x00 # ALS GAIN VALUE - 1x Gain
TMD37821_REG_CONTROL_AGAIN_4        = 0x01 # ALS GAIN VALUE - 4x Gain
TMD37821_REG_CONTROL_AGAIN_16		= 0x02 # ALS GAIN VALUE - 16x Gain
TMD37821_REG_CONTROL_AGAIN_60		= 0x03 # ALS GAIN VALUE - 60x Gain

class TMD37821():
	def __init__(self):
		self.enable_selection()
		self.time_selection()
		self.pulse_selection()
		self.gain_selection()
	
	def enable_selection(self):
		"""Select the ENABLE register configuration from the given provided values"""
		ENABLE_CONFIGURATION = (TMD37821_REG_ENABLE_WEN | TMD37821_REG_ENABLE_PEN | TMD37821_REG_ENABLE_AEN | TMD37821_REG_ENABLE_PON)
		bus.write_byte_data(TMD37821_DEFAULT_ADDRESS, TMD37821_REG_ENABLE | TMD37821_COMMAND_BIT, ENABLE_CONFIGURATION)
	
	time.sleep(0.3)
	
	def time_selection(self):
		"""Select the ATIME register configuration from the given provided values"""
		bus.write_byte_data(TMD37821_DEFAULT_ADDRESS, TMD37821_REG_ATIME | TMD37821_COMMAND_BIT, TMD37821_REG_ATIME_100)
		
		"""Select the WTIME register configuration from the given provided values"""
		bus.write_byte_data(TMD37821_DEFAULT_ADDRESS, TMD37821_REG_WTIME | TMD37821_COMMAND_BIT, TMD37821_REG_WTIME_2_38)
	
	def pulse_selection(self):
		"""Select the PPULSE register configuration from the given provided values"""
		bus.write_byte_data(TMD37821_DEFAULT_ADDRESS, TMD37821_REG_PPULSE, TMD37821_REG_PPULSE_COUNT)
	
	def gain_selection(self):
		"""Select the CONTROL register configuration from the given provided values"""
		GAIN_CONFIGURATION = (TMD37821_REG_CONTROL_PDRIVE_100 | TMD37821_REG_CONTROL_PSAT_0 | TMD37821_REG_CONTROL_AGAIN_1)
		bus.write_byte_data(TMD37821_DEFAULT_ADDRESS, TMD37821_REG_CONTROL | TMD37821_COMMAND_BIT, GAIN_CONFIGURATION)

	def readluminance(self):
		"""Read data back from TMD37821_REG_C0DATAL(0x14), 10 bytes, with TMD37821_COMMAND_BIT, (0xA0)
		cData LSB, cData MSB, rData LSB, rData MSB, gData LSB, gData MSB, bData LSB, bData MSB, Proximity LSB, Proximity MSB"""
		data = bus.read_i2c_block_data(TMD37821_DEFAULT_ADDRESS, TMD37821_REG_CDATAL | TMD37821_COMMAND_BIT, 10)
		
		# Convert the data
		cData = (data[1] * 256) + data[0]
		rData = (data[3] * 256) + data[2]
        gData = (data[5] * 256) + data[4]
        bData = (data[7] * 256) + data[6]
		proximity = (data[9] * 256) + data[8]
		
		return {'c' : clear, 'r' : red, 'g' : green, 'b' : blue, 'p' : proximity}

from TMD37821 import TMD37821
tmd37821 = TMD37821()

while True:
	lum = tmd37821.readluminance()
    print "Clear Data Luminance : %d "%(lum['c'])
    print "Red Color Luminance : %d "%(lum['r'])
    print "Green Color Luminance : %d "%(lum['g'])
    print "Blue Color Luminance : %d "%(lum['b'])
	print "Proximity of the Device : %d " %(lum['p'])
	print " ************************************************ "
	time.sleep(1)
