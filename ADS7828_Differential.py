# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# ADS7828
# This code is designed to work with the ADS7828_I2CADC_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Analog-Digital-Converters?sku=ADS7828_I2CADC#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
ADS7828_DEFAULT_ADDRESS				= 0x48

# ADS7828 Command Set
ADS7828_CMD_SD_DIFF					= 0x00 # Differential Inputs
ADS7828_CMD_SD_SINGLE				= 0x80 # Single-Ended Inputs
ADS7828_CMD_DIFF_CHANNEL_0_1		= 0x00 # +IN = CH0, -IN = CH1
ADS7828_CMD_DIFF_CHANNEL_2_3		= 0x10 # +IN = CH2, -IN = CH3
ADS7828_CMD_DIFF_CHANNEL_4_5		= 0x20 # +IN = CH4, -IN = CH5
ADS7828_CMD_DIFF_CHANNEL_6_7		= 0x30 # +IN = CH6, -IN = CH7
ADS7828_CMD_DIFF_CHANNEL_1_0		= 0x40 # +IN = CH1, -IN = CH0
ADS7828_CMD_DIFF_CHANNEL_3_2		= 0x50 # +IN = CH3, -IN = CH2
ADS7828_CMD_DIFF_CHANNEL_5_4		= 0x60 # +IN = CH5, -IN = CH4
ADS7828_CMD_DIFF_CHANNEL_7_6		= 0x70 # +IN = CH7, -IN = CH6
ADS7828_CMD_SNGL_CHANNEL_0			= 0x00 # +IN = CH0, -IN = GND
ADS7828_CMD_SNGL_CHANNEL_1			= 0x10 # +IN = CH1, -IN = GND
ADS7828_CMD_SNGL_CHANNEL_2			= 0x20 # +IN = CH2, -IN = GND
ADS7828_CMD_SNGL_CHANNEL_3			= 0x30 # +IN = CH3, -IN = GND
ADS7828_CMD_SNGL_CHANNEL_4			= 0x40 # +IN = CH4, -IN = GND
ADS7828_CMD_SNGL_CHANNEL_5			= 0x50 # +IN = CH5, -IN = GND
ADS7828_CMD_SNGL_CHANNEL_6			= 0x60 # +IN = CH6, -IN = GND
ADS7828_CMD_SNGL_CHANNEL_7			= 0x70 # +IN = CH7, -IN = GND
ADS7828_CMD_PD_POWER_DOWN			= 0x00 # Power Down Between A/D Converter Conversions
ADS7828_CMD_PD_REF_OFF				= 0x04 # Internal Reference OFF and A/D Converter ON
ADS7828_CMD_PD_REF_ON				= 0x08 # Internal Reference ON and A/D Converter OFF
ADS7828_CMD_PD_REF_ON_AD_ON			= 0x0C # Internal Reference ON and A/D Converter ON

class ADS7828():
	def set_channel(self):
		"""Select the Channel (Differential) user want to use from 0-7
		0 : +IN = CH0, -IN = CH1
		1 : +IN = CH2, -IN = CH3
		2 : +IN = CH4, -IN = CH5
		3 : +IN = CH6, -IN = CH7
		4 : +IN = CH1, -IN = CH0
		5 : +IN = CH3, -IN = CH2
		6 : +IN = CH5, -IN = CH4
		7 : +IN = CH7, -IN = CH6"""
		self.channel = int(input("Enter the Channel No. = "))
		while self.channel > 7 :
			self.channel = int(input("Enter the Channel No. = "))
		
		return self.channel
	
	def set_command(self):
		"""Select the Command data from the given provided value above"""
		if self.channel == 0:
			COMMAND_SET = (ADS7828_CMD_SD_DIFF | ADS7828_CMD_DIFF_CHANNEL_0_1)
		elif self.channel == 1:
			COMMAND_SET = (ADS7828_CMD_SD_DIFF | ADS7828_CMD_DIFF_CHANNEL_2_3)
		elif self.channel == 2:
			COMMAND_SET = (ADS7828_CMD_SD_DIFF | ADS7828_CMD_DIFF_CHANNEL_4_5)
		elif self.channel == 3:
			COMMAND_SET = (ADS7828_CMD_SD_DIFF | ADS7828_CMD_DIFF_CHANNEL_6_7)
		elif self.channel == 4:
			COMMAND_SET = (ADS7828_CMD_SD_DIFF | ADS7828_CMD_DIFF_CHANNEL_1_0)
		elif self.channel == 5:
			COMMAND_SET = (ADS7828_CMD_SD_DIFF | ADS7828_CMD_DIFF_CHANNEL_3_2)
		elif self.channel == 6:
			COMMAND_SET = (ADS7828_CMD_SD_DIFF | ADS7828_CMD_DIFF_CHANNEL_5_4)
		elif self.channel == 7:
			COMMAND_SET = (ADS7828_CMD_SD_DIFF | ADS7828_CMD_DIFF_CHANNEL_7_6)
		
		bus.write_byte(ADS7828_DEFAULT_ADDRESS, COMMAND_SET)
	
	def read_adc(self):
		"""Read data back from the device address, 1 byte"""
		
		data = bus.read_byte(ADS7828_DEFAULT_ADDRESS)
		
		raw_adc = data
		
		return {'r' : raw_adc}

from ADS7828_Differential import ADS7828
ads7828 = ADS7828()

while True :
	ads7828.set_channel()
	ads7828.set_command()
	time.sleep(0.1)
	adc = ads7828.read_adc()
	print "Digital Value of Analog Input : %d "%(adc['r'])
	print " ************************************************** "
	time.sleep(0.8)
