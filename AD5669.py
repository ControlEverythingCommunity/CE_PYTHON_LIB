# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# AD5669
# This code is designed to work with the AD5669_I2CDAC I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Digital-Analog?sku=AD5669_I2CDAC#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
AD5669_DEFAULT_ADDRESS				= 0x56

# AD5669 Command Set
AD5669_CMD_WRITE_INPUT				= 0x00 # Write to input register
AD5669_CMD_UPDATE_DAC				= 0x10 # Update DAC registe
AD5669_CMD_WRITE_UPDATE_ALL			= 0x20 # Write to input register, update all
AD5669_CMD_WRITE_UPDATE_DAC			= 0x30 # Write to and update DAC channel
AD5669_CMD_POWER					= 0x40 # Power up
AD5669_CMD_LOAD_CLEAR				= 0x50 # Load clear code register
AD5669_CMD_LOAD_LDAC				= 0x60 # Load LDAC register
AD5669_CMD_RESET					= 0x70 # Reset
AD5669_CMD_INT_REF_SETUP			= 0x80 # Set up internal REF register
AD5669_CMD_MULTIBYTE_EN				= 0x90 # Enable multiple byte mode
AD5669_CMD_DAC_A					= 0x00 # Select DAC A Channel
AD5669_CMD_DAC_B					= 0x01 # Select DAC B Channel
AD5669_CMD_DAC_C					= 0x02 # Select DAC C Channel
AD5669_CMD_DAC_D					= 0x03 # Select DAC D Channel
AD5669_CMD_DAC_E					= 0x04 # Select DAC E Channel
AD5669_CMD_DAC_F					= 0x05 # Select DAC F Channel
AD5669_CMD_DAC_G					= 0x06 # Select DAC G Channel
AD5669_CMD_DAC_H					= 0x07 # Select DAC H Channel
AD5669_CMD_DAC_ALL					= 0x08 # Select All DAC Channel

class AD5669():
	def set_channel(self):
		"""Select the Channel user want to use from 0-8
		0 : DAC A Channel
		1 : DAC B Channel
		2 : DAC C Channel
		3 : DAC D Channel
		4 : DAC E Channel
		5 : DAC F Channel
		6 : DAC G Channel
		7 : DAC H Channel
		8 : All DAC Channel"""
		self.channel = int(input("Enter the Channel No.(0-8) = "))
		while self.channel > 8 :
			self.channel = int(input("Enter the Channel No.(0-8) = "))
		
		return self.channel
	
	def set_voltage(self):
		"""Enter the value from 0-65536 position for channel"""
		self.voltage = int(input("Enter the Value from (0-65536)= "))
		while self.voltage > 65536 :
			self.voltage = int(input("Enter the Value from (0-65536)= "))
		
		self.data = [self.voltage >> 8, self.voltage & 0xFF]
		
		return self.data
	
	def write_voltage(self):
		if self.channel == 0 :
			bus.write_i2c_block_data(AD5669_DEFAULT_ADDRESS, (AD5669_CMD_WRITE_UPDATE_DAC | AD5669_CMD_DAC_A), self.data)
		elif self.channel == 1 :
			bus.write_i2c_block_data(AD5669_DEFAULT_ADDRESS, (AD5669_CMD_WRITE_UPDATE_DAC | AD5669_CMD_DAC_B), self.data)
		elif self.channel == 2 :
			bus.write_i2c_block_data(AD5669_DEFAULT_ADDRESS, (AD5669_CMD_WRITE_UPDATE_DAC | AD5669_CMD_DAC_C), self.data)
		elif self.channel == 3 :
			bus.write_i2c_block_data(AD5669_DEFAULT_ADDRESS, (AD5669_CMD_WRITE_UPDATE_DAC | AD5669_CMD_DAC_D), self.data)
		elif self.channel == 4 :
			bus.write_i2c_block_data(AD5669_DEFAULT_ADDRESS, (AD5669_CMD_WRITE_UPDATE_DAC | AD5669_CMD_DAC_E), self.data)
		elif self.channel == 5 :
			bus.write_i2c_block_data(AD5669_DEFAULT_ADDRESS, (AD5669_CMD_WRITE_UPDATE_DAC | AD5669_CMD_DAC_F), self.data)
		elif self.channel == 6 :
			bus.write_i2c_block_data(AD5669_DEFAULT_ADDRESS, (AD5669_CMD_WRITE_UPDATE_DAC | AD5669_CMD_DAC_G), self.data)
		elif self.channel == 7 :
			bus.write_i2c_block_data(AD5669_DEFAULT_ADDRESS, (AD5669_CMD_WRITE_UPDATE_DAC | AD5669_CMD_DAC_H), self.data)
		elif self.channel == 8 :
			bus.write_i2c_block_data(AD5669_DEFAULT_ADDRESS, (AD5669_CMD_WRITE_UPDATE_DAC | AD5669_CMD_DAC_ALL), self.data)
	
	def voltage_conversion(self):
		"""Convert the data to get the final digital voltage"""
		voltage = ((self.data[0] * 256 + self.data[1]) / 65536.0) * 5.0
		
		return {'v' : voltage}

from AD5669 import AD5669
ad5669 = AD5669()

while True:
	ad5669.set_channel()
	ad5669.set_voltage()
	ad5669.write_voltage()
	volt = ad5669.voltage_conversion()
	print "Voltage : %.2fV"%(volt['v'])
	print " ******************************** "
	time.sleep(1)
