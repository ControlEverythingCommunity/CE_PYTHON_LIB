# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# SHT31
# This code is designed to work with the SHT31_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Humidity?sku=SHT31_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
SHT31_DEFAULT_ADDRESS				= 0x44

# SHT31 Command Set
SHT31_MEAS_REP_STRETCH_EN			= 0x2C # Clock stretching enabled
SHT31_MEAS_HIGH_REP_STRETCH_EN		= 0x06 # High repeatability measurement with clock stretching enabled
SHT31_MEAS_MED_REP_STRETCH_EN		= 0x0D # Medium repeatability measurement with clock stretching enabled
SHT31_MEAS_LOW_REP_STRETCH_EN		= 0x10 # Low repeatability measurement with clock stretching enabled
SHT31_MEAS_REP_STRETCH_DS			= 0x24 # Clock stretching disabled
SHT31_MEAS_HIGH_REP_STRETCH_DS		= 0x00 # High repeatability measurement with clock stretching disabled
SHT31_MEAS_MED_REP_STRETCH_DS		= 0x0B # Medium repeatability measurement with clock stretching disabled
SHT31_MEAS_LOW_REP_STRETCH_DS		= 0x16 # Low repeatability measurement with clock stretching disabled
SHT31_CMD_READSTATUS				= 0xF32D # Command to read out the status register
SHT31_CMD_CLEARSTATUS				= 0x3041 # Command to clear the status register
SHT31_CMD_SOFTRESET					= 0x30A2 # Soft reset command
SHT31_CMD_HEATERENABLE				= 0x306D # Heater enable command
SHT31_CMD_HEATERDISABLE				= 0x3066 # Heater disable command

class SHT31():
	def __init__(self):
		self.write_command()
		time.sleep(0.3)
		self.read_data()
	
	def write_command(self):
		"""Select the temperature & humidity command from the given provided values"""
		COMMAND = [SHT31_MEAS_HIGH_REP_STRETCH_EN]
		bus.write_i2c_block_data(SHT31_DEFAULT_ADDRESS, SHT31_MEAS_REP_STRETCH_EN, COMMAND)
	
	def read_data(self):
		"""Read data back from device address, 6 bytes
		temp MSB, temp LSB, temp CRC, humidity MSB, humidity LSB, humidity CRC"""
		data = bus.read_i2c_block_data(SHT31_DEFAULT_ADDRESS, 6)
		
		# Convert the data
		temp = data[0] * 256 + data[1]
		cTemp = -45 + (175 * temp / 65535.0)
		fTemp = -49 + (315 * temp / 65535.0)
		humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
		
		return {'c' : cTemp, 'f' : fTemp, 'h' : humidity}

from SHT31 import SHT31
sht31 = SHT31()

while True:
	sht31.write_command()
	time.sleep(0.3)
	result = sht31.read_data()
	print "Relative Humidity : %.2f %%"%(result['h'])
	print "Temperature in Celsius : %.2f C"%(result['c'])
	print "Temperature in Fahrenheit : %.2f F"%(result['f'])
	print " ************************************* "
	time.sleep(1)
