# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# BMP180
# This code is designed to work with the BMP180_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Pressure?sku=BMP180_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
BMP180_DEFAULT_ADDRESS				= 0x77

# BMP180 Register Map
BMP180_REG_CAL_AC1					= 0xAA # Calibration data (16 bits)
BMP180_REG_CAL_AC2					= 0xAC # Calibration data (16 bits)
BMP180_REG_CAL_AC3					= 0xAE # Calibration data (16 bits)
BMP180_REG_CAL_AC4					= 0xB0 # Calibration data (16 bits)
BMP180_REG_CAL_AC5					= 0xB2 # Calibration data (16 bits)
BMP180_REG_CAL_AC6					= 0xB4 # Calibration data (16 bits)
BMP180_REG_CAL_B1					= 0xB6 # Calibration data (16 bits)
BMP180_REG_CAL_B2					= 0xB8 # Calibration data (16 bits)
BMP180_REG_CAL_MB					= 0xBA # Calibration data (16 bits)
BMP180_REG_CAL_MC					= 0xBC # Calibration data (16 bits)
BMP180_REG_CAL_MD					= 0xBE # Calibration data (16 bits)
BMP180_REG_CHIPID					= 0xD0 # Chip ID
BMP180_REG_SOFTRESET				= 0xE0 # Softreset Register
BMP180_REG_CONTROL					= 0xF4 # Control Register
BMP180_REG_OUT_MSB					= 0xF6 # Data Out MSB
BMP180_REG_OUT_LSB					= 0xF7 # Data Out LSB
BMP180_REG_OUT_xLSB					= 0xF8 # Data Out xLSB

# BMP180 Control Register Configuration
BMP180_P_OVERSAMPLE_1				= 0x00 # Oversampling x 1
BMP180_P_OVERSAMPLE_2				= 0x40 # Oversampling x 2
BMP180_P_OVERSAMPLE_4				= 0x80 # Oversampling x 4
BMP180_P_OVERSAMPLE_8				= 0xC0 # Oversampling x 8
BMP180_SCO_CNVRSN					= 0x20 # Conversion in process
BMP180_SCO_CNVRSN_CMPLT				= 0x00 # Conversion is complete
BMP180_MEASURE_TEMP					= 0x0E # Temperature Measurement
BMP180_MEASURE_PRES					= 0x14 # Pressure Measurement

