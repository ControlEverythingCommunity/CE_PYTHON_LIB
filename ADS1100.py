# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# ADS1100
# This code is designed to work with the ADS1100_I2CADC I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Analog-Digital-Converters?sku=ADS1100_I2CADC#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
ADS1100_DEFAULT_ADDRESS				= 0x48

# ADS1100 Configuration Register
ADS1100_REG_CONFIG_OS_NOEFFECT		= 0x00 # Write: Bit = 0 No effect
ADS1100_REG_CONFIG_OS_SINGLE		= 0x80 # Write: Bit = 1 Begin a conversion (default)
ADS1100_REG_CONFIG_MODE_CONTIN		= 0x00 # Continuous conversion mode (default)
ADS1100_REG_CONFIG_MODE_SINGLE		= 0x10 # Single-conversion mode
ADS1100_REG_CONFIG_DR_128SPS		= 0x00 # 128 samples per second
ADS1100_REG_CONFIG_DR_32SPS			= 0x04 # 32 samples per second
ADS1100_REG_CONFIG_DR_16SPS			= 0x08 # 16 samples per second
ADS1100_REG_CONFIG_DR_8SPS			= 0x0C # 8 samples per second (default)
ADS1100_REG_CONFIG_PGA_1			= 0x00 # Gain 1 (default)
ADS1100_REG_CONFIG_PGA_2			= 0x01 # Gain 2
ADS1100_REG_CONFIG_PGA_4			= 0x02 # Gain 4
ADS1100_REG_CONFIG_PGA_8			= 0x03 # Gain 8

class ADS1100():
	def config_command(self):
		"""Select the Configuration Register data from the given provided values"""
		CONFIG = (ADS1100_REG_CONFIG_OS_SINGLE | ADS1100_REG_CONFIG_MODE_CONTIN | ADS1100_REG_CONFIG_DR_8SPS | ADS1100_REG_CONFIG_PGA_1)
		bus.write_byte(ADS1100_DEFAULT_ADDRESS, CONFIG)
	
	def read_adc(self):
		"""Read data back from the device address, 2 bytes
		raw_adc MSB, raw_adc LSB"""
		data = bus.read_i2c_block_data(ADS1100_DEFAULT_ADDRESS, 2)
		
		# Convert the data
		raw_adc = data[0] * 256 + data[1]
		
		if raw_adc > 32767 :
			raw_adc -= 65536
		
		return {'r' : raw_adc}

from ADS1100 import ADS1100
ads1100 = ADS1100()

while True :
	ads1100.config_command()
	time.sleep(0.3)
	adc = ads1100.read_adc()
	print "Digital Value of Analog Input : %d "%(adc['r'])
	print " ********************************* "
	time.sleep(0.5)
