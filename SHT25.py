# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# SHT25
# This code is designed to work with the SHT25_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Humidity?sku=SHT25_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
SHT25_DEFAULT_ADDRESS			= 0x40

# SHT25 Command Set
SHT25_MEAS_RH_HOLD				= 0xE5 # Measure Relative Humidity, Hold Master Mode
SHT25_MEAS_RH_NOHOLD			= 0xF5 # Measure Relative Humidity, No Hold Master Mode
SHT25_MEAS_TEMP_HOLD			= 0xE3 # Measure Temperature, Hold Master Mode
SHT25_MEAS_TEMP_NOHOLD			= 0xF3 # Measure Temperature, No Hold Master Mode
SHT25_READ_PREV_TEMP			= 0xE0 # Read Temperature Value from Previous RH Measurement
SHT25_RESET						= 0xFE # Reset
SHT25_WRITERHT_REG				= 0xE6 # Write RH/T User Register 1
SHT25_READRHT_REG				= 0xE7 # Read RH/T User Register 1
SHT25_WRITEHEATER_REG			= 0x51 # Write Heater Control Register
SHT25_READHEATER_REG			= 0x11 # Read Heater Control Register

class SHT25():
	def __init__(self):
		self.writehumidity()
		time.sleep(0.3)
		self.writetemperature()
	
	def writehumidity(self):
		"""Select the relative humidity command from the given provided values"""
		bus.write_byte(SHT25_DEFAULT_ADDRESS, SHT25_MEAS_RH_NOHOLD)
	
	def readhumidity(self):
		"""Read data back from the device address, 2 bytes, humidity MSB, humidity LSB"""
		data0 = bus.read_byte(SHT25_DEFAULT_ADDRESS)
		data1 = bus.read_byte(SHT25_DEFAULT_ADDRESS)
		
		# Convert the data
		humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6
		
		return {'h' : humidity}
	
	def writetemperature(self):
		"""Select the temperature command from the given provided values"""
		bus.write_byte(SHT25_DEFAULT_ADDRESS, SHT25_MEAS_TEMP_NOHOLD)
	
	def readtemperature(self):
		"""Read data back from the device address, 2 bytes, temperature MSB, temperature LSB"""
		data0 = bus.read_byte(SHT25_DEFAULT_ADDRESS)
		data1 = bus.read_byte(SHT25_DEFAULT_ADDRESS)
		
		# Convert the data
		cTemp = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85
		fTemp = cTemp * 1.8 + 32
		
		return {'c' : cTemp, 'f' : fTemp}

from SHT25 import SHT25
sht25 = SHT25()

while True:
	time.sleep(0.1)
	sht25.writehumidity()
	time.sleep(0.1)
	hum = sht25.readhumidity()
	print "Relative Humidity : %.2f %%"%(hum['h'])
	sht25.writetemperature()
	time.sleep(0.1)
	temp = sht25.readtemperature()
	print "Temperature in Celsius : %.2f C"%(temp['c'])
	print "Temperature in Fahrenheit : %.2f F"%(temp['f'])
	print " ************************************* "
	time.sleep(1)
