# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MCP9803
# This code is designed to work with the MCP9803_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Temperature?sku=MCP9803_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
MCP9803_DEFAULT_ADDRESS				= 0x48

# MCP9803 Register Pointer
MCP9803_REG_TEMP					= 0x00 # Temperature register
MCP9803_REG_CONFIG					= 0x01 # Configuration Register
MCP9803_REG_TEMP_HYST				= 0x02 # Temperature Hysteresis Register
MCP9803_REG_TEMP_LIMIT				= 0x03 # Temperature Limit-set Registe

# Configuration register values
MCP9803_REG_CONFIG_DEFAULT			= 0x00 # Power-up Default
MCP9803_REG_CONFIG_OS_EN			= 0x80 # One-Shot bit enabled
MCP9803_REG_CONFIG_RES_10			= 0x20 # 10-bit Resolution
MCP9803_REG_CONFIG_RES_11			= 0x40 # 11-bit Resolution
MCP9803_REG_CONFIG_RES_12			= 0x60 # 12-bit Resolution
MCP9803_REG_CONFIG_FQ_2				= 0x08 # Fault Queue = 2
MCP9803_REG_CONFIG_FQ_4				= 0x10 # Fault Queue = 4
MCP9803_REG_CONFIG_FQ_6				= 0x18 # Fault Queue = 6
MCP9803_REG_CONFIG_POLAR_H			= 0x04 # Alert Polarity Active-High
MCP9803_REG_CONFIG_INT_MODE			= 0x02 # Interrupt Mode
MCP9803_REG_CONFIG_SHUTDOWN			= 0x01 # Shutdwown

class MCP9803():
	def __init__(self):
		self.configuration()
	
	def configuration(self):
		"""Select the configuration from the given provided values above"""
		CONFIGURATION = (MCP9803_REG_CONFIG_RES_12 | MCP9803_REG_CONFIG_DEFAULT)
		bus.write_byte_data(MCP9803_DEFAULT_ADDRESS, MCP9803_REG_CONFIG, CONFIGURATION)
	
	def readTemp(self):
		"""Read data back from TEMP (0x00), 2 bytes
		Temp MSB, Temp LSB"""
		data = bus.read_i2c_block_data(MCP9803_DEFAULT_ADDRESS, MCP9803_REG_TEMP, 2)
		
		# Convert the data to 12-bits
		cTemp = (data[0] * 256 + data[1]) / 16.0
		if cTemp > 2047 :
			cTemp -= 4096
		cTemp = cTemp * 0.0625
		fTemp = cTemp * 1.8 + 32
		return {"c": cTemp, "f": fTemp}

from MCP9803 import MCP9803
mcp9803 = MCP9803()

while True:
	temp = mcp9803.readTemp()
	print "Temperature in Celsius : %.2f C"%(temp['c'])
	print "Temperature in Fahrenheit : %.2f F"%(temp['f'])
	print " ******************************** "
	time.sleep(1)
