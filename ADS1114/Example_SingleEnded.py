# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# ADS1114
# This code is designed to work with the ADS1114_I2CADC I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Analog-Digital-Converters?sku=ADS1114_I2CADC#tabs-0-product_tabset-2

import time

from ADS1114 import ADS1114
ads1114 = ADS1114()

while True :
	ads1114.config_single_ended()
	adc = ads1114.read_adc()
	print "Digital Value of Analog Input on AIN0 & GND: %d "%(adc['r'])
	print " ********************************* "
	time.sleep(0.8)
