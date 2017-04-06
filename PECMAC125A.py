# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# PECMAC125A
# This code is designed to work with the PECMAC125A_DLCT03C20 I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Current?sku=PECMAC125A_DLCT03C20#tabs-0-product_tabset-2
# NT

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
PECMAC125A_DEFAULT_ADDRESS				= 0x2A

# PECMAC125A Command Set
PECMAC125A_COMMAND_1					= 0x01 # Command 1: Reading Current
PECMAC125A_COMMAND_2					= 0x02 # Command 2: Reading Device Information
PECMAC125A_COMMAND_3					= 0x03 # Command 3: Reading Calibration Values
PECMAC125A_COMMAND_4					= 0x04 # Command 4: Writing Calibration Values
PECMAC125A_HEADER_BYTE_1				= 0x92 # Header Byte-1
PECMAC125A_HEADER_BYTE_2				= 0x6A # Header Byte-2
PECMAC125A_RESERVED						= 0x00 # Reserved Byte
PECMAC125A_READ_DATA					= 0x55 # Read back data

class PECMAC125A():
	def select_channel(self):
		"""Select the Start Channel and End Channel for the use
		1 : Channel-1
		2 : Channel-2
		3 : Channel-3
		4 : Channel-4
		5 : Channel-5
		6 : Channel-6
		7 : Channel-7
		8 : Channel-8
		9 : Channel-9
		10 : Channel-10
		11 : Channel-11
		12 : Channel-12"""
		self.start_chnl = int(input("Enter the Start Channel No.(1-12) = "))
		while self.start_chnl > 12 or self.start_chnl < 1 :
			self.start_chnl = int(input("Enter the Start Channel No.(1-12) = "))
		
		self.end_chnl = int(input("Enter the End Channel No.(1-12) = "))
		while self.end_chnl > 12 or self.end_chnl < self.start_chnl :
			self.end_chnl = int(input("Enter the End Channel No.(1-12) = "))
	
	def checksum_cmd2(self):
		"""Calculate the Checksum needed for data transmission and reception"""
		self.checksum = (PECMAC125A_HEADER_BYTE_1 + PECMAC125A_HEADER_BYTE_2 + PECMAC125A_COMMAND_2)
	
	def cmd_device_info(self):
		"""Select the Command for Device Information from the given provided value"""
		COMMAND = [PECMAC125A_HEADER_BYTE_2, PECMAC125A_COMMAND_2, PECMAC125A_RESERVED, PECMAC125A_RESERVED, PECMAC125A_RESERVED, PECMAC125A_RESERVED, self.checksum]
		bus.write_i2c_block_data(PECMAC125A_DEFAULT_ADDRESS, PECMAC125A_HEADER_BYTE_1, COMMAND)
	
	def checksum_cmd1(self):
		"""Calculate the Checksum needed for data transmission and reception"""
		self.checksum = (PECMAC125A_HEADER_BYTE_1 + PECMAC125A_HEADER_BYTE_2 + PECMAC125A_COMMAND_1 + self.start_chnl + self.end_chnl)
		print self.checksum
	def cmd_current(self):
		"""Select the Command for Reading Current from the given provided value"""
		COMMAND = [PECMAC125A_HEADER_BYTE_2, PECMAC125A_COMMAND_1, self.start_chnl, self.end_chnl, PECMAC125A_RESERVED, PECMAC125A_RESERVED, self.checksum]
		bus.write_i2c_block_data(PECMAC125A_DEFAULT_ADDRESS, PECMAC125A_HEADER_BYTE_1, COMMAND)
	
	def read_device_info(self):
		"""Read data back from PECMAC125A_READ_DATA(0x55), 3 bytes
		Type of Sensor, Maximum Current, No. of Channels"""
		data = bus.read_i2c_block_data(PECMAC125A_DEFAULT_ADDRESS, PECMAC125A_READ_DATA, 3)
		
		# Convert the data
		typeOfSensor = data[0]
		maxCurrent = data[1]
		noOfChannel = data[2]
		
		# Output data to screen
		print "Type of Sensor : %d" %typeOfSensor
		print "Maximum Current : %d A" %maxCurrent
		print "No. of Channels : %d" %noOfChannel
		print " ******************************* "
	
	def read_current(self):
		"""Read data back from PECMAC125A_READ_DATA(0x55), No. of Channels * 3 bytes
		current MSB1, current MSB, current LSB"""
		data = bus.read_i2c_block_data(PECMAC125A_DEFAULT_ADDRESS, PECMAC125A_READ_DATA, self.end_chnl * 3)
		
		# Convert the data
		for i in range(self.start_chnl-1, self.end_chnl) :
			if i > 10 :
				i = 0
			msb1 = data[i * 3]
			msb = data[1 + i * 3]
			lsb = data[2 + i * 3]
			
			# Convert the data to ampere
			current = ((msb1 * 65536) + (msb * 256) + lsb) / 1000.0
			
			# Output data to screen
			print "Channel no : %d " %(i + 1)
			print "Current Value : %.3f A" %current
			print " ******************************* "

from PECMAC125A import PECMAC125A
pecmac125a = PECMAC125A()

while True :
	pecmac125a.select_channel()
	pecmac125a.checksum_cmd2()
	pecmac125a.cmd_device_info()
	time.sleep(0.5)
	pecmac125a.read_device_info()
	pecmac125a.checksum_cmd1()
	pecmac125a.cmd_current()
	time.sleep(0.5)
	pecmac125a.read_current()
	time.sleep(0.2)
