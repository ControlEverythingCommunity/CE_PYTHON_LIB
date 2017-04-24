# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# DS620
# This code is designed to work with the DS620_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Temperature?sku=DS620_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
DS620_DEFAULT_ADDRESS		= 0x48

# DS620 Register Map
DS620_REG_TH_MSB            = 0xA0
DS620_REG_TH_LSB            = 0xA1
DS620_REG_TL_MSB            = 0xA2
DS620_REG_TL_LSB            = 0xA3
DS620_REG_TEMP_MSB          = 0xAA
DS620_REG_TEMP_LSB          = 0xAB
DS620_REG_CONFIG_MSB        = 0xAC
DS620_REG_CONFIG_LSB        = 0xAD

# DS620 Configuration Register
DS620_RES_10BIT			= 0x00 # Resolution: 10-bit
DS620_RES_11BIT			= 0x04 # Resolution: 11-bit
DS620_RES_12BIT			= 0x08 # Resolution: 12-bit
DS620_RES_13BIT			= 0x0C # Resolution: 13-bit
DS620_POWER_IDLE        = 0x00 # DS620 Powers-up Idle
DS620_POWER_CONVERT     = 0x02 # DS620 Powers-up Converting Temperature
DS620_MODE_CONTINUOUS   = 0x00 # Continuous Conversion Mode
DS620_MODE_ONESHOT      = 0x01 # One-Shot Mode
DS620_FORCE_PO_LOW      = 0x00 # Force PO Low



class DS620():
	def __init__(self):
		self.temp_configuration()
	
	def temp_configuration(self):
		"""Select the temperature configuration MSB from the given provided values"""
		TEMP_CONFIG_MSB = (DS620_RES_13BIT | DS620_POWER_CONVERT | DS620_MODE_CONTINUOUS)
		bus.write_byte_data(DS620_DEFAULT_ADDRESS, DS620_REG_CONFIG_MSB, TEMP_CONFIG_MSB)
    
        """Select the temperature configuration LSB from the given provided values"""
        TEMP_CONFIG_LSB = (DS620_FORCE_PO_LOW)
        bus.write_byte_data(DS620_DEFAULT_ADDRESS, DS620_REG_CONFIG_LSB, TEMP_CONFIG_LSB)
	
	def read_temp(self):
		"""Read data back from DS620_REG_TEMP_MSB(0xAA), 2 bytes, temp MSB, temp LSB"""
		data = bus.read_i2c_block_data(DS620_DEFAULT_ADDRESS, DS620_REG_TEMP_MSB, 2)
		
		# Convert the data to 12-bits
		temp = ((data[0] * 256) + (data[1] & 0xF8)) / 8
		if temp > 4095 :
			temp -= 8192
		cTemp = temp * 0.0625
		fTemp = (cTemp * 1.8) + 32
		
		return {'c' : cTemp, 'f' : fTemp}

from DS620 import DS620
ds620 = DS620()

while True:
	temp = ds620.read_temp()
	print "Temperature in Celsius : %.2f C"%(temp['c'])
	print "Temperature in Fahrenheit : %.2f F"%(temp['f'])
	print " ***************************************** "
	time.sleep(1)
