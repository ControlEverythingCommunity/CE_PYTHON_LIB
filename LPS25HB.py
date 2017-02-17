# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# LPS25HB
# This code is designed to work with the LPS25HB_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Barometer?sku=LPS25HB_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
LPS25HB_DEFAULT_ADDRESS				= 0x5C

# LPS25HB Register Map
LPS25HB_COMMAND_BIT						= 0x80 
LPS25HB_REG_REF_PRES_LSB				= 0x08 # Reference Pressure (LSB Data)
LPS25HB_REG_REF_PRES_MIDDLE				= 0x09 # Reference Pressure (Middle Part)
LPS25HB_REG_REF_PRES_MSB				= 0x0A # Reference Pressure (MSB Data)
LPS25HB_REG_WHO_AM_I					= 0x0F # Device Identification Register
LPS25HB_REG_RES_CONFIG					= 0x10 # Pressure and Temperature Resolution
LPS25HB_REG_CTRL_REG1					= 0x20 # Barometer Control Register 1
LPS25HB_REG_CTRL_REG2					= 0x21 # Barometer Control Register 2
LPS25HB_REG_CTRL_REG3					= 0x22 # Barometer Interrupt Control Register
LPS25HB_REG_CTRL_REG4					= 0x23 # Barometer Interrupt Configuration Register
LPS25HB_REG_INTERRUPT_CFG				= 0x24 # Barometer Interrupt Configuration Register
LPS25HB_REG_INT_SOURCE					= 0x25 # Interrupt Source Register
LPS25HB_REG_STATUS						= 0x27 # Status Register
LPS25HB_REG_PRESS_OUT_XL				= 0x28 # Pressure Output Value Low Register
LPS25HB_REG_PRESS_OUT_L					= 0x29 # Pressure Output Value Mid Register
LPS25HB_REG_PRESS_OUT_H					= 0x2A # Pressure Output Value High Register
LPS25HB_REG_TEMP_OUT_L					= 0x2B # Temperature Output Value Low Register
LPS25HB_REG_TEMP_OUT_H					= 0x2C # Temperature Output Value High Register
LPS25HB_REG_FIFO_CTRL					= 0x2E # FIFO Control Register
LPS25HB_REG_FIFO_STATUS					= 0x2F # FIFO Status Register
LPS25HB_REG_THS_P_L						= 0x30 # Interrupt Pressure Low Threshold Register
LPS25HB_REG_THS_P_H						= 0x31 # Interrupt Pressure High Threshold Register
LPS25HB_REG_RPDS_L						= 0x39 # Pressure Offset Low Register
LPS25HB_REG_RPDS_H						= 0x3A # Pressure Offset High Register

# LPS25HB Pressure and Temperature Resolution Configuration
LPS25HB_RES_CONF_TEMP_8					= 0x00 # Nr. Internal Average: 8
LPS25HB_RES_CONF_TEMP_16				= 0x04 # Nr. Internal Average: 16
LPS25HB_RES_CONF_TEMP_32				= 0x08 # Nr. Internal Average: 32
LPS25HB_RES_CONF_TEMP_64				= 0x0C # Nr. Internal Average: 64
LPS25HB_RES_CONF_PRES_8					= 0x00 # Nr. Internal Average: 8
LPS25HB_RES_CONF_PRES_32				= 0x01 # Nr. Internal Average: 32
LPS25HB_RES_CONF_PRES_128				= 0x02 # Nr. Internal Average: 128
LPS25HB_RES_CONF_PRES_512				= 0x03 # Nr. Internal Average: 512

# LPS25HB Control Register-1 Configuration
LPS25HB_CTRL_REG1_PD_DOWN				= 0x00 # Power-Down Mode
LPS25HB_CTRL_REG1_PD_ACTIVE				= 0x80 # Active Mode
LPS25HB_CTRL_REG1_ODR_ONE_SHOT			= 0x00 # One-Shot Mode Enabled
LPS25HB_CTRL_REG1_ODR_1HZ				= 0x10 # Pressure (Hz): 1, Temperature (Hz): 1
LPS25HB_CTRL_REG1_ODR_7HZ				= 0x20 # Pressure (Hz): 7, Temperature (Hz): 7
LPS25HB_CTRL_REG1_ODR_12_5HZ			= 0x30 # Pressure (Hz): 12.5, Temperature (Hz): 12.5
LPS25HB_CTRL_REG1_ODR_25HZ				= 0x40 # Pressure (Hz): 25, Temperature (Hz): 25
LPS25HB_CTRL_REG1_DIFF_EN_DISABLE		= 0x00 # Interrupt Generation Disabled
LPS25HB_CTRL_REG1_DIFF_EN_ENABLE		= 0x08 # Interrupt Generation Enabled
LPS25HB_CTRL_REG1_BDU_CONTINUOUS		= 0x00 # Continuous Update
LPS25HB_CTRL_REG1_BDU_NOTUPDATE			= 0x04 # Output Registers Not Updated until MSB and LSB Read
LPS25HB_CTRL_REG1_RESET_AZ_NORMAL		= 0x00 # Normal Mode
LPS25HB_CTRL_REG1_RESET_AZ_RESET		= 0x02 # Reset Autozero Function
LPS25HB_CTRL_REG1_SIM_4WIRE				= 0x00 # 4-Wire Interface
LPS25HB_CTRL_REG1_SIM_3WIRE				= 0x01 # 3-Wire Interface

class LPS25HB():
	def __init__(self):
		self.resolution_config()
		self.datarate_config()
	
	def resolution_config(self):
		"""Select the Pressure and Temperature Resolution Configuration from the given provided value"""
		RESO_CONFIG = (LPS25HB_RES_CONF_TEMP_8 | LPS25HB_RES_CONF_PRES_8)
		bus.write_byte_data(LPS25HB_DEFAULT_ADDRESS, LPS25HB_REG_RES_CONFIG, RESO_CONFIG)
	
	def datarate_config(self):
		"""Select the Control Register-1 Configuration from the given provided value"""
		DATARATE_CONFIG = (LPS25HB_CTRL_REG1_PD_ACTIVE | LPS25HB_CTRL_REG1_ODR_1HZ | LPS25HB_CTRL_REG1_BDU_CONTINUOUS | LPS25HB_CTRL_REG1_RESET_AZ_NORMAL)
		bus.write_byte_data(LPS25HB_DEFAULT_ADDRESS, LPS25HB_REG_CTRL_REG1, DATARATE_CONFIG)
	
	def read_pres(self):
		"""Read data back from LPS25HB_REG_PRESS_OUT_XL(0x28), with LPS25HB_COMMAND_BIT,(0x80), 3 bytes
		pressure LSB, pressure CSB, pressure MSB"""
		data = bus.read_i2c_block_data(LPS25HB_DEFAULT_ADDRESS, LPS25HB_REG_PRESS_OUT_XL | LPS25HB_COMMAND_BIT, 3)
		
		# Convert the data
		pressure = ((data[2] * 65536) + (data[1] * 256) + data[0]) / 4096.0
		mbar = pressure
		mmHg = pressure * 0.75
		
		return {'p' : pressure, 'm' : mbar, 'h' : mmHg}

from LPS25HB import LPS25HB
lps25hb = LPS25HB()

while True :
	pres = lps25hb.read_pres()
	print "Pressure in hPa : %.2f"%(pres['p'])
	print "Pressure in mbar : %.2f"%(pres['m'])
	print "Pressure in mmHg : %.2f"%(pres['h'])
	print " ***************************************** "
	time.sleep(1)
