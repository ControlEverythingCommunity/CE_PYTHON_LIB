# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# ADC121C_MQ135
# This code is designed to work with the ADC121C_I2CGAS_MQ2 I2C Mini Module available from ControlEverything.com.
# https://shop.controleverything.com/products/nh3-amonia-benzene-alcohol-gas-sensor

import smbus
import time
import math

# Get I2C bus
bus = smbus.SMBus(1)

Measure_RL = 20.0
MQ_Sample_Time = 5
Measure_RoInCleanAir = 3.7

# I2C address of the device
ADC121C_MQ135_DEFAULT_ADDRESS               = 0x50

# ADC121C_MQ135 Register Map
ADC121C_MQ135_REG_CONVERSION                = 0x00 # Conversion Result Register
ADC121C_MQ135_REG_ALERT_STATUS				= 0x01 # Alert Status Register
ADC121C_MQ135_REG_CONFIG                    = 0x02 # Configuration Register
ADC121C_MQ135_REG_LOW_LIMIT					= 0x03 # Alert Low Limit Register
ADC121C_MQ135_REG_HIGH_LIMIT                = 0x04 # Alert High Limit Register
ADC121C_MQ135_REG_HYSTERESIS                = 0x05 # Alert Hysteresis Register
ADC121C_MQ135_REG_LOWCONV                   = 0x06 # Lowest Conversion Register
ADC121C_MQ135_REG_HIGHCONV					= 0x07 # Highest Conversion Register

# ADC121C_MQ135 Configuration Register
ADC121C_MQ135_CONFIG_CYCLE_TIME_DIS			= 0x00 # Automatic Conversion Mode Disabled, 0 ksps
ADC121C_MQ135_CONFIG_CYCLE_TIME_32			= 0x20 # Tconvert x 32, 27 ksps
ADC121C_MQ135_CONFIG_CYCLE_TIME_64			= 0x40 # Tconvert x 64, 13.5 ksps
ADC121C_MQ135_CONFIG_CYCLE_TIME_128			= 0x60 # Tconvert x 128, 6.7 ksps
ADC121C_MQ135_CONFIG_CYCLE_TIME_256			= 0x80 # Tconvert x 256, 3.4 ksps
ADC121C_MQ135_CONFIG_CYCLE_TIME_512			= 0xA0 # Tconvert x 512, 1.7 ksps
ADC121C_MQ135_CONFIG_CYCLE_TIME_1024        = 0xC0 # Tconvert x 1024, 0.9 ksps
ADC121C_MQ135_CONFIG_CYCLE_TIME_2048        = 0xE0 # Tconvert x 2048, 0.4 ksps
ADC121C_MQ135_CONFIG_ALERT_HOLD_CLEAR       = 0x00 # Alerts will self-clear
ADC121C_MQ135_CONFIG_ALERT_FLAG_NOCLEAR		= 0x10 # Alerts will not self-clear
ADC121C_MQ135_CONFIG_ALERT_FLAG_DIS			= 0x00 # Disables alert status bit in the Conversion Result register
ADC121C_MQ135_CONFIG_ALERT_FLAG_EN			= 0x08 # Enables alert status bit in the Conversion Result register
ADC121C_MQ135_CONFIG_ALERT_PIN_DIS			= 0x00 # Disables the ALERT output pin
ADC121C_MQ135_CONFIG_ALERT_PIN_EN           = 0x04 # Enables the ALERT output pin
ADC121C_MQ135_CONFIG_POLARITY_LOW           = 0x00 # Sets the ALERT pin to active low
ADC121C_MQ135_CONFIG_POLARITY_HIGH			= 0x01 # Sets the ALERT pin to active high

class ADC121C_MQ135():
	def data_config(self):
		"""Select the Configuration Register data from the given provided values"""
		DATA_CONFIG = (ADC121C_MQ135_CONFIG_CYCLE_TIME_32 | ADC121C_MQ135_CONFIG_ALERT_HOLD_CLEAR | ADC121C_MQ135_CONFIG_ALERT_FLAG_DIS)
		bus.write_byte_data(ADC121C_MQ135_DEFAULT_ADDRESS, ADC121C_MQ135_REG_CONFIG, DATA_CONFIG)
		
		time.sleep(0.1)
		"""Read data back from ADC121C_MQ135_REG_CONVERSION(0x00), 2 bytes
		raw_adc MSB, raw_adc LSB"""
		data = bus.read_i2c_block_data(ADC121C_MQ135_DEFAULT_ADDRESS, ADC121C_MQ135_REG_CONVERSION, 2)
		
		# Convert the data to 12-bits
		self.raw_adc = (data[0] & 0x0F) * 256.0 + data[1]
	
	def measure_rsAir(self):
		"""Calculate the sensor resistance in clean air from raw_adc"""
		vrl = self.raw_adc * (5.0 / 4096.0)
		self.rsAir = ((5.0 - vrl) / vrl) * Measure_RL
	
	def measure_Ro(self):
		"""Calculate Rs/Ro ratio from the resistance Rs & Ro"""
		Measure_Ro = 0.0
		for i in range(0, MQ_Sample_Time):
			Measure_Ro += self.rsAir
			time.sleep(0.1)
		Measure_Ro = Measure_Ro / MQ_Sample_Time
		Measure_Ro = Measure_Ro / Measure_RoInCleanAir
		return Measure_Ro
		
	def measure_Rs(self):
		Measure_Rs = 0.0
		for i in range(0, MQ_Sample_Time):
			Measure_Rs += self.rsAir
			time.sleep(0.1)
		Measure_Rs = Measure_Rs / MQ_Sample_Time
		return Measure_Rs
	
	def measure_ratio(self):
		self.ratio = self.measure_Rs() / self.measure_Ro()
		print "Ratio = %.3f "%self.ratio
	
	def calculate_ppm_CO2(self):
		"""Calculate the final concentration value"""
		a = -0.32
		b = 1.0
		ppm = math.exp(((math.log(self.ratio, 10)) - b) / a)
		
		return {'co2' : ppm}

    def calculate_ppm_NH3(self):
    """Calculate the final concentration value"""
        a = -0.41
        b = 1.0
        ppm = math.exp(((math.log(self.ratio, 10)) - b) / a)
                
        return {'nh3' : ppm}

from ADC121C_MQ135 import ADC121C_MQ135
ADC121C_mq135 = ADC121C_MQ135()

while True :
	adc121c_mq135.data_config()
	adc121c_mq135.measure_rsAir()
	adc121c_mq135.measure_Rs()
	adc121c_mq135.measure_Ro()
	adc121c_mq135.measure_ratio()
	data1 = adc121c_mq135.calculate_ppm_CO2()
    data2 = adc121c_mq135.calculate_ppm_NH3()
	print "Carbon Dioxide Concentration : %.3f ppm" %(data1['co2'])
    print "Ammonia Concentration : %.3f ppm" %(data2['nh3'])
	print " ********************************* "
	time.sleep(1)