class BMP180():
	def read_pres_temp_coeff(self):
		"""Read data back from BMP180_REG_CAL_AC1(0xAA), 22 bytes"""
		data = bus.read_i2c_block_data(BMP180_DEFAULT_ADDRESS, BMP180_REG_CAL_AC1, 22)
		
		# Convert the data
		self.AC1 = data[0] * 256 + data[1]
		if self.AC1 > 32767 :
			self.AC1 -= 65535
		
		self.AC2 = data[2] * 256 + data[3]
		if self.AC2 > 32767 :
			self.AC2 -= 65535
		
		self.AC3 = data[4] * 256 + data[5]
		if self.AC3 > 32767 :
			self.AC3 -= 65535
		
		self.AC4 = data[6] * 256 + data[7]
		
		self.AC5 = data[8] * 256 + data[9]
		
		self.AC6 = data[10] * 256 + data[11]
		
		self.B1 = data[12] * 256 + data[13]
		if self.B1 > 32767 :
			self.B1 -= 65535
		
		self.B2 = data[14] * 256 + data[15]
		if self.B2 > 32767 :
			self.B2 -= 65535
		
		self.MB = data[16] * 256 + data[17]
		if self.MB > 32767 :
			self.MB -= 65535
		
		self.MC = data[18] * 256 + data[19]
		if self.MC > 32767 :
			self.MC -= 65535
		
		self.MD = data[20] * 256 + data[21]
		if self.MD > 32767 :
			self.MD -= 65535
	
	def temp_measure(self):
		"""Select the Control Register Configuration for the temperature measurement from the given provided value"""
		TEMP_MEASURE = (BMP180_SCO_CNVRSN | BMP180_MEASURE_TEMP)
		bus.write_byte_data(BMP180_DEFAULT_ADDRESS, BMP180_REG_CONTROL, TEMP_MEASURE)
	
	def read_temp(self):
		"""Read data back from BMP180_REG_OUT_MSB(0xF6), 2 bytes
		temp MSB, temp LSB"""
		data = bus.read_i2c_block_data(BMP180_DEFAULT_ADDRESS, BMP180_REG_OUT_MSB, 2)
		
		# Convert the data
		self.temp = data[0] * 256 + data[1]
	
	def pres_measure(self):
		""""Select the Control Register Configuration for the pressure measurement from the given provided value"""
		PRES_MEASURE = (BMP180_MEASURE_PRES | BMP180_P_OVERSAMPLE_1 | BMP180_SCO_CNVRSN)
		bus.write_byte_data(BMP180_DEFAULT_ADDRESS, BMP180_REG_CONTROL, PRES_MEASURE)
	
	def read_pres(self):
		"""Read data back from BMP180_REG_OUT_MSB(0xF6), 3 bytes
		pres MSB, pres LSB, pres xLSB"""
		data = bus.read_i2c_block_data(BMP180_DEFAULT_ADDRESS, BMP180_REG_OUT_MSB, 3)
		
		# Convert the data
		self.pres = ((data[0] * 65536) + (data[1] * 256) + data[2]) / 128
	
	def result_calculation(self):
		"""Callibration for the final pressure, temperature and altitude"""
		
		# Callibration for Temperature
		X1 = (self.temp - self.AC6) * self.AC5 / 32768.0
		X2 = (self.MC * 2048.0) / (X1 + self.MD)
		B5 = X1 + X2
		cTemp = ((B5 + 8.0) / 16.0) / 10.0
		fTemp = cTemp * 1.8 + 32
		
		# Calibration for Pressure
		B6 = B5 - 4000
		X1 = (self.B2 * (B6 * B6 / 4096.0)) / 2048.0
		X2 = self.AC2 * B6 / 2048.0
		X3 = X1 + X2
		B3 = (((self.AC1 * 4 + X3) * 2) + 2) / 4.0
		X1 = self.AC3 * B6 / 8192.0
		X2 = (self.B1 * (B6 * B6 / 2048.0)) / 65536.0
		X3 = ((X1 + X2) + 2) / 4.0
		B4 = self.AC4 * (X3 + 32768) / 32768.0
		B7 = ((self.pres - B3) * (25000.0))
		pressure = 0.0
		if B7 < 2147483648L :
			pressure = (B7 * 2) / B4
		else :
			pressure = (B7 / B4) * 2
		X1 = (pressure / 256.0) * (pressure / 256.0)
		X1 = (X1 * 3038.0) / 65536.0
		X2 = ((-7357) * pressure) / 65536.0
		pressure = (pressure + (X1 + X2 + 3791) / 16.0) / 100
		
		# Calculate Altitude
		altitude = 44330 * (1 - ((pressure / 1013.25) ** 0.1902))
		
		return {'a' : altitude, 'p' : pressure, 'c' : cTemp, 'f' : fTemp}

from BMP180 import BMP180
bmp180 = BMP180()

while True :
	bmp180.read_pres_temp_coeff()
	bmp180.temp_measure()
	time.sleep(0.5)
	bmp180.read_temp()
	bmp180.pres_measure()
	time.sleep(0.5)
	bmp180.read_pres()
	data = bmp180.result_calculation()
	print "Altitude : %.2f m"%(data['a'])
	print "Pressure : %.2f hPa"%(data['p'])
	print "Temperature in Celsius : %.2f C"%(data['c'])
	print "Temperature in Fahrenheit : %.2f F"%(data['f'])
	print " ***************************************** "
	time.sleep(0.7)
