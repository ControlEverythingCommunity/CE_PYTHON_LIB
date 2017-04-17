# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# 24AA32
# This code is designed to work with the 24AA32_I2CMEM I2C Mini Module available from ControlEverything.com.
# https://shop.controleverything.com/

import time
import smbus

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
24AA32_DEFAULT_ADDRESS			= 0x50

class 24AA32():
	def select_address(self):
		"""Select the address where data has to be written (0-65535)"""
		self.address = int(input("Enter the Address = "))
		while self.address > 65535:
			self.address = int(input("Enter the Address = "))
		
		self.addressbyte1 = (self.address >> 8)
		self.addressbyte2 = (self.address & 0xFF)
		
		return self.addressbyte1, self.addressbyte2
	
	def select_data(self):
		"""Select the data to be written on the address given (0-255)"""
		self.data = int(input("Enter the Data = "))
		while self.data > 255:
			self.data = int(input("Enter the Data = "))
		
		return self.data
	
	def write_data(self):
		"""Write the given data on the given address by the user"""
		bus.write_i2c_block_data(24AA32_DEFAULT_ADDRESS, self.addressbyte1, [self.addressbyte2, self.data])
	
	def select_readaddress(self):
		"""Read the given provided data by the user"""
		bus.write_i2c_block_data(24AA32_DEFAULT_ADDRESS, self.addressbyte1, [self.addressbyte2])
	
	def read_data(self):
		"""Read the data back from the device address"""
		data = bus.read_byte(24AA32_DEFAULT_ADDRESS)
		
		return {'d' : data}

from 24AA32 import 24AA32
_24AA32 = 24AA32()

while True :
	"""Select the Write/Read for the use
		0 : Write
		1 : Read"""
	user_wr = int(input("Select Write/Read (0:W, 1:R) = "))
	while user_wr > 1 :
		user_wr = int(input("Select Write/Read (0:W, 1:R) = "))
	
	if user_wr == 0 :
		_24AA32.select_address()
		_24AA32.select_data()
		_24AA32.write_data()
		time.sleep(0.5)
		_24AA32.select_readaddress()
		time.sleep(0.5)
		result = _24AA32.read_data()
		print "Input Data : %d"%(result['d'])
		print " ******************************** "
	elif user_wr == 1 :
		_24AA32.select_address()
		time.sleep(0.5)
		_24AA32.select_readaddress()
		time.sleep(0.5)
		result = _24AA32.read_data()
		print "Input Data : %d"%(result['d'])
		print " ******************************** "
	
