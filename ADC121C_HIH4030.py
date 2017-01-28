# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# ADC121C_HIH4030
# This code is designed to work with the ADC121C_I2CS_HIH4030 I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/products

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
ADC121C_HIH4030_DEFAULT_ADDRESS				= 0x50

# ADC121C_HIH4030 Register Map
ADC121C_HIH4030_REG_CONVERSION				= 0x00 # Conversion Result Register
ADC121C_HIH4030_REG_ALERT_STATUS			= 0x01 # Alert Status Register
ADC121C_HIH4030_REG_CONFIG					= 0x02 # Configuration Register
ADC121C_HIH4030_REG_LOW_LIMIT				= 0x03 # Alert Low Limit Register
ADC121C_HIH4030_REG_HIGH_LIMIT				= 0x04 # Alert High Limit Register
ADC121C_HIH4030_REG_HYSTERESIS				= 0x05 # Alert Hysteresis Register
ADC121C_HIH4030_REG_LOWCONV					= 0x06 # Lowest Conversion Register
ADC121C_HIH4030_REG_HIGHCONV				= 0x07 # Highest Conversion Register

# ADC121C_HIH4030 Configuration Register
ADC121C_HIH4030_CONFIG_CYCLE_TIME_DIS		= 0x00 # Automatic Conversion Mode Disabled, 0 ksps
ADC121C_HIH4030_CONFIG_CYCLE_TIME_32		= 0x20 # Tconvert x 32, 27 ksps
ADC121C_HIH4030_CONFIG_CYCLE_TIME_64		= 0x40 # Tconvert x 64, 13.5 ksps
ADC121C_HIH4030_CONFIG_CYCLE_TIME_128		= 0x60 # Tconvert x 128, 6.7 ksps
ADC121C_HIH4030_CONFIG_CYCLE_TIME_256		= 0x80 # Tconvert x 256, 3.4 ksps
ADC121C_HIH4030_CONFIG_CYCLE_TIME_512		= 0xA0 # Tconvert x 512, 1.7 ksps
ADC121C_HIH4030_CONFIG_CYCLE_TIME_1024		= 0xC0 # Tconvert x 1024, 0.9 ksps
ADC121C_HIH4030_CONFIG_CYCLE_TIME_2048		= 0xE0 # Tconvert x 2048, 0.4 ksps
ADC121C_HIH4030_CONFIG_ALERT_HOLD_CLEAR		= 0x00 # Alerts will self-clear
ADC121C_HIH4030_CONFIG_ALERT_FLAG_NOCLEAR	= 0x10 # Alerts will not self-clear
ADC121C_HIH4030_CONFIG_ALERT_FLAG_DIS		= 0x00 # Disables alert status bit in the Conversion Result register
ADC121C_HIH4030_CONFIG_ALERT_FLAG_EN		= 0x08 # Enables alert status bit in the Conversion Result register
ADC121C_HIH4030_CONFIG_ALERT_PIN_DIS		= 0x00 # Disables the ALERT output pin
ADC121C_HIH4030_CONFIG_ALERT_PIN_EN			= 0x04 # Enables the ALERT output pin
ADC121C_HIH4030_CONFIG_POLARITY_LOW			= 0x00 # Sets the ALERT pin to active low
ADC121C_HIH4030_CONFIG_POLARITY_HIGH		= 0x01 # Sets the ALERT pin to active high

class ADC121C_HIH4030():
	def __init__(self):
		self.data_config()
	
	def data_config(self):
		"""Select the Configuration Register data from the given provided values"""
		DATA_CONFIG = (ADC121C_HIH4030_CONFIG_CYCLE_TIME_32 | ADC121C_HIH4030_CONFIG_ALERT_HOLD_CLEAR | ADC121C_HIH4030_CONFIG_ALERT_FLAG_DIS)
		bus.write_byte_data(ADC121C_HIH4030_DEFAULT_ADDRESS, ADC121C_HIH4030_REG_CONFIG, DATA_CONFIG)
	
	def read_hum(self):
		"""Read data back from ADC121C_HIH4030_REG_CONVERSION(0x00), 2 bytes
		raw_adc MSB, raw_adc LSB"""
		data = bus.read_i2c_block_data(ADC121C_HIH4030_DEFAULT_ADDRESS, ADC121C_HIH4030_REG_CONVERSION, 2)
		
		# Convert the data to 12-bits
		raw_adc = (data[0] & 0x0F) * 256 + data[1]
		humidity = (100.0 / 4095.0) * raw_adc
		
		return {'h' : humidity}

from ADC121C_HIH4030 import ADC121C_HIH4030
adc121c_hih4030 = ADC121C_HIH4030()

while True :
	hum = adc121c_hih4030.read_hum()
	print "Relative Humidity : %.2f %%RH"%(hum['h'])
	print " ********************************* "
	time.sleep(1)
