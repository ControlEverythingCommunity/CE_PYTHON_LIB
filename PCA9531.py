# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# PCA9531
# This code is designed to work with the PCA9531_I2CPWM I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Open-Collectors?sku=PCA9531_I2CPWM#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
PCA9531_DEFAULT_ADDRESS				= 0x60

# PCA9531 Register Map
PCA9531_REG_INPUT					= 0x00 # Input Register
PCA9531_REG_PSC0					= 0x01 # Frequency Prescalar-0
PCA9531_REG_PWM0					= 0x02 # PWM Register-0
PCA9531_REG_PSC1					= 0x03 # Frequency Prescalar-1
PCA9531_REG_PWM1					= 0x04 # PWM Register-1
PCA9531_REG_LS0						= 0x05 # LED0 to LED3 selector
PCA9531_REG_LS1						= 0x06 # LED4 to LED7 selector

# PCA9531 Frequency Prescalar Configuration
PCA9531_PSC0_USERDEFINED			= 0x4B # User-Defined
PCA9531_PSC1_USERDEFINED			= 0x4B # User-Defined

# PCA9531 PWM Register Configuration
PCA9531_PWM0_USERDEFINED			= 0x80 # User-Defined
PCA9531_PWM1_USERDEFINED			= 0x80 # User-Defined

# PCA9531 LED Selector configuration
PCA9531_LS_LED_OFF					= 0x00 # LED off
PCA9531_LS_LED_ON					= 0x01 # LED on
PCA9531_LS_LED_PWM0					= 0x02 # Output blinks at PWM0 rate
PCA9531_LS_LED_PWM1					= 0x03 # Output blinks at PWM1 rate

"""For the particular LED output user have to shift configuration according to the given below data
LS0					LED0 to LED3 selector
7:6		00*			LED3 selected
5:4		00*			LED2 selected
3:2		00*			LED1 selected
1:0		00*			LED0 selected

LS1					LED4 to LED7 selector
7:6		00*			LED7 selected
5:4		00*			LED6 selected
3:2		00*			LED5 selected
1:0		00*			LED4 selected"""

class PCA9531():
	def set_frequency(self):
		"""Select the Frequency Prescalar Configuration from the given provided value"""
		"""For Frequency Prescalar-0"""
		bus.write_byte_data(PCA9531_DEFAULT_ADDRESS, PCA9531_REG_PSC0, PCA9531_PSC0_USERDEFINED)
		
		"""For Frequency Prescalar-1"""
		bus.write_byte_data(PCA9531_DEFAULT_ADDRESS, PCA9531_REG_PSC1, PCA9531_PSC1_USERDEFINED)
	
	def set_pulse_width(self):
		"""Select the PWM Register Configuration from the given provided value"""
		"""For PWM Register-0"""
		bus.write_byte_data(PCA9531_DEFAULT_ADDRESS, PCA9531_REG_PWM0, PCA9531_PWM0_USERDEFINED)
		
		"""For PWM Register-1"""
		bus.write_byte_data(PCA9531_DEFAULT_ADDRESS, PCA9531_REG_PWM1, PCA9531_PWM1_USERDEFINED)
	
	def set_led_selector(self):
		"""Select the LED Selector Configuration from the given provided value"""
		"""For LED0 to LED3 selector"""
		DATA0 = (PCA9531_LS_LED_PWM0 << 6 | PCA9531_LS_LED_PWM0 << 4 | PCA9531_LS_LED_PWM0 << 2 | PCA9531_LS_LED_PWM0)
		bus.write_byte_data(PCA9531_DEFAULT_ADDRESS, PCA9531_REG_PWM0, DATA0)
		
		"""For LED4 to LED7 selector"""
		DATA1 = (PCA9531_LS_LED_PWM0 << 6 | PCA9531_LS_LED_PWM0 << 4 | PCA9531_LS_LED_PWM0 << 2 | PCA9531_LS_LED_PWM0)
		bus.write_byte_data(PCA9531_DEFAULT_ADDRESS, PCA9531_REG_PWM1, DATA1)

from PCA9531 import PCA9531
pca9531 = PCA9531()

pca9531.set_frequency()
time.sleep(0.1)
pca9531.set_pulse_width()
time.sleep(0.1)
pca9531.set_led_selector()
