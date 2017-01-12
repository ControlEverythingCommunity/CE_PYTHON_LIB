# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# CAT34TS02
# This code is designed to work with the CAT34TS02_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/products

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
CAT34TS02_DEFAULT_ADDRESS		= 0x18

# CAT34TS02 Register Map
CAT34TS02_REG_CAP					= 0x00 # Capability Register
CAT34TS02_REG_CONFIG				= 0x01 # Configuration Register
CAT34TS02_REG_THIGH					= 0x02 # High Limit Register
CAT34TS02_REG_TLOW					= 0x03 # Low Limit Register
CAT34TS02_REG_CRITICAL				= 0x04 # Critical Limit Register
CAT34TS02_REG_TEMP					= 0x05 # Temperature Data Register

# CAT34TS02 Configuration Register
CAT34TS02_CONFIG_HYST_DS			= 0x0000 # Disable Hystersis
CAT34TS02_CONFIG_HYST_1_5			= 0x0200 # Set hysteresis at 1.5 C
CAT34TS02_CONFIG_HYST_3				= 0x0400 # Set hysteresis at 3 C
CAT34TS02_CONFIG_HYST_6				= 0x0600 # Set hysteresis at 6 C
CAT34TS02_CONFIG_SHDN_EN			= 0x0000 # Thermal Sensor is enabled
CAT34TS02_CONFIG_SHDN_DS			= 0x0100 # Thermal Sensor is disabled
CAT34TS02_TCRIT_LOCK_UPDT			= 0x0000 # Critical trip register can be updated
CAT34TS02_TCRIT_LOCK_DS				= 0x0080 # Critical trip register cannot be modified
CAT34TS02_EVENT_LOCK_UPDT			= 0x0000 # Alarm trip registers can be updated
CAT34TS02_EVENT_LOCK_DS				= 0x0040 # Alarm trip registers cannot be modified
CAT34TS02_EVENT_STS_NASRTD			= 0x0000 # EVENT output pin is not being asserted
CAT34TS02_EVENT_STS_ASSRTD			= 0x0010 # EVENT output pin is being asserted
CAT34TS02_EVENT_CTRL_DS				= 0x0000 # EVENT output disabled
CAT34TS02_EVENT_CTRL_EN				= 0x0008 # EVENT output enabled
CAT34TS02_EVENT_POL_LOW				= 0x0000 # EVENT output active low
CAT34TS02_EVENT_POL_HIGH			= 0x0002 # EVENT output active high
CAT34TS02_EVENT_MODE_CMP			= 0x0000 # Comparater Mode
CAT34TS02_EVENT_MODE_INT			= 0x0001 # Interrupt Mode


class CAT34TS02():
	def __init__(self):
		self.temp_configuration()
	
	def temp_configuration(self):
		"""Select the temperature configuration from the given provided values"""
		TEMP_CONFIG = (CAT34TS02_CONFIG_SHDN_EN | CAT34TS02_EVENT_MODE_CMP | CAT34TS02_CONFIG_HYST_DS | CAT34TS02_EVENT_CTRL_DS)
		bus.write_byte_data(CAT34TS02_DEFAULT_ADDRESS, CAT34TS02_REG_CONFIG, TEMP_CONFIG)
	
	def read_temp(self):
		"""Read data back from CAT34TS02_REG_TEMP(0x05), 2 bytes, temp MSB, temp LSB"""
		data = bus.read_i2c_block_data(CAT34TS02_DEFAULT_ADDRESS, CAT34TS02_REG_TEMP, 2)
		
		# Convert the data to 13-bits
		temp = ((data[0] & 0x0F) * 256 + data[1])
		if temp > 4095 :
			temp -= 8192
		cTemp = temp * 0.0625
		fTemp = cTemp * 1.8 + 32
		
		return {'c' : cTemp, 'f' : fTemp}

from CAT34TS02 import CAT34TS02
cat34ts02 = CAT34TS02()

while True:
	temp = cat34ts02.read_temp()
	print "Temperature in Celsius : %.2f C"%(temp['c'])
	print "Temperature in Fahrenheit : %.2f F"%(temp['f'])
	print " ***************************************** "
	time.sleep(1)
