# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# PCA9530_1C
# This code is designed to work with the PCA9530_I2CPWM_1C_IRFR3710PBF I2C Mini Module available from ControlEverything.com.
# https://shop.controleverything.com/
# NT

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
PCA9530_1C_DEFAULT_ADDRESS				= 0x60

# PCA9530_1C Register Map
PCA9530_1C_REG_INPUT					= 0x00 # Input Register
PCA9530_1C_REG_PSC0                     = 0x01 # Frequency Prescalar-0
PCA9530_1C_REG_PWM0                     = 0x02 # PWM Register-0
PCA9530_1C_REG_PSC1                     = 0x03 # Frequency Prescalar-1
PCA9530_1C_REG_PWM1                     = 0x04 # PWM Register-1
PCA9530_1C_REG_LS0						= 0x05 # LED selector

# PCA9530_1C Frequency Prescalar Configuration
PCA9530_1C_PSC0_USERDEFINED             = 0x4B # User-Defined
PCA9530_1C_PSC1_USERDEFINED             = 0x4B # User-Defined

# PCA9530_1C PWM Register Configuration
PCA9530_1C_PWM0_USERDEFINED             = 0x80 # User-Defined
PCA9530_1C_PWM1_USERDEFINED             = 0x80 # User-Defined

# PCA9530_1C LED Selector configuration
PCA9530_1C_LS_LED_OFF					= 0x00 # LED off
PCA9530_1C_LS_LED_ON					= 0x01 # LED on
PCA9530_1C_LS_LED_PWM0					= 0x02 # Output blinks at PWM0 rate
PCA9530_1C_LS_LED_PWM1					= 0x03 # Output blinks at PWM1 rate

"""For the particular LED output user have to shift configuration according to the given below data
LS0					LED selector
1:0		00*			LED0 selected"""

class PCA9530_1C():
	def set_frequency(self):
		"""Select the Frequency Prescalar Configuration from the given provided value"""
		"""For Frequency Prescalar-0"""
		bus.write_byte_data(PCA9530_1C_DEFAULT_ADDRESS, PCA9530_1C_REG_PSC0, PCA9530_1C_PSC0_USERDEFINED)
		
		"""For Frequency Prescalar-1"""
		bus.write_byte_data(PCA9530_1C_DEFAULT_ADDRESS, PCA9530_1C_REG_PSC1, PCA9530_1C_PSC1_USERDEFINED)
	
	def set_pulse_width(self):
		"""Select the PWM Register Configuration from the given provided value"""
		"""For PWM Register-0"""
		bus.write_byte_data(PCA9530_1C_DEFAULT_ADDRESS, PCA9530_1C_REG_PWM0, PCA9530_1C_PWM0_USERDEFINED)
		
		"""For PWM Register-1"""
		bus.write_byte_data(PCA9530_1C_DEFAULT_ADDRESS, PCA9530_1C_REG_PWM1, PCA9530_1C_PWM1_USERDEFINED)
	
	def set_led_selector(self):
		"""Select the LED Selector Configuration from the given provided value"""
		"""For LED selector"""
		DATA0 = (PCA9530_1C_LS_LED_PWM0)
		bus.write_byte_data(PCA9530_1C_DEFAULT_ADDRESS, PCA9530_1C_REG_PWM0, DATA0)


from PCA9530_1C import PCA9530_1C
pca9530_1C = PCA9530_1C()

pca9530_1C.set_frequency()
time.sleep(0.1)
pca9530_1C.set_pulse_width()
time.sleep(0.1)
pca9530_1C.set_led_selector()
