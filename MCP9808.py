# -*- coding: utf-8 -*-
# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MCP9808
# This code is designed to work with the MCP9808_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Temperature?sku=MCP9808_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
MCP9808_DEFAULT_ADDRESS			= 0x18

# MCP9808 Register Pointer
MCP9808_REG_CONFIG				= 0x01 # Configuration Register
MCP9808_REG_UPPER_TEMP			= 0x02 # Alert Temperature Upper Boundary Trip register
MCP9808_REG_LOWER_TEMP			= 0x03 # Alert Temperature Lower Boundary Trip register
MCP9808_REG_CRIT_TEMP			= 0x04 # Critical Temperature Trip register
MCP9808_REG_AMBIENT_TEMP		= 0x05 # Temperature register
MCP9808_REG_MANUF_ID			= 0x06 # Manufacturer ID register
MCP9808_REG_DEVICE_ID			= 0x07 # Device ID/Revision register
MCP9808_REG_RSLTN				= 0x08 # Resolution register

# Configuration register values
MCP9808_REG_CONFIG_DEFAULT		= 0x0000 # Continuous conversion (power-up default)
MCP9808_REG_CONFIG_SHUTDOWN		= 0x0100 # Shutdown
MCP9808_REG_CONFIG_CRITLOCKED	= 0x0080 # Locked, TCRIT register can not be written
MCP9808_REG_CONFIG_WINLOCKED	= 0x0040 # Locked, TUPPER and TLOWER registers can not be written
MCP9808_REG_CONFIG_INTCLR		= 0x0020 # Clear interrupt output
MCP9808_REG_CONFIG_ALERTSTAT	= 0x0010 # Alert output is asserted
MCP9808_REG_CONFIG_ALERTCTRL	= 0x0008 # Alert Output Control bit is enabled
MCP9808_REG_CONFIG_ALERTSEL		= 0x0004 # TA > TCRIT only
MCP9808_REG_CONFIG_ALERTPOL		= 0x0002 # Alert Output Polarity bit active-high
MCP9808_REG_CONFIG_ALERTMODE	= 0x0001 # Interrupt output

# Resolution Register Value
MCP9808_REG_RSLTN_5				= 0x00 # +0.5°C
MCP9808_REG_RSLTN_25			= 0x01 # +0.25°C
MCP9808_REG_RSLTN_125			= 0x02 # +0.125°C
MCP9808_REG_RSLTN_0625			= 0x03 # +0.0625°C

class MCP9808():
	def __init__(self):
		self.configuration()
		self.resolution()
	
	def configuration(self):
		"""Select the configuration from the given provided values above"""
		config = [MCP9808_REG_CONFIG_DEFAULT]
		bus.write_i2c_block_data(MCP9808_DEFAULT_ADDRESS, MCP9808_REG_CONFIG, config)
	
	def resolution(self):
		"""Select the resolution from the given provided values above"""
		resolution = [MCP9808_REG_RSLTN_0625]
		bus.write_i2c_block_data(MCP9808_DEFAULT_ADDRESS, MCP9808_REG_RSLTN, resolution)
	
	def readTemp(self):
		"""Read data back from AMBIENT_TEMP (0x05), 2 bytes
		Temp MSB, Temp LSB"""
		data = bus.read_i2c_block_data(MCP9808_DEFAULT_ADDRESS, MCP9808_REG_AMBIENT_TEMP, 2)
		
		# Convert the data to 13-bits
		cTemp = ((data[0] & 0x1F) * 256) + data[1]
		if cTemp > 4095 :
			cTemp -= 8192
		cTemp = cTemp * 0.0625
		fTemp = cTemp * 1.8 + 32
		return {"c": cTemp, "f": fTemp}

from MCP9808 import MCP9808
mcp9808 = MCP9808()

while True:
	temp = mcp9808.readTemp()
	print "Temperature in Celsius : %.2f C"%(temp['c'])
	print "Temperature in Fahrenheit : %.2f F"%(temp['f'])
	time.sleep(1)
