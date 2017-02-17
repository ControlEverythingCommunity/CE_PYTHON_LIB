# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# AD5667
# This code is designed to work with the AD5667_I2CDAC I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Digital-Analog?sku=AD5667_I2CDAC#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
AD5667_DEFAULT_ADDRESS				= 0x0E

# AD5667 Command Set
AD5667_CMD_DAC_A					= 0x00 # Select DAC A Channel
AD5667_CMD_DAC_B					= 0x01 # Select DAC B Channel
AD5667_CMD_DAC_ALL					= 0x07 # Select Both DAC Channel
AD5669_CMD_WRITE_INPUT				= 0x00 # Write to input register
AD5669_CMD_UPDATE_DAC				= 0x08 # Update DAC registe
AD5667_CMD_WRITE_UPDATE_ALL			= 0x10 # Write to input register, update all
AD5667_CMD_WRITE_UPDATE_DAC			= 0x18 # Write to and update DAC channel
AD5667_CMD_POWER					= 0x20 # Power up
AD5667_CMD_RESET					= 0x28 # Reset
AD5667_CMD_LDAC_SETUP				= 0x30 # LDAC register setup
AD5667_CMD_INT_REF_SETUP			= 0x38 # Internal reference setup

class AD5667():
	def set_channel(self):
		"""Select the Channel user want to use from 0-2
		0 : DAC A Channel
		1 : DAC B Channel
		2 : DAC All Channel"""
		self.channel = int(input("Enter the Channel No.(0-2)= "))
		while self.channel > 2 :
			self.channel = int(input("Enter the Channel No.(0-2) = "))
		
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
			bus.write_i2c_block_data(AD5667_DEFAULT_ADDRESS, (AD5667_CMD_WRITE_UPDATE_DAC | AD5667_CMD_DAC_A), self.data)
		elif self.channel == 1 :
			bus.write_i2c_block_data(AD5667_DEFAULT_ADDRESS, (AD5667_CMD_WRITE_UPDATE_DAC | AD5667_CMD_DAC_B), self.data)
		elif self.channel == 2 :
			bus.write_i2c_block_data(AD5667_DEFAULT_ADDRESS, (AD5667_CMD_WRITE_UPDATE_DAC | AD5667_CMD_DAC_ALL), self.data)
	
	def voltage_conversion(self):
		"""Convert the data to get the voltage"""
		voltage = ((self.data[0] * 256 + self.data[1]) / 65536.0) * 5.0
		
		return {'v' : voltage}

from AD5667 import AD5667
ad5667 = AD5667()

while True:
	ad5667.set_channel()
	ad5667.set_voltage()
	ad5667.write_voltage()
	volt = ad5667.voltage_conversion()
	print "Voltage : %.2fV"%(volt['v'])
	print " ******************************** "
	time.sleep(1)
