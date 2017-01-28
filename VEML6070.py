# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# VEML6070
# This code is designed to work with the VEML6070_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/products

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
VEML6070_DEFAULT_ADDRESS				= 0x38

# VEML6070 Command Set
VEML6070_CMD_ACK_DISABLE				= 0x00 # Acknowledge Disable
VEML6070_CMD_ACK_ENABLE					= 0x20 # Acknowledge Enable
VEML6070_CMD_ACK_THD_102				= 0x00 # Acknowledge threshold 102 Steps
VEML6070_CMD_ACK_THD_145				= 0x10 # Acknowledge threshold 145 Steps
VEML6070_CMD_IT_1_2T					= 0x00 # Integration time = 1/2T
VEML6070_CMD_IT_1T						= 0x04 # Integration time = 1T
VEML6070_CMD_IT_2T						= 0x08 # Integration time = 2T
VEML6070_CMD_IT_4T						= 0x0C # Integration time = 4T
VEML6070_CMD_RESERVED					= 0x02 # Reserved, Set to 1
VEML6070_CMD_SD_DISABLE					= 0x00 # Shut-down Disable
VEML6070_CMD_SD_ENABLE					= 0x01 # Shut-down Enable
VEML6070_CMD_READ_LSB					= 0x38 # Read LSB of the data
VEML6070_CMD_READ_MSB					= 0x39 # Read MSB of the data

class VEML6070():
	def __init__(self):
		self.write_command()
	
	def write_command(self):
		"""Select the UV light command from the given provided values"""
		COMMAND_CONFIG = (VEML6070_CMD_ACK_DISABLE | VEML6070_CMD_IT_1_2T | VEML6070_CMD_SD_DISABLE | VEML6070_CMD_RESERVED)
		bus.write_byte(VEML6070_DEFAULT_ADDRESS, COMMAND_CONFIG)
	
	def read_uvlight(self):
		"""Read data back VEML6070_CMD_READ_MSB(0x73) and VEML6070_CMD_READ_LSB(0x71), uvlight MSB, uvlight LSB"""
		data0 = bus.read_byte(VEML6070_CMD_READ_MSB)
		data1 = bus.read_byte(VEML6070_CMD_READ_LSB)
		
		# Convert the data
		uvlight = data0 * 256 + data1
		
		return {'u' : uvlight}

from VEML6070 import VEML6070
veml6070 = VEML6070()

while True:
	light = veml6070.read_uvlight()
	print "UV Light Level : %d" %(light['u'])
	print " *********************************** "
	time.sleep(0.5)
