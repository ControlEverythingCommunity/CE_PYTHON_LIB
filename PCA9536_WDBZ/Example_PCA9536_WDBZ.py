# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# PCA9536_WDBZ_BZ
# This code is designed to work with the PCA9536_WDBZ_I2CS I2C Mini Module available from ControlEverything.com.
# https://shop.controleverything.com/products/water-detect-sensor-with-buzzer

import time

from PCA9536_WDBZ import PCA9536_WDBZ
PCA9536_WDBZ = PCA9536_WDBZ()

while True :
	PCA9536_WDBZ.select_io()
	PCA9536_WDBZ.select_pin()
	PCA9536_WDBZ.input_output_config()
	time.sleep(0.5)
	PCA9536_WDBZ.read_data()
	print " ******************************** "
	time.sleep(0.5)
