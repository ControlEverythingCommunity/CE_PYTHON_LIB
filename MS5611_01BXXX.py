# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MS5611_01BXXX
# This code is designed to work with the MS5611_01BXXX_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Analog-Digital-Converters?sku=MS5611-01BXXX_I2CS_A01#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
MS5611_01BXXX_DEFAULT_ADDRESS			= 0x77

# MS5611_01BXXX Command Set
MS5611_01BXXX_CMD_ADC_READ				= 0x00 # ADC Read
MS5611_01BXXX_CMD_RESET					= 0x1E # Reset Command
MS5611_01BXXX_CMD_CONV_D1_256			= 0x40 # Convert D1 (OSR=256)
MS5611_01BXXX_CMD_CONV_D1_512			= 0x42 # Convert D1 (OSR=512)
MS5611_01BXXX_CMD_CONV_D1_1024			= 0x44 # Convert D1 (OSR=1024)
MS5611_01BXXX_CMD_CONV_D1_2048			= 0x46 # Convert D1 (OSR=2048)
MS5611_01BXXX_CMD_CONV_D1_4096			= 0x48 # Convert D1 (OSR=4096)
MS5611_01BXXX_CMD_CONV_D2_256			= 0x50 # Convert D2 (OSR=256)
MS5611_01BXXX_CMD_CONV_D2_512			= 0x52 # Convert D2 (OSR=512)
MS5611_01BXXX_CMD_CONV_D2_1024			= 0x54 # Convert D2 (OSR=1024)
MS5611_01BXXX_CMD_CONV_D2_2048			= 0x56 # Convert D2 (OSR=2048)
MS5611_01BXXX_CMD_CONV_D2_4096			= 0x58 # Convert D2 (OSR=4096)
MS5611_01BXXX_CMD_READ_PROM_C1			= 0xA2 # PROM Read (Coefficient C1)
MS5611_01BXXX_CMD_READ_PROM_C2			= 0xA4 # PROM Read (Coefficient C2)
MS5611_01BXXX_CMD_READ_PROM_C3			= 0xA6 # PROM Read (Coefficient C3)
MS5611_01BXXX_CMD_READ_PROM_C4			= 0xA8 # PROM Read (Coefficient C4)
MS5611_01BXXX_CMD_READ_PROM_C5			= 0xAA # PROM Read (Coefficient C5)
MS5611_01BXXX_CMD_READ_PROM_C6			= 0xAC # PROM Read (Coefficient C6)

