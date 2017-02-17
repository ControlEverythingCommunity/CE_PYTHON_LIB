# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# ADS1115
# This code is designed to work with the ADS1115_I2CADC I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Analog-Digital-Converters?sku=ADS1115_I2CADC#tabs-0-product_tabset-2

import time

from ADS1115 import ADS1115
ads1115 = ADS1115()

while True :
	ads1115.set_channel()
	ads1115.config_single_ended()
	time.sleep(0.1)
	adc = ads1115.read_adc()
	print "Digital Value of Analog Input : %d "%(adc['r'])
	print " ********************************************* "
	time.sleep(0.8)
