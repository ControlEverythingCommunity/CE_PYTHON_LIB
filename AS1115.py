# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# AS1115
# This code is designed to work with the AS1115_I2CL_3CE I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/LED-Display?sku=AS1115_I2CL_3CE#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
AS1115_DEFAULT_ADDRESS				= 0x00

# AS1115 Digit & Control Register Map
AS1115_REG_DIGIT0					= 0x01 # Digit 0 Register
AS1115_REG_DIGIT1					= 0x02 # Digit 1 Register
AS1115_REG_DIGIT2					= 0x03 # Digit 2 Register
AS1115_REG_DIGIT3					= 0x04 # Digit 3 Register
AS1115_REG_DIGIT4					= 0x05 # Digit 4 Register
AS1115_REG_DIGIT5					= 0x06 # Digit 5 Register
AS1115_REG_DIGIT6					= 0x07 # Digit 6 Register
AS1115_REG_DIGIT7					= 0x08 # Digit 7 Register
AS1115_REG_DECODE_MODE				= 0x09 # Decode Enable Register
AS1115_REG_GLOBAL_INTEN				= 0x0A # Intensity Control Register
AS1115_REG_SCAN_LIMIT				= 0x0B # Scan-Limit Register
AS1115_REG_SHUTDOWN					= 0x0C # Shutdown Register
AS1115_REG_FEATURE					= 0x0E # Feature Register
AS1115_REG_DISP_TEST				= 0x0F # Display-Test Mode
AS1115_REG_DIGIT01_INTEN			= 0x10 # Digit 0-1 Intensity Control Register
AS1115_REG_DIGIT23_INTEN			= 0x11 # Digit 2-3 Intensity Control Register
AS1115_REG_DIGIT45_INTEN			= 0x12 # Digit 4-5 Intensity Control Register
AS1115_REG_DIGIT67_INTEN			= 0x13 # Digit 6-7 Intensity Control Register

# AS1115 Shutdown Register Configuration
AS1115_SHUTDOWN_FEATURE_RESET		= 0x00 # Shutdown Mode, Reset Feature Register to Default Settings 
AS1115_SHUTDOWN_FEATURE_UNCHANGED	= 0x80 # Shutdown Mode, Feature Register Unchanged
AS1115_NORMAL_FEATURE_RESET			= 0x01 # Normal Operation, Reset Feature Register to Default Settings 
AS1115_NORMAL_FEATURE_UNCHANGED		= 0x81 # Normal Operation, Feature Register Unchanged

# AS1115 Feature Register Configuration
AS1115_FEATURE_CLK_IN				= 0x00 # Internal oscillator is used for system clock
AS1115_FEATURE_CLK_EN				= 0x01 # Pin CLK of the serial interface operates as system clock input
AS1115_FEATURE_RESET_DS				= 0x00 # Reset Disabled. Normal operation
AS1115_FEATURE_RESET_EN				= 0x02 # All control registers are reset to default state
AS1115_FEATURE_DECODE_CODEB			= 0x00 # Enable Code-B decoding
AS1115_FEATURE_DECODE_HEX			= 0x04 # Enable HEX decoding
AS1115_FEATURE_BLINK_DS				= 0x00 # Disable blinking
AS1115_FEATURE_BLINK_EN				= 0x10 # Enable blinking
AS1115_FEATURE_BLINKFREQ_1			= 0x00 # Blink period typically is 1 second
AS1115_FEATURE_BLINKFREQ_2			= 0x20 # Blink period is 2 second
AS1115_FEATURE_BLINKSYNC			= 0x40 # The blink timing can be synchronized across all the devices
AS1115_FEATURE_BLINKOFF				= 0x00 # Blinking starts with the display turned off
AS1115_FEATURE_BLINKSTART			= 0x80 # Blinking starts with the display turned on

# AS1115 Decode Register Configuration
AS1115_DECODE_NODIGIT				= 0x00 # No decode for digits 7:0
AS1115_DECODE_DIGIT_0				= 0x01 # Code-B/HEX decode for digit 0, No decode for digits 7:1
AS1115_DECODE_DIGIT_0_2				= 0x07 # Code-B/HEX decode for digit 0-2, No decode for digits 7:3
AS1115_DECODE_DIGIT_0_5				= 0x3F # Code-B/HEX decode for digit 0-5, No decode for digits 7:6
AS1115_DECODE_DIGIT_0_2_5			= 0x25 # Code-B/HEX decode for digit 0,2,5, No decode for digits 1,3,4,6,7

# AS1115 Scan-Limit Register Configuration
AS1115_SCAN_DIGIT_0					= 0x00 # Display digit 0 only
AS1115_SCAN_DIGIT_01				= 0x01 # Display digit 0-1
AS1115_SCAN_DIGIT_02				= 0x02 # Display digit 0-2
AS1115_SCAN_DIGIT_03				= 0x03 # Display digit 0-3
AS1115_SCAN_DIGIT_04				= 0x04 # Display digit 0-4
AS1115_SCAN_DIGIT_05				= 0x05 # Display digit 0-5
AS1115_SCAN_DIGIT_06				= 0x06 # Display digit 0-6
AS1115_SCAN_DIGIT_07				= 0x07 # Display digit 0-7

class AS1115():
	def mode_config(self):
		"""Select the Shutdown register configuration from the given provided values"""
		bus.write_byte_data(AS1115_DEFAULT_ADDRESS, AS1115_REG_SHUTDOWN, AS1115_NORMAL_FEATURE_RESET)
	
	def feature_config(self):
		"""Select the Feature register configuration from the given provided values"""
		bus.write_byte_data(AS1115_DEFAULT_ADDRESS, AS1115_REG_FEATURE, AS1115_FEATURE_DECODE_HEX)
	
	def display_config(self):
		"""Select the Scan-Limit register configuration from the given provided values"""
		bus.write_byte_data(AS1115_DEFAULT_ADDRESS, AS1115_REG_SCAN_LIMIT, AS1115_SCAN_DIGIT_02)
	
	def decode_config(self):
		"""Select the Decode register configuration from the given provided values"""
		bus.write_byte_data(AS1115_DEFAULT_ADDRESS, AS1115_REG_DECODE_MODE, AS1115_DECODE_DIGIT_0_2)

from AS1115 import AS1115
as1115 = AS1115()

as1115.mode_config()
as1115.feature_config()
as1115.display_config()
as1115.decode_config()
time.sleep(0.2)
for data in range(0, 16):
	for digit in range(3):
		# Write data on the digits
		bus.write_byte_data(0x00, digit+1, data)
	# Output to screen
	print "Display on 7-Segment : ",hex(data)
	time.sleep(0.8)