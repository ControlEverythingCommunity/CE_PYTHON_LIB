# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# VCNL4010
# This code is designed to work with the VCNL4010_REG_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Light?sku=VCNL4010_REG_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
VCNL4010_DEFAULT_ADDRESS				= 0x13

# VCNL4010 Register Map
VCNL4010_REG_COMMAND					= 0x80 # COMMAND REGISTER
VCNL4010_REG_PRODUCTID					= 0x81 # PRODUCT ID REVISION REGISTER
VCNL4010_REG_PROXRATE					= 0x82 # PROXIMITY RATE REGISTER
VCNL4010_REG_IRLED						= 0x83 # IR LED CURRENT REGISTER
VCNL4010_REG_AMBIENTPARAMETER			= 0x84 # AMBIENT LIGHT PARAMETER REGISTER
VCNL4010_REG_AMBIENTDATA				= 0x85 # AMBIENT LIGHT RESULT REGISTER
VCNL4010_REG_PROXIMITYDATA				= 0x87 # PROXIMITY RESULT REGISTER 
VCNL4010_REG_INTCONTROL					= 0x89 # INTERRUPT CONTROL REGISTER
VCNL4010_REG_INTSTAT					= 0x8E # INTERRUPT STATUS REGISTER
VCNL4010_REG_MODTIMING					= 0x8F # PROXIMITY MODULATOR TIMING ADJUSTMENT

# VCNL4010 Command Register
VCNL4010_DEFAULT						= 0xE0 # Read only bit-7, 6, 5, Default Value = 1
VCNL4010_CMD_ALS_OD						= 0x10 # Starts a single on-demand measurement for ambient light
VCNL4010_CMD_PROX_OD					= 0x08 # Starts a single on-demand measurement for proximity
VCNL4010_CMD_ALS_EN						= 0x04 # Enables periodic als measurement
VCNL4010_CMD_PROX_EN					= 0x02 # Enables periodic proximity measurement
VCNL4010_CMD_SELFTIMED_EN				= 0x01 # Enables state machine and LP oscillator for self timed measurements

# VCNL4010 Proximity Rate Register
VCNL4010_PROX_RATE_1_95					= 0x00 # 1.95 measurements per sec
VCNL4010_PROX_RATE_3_90					= 0x01 # 3.90 measurements per sec
VCNL4010_PROX_RATE_7_81					= 0x02 # 7.81 measurements per sec
VCNL4010_PROX_RATE_16_625				= 0x03 # 16.625 measurements per sec
VCNL4010_PROX_RATE_31_25				= 0x04 # 31.25 measurements per sec
VCNL4010_PROX_RATE_62_5					= 0x05 # 62.5 measurements per sec
VCNL4010_PROX_RATE_125					= 0x06 # 125 measurements per sec
VCNL4010_PROX_RATE_250					= 0x07 # 250 measurements per sec

# VCNL4010 Ambient Light Parameter Register
VCNL4010_AMBI_CONT_MODE					= 0x80 # Continuous conversion mode enable
VCNL4010_AMBI_RATE_1					= 0x00 # 1 samples/s
VCNL4010_AMBI_RATE_2					= 0x10 # 2 samples/s
VCNL4010_AMBI_RATE_3					= 0x20 # 3 samples/s
VCNL4010_AMBI_RATE_4					= 0x30 # 4 samples/s
VCNL4010_AMBI_RATE_5					= 0x40 # 5 samples/s
VCNL4010_AMBI_RATE_6					= 0x50 # 6 samples/s
VCNL4010_AMBI_RATE_8					= 0x60 # 8 samples/s
VCNL4010_AMBI_RATE_10					= 0x70 # 10 samples/s
VCNL4010_AMBI_AUTO_OFFSET				= 0x08 # Automatic offset compensation enable
VCNL4010_AMBI_AVE_NUM_1					= 0x00 # Number of Single conversions = 1
VCNL4010_AMBI_AVE_NUM_2					= 0x01 # Number of Single conversions = 2
VCNL4010_AMBI_AVE_NUM_4					= 0x02 # Number of Single conversions = 4
VCNL4010_AMBI_AVE_NUM_8					= 0x03 # Number of Single conversions = 8
VCNL4010_AMBI_AVE_NUM_16				= 0x04 # Number of Single conversions = 16
VCNL4010_AMBI_AVE_NUM_32				= 0x05 # Number of Single conversions = 32
VCNL4010_AMBI_AVE_NUM_64				= 0x06 # Number of Single conversions = 64
VCNL4010_AMBI_AVE_NUM_128				= 0x07 # Number of Single conversions = 128

class VCNL4010():
	def command_register(self):
		"""Select the Command Register data from the given provided value"""
		COMMAND_REG = (VCNL4010_DEFAULT | VCNL4010_CMD_PROX_OD | VCNL4010_CMD_ALS_OD | VCNL4010_CMD_ALS_EN | VCNL4010_CMD_PROX_EN)
		bus.write_byte_data(VCNL4010_DEFAULT_ADDRESS, VCNL4010_REG_COMMAND, COMMAND_REG)
	
	def prox_rate_config(self):
		"""Select the Proximity Rate Register data from the given provided value"""
		PROX_RATE = (VCNL4010_PROX_RATE_1_95)
		bus.write_byte_data(VCNL4010_DEFAULT_ADDRESS, VCNL4010_REG_PROXRATE, PROX_RATE)
	
	def light_parameter_config(self):
		"""Select the Ambient Light Parameter Register data from the given provided value"""
		LIGHT_PARA = (VCNL4010_AMBI_CONT_MODE | VCNL4010_AMBI_RATE_2 | VCNL4010_AMBI_AUTO_OFFSET | VCNL4010_AMBI_AVE_NUM_32)
		bus.write_byte_data(VCNL4010_DEFAULT_ADDRESS, VCNL4010_REG_AMBIENTPARAMETER, LIGHT_PARA)
	
	def read_prox(self):
		"""Read data back from VCNL4010_REG_AMBIENTDATA(0x85), 4 bytes
		luminance MSB, luminance LSB, Proximity MSB, Proximity LSB"""
		data = bus.read_i2c_block_data(VCNL4010_DEFAULT_ADDRESS, VCNL4010_REG_AMBIENTDATA, 4)
		
		# Convert the data
		luminance = data[0] * 256 + data[1]
		proximity = data[2] * 256 + data[3]
		
		return {'l' : luminance, 'p' : proximity}

from VCNL4010 import VCNL4010
vcnl4010 = VCNL4010()

while True :
	vcnl4010.command_register()
	vcnl4010.prox_rate_config()
	vcnl4010.light_parameter_config()
	time.sleep(0.8)
	prox = vcnl4010.read_prox()
	print "Ambient Light Luminance : %.2f lux"%(prox['l'])
	print "Proximity of the Device : %d " %(prox['p'])
	print " ******************************************** "
	time.sleep(0.2)