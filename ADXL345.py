# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# ADXL345
# This code is designed to work with the ADXL345_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Accelorometer?sku=ADXL345_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
ADXL345_DEFAULT_ADDRESS			= 0x53

# ADXL345 Register Map
ADXL345_REG_DEVID				= 0x00 # Device ID
ADXL345_REG_THRESH_TAP			= 0x1D # Tap Threshold
ADXL345_REG_TAP_AXES			= 0x2A # Axis control for single tap/double tap
ADXL345_REG_ACT_TAP_STATUS		= 0x2B # Source of single tap/double tap
ADXL345_REG_BW_RATE				= 0x2C # Data rate and power mode control
ADXL345_REG_POWER_CTL			= 0x2D # Power-saving features control
ADXL345_REG_DATA_FORMAT			= 0x31 # Data Format Register
ADXL345_REG_DATAX0				= 0x32 # X-axis data 0
ADXL345_REG_DATAX1				= 0x33 # X-axis data 1
ADXL345_REG_DATAY0				= 0x34 # Y-axis data 0
ADXL345_REG_DATAY1				= 0x35 # Y-axis data 1
ADXL345_REG_DATAZ0				= 0x36 # Z-axis data 0
ADXL345_REG_DATAZ1				= 0x37 # Z-axis data 1

# ADXL345 Datarate Configuration
ADXL345_DATARATE_0_10_HZ		= 0x00 # Datarate = 0.1 Hz
ADXL345_DATARATE_0_20_HZ		= 0x01 # Datarate = 0.2 Hz
ADXL345_DATARATE_0_39_HZ		= 0x02 # Datarate = 0.39 Hz
ADXL345_DATARATE_0_78_HZ		= 0x03 # Datarate = 0.78 Hz
ADXL345_DATARATE_1_56_HZ		= 0x04 # Datarate = 1.56 Hz
ADXL345_DATARATE_3_13_HZ		= 0x05 # Datarate = 3.13 Hz
ADXL345_DATARATE_6_25HZ			= 0x06 # Datarate = 6.25 Hz
ADXL345_DATARATE_12_5_HZ		= 0x07 # Datarate = 12.5 Hz
ADXL345_DATARATE_25_HZ			= 0x08 # Datarate = 25 Hz
ADXL345_DATARATE_50_HZ			= 0x09 # Datarate = 50 Hz
ADXL345_DATARATE_100_HZ			= 0x0A # Datarate = 100 Hz
ADXL345_DATARATE_200_HZ			= 0x0B # Datarate = 200 Hz
ADXL345_DATARATE_400_HZ			= 0x0C # Datarate = 400 Hz
ADXL345_DATARATE_800_HZ			= 0x0D # Datarate = 800 Hz
ADXL345_DATARATE_1600_HZ		= 0x0E # Datarate = 1600 Hz
ADXL345_DATARATE_3200_HZ		= 0x0F # Datarate = 3200 Hz

# ADXL345 Mode Configuration
ADXL345_SLP_DSBL_EN				= 0x80 # Auto Sleep Enable
ADXL345_SLP_DSBL_DS				= 0x00 # Auto Sleep Disable
ADXL345_MSRE_STNADBY			= 0x00 # Stand-by Mode
ADXL345_MSRE_MSREMNT			= 0x08 # Measurement Mode
ADXL345_SLEEP_DS				= 0x00 # Sleep bit disable
ADXL345_SLEEP_EN				= 0x04 # Sleep Enable
ADXL34_WAKEUP_8					= 0x00 # Reading Frequency in Sleep Mode = 8
ADXL34_WAKEUP_4					= 0x01 # Reading Frequency in Sleep Mode = 4
ADXL34_WAKEUP_2					= 0x02 # Reading Frequency in Sleep Mode = 2
ADXL34_WAKEUP_1					= 0x03 # Reading Frequency in Sleep Mode = 1

# ADXL345 Range Configuration
ADXL345_RANGE_2_G				= 0x00 # +/- 2g (default)
ADXL345_RANGE_4_G				= 0x01 # +/- 4g
ADXL345_RANGE_8_G				= 0x02 # +/- 8g
ADXL345_RANGE_16_G				= 0x03 # +/- 16g

