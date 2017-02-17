# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# HTS221
# This code is designed to work with the HTS221_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Humidity?sku=HTS221_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
HTS221_DEFAULT_ADDRESS				=0x5F

# HTS221 Register Map
HTS221_COMMAND_BIT					= 0x80
HTS221_WHO_AM_I						= 0x0F # Device identification
HTS221_AV_CONF						= 0x10 # Humidity and temperature resolution mode
HTS221_CTRL_REG1					= 0x20 # Control register 1
HTS221_CTRL_REG2					= 0x21 # Control register 2
HTS221_CTRL_REG3					= 0x22 # Control register 3
HTS221_STATUS_REG					= 0x27 # Status register
HTS221_HUMIDITY_OUT_L				= 0x28 # Relative humidity data LSB
HTS221_HUMIDITY_OUT_H				= 0x29 # Relative humidity data MSB
HTS221_TEMP_OUT_L					= 0x2A # Temperature data LSB
HTS221_TEMP_OUT_H					= 0x2B # Temperature data MSB
HTS221_H0_RH_X2						= 0x30 # Calibration registers
HTS221_H1_RH_X2						= 0x31 # Calibration registers
HTS221_T0_DEGC_X8					= 0x32 # Calibration registers
HTS221_T1_DEGC_X8					= 0x33 # Calibration registers
HTS221_T1_T0_MSB					= 0x35 # Calibration registers
HTS221_H0_T0_OUT_L					= 0x36 # Calibration registers
HTS221_H0_T0_OUT_H					= 0x37 # Calibration registers
HTS221_H1_T0_OUT_L					= 0x3A # Calibration registers
HTS221_H1_T0_OUT_H					= 0x3B # Calibration registers
HTS221_T0_OUT_L						= 0x3C # Calibration registers
HTS221_T0_OUT_H						= 0x3D # Calibration registers
HTS221_T1_OUT_L						= 0x3E # Calibration registers
HTS221_T1_OUT_H						= 0x3F # Calibration registers

# HTS221 Resolution Configuration
HTS221_AVGH_4						= 0x00 # Nr. internal average = 4
HTS221_AVGH_8						= 0x01 # Nr. internal average = 8
HTS221_AVGH_16						= 0x02 # Nr. internal average = 16
HTS221_AVGH_32						= 0x03 # Nr. internal average = 32
HTS221_AVGH_64						= 0x04 # Nr. internal average = 64
HTS221_AVGH_128						= 0x05 # Nr. internal average = 128
HTS221_AVGH_256						= 0x06 # Nr. internal average = 256
HTS221_AVGH_512						= 0x07 # Nr. internal average = 512
HTS221_AVGT_2						= 0x00 # Nr. internal average = 2
HTS221_AVGT_4						= 0x08 # Nr. internal average = 4
HTS221_AVGT_8						= 0x10 # Nr. internal average = 8
HTS221_AVGT_16						= 0x18 # Nr. internal average = 16
HTS221_AVGT_32						= 0x20 # Nr. internal average = 32
HTS221_AVGT_64						= 0x28 # Nr. internal average = 64
HTS221_AVGT_128						= 0x30 # Nr. internal average = 128
HTS221_AVGT_256						= 0x38 # Nr. internal average = 256

# HTS221 Control Register-1 Configuration
HTS221_MODE_POWERDOWN				= 0x00 # Power Down Mode
HTS221_MODE_ACTIVE					= 0x80 # Active Mode
HTS221_BDU_CONT						= 0x00 # Continuous Update
HTS221_BDU_NOUPDATE					= 0x00 # Output Registers not updated until MSB and LSB reading
HTS221_ODR_ONE						= 0x00 # Output Data Rate : One Shot
HTS221_ODR_1HZ						= 0x01 # Output Data Rate : 1Hz
HTS221_ODR_7HZ						= 0X02 # Output Data Rate : 7Hz
HTS221_ODR_12_5HZ					= 0x03 # Output Data Rate : 12.5Hz

# HTS221 Control Register-2 Configuration
HTS221_BOOT_NORMAL					= 0x00 # Normal Mode
HTS221_BOOT_REBOOT					= 0x80 # Reboot memory content
HTS221_HEATER_ENABLE				= 0x02 # Heater Enable
HTS221_HEATER_DISABLE				= 0x00 # Heater Disable
HTS221_ONE_SHOT_CONV				= 0x00 # Waiting for start of conversion
HTS221_ONE_SHOT_DATASET				= 0x01 # Start for a new dataset

