# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# SI7020-A20
# This code is designed to work with the SI7020-A20_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Humidity?sku=SI7020-A20_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
SI7020_A20_DEFAULT_ADDRESS			= 0x40

# SI7020_A20 Command Set
SI7020_A20_MEAS_RH_HOLD				= 0xE5 # Measure Relative Humidity, Hold Master Mode
SI7020_A20_MEAS_RH_NOHOLD			= 0xF5 # Measure Relative Humidity, No Hold Master Mode
SI7020_A20_MEAS_TEMP_HOLD			= 0xE3 # Measure Temperature, Hold Master Mode
SI7020_A20_MEAS_TEMP_NOHOLD			= 0xF3 # Measure Temperature, No Hold Master Mode
SI7020_A20_READ_PREV_TEMP			= 0xE0 # Read Temperature Value from Previous RH Measurement
SI7020_A20_RESET					= 0xFE # Reset
SI7020_A20_WRITERHT_REG				= 0xE6 # Write RH/T User Register 1
SI7020_A20_READRHT_REG				= 0xE7 # Read RH/T User Register 1
SI7020_A20_WRITEHEATER_REG			= 0x51 # Write Heater Control Register
SI7020_A20_READHEATER_REG			= 0x11 # Read Heater Control Register

class SI7020_A20():
	def __init__(self):
		self.writehumidity()
		time.sleep(0.3)
		self.writetemperature()
	
	def writehumidity(self):
		"""Select the relative humidity command from the given provided values"""
		bus.write_byte(SI7020_A20_DEFAULT_ADDRESS, SI7020_A20_MEAS_RH_NOHOLD)
	
	def readhumidity(self):
		"""Read data back from the device address, 2 bytes, humidity MSB, humidity LSB"""
		data0 = bus.read_byte(SI7020_A20_DEFAULT_ADDRESS)
		data1 = bus.read_byte(SI7020_A20_DEFAULT_ADDRESS)
		
		# Convert the data
		humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6
		
		return {'h' : humidity}
	
	def writetemperature(self):
		"""Select the temperature command from the given provided values"""
		bus.write_byte(SI7020_A20_DEFAULT_ADDRESS, SI7020_A20_MEAS_TEMP_NOHOLD)
	
	def readtemperature(self):
		"""Read data back from the device address, 2 bytes, temperature MSB, temperature LSB"""
		data0 = bus.read_byte(SI7020_A20_DEFAULT_ADDRESS)
		data1 = bus.read_byte(SI7020_A20_DEFAULT_ADDRESS)
		
		# Convert the data
		cTemp = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85
		fTemp = cTemp * 1.8 + 32
		
		return {'c' : cTemp, 'f' : fTemp}

from SI7020_A20 import SI7020_A20
si7020_a20 = SI7020_A20()

while True:
	time.sleep(0.3)
	si7020_a20.writehumidity()
	time.sleep(0.3)
	si7020_a20.writetemperature()
	time.sleep(0.3)
	hum = si7020_a20.readhumidity()
	time.sleep(0.3)
	print "Relative Humidity : %.2f %%RH"%(hum['h'])
	temp = si7020_a20.readtemperature()
	print "Temperature in Celsius : %.2f C"%(temp['c'])
	print "Temperature in Fahrenheit : %.2f F"%(temp['f'])
	print " ************************************* "