# ADXL345 Data Output Configuration
ADXL345_SELFTEST_DS				= 0x00 # Self-Test Disable
ADXL345_SELFTEST_EN				= 0x80 # Self-Test Enable
ADXL345_SPI_3					= 0x40 # 3-Wire Interface
ADXL345_SPI_4					= 0x00 # 4-Wire Interface
ADXL345_FULL_RES_EN				= 0x08 # Full-Resolution Enable
ADXL345_FULL_RES_DS				= 0x00 # Full-Resolution Disable, 10-bit

class ADXL345():
	def __init__(self):
		self.select_datarate()
		self.select_range()
		self.enable_measurement()

	def select_datarate(self):
		"""Select the data rate of the accelerometer from the given provided values"""
		DATARATE_CONFIG = (ADXL345_DATARATE_100_HZ)
		bus.write_byte_data(ADXL345_DEFAULT_ADDRESS, ADXL345_REG_BW_RATE, DATARATE_CONFIG)

	def select_range(self):
		"""Select the range of the accelerometer from the given provided values"""
		RANGE = (ADXL345_SELFTEST_DS | ADXL345_SPI_4 | ADXL345_FULL_RES_DS | ADXL345_RANGE_2_G)
		bus.write_byte_data(ADXL345_DEFAULT_ADDRESS, ADXL345_REG_DATA_FORMAT, RANGE)

	def enable_measurement(self):
		"""Select the mode of the accelerometer from the given provided values"""
		MODE = (ADXL345_SLP_DSBL_DS | ADXL345_MSRE_MSREMNT)
		bus.write_byte_data(ADXL345_DEFAULT_ADDRESS, ADXL345_REG_POWER_CTL, MODE)

	def readAccl(self):
		"""Read data back from ADXL345_REG_DATAX0(0x32), 2 bytes
		X-Axis LSB, X-Axis MSB"""
		data0 = bus.read_byte_data(ADXL345_DEFAULT_ADDRESS, ADXL345_REG_DATAX0)
		data1 = bus.read_byte_data(ADXL345_DEFAULT_ADDRESS, ADXL345_REG_DATAX1)
		
		# Convert the data to 10-bits
		xAccl = ((data1 & 0x03) * 256) + data0
		if xAccl > 511 :
			xAccl -= 1024
		
		"""Read data back from ADXL345_REG_DATAY0(0x34), 2 bytes
		Y-Axis LSB, Y-Axis MSB"""
		data0 = bus.read_byte_data(ADXL345_DEFAULT_ADDRESS, ADXL345_REG_DATAY0)
		data1 = bus.read_byte_data(ADXL345_DEFAULT_ADDRESS, ADXL345_REG_DATAY1)
		
		# Convert the data to 10-bits
		yAccl = ((data1 & 0x03) * 256) + data0
		if yAccl > 511 :
			yAccl -= 1024
		
		"""Read data back from ADXL345_REG_DATAZ0(54), 2 bytes
		Z-Axis LSB, Z-Axis MSB"""
		data0 = bus.read_byte_data(ADXL345_DEFAULT_ADDRESS, ADXL345_REG_DATAZ0)
		data1 = bus.read_byte_data(ADXL345_DEFAULT_ADDRESS, ADXL345_REG_DATAZ1)
		
		# Convert the data to 10-bits
		zAccl = ((data1 & 0x03) * 256) + data0
		if zAccl > 511 :
			zAccl -= 1024
		
		return {"x": xAccl, "y": yAccl, "z": zAccl}

from ADXL345 import ADXL345
adxl345 = ADXL345()

while True:
	adxl345.select_datarate()
	adxl345.select_range()
	adxl345.enable_measurement()
	time.sleep(0.1)
	axes = adxl345.readAccl()
	print "Acceleration in X-Axis : %d" %(axes['x'])
	print "Acceleration in Y-Axis : %d" %(axes['y'])
	print "Acceleration in Z-Axis : %d" %(axes['z'])
	print " ************************************* "
	time.sleep(0.9)
