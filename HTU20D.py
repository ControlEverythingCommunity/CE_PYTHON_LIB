# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# HTU20D
# This code is designed to work with the SHT30_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Temperature?sku=HTU20D_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
HTU20D_DEFAULT_ADDRESS			= 0x40

# HTU20D Command Set
HTU20D_MEAS_RH_HOLD				= 0xE5 # Measure Relative Humidity, Hold Master Mode
HTU20D_MEAS_RH_NOHOLD			= 0xF5 # Measure Relative Humidity, No Hold Master Mode
HTU20D_MEAS_TEMP_HOLD			= 0xE3 # Measure Temperature, Hold Master Mode
HTU20D_MEAS_TEMP_NOHOLD			= 0xF3 # Measure Temperature, No Hold Master Mode
HTU20D_READ_PREV_TEMP			= 0xE0 # Read Temperature Value from Previous RH Measurement
HTU20D_RESET					= 0xFE # Reset
HTU20D_WRITERHT_REG				= 0xE6 # Write RH/T User Register 1
HTU20D_READRHT_REG				= 0xE7 # Read RH/T User Register 1
HTU20D_WRITEHEATER_REG			= 0x51 # Write Heater Control Register
HTU20D_READHEATER_REG			= 0x11 # Read Heater Control Register

class HTU20D():
	def __init__(self):
		self.writetemperature()
		self.writehumidity()
	
	def writetemperature(self):
		"""Select the temperature command from the given provided values"""
		bus.write_byte(HTU20D_DEFAULT_ADDRESS, HTU20D_MEAS_TEMP_NOHOLD)
	
	def readtemperature(self):
		"""Read data back from the device address, 2 bytes, temperature MSB, temperature LSB"""
		data0 = bus.read_byte(HTU20D_DEFAULT_ADDRESS)
		data1 = bus.read_byte(HTU20D_DEFAULT_ADDRESS)
		
		# Convert the data
		cTemp = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85
		fTemp = cTemp * 1.8 + 32
		
		return {'c' : cTemp, 'f' : fTemp}
	
	def writehumidity(self):
		"""Select the relative humidity command from the given provided values"""
		bus.write_byte(HTU20D_DEFAULT_ADDRESS, HTU20D_MEAS_RH_NOHOLD)
	
	def readhumidity(self):
		"""Read data back from the device address, 2 bytes, humidity MSB, humidity LSB"""
		data0 = bus.read_byte(HTU20D_DEFAULT_ADDRESS)
		data1 = bus.read_byte(HTU20D_DEFAULT_ADDRESS)
		
		# Convert the data
		humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6
		
		return {'h' : humidity}
	

from HTU20D import HTU20D
htu20d = HTU20D()

while True:
	htu20d.writehumidity()
	hum = htu20d.readhumidity()
	print "Relative Humidity : %.2f %%"%(hum['h'])
	htu20d.writetemperature()
	temp = htu20d.readtemperature()
	print "Temperature in Celsius : %.2f C"%(temp['c'])
	print "Temperature in Fahrenheit : %.2f F"%(temp['f'])
	print " ************************************* "
	time.sleep(1)