class MS5611_01BXXX():
	def reset_cmd(self):
		"""Select the Reset Command from the given provided value"""
		bus.write_byte(MS5611_01BXXX_DEFAULT_ADDRESS, MS5611_01BXXX_CMD_RESET)
	
	def read_coefficient(self):
		"""Read 12 bytes of calibration data from MS5611_01BXXX_CMD_READ_PROM(0xA2)"""
		
		# Read pressure sensitivity
		data = bus.read_i2c_block_data(MS5611_01BXXX_DEFAULT_ADDRESS, MS5611_01BXXX_CMD_READ_PROM_C1, 2)
		self.C1 = data[0] * 256 + data[1]
		
		# Read pressure offset
		data = bus.read_i2c_block_data(MS5611_01BXXX_DEFAULT_ADDRESS, MS5611_01BXXX_CMD_READ_PROM_C2, 2)
		self.C2 = data[0] * 256 + data[1]
		
		# Read temperature coefficient of pressure sensitivity
		data = bus.read_i2c_block_data(MS5611_01BXXX_DEFAULT_ADDRESS, MS5611_01BXXX_CMD_READ_PROM_C3, 2)
		self.C3 = data[0] * 256 + data[1]
		
		# Read temperature coefficient of pressure offset
		data = bus.read_i2c_block_data(MS5611_01BXXX_DEFAULT_ADDRESS, MS5611_01BXXX_CMD_READ_PROM_C4, 2)
		self.C4 = data[0] * 256 + data[1]
		
		# Read reference temperature
		data = bus.read_i2c_block_data(MS5611_01BXXX_DEFAULT_ADDRESS, MS5611_01BXXX_CMD_READ_PROM_C5, 2)
		self.C5 = data[0] * 256 + data[1]
		
		# Read temperature coefficient of the temperature
		data = bus.read_i2c_block_data(MS5611_01BXXX_DEFAULT_ADDRESS, MS5611_01BXXX_CMD_READ_PROM_C6, 2)
		self.C6 = data[0] * 256 + data[1]
	
	def pres_conversion(self):
		"""Select the Pressure Conversion Command from the given provided value"""
		bus.write_byte(MS5611_01BXXX_DEFAULT_ADDRESS, MS5611_01BXXX_CMD_CONV_D1_256)
	
	def read_pressure(self):
		"""Read data back from MS5611_01BXXX_CMD_ADC_READ(0x00), 3 bytes
		D1 MSB2, D1 MSB1, D1 LSB"""
		value = bus.read_i2c_block_data(MS5611_01BXXX_DEFAULT_ADDRESS, MS5611_01BXXX_CMD_ADC_READ, 3)
		
		self.D1 = value[0] * 65536 + value[1] * 256 + value[2]
		
	
	def temp_conversion(self):
		"""Select the Temperature Conversion Command from the given provided value"""
		bus.write_byte(MS5611_01BXXX_DEFAULT_ADDRESS, MS5611_01BXXX_CMD_CONV_D2_256)
	
	def read_temp(self):
		"""Read data back from MS5611_01BXXX_CMD_ADC_READ(0x00), 3 bytes
		D2 MSB2, D2 MSB1, D2 LSB"""
		value = bus.read_i2c_block_data(MS5611_01BXXX_DEFAULT_ADDRESS, MS5611_01BXXX_CMD_ADC_READ, 3)
		
		self.D2 = value[0] * 65536 + value[1] * 256 + value[2]
		
	
	def result_conversion(self):
		"""Conversion of the read data to get the final output"""
		
		dT = self.D2 - (self.C5 * 256)
		TEMP = 2000 + ((dT * self.C6) / 8388608)
		OFF = self.C2 * 65536 + (self.C4 * dT) / 128
		SENS = self.C1 * 32768 + (self.C3 * dT ) / 256
		
		T2 = 0
		OFF2 = 0
		SENS2 = 0
		
		if TEMP >= 2000 :
			T2 = 0
			OFF2 = 0
			SENS2 = 0
		elif TEMP < 2000 :
			T2 = (dT * dT) / 2147483648
			OFF2 = 5 * ((TEMP - 2000) * (TEMP - 2000)) / 2
			SENS2 = 5 * ((TEMP - 2000) * (TEMP - 2000)) / 4
			if TEMP < -1500 :
				OFF2 = OFF2 + 7 * ((TEMP + 1500) * (TEMP + 1500))
				SENS2 = SENS2 + 11 * ((TEMP + 1500) * (TEMP + 1500)) / 2
		
		TEMP = TEMP - T2
		OFF = OFF - OFF2
		SENS = SENS - SENS2
		
		pressure = ((((self.D1 * SENS) / 2097152) - OFF) / 32768.0) / 100.0
		cTemp = TEMP / 100.0
		fTemp = cTemp * 1.8 + 32
		
		return {'p' : pressure, 'c' : cTemp, 'f' : fTemp}

from MS5611_01BXXX import MS5611_01BXXX
ms5611_01bxxx = MS5611_01BXXX()

while True :
	ms5611_01bxxx.reset_cmd()
	time.sleep(0.2)
	ms5611_01bxxx.read_coefficient()
	ms5611_01bxxx.pres_conversion()
	time.sleep(0.2)
	ms5611_01bxxx.read_pressure()
	ms5611_01bxxx.temp_conversion()
	time.sleep(0.2)
	ms5611_01bxxx.read_temp()
	pres = ms5611_01bxxx.result_conversion()
	print "Pressure : %.2f mbar"%(pres['p'])
	print "Temperature in Celsius : %.2f C"%(pres['c'])
	print "Temperature in Fahrenheit : %.2f F"%(pres['f'])
	print " ***************************************** "
	time.sleep(0.7)
