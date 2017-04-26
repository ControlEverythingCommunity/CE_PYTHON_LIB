# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# LT-1PA01
# This code is designed to work with the LT-1PA01_I2CS I2C Mini Module available from ControlEverything.com.
# https://shop.controleverything.com/

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
LT_1PA01_DEFAULT_ADDRESS                        = 0x44

# LT_1PA01 Register Set
LT_1PA01_REG_ALSPROX_DEVID                      = 0x00 # Device Identification Register
LT_1PA01_REG_ALSPROX_CONFIG0					= 0x01 # Proximity Configuration Register
LT_1PA01_REG_ALSPROX_CONFIG1					= 0x02 # Proximity/ALS Configuration Register
LT_1PA01_REG_ALSPROX_CONFIG2					= 0x03 # Ambient Light Sensor IR Compensation Register
LT_1PA01_REG_ALSPROX_INTCONFIG					= 0x04 # Interrupt Configuration, Status & Control Register
LT_1PA01_REG_ALSPROX_PROX_INT_TL                = 0x05 # Proximity Interrupt LOW Threshold Byte Register
LT_1PA01_REG_ALSPROX_PROX_INT_TH				= 0x06 # Proximity Interrupt HIGH Threshold Byte Register
LT_1PA01_REG_ALSPROX_ALS_INT_TL					= 0x07 # ALS Interrupt LOW Threshold Bit [11:4] Register
LT_1PA01_REG_ALSPROX_ALS_INT_TLH				= 0x08 # ALS Interrupt LOW/HIGH Threshold Bit Register
LT_1PA01_REG_ALSPROX_ALS_INT_TH					= 0x09 # ALS Interrupt HIGH Threshold Bit [7:0] Register
LT_1PA01_REG_ALSPROX_PROX_DATA					= 0x0A # Proximity Data (Unsigned Binary) Register
LT_1PA01_REG_ALSPROX_ALS_DATA_HB				= 0x0B # ALS Data HIGH Byte Register
LT_1PA01_REG_ALSPROX_ALS_DATA_LB				= 0x0C # ALS Data LOW Byte Register
LT_1PA01_REG_ALSPROX_PROX_AMBIR					= 0x0D # Proximity Mode Ambient IR Measurement Register
LT_1PA01_REG_ALSPROX_CONFIG3					= 0x0E # Software Reset Register

# LT_1PA01 Proximity Configuration Register
LT_1PA01_REG_CONFIG0_PROX_EN_DISABLE            = 0x00 # Proximity Disable
LT_1PA01_REG_CONFIG0_PROX_EN_ENABLE				= 0x20 # Proximity Enable

LT_1PA01_REG_CONFIG0_PROX_SLP_800MS             = 0x00 # Proximity Sleep Time: 800ms
LT_1PA01_REG_CONFIG0_PROX_SLP_200MS             = 0x04 # Proximity Sleep Time: 200ms
LT_1PA01_REG_CONFIG0_PROX_SLP_100MS             = 0x08 # Proximity Sleep Time: 100ms

LT_1PA01_REG_CONFIG0_IRDR_DRV_3_6MA             = 0x00 # IRDR (VCSEL) Current: 3.6 mA
LT_1PA01_REG_CONFIG0_IRDR_DRV_7_2MA             = 0x01 # IRDR (VCSEL) Current: 7.2 mA
LT_1PA01_REG_CONFIG0_IRDR_DRV_10_8MA            = 0x02 # IRDR (VCSEL) Current: 10.8 mA
LT_1PA01_REG_CONFIG0_IRDR_DRV_14_4MA            = 0x03 # IRDR (VCSEL) Current: 14.4 mA

# LT_1PA01 Proximity/ALS Configuration Register
LT_1PA01_REG_CONFIG1_INT_ALG_HYST               = 0x00 # Hysteresis Window
LT_1PA01_REG_CONFIG1_INT_ALG_WINDOW             = 0x80 # Window Comparator

LT_1PA01_REG_CONFIG1_PROX_OFFSET_DISABLE        = 0x00 # Proximity Offset Compensation Disable
LT_1PA01_REG_CONFIG1_PROX_OFFSET_ENABLE         = 0x78 # Proximity Offset Compensation Enable

LT_1PA01_REG_CONFIG1_ALS_EN_DISABLE             = 0x00 # Ambient Light Sensing Disable
LT_1PA01_REG_CONFIG1_ALS_EN_ENABLE              = 0x04 # Ambient Light Sensing Enable

LT_1PA01_REG_CONFIG1_ALS_RANGE_62_5LX           = 0x00 # 62.5 Lux
LT_1PA01_REG_CONFIG1_ALS_RANGE_125LX            = 0x01 # 125 Lux
LT_1PA01_REG_CONFIG1_ALS_RANGE_1000LX           = 0x02 # 1000 Lux
LT_1PA01_REG_CONFIG1_ALS_RANGE_2000LX           = 0x03 # 2000 Lux

class LT_1PA01():
	def __init__(self):
		self.config_selection()

	
	def config_selection(self):
		"""Select the Proximity Configuration register configuration from the given provided values"""
		CONFIG0 = (LT_1PA01_REG_CONFIG0_PROX_EN_ENABLE | LT_1PA01_REG_CONFIG0_PROX_SLP_800MS | LT_1PA01_REG_CONFIG0_IRDR_DRV_3_6MA)
		bus.write_byte_data(LT_1PA01_DEFAULT_ADDRESS, LT_1PA01_REG_ALSPROX_CONFIG0, CONFIG0)
		
		"""Select the Proximity/ALS Configuration register configuration from the given provided values"""
        	CONFIG1 = (LT_1PA01_REG_CONFIG1_INT_ALG_HYST | LT_1PA01_REG_CONFIG1_PROX_OFFSET_DISABLE | LT_1PA01_REG_CONFIG1_ALS_EN_ENABLE | LT_1PA01_REG_CONFIG1_ALS_RANGE_2000LX)
        	bus.write_byte_data(LT_1PA01_DEFAULT_ADDRESS, LT_1PA01_REG_ALSPROX_CONFIG1, CONFIG1)

	def readluminance(self):
		"""Read data back from LT_1PA01_REG_ALSPROX_PROX_DATA(0x0A), 3 bytes, Proximity, ALS MSB, ALS LSB"""
		data = bus.read_i2c_block_data(LT_1PA01_DEFAULT_ADDRESS, LT_1PA01_REG_ALSPROX_PROX_DATA, 3)
		
		# Convert the data
        	# Convert the data
        	proximity = data[0]
        	luminance = data[1] * 256 + data[2]
		
		return {'l' : luminance, 'p' : proximity}

from LT_1PA01 import LT_1PA01
lt_1pa01 = LT_1PA01()

while True:
	lum = lt_1pa01.readluminance()
	print "Ambient Light Luminance : %.2f lux"%(lum['l'])
	print "Proximity of the Device : %d " %(lum['p'])
	print " ************************************************ "
	time.sleep(1)
