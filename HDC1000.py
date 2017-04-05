# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# HDC1000
# This code is designed to work with the HDC1000_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Temperature?sku=HDC1000_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
HDC1000_DEFAULT_ADDRESS				= 0x40

# HDC1000 Register Map
HDC1000_REG_TEMP					= 0x00 # Temperature measurement output
HDC1000_REG_HUMI					= 0x01 # Humidity measurement output
HDC1000_REG_CONFIG					= 0x02 # HDC1000 configuration and status
HDC1000_REG_SERID_1					= 0xFB # First 2 bytes of the serial ID of the part
HDC1000_REG_SERID_2					= 0xFC # Mid 2 bytes of the serial ID of the part
HDC1000_REG_SERID_3					= 0xFD # Last byte bit of the serial ID of the part
HDC1000_REG_MFID					= 0xFE # ID of Texas Instruments
HDC1000_REG_DEVID					= 0xFF # ID of HDC1000 device

# HDC1000 Configuration Register
HDC1000_CONFIG_RST					= 0x80 # Software Reset
HDC1000_CONFIG_HEAT_ON				= 0x20 # Heater Enabled
HDC1000_CONFIG_HEAT_OFF				= 0x00 # Heater Disabled
HDC1000_CONFIG_BOTH_TEMP_HUMI		= 0x10 # Temperature and Humidity are acquired in sequence, Temperature first
HDC1000_CONFIG_SINGLE_MEASUR		= 0x00 # Temperature or Humidity is acquired
HDC1000_CONFIG_TEMP_HUMI_14BIT		= 0x00 # Temperature & Humidity Resolution = 14-bits
HDC1000_CONFIG_TEMP_11BIT			= 0x04 # Temperature Resolution = 11-bits
HDC1000_CONFIG_HUMI_11BIT			= 0x01 # Humidity Resolution = 11-bits
HDC1000_CONFIG_HUMI_8BIT			= 0x02 # Humidity Resolution = 8-bits

class HDC1000():
	def __init__(self):
		self.write_configuration()
		self.write_tempcommand()
		self.write_humicommnad()
	
	def write_configuration(self):
		"""Select the temperature & humidity configuration from the given provided values"""
		CONFIG = (HDC1000_CONFIG_HEAT_ON | HDC1000_CONFIG_BOTH_TEMP_HUMI | HDC1000_CONFIG_TEMP_HUMI_14BIT)
		bus.write_byte_data(HDC1000_DEFAULT_ADDRESS, HDC1000_REG_CONFIG, CONFIG)
	
	def write_tempcommand(self):
		"""Select the temperature command from the given provided values"""
		bus.write_byte(HDC1000_DEFAULT_ADDRESS, HDC1000_REG_TEMP)
	
	def read_temp(self):
		"""Read data back from device address, 2 bytes, temp MSB, temp LSB"""
		data0 = bus.read_byte(HDC1000_DEFAULT_ADDRESS)
		data1 = bus.read_byte(HDC1000_DEFAULT_ADDRESS)
		
		# Convert the data
		temp = (data0 * 256) + data1
		cTemp = (temp / 65536.0) * 165.0 - 40
		fTemp = cTemp * 1.8 + 32
		
		return {'c' : cTemp, 'f' : fTemp}
	
	def write_humicommnad(self):
		"""Select the humidity command from the given provided values"""
		bus.write_byte(HDC1000_DEFAULT_ADDRESS, HDC1000_REG_HUMI)
	
	def read_humidity(self):
		"""Read data back from the device address, 2 bytes, humidity MSB, humidity LSB"""
		data0 = bus.read_byte(HDC1000_DEFAULT_ADDRESS)
		data1 = bus.read_byte(HDC1000_DEFAULT_ADDRESS)
		
		# Convert the data
		humidity = (data0 * 256) + data1
		humidity = (humidity / 65536.0) * 100.0
		
		return {'h' : humidity}

from HDC1000 import HDC1000
hdc1000 = HDC1000()

while True:
	hdc1000.write_configuration()
	hdc1000.write_tempcommand()
	time.sleep(0.3)
	temp = hdc1000.read_temp()
	print "Temperature in Celsius : %.2f C"%(temp['c'])
	print "Temperature in Fahrenheit : %.2f F"%(temp['f'])
	hdc1000.write_humicommnad()
	time.sleep(0.3)
	hum = hdc1000.read_humidity()
	print "Relative Humidity : %.2f %%RH"%(hum['h'])
	print " **************************************** "
	time.sleep(0.5)