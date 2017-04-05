# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MPL115A2
# This code is designed to work with the MPL115A2_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Barometer?sku=MPL115A2_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
MPL115A2_DEFAULT_ADDRESS			= 0x60

# MPL115A2 Register Map
MPL115A2_REG_PRESSURE_MSB			= 0x00 # Pressure ADC output value MSB
MPL115A2_REG_PRESSURE_LSB			= 0x01 # Pressure ADC output value LSB
MPL115A2_REG_TEMP_MSB				= 0x02 # Temperature ADC output value MSB
MPL115A2_REG_TEMP_LSB				= 0x03 # Temperature ADC output value LSB
MPL115A2_REG_A0_COEFF_MSB			= 0x04 # A0 coefficient MSB
MPL115A2_REG_A0_COEFF_LSB			= 0x05 # A0 coefficient LSB
MPL115A2_REG_B1_COEFF_MSB			= 0x06 # B1 coefficient MSB
MPL115A2_REG_B1_COEFF_LSB			= 0x07 # B1 coefficient LSB
MPL115A2_REG_B2_COEFF_MSB			= 0x08 # B2 coefficient MSB
MPL115A2_REG_B2_COEFF_LSB			= 0x09 # B2 coefficient LSB
MPL115A2_REG_C12_COEFF_MSB			= 0x0A # C12 coefficient MSB
MPL115A2_REG_C12_COEFF_LSB			= 0x0B # C12 coefficient LSB
MPL115A2_REG_STARTCONVERSION		= 0x12 # Start Pressure and Temperature Conversion

class MPL115A2():
	def read_coefficient(self):
		"""Read data back from MPL115A2_REG_A0_COEFF_MSB(0x04), 8 bytes
		A0 MSB, A0 LSB, B1 MSB, B1 LSB, B2 MSB, B2 LSB, C12 MSB, C12 LSB"""
		data = bus.read_i2c_block_data(MPL115A2_DEFAULT_ADDRESS, MPL115A2_REG_A0_COEFF_MSB, 8)
		
		# Convert the data to floating points
		self.A0 = (data[0] * 256 + data[1]) / 8.0
		
		self.B1 = (data[2] * 256 + data[3])
		if self.B1 > 32767 :
			self.B1 -= 65536
		self.B1 = self.B1 / 8192.0
		
		self.B2 = (data[4] * 256 + data[5])
		if self.B2 > 32767 :
			self.B2 -= 65535
		self.B2 = self.B2 / 16384.0
		
		self.C12 = ((data[6] * 256 + data[7]) / 4) / 4194304.0
		
	def start_conversion(self):
		"""Select the Start Conversion Register Configuration from the given provided value"""
		bus.write_byte_data(MPL115A2_DEFAULT_ADDRESS, MPL115A2_REG_STARTCONVERSION, 0x00)
	
	def read_pres(self):
		"""Read data back from MPL115A2_REG_PRESSURE_MSB(0x00), 4 bytes
		pres MSB, pres LSB, temp MSB, temp LSB"""
		data = bus.read_i2c_block_data(MPL115A2_DEFAULT_ADDRESS, MPL115A2_REG_PRESSURE_MSB, 4)
		
		# Convert the data to 10-bits
		pres = ((data[0] * 256) + (data[1] & 0xC0)) / 64
		temp = ((data[2] * 256) + (data[3] & 0xC0)) / 64
		
		# Calculate pressure compensation
		presComp = (self.A0 + ((self.B1 + (self.C12 * temp)) * pres)) + (self.B2 * temp)
		
		# Convert the data
		pressure = (65.0 / 1023.0) * presComp + 50.0
		cTemp = (temp - 498) / (-5.35) + 25
		fTemp = cTemp * 1.8 + 32
		
		return {'p' : pressure, 'c' : cTemp, 'f' : fTemp}

from MPL115A2 import MPL115A2
mpl115a2 = MPL115A2()

while True :
	mpl115a2.read_coefficient()
	mpl115a2.start_conversion()
	time.sleep(0.5)
	pres = mpl115a2.read_pres()
	print "Pressure : %.2f kPa"%(pres['p'])
	print "Temperature in Celsius : %.2f C"%(pres['c'])
	print "Temperature in Fahrenheit : %.2f F"%(pres['f'])
	print " ***************************************** "
	time.sleep(0.5)
