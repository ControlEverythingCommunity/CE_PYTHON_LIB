# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# PCA9537
# This code is designed to work with the PCA9537_I2CO4_IRFR3710 I2C Mini Module available from ControlEverything.com.
# https://shop.controleverything.com/

import time

from PCA9537 import PCA9537
pca9537 = PCA9537()

while True :
	pca9537.select_io()
	pca9537.select_pin()
	pca9537.input_output_config()
	time.sleep(0.5)
	pca9537.read_data()
	print " ******************************** "
	time.sleep(0.5)
