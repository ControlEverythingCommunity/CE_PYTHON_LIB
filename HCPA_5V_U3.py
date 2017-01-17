# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# HCPA_5V_U3
# This code is designed to work with the HCPA-5V-U3_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Temperature?sku=HCPA-5V-U3_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

#I2C address of the device
HCPA_5V_U3_DEFAULT_ADDRESS				= 0x28

# HCPA_5V_U3 Command Set
HCPA_5V_U3_START_NOM					= 0x80 # Ends Command Mode and transitions to Normal Operation Mode
HCPA_5V_U3_START_CM						= 0xA0 # Start Command Mode: used to enter the command interpreting mode

class HCPA_5V_U3():
	def __init__(self):
		self.write_command()
		self.read_temp()
	
	def write_command(self):
		"""Select the temperature command from the given provided values"""
		bus.write_byte(HCPA_5V_U3_DEFAULT_ADDRESS, HCPA_5V_U3_START_NOM)
	
	def read_temp(self):
		"""Read data back from device address, 4 bytes, humidity MSB, humidity LSB, cTemp MSB, cTemp LSB"""
		data = bus.read_i2c_block_data(HCPA_5V_U3_DEFAULT_ADDRESS, 4)
		
		# Convert the data to 14-bits
		humidity = (((data[0] & 0x3F) * 256) + data[1]) / 16384.0 * 100.0
		cTemp = (((data[2] * 256) + (data[3] & 0xFC)) / 4) / 16384.0 * 165.0 - 40.0
		fTemp = (cTemp * 1.8) + 32
		
		return {'h' : humidity, 'c' : cTemp, 'f' : fTemp}

from HCPA_5V_U3 import HCPA_5V_U3
hcpa_5v_u3 = HCPA_5V_U3()

while True:
	result = hcpa_5v_u3.read_temp()
	print "Relative Humidity : %.2f %%RH"%(result['h'])
	print "Temperature in Celsius : %.2f C"%(result['c'])
	print "Temperature in Fahrenheit : %.2f F"%(result['f'])
	print " ************************************* "
	time.sleep(1)