class HTS221():
	def reso_config(self):
		"""Select the Humidity and Temperature Resolution Configuration from the given provided value"""
		RESO_CONFIG = (HTS221_AVGH_512 | HTS221_AVGT_256)
		bus.write_byte_data(HTS221_DEFAULT_ADDRESS, HTS221_AV_CONF, RESO_CONFIG)
	
	def control_register(self):
		"""Select the Control register-1 Configuration from the given provided value"""
		CONTROL_REG = (HTS221_MODE_ACTIVE | HTS221_BDU_CONT | HTS221_ODR_1HZ)
		bus.write_byte_data(HTS221_DEFAULT_ADDRESS, HTS221_CTRL_REG1, CONTROL_REG)
	
	def humidity_calibration(self):
		"""Read Humidity Calibration values from non-volatile memory of the device"""
		
		# Read data back from HTS221_H0_RH_X2(0x30), 1 byte
		val = bus.read_byte_data(HTS221_DEFAULT_ADDRESS, HTS221_H0_RH_X2)
		self.H0 = val / 2
		
		# Read data back from HTS221_H1_RH_X2(0x31), 1 byte
		val = bus.read_byte_data(HTS221_DEFAULT_ADDRESS, HTS221_H1_RH_X2)
		self.H1 = val /2
		
		# Read data back from HTS221_H0_T0_OUT_L(0x36), 2 bytes
		val0 = bus.read_byte_data(HTS221_DEFAULT_ADDRESS, HTS221_H0_T0_OUT_L)
		val1 = bus.read_byte_data(HTS221_DEFAULT_ADDRESS, HTS221_H0_T0_OUT_H)
		self.H2 = ((val1 & 0xFF) * 256) + (val0 & 0xFF)
		
		# Read data back from HTS221_H1_T0_OUT_L(0x3A), 2 bytes
		val0 = bus.read_byte_data(HTS221_DEFAULT_ADDRESS, HTS221_H1_T0_OUT_L)
		val1 = bus.read_byte_data(HTS221_DEFAULT_ADDRESS, HTS221_H1_T0_OUT_H)
		self.H3 = ((val1 & 0xFF) * 256) + (val0 & 0xFF)
	
	def temperature_calibration(self):
		"""Read Temperature Calibration values from non-volatile memory of the device"""
		
		# Read data back from HTS221_T0_DEGC_X8(0x32), 1 byte
		T0 = bus.read_byte_data(HTS221_DEFAULT_ADDRESS, HTS221_T0_DEGC_X8)
		T0 = (T0 & 0xFF)
		
		# Read data back from HTS221_T1_DEGC_X8(0x33), 1 byte
		T1 = bus.read_byte_data(HTS221_DEFAULT_ADDRESS, HTS221_T1_DEGC_X8)
		T1 = (T1 & 0xFF)
		
		# Read data back from HTS221_T1_T0_MSB(0x35), 1 byte
		raw = bus.read_byte_data(HTS221_DEFAULT_ADDRESS, HTS221_T1_T0_MSB)
		raw = (raw & 0x0F)
		
		# Convert the temperature Calibration values to 10-bits
		self.T0 = ((raw & 0x03) * 256) + T0
		self.T1 = ((raw & 0x0C) * 64) + T1
		
		# Read data back from HTS221_T0_OUT_L(0x3C), 2 bytes
		val0 = bus.read_byte_data(HTS221_DEFAULT_ADDRESS, HTS221_T0_OUT_L)
		val1 = bus.read_byte_data(HTS221_DEFAULT_ADDRESS, HTS221_T0_OUT_H)
		self.T2 = ((val1 & 0xFF) * 256) + (val0 & 0xFF)
		
		# Read data back from HTS221_T1_OUT_L(0x3E), 2 bytes
		val0 = bus.read_byte_data(HTS221_DEFAULT_ADDRESS, HTS221_T1_OUT_L)
		val1 = bus.read_byte_data(HTS221_DEFAULT_ADDRESS, HTS221_T1_OUT_H)
		self.T3 = ((val1 & 0xFF) * 256) + (val0 & 0xFF)
	
	def read_data(self):
		"""Read data back from HTS221_HUMIDITY_OUT_L(0x28) HTS221_COMMAND_BIT(0x80), 4 bytes
		humidity msb, humidity lsb, temp msb, temp lsb"""
		data = bus.read_i2c_block_data(HTS221_DEFAULT_ADDRESS, HTS221_HUMIDITY_OUT_L | HTS221_COMMAND_BIT, 4)
		
		# Convert the data
		humidity = (data[1] * 256) + data[0]
		humidity = ((1.0 * self.H1) - (1.0 * self.H0)) * (1.0 * humidity - 1.0 * self.H2) / (1.0 * self.H3 - 1.0 * self.H2) + (1.0 * self.H0)
		temp = (data[3] * 256) + data[2]
		if temp > 32767 :
			temp -= 65536
		cTemp = ((self.T1 - self.T0) / 8.0) * (temp - self.T2) / (self.T3 - self.T2) + (self.T0 / 8.0)
		fTemp = (cTemp * 1.8 ) + 32
		
		return {'h' : humidity, 'c' : cTemp, 'f' : fTemp}

from HTS221 import HTS221
hts221 = HTS221()

while True:
	hts221.reso_config()
	hts221.control_register()
	hts221.humidity_calibration()
	hts221.temperature_calibration()
	hum = hts221.read_data()
	print "Relative Humidity : %.2f %%"%(hum['h'])
	print "Temperature in Celsius : %.2f C"%(hum['c'])
	print "Temperature in Fahrenheit : %.2f F"%(hum['f'])
	print " ************************************* "
	time.sleep(1)
