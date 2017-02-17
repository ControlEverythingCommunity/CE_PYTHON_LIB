# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MCP3425
# This code is designed to work with the MCP3425_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Analog-Digital-Converters?sku=MCP3425_I2CADC#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
MCP3425_DEFAULT_ADDRESS				= 0x68

# MCP3425 Configuration Command Set
MCP3425_CMD_NEW_CNVRSN				= 0x80 # Initiate a new conversion(One-Shot Conversion mode only)
MCP3425_CMD_MODE_CONT				= 0x10 # Continuous Conversion Mode
MCP3425_CMD_MODE_ONESHOT			= 0x00 # One-Shot Conversion Mode
MCP3425_CMD_SPS_240					= 0x00 # 240 SPS (12-bit)
MCP3425_CMD_SPS_60					= 0x04 # 60 SPS (14-bit)
MCP3425_CMD_SPS_15					= 0x08 # 15 SPS (16-bit)
MCP3425_CMD_GAIN_1					= 0x00 # PGA Gain = 1V/V
MCP3425_CMD_GAIN_2					= 0x01 # PGA Gain = 2V/V
MCP3425_CMD_GAIN_4					= 0x02 # PGA Gain = 4V/V
MCP3425_CMD_GAIN_8					= 0x03 # PGA Gain = 8V/V
MCP3425_CMD_READ_CNVRSN				= 0x00 # Read Conversion Result Data

class MCP3425():
	def __init__(self):
		self.config_command()
	
	def config_command(self):
		"""Select the Configuration Command from the given provided values"""
		CONFIG_CMD = (MCP3425_CMD_MODE_CONT | MCP3425_CMD_SPS_240 | MCP3425_CMD_GAIN_1)
		bus.write_byte(MCP3425_DEFAULT_ADDRESS, CONFIG_CMD)
	
	def read_adc(self):
		"""Read data back from MCP3425_CMD_READ_CNVRSN(0x00), 2 bytes
		raw_adc MSB, raw_adc LSB"""
		data = bus.read_i2c_block_data(MCP3425_DEFAULT_ADDRESS, MCP3425_CMD_READ_CNVRSN, 2)
		
		# Convert the data to 12-bits
		raw_adc = ((data[0] & 0x0F) * 256) + data[1]
		if raw_adc > 2047 :
			raw_adc -= 4095
		
		return {'r' : raw_adc}

from MCP3425 import MCP3425
mcp3425 = MCP3425()

while True :
	adc = mcp3425.read_adc()
	print "Digital Value of Analog Input : %d "%(adc['r'])
	print " ********************************* "
	time.sleep(0.8)
