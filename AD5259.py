# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# AD5259
# This code is designed to work with the AD5259_I2CPOT_5K I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Potentiometers?sku=AD5259_I2CPOT_5K#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
AD5259_DEFAULT_ADDRESS				= 0x18

# AD5259 Command Set
AD5259_WORD_ADDR_RDAC				= 0x00 # Operation Between Interface and RDAC
AD5259_WORD_ADDR_EEPROM				= 0x01 # Operation Between Interface and EEPROM
AD5259_WORD_ADDR_WP					= 0x02 # Operation Between Interface and Write Protection Register
AD5259_WORD_ADDR_EEPROM_RDAC		= 0x05 # Restore EEPROM to RDAC
AD5259_WORD_ADDR_RDAC_EEPROM		= 0x06 # Store RDAC to EEPROM

class AD5259():
	def set_resistance(self, resistance):
		"""User have to enter the desired value from 0-256 position"""
		self.resistance = int(input("Enter the Value from (0-256)= "))
		if self.resistance > 256 :
			self.resistance = int(input("Enter the Value from (0-256)= "))
		
		return self.resistance
	
	def write_resistance(self, resistance):
		"""Write the desired resistance value on the given provided command above"""
		bus.write_i2c_block_data(AD5259_DEFAULT_ADDRESS, AD5259_WORD_ADDR_RDAC, [self.resistance])
	
	def get_resistance(self):
		"""Read data back from AD5259_WORD_ADDR_RDAC(0x00), 1 byte"""
		data = bus.read_byte_data(AD5259_DEFAULT_ADDRESS, AD5259_WORD_ADDR_RDAC)
		
		# Convert the data
		resistance_wb = (data / 256.0) * 5.0
		resistance_wa = 5 - resistance_wb
		
		return {'a' : resistance_wa, 'b' : resistance_wb}

from AD5259 import AD5259
ad5259 = AD5259()

while True:
	ad5259.set_resistance(2)
	ad5259.write_resistance(2)
	time.sleep(0.1)
	res = ad5259.get_resistance()
	print "Resistance at WB: %.2f K"%(res['b'])
	print "Resistance at WA: %.2f K"%(res['a'])
	print " ******************************** "
	time.sleep(1)
