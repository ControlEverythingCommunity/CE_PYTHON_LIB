# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# STTS751
# This code is designed to work with the STTS751_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/products

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
STTS751_DEFAULT_ADDRESS				= 0x39

# STTS751 Register Map
STTS751_REG_TEMP_HIGH				= 0x00 # Temperature value high byte
STTS751_REG_STATUS					= 0x01 # Status Register
STTS751_REG_TEMP_LOW				= 0x02 # Temperature value low byte
STTS751_REG_CONFIG					= 0x03 # Configuration Register
STTS751_REG_CONVER					= 0x04 # Conversion Rate Register
STTS751_REG_HIGHLIMIT_HIGH			= 0x05 # Temperature high limit high byte
STTS751_REG_HIGHLIMIT_LOW			= 0x06 # Temperature high limit low byte
STTS751_REG_LOWLIMIT_HIGH			= 0x07 # Temperature low limit high byte
STTS751_REG_LOWLIMIT_LOW			= 0x08 # Temperature low limit low byte
STTS751_REG_ONESHOT					= 0x0F # One-Shot Register
STTS751_REG_THERM_LIMIT				= 0x20 # THERM Limit Register
STTS751_REG_THERM_HYST				= 0x21 # THERM Hysteresis Register
STTS751_REG_SMBUS_TIMEOUT			= 0x22 # SMBus Timeout Register
STTS751_REG_PRODUCT_ID				= 0xFD # Product ID Register
STTS751_REG_MANUFACTURER_ID			= 0xFE # Manufacturer ID Register
STTS751_REG_REVISION_ID				= 0xFF # Revision ID Register

# STTS751 Configuration Register
STTS751_CONFIG_MASK_EN				= 0x00 # EVENT is enabled
STTS751_CONFIG_MASK_DS				= 0x80 # EVENT is disabled
STTS751_CONFIG_RUNNING				= 0x00 # Device is running in continuous conversion mode
STTS751_CONFIG_STOP					= 0x40 # Device is in standby mode drawing minimum power
STTS751_CONFIG_RES_10				= 0x00 # Temperature Resolution = 10-bits
STTS751_CONFIG_RES_11				= 0x04 # Temperature Resolution = 11-bits
STTS751_CONFIG_RES_12				= 0x0C # Temperature Resolution = 12-bits
STTS751_CONFIG_RES_9				= 0x08 # Temperature Resolution = 9-bits

# STTS751 Conversion Rate Register
STTS751_CONVER_0_0625				= 0x00 # Conversion per sec = 0.0625
STTS751_CONVER_0_125				= 0x01 # Conversion per sec = 0.125
STTS751_CONVER_0_25					= 0x02 # Conversion per sec = 0.25
STTS751_CONVER_0_5					= 0x03 # Conversion per sec = 0.5
STTS751_CONVER_1					= 0x04 # Conversion per sec = 1
STTS751_CONVER_2					= 0x05 # Conversion per sec = 2
STTS751_CONVER_4					= 0x06 # Conversion per sec = 4
STTS751_CONVER_8					= 0x07 # Conversion per sec = 8
STTS751_CONVER_16					= 0x08 # Conversion per sec = 16
STTS751_CONVER_32					= 0x09 # Conversion per sec = 32

class STTS751():
	def __init__(self):
		self.write_config()
		self.write_conversionrate()
	
	def write_config(self):
		"""Select the temperature configuration from the given provided values"""
		CONFIG = (STTS751_CONFIG_MASK_DS | STTS751_CONFIG_RES_12 | STTS751_CONFIG_RUNNING)
		bus.write_byte_data(STTS751_DEFAULT_ADDRESS, STTS751_REG_CONFIG, CONFIG)
	
	def write_conversionrate(self):
		"""Select the temperature conversion rate from the given provided values"""
		CONVER_RATE = (STTS751_CONVER_1)
		bus.write_byte_data(STTS751_DEFAULT_ADDRESS, STTS751_REG_CONVER, CONVER_RATE)
	
	def read_temp(self):
		"""Read data back from STTS751_REG_TEMP_HIGH(0x00) & STTS751_REG_TEMP_LOW(0x02)
		2 bytes, temp MSB, temp LSB"""
		data0 = bus.read_byte_data(0x39, 0x00)
		data1 = bus.read_byte_data(0x39, 0x02)
		
		# Convert the data to 12-bits
		temp = ((data0 * 256) + (data1 & 0xF0)) / 16
		if temp > 2047 :
			temp -= 4096
		cTemp = temp * 0.0625;
		fTemp = cTemp * 1.8 + 32
		
		return {'c' : cTemp, 'f' : fTemp}

from STTS751 import STTS751
stts751 = STTS751()

while True:
	temp = stts751.read_temp()
	print "Temperature in Celsius : %.2f C"%(temp['c'])
	print "Temperature in Fahrenheit : %.2f F"%(temp['f'])
	print " ************************************* "
	time.sleep(0.5)
