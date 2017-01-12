# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# ISL29003
# This code is designed to work with the ISL29003_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Light?sku=ISL29003_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
ISL29003_DEFAULT_ADDRESS			= 0x44

# ISL29003 Register Set
ISL29003_REG_COMMAND					= 0x00 # Command Register
ISL29003_REG_CONTROL					= 0x01 # Control Register
ISL29003_REG_INTR_TH_HI					= 0x02 # Interrupt Threshold HI
ISL29003_REG_INTR_TH_LO					= 0x03 # Interrupt Threshold LO
ISL29003_REG_SENSOR_LSB					= 0x04 # LSB_Sensor
ISL29003_REG_SENSOR_MSB					= 0x05 # MSB_Sensor
ISL29003_REG_TIMER_LSB					= 0x06 # LSB_Timer
ISL29003_REG_TIMER_MSB					= 0x07 # MSB_Timer

# ISL29003 Command Register Configuration
ISL29003_REG_CMND_ADC_DISABLE			= 0x00 # Disable ADC-Core
ISL29003_REG_CMND_ADC_ENABLE			= 0x80 # Enable ADC-Core
ISL29003_REG_CMND_ADCPD_NORMAL			= 0x00 # Normal Operation
ISL29003_REG_CMND_ADCPD_PDOWN			= 0x40 # Power-Down Mode
ISL29003_REG_CMND_TMODE_INT				= 0x00 # Integration is Internally Timed
ISL29003_REG_CMND_TMODE_EXT				= 0x20 # Integration is externally sync/controlled by I2C host
ISL29003_REG_CMND_ADCMODE_DIODE1		= 0x00 # Diode-1's current to unsigned 16-bit data
ISL29003_REG_CMND_ADCMODE_DIODE2		= 0x04 # Diode-2's current to unsigned 16-bit data
ISL29003_REG_CMND_ADCMODE_DIFF			= 0x08 # Difference between diodes (I1 - I2) to signed 15-bit data
ISL29003_REG_CMND_RES_16				= 0x00 # 16-bit Resolution
ISL29003_REG_CMND_RES_12				= 0x01 # 12-bit Resolution
ISL29003_REG_CMND_RES_8					= 0x02 # 8-bit Resolution
ISL29003_REG_CMND_RES_4					= 0x03 # 4-bit Resolution

# ISL29003 Control Register Configuration
ISL29003_REG_CONTROL_INTRFLAG_NOTRIG	= 0x00 # Interrupt is cleared or not yet Triggered
ISL29003_REG_CONTROL_INTRFLAG_TRIG		= 0x20 # Interrupt is Triggered
ISL29003_REG_CONTROL_GAIN_0_1K			= 0x00 # 0 to 1000 lux
ISL29003_REG_CONTROL_GAIN_0_4K			= 0x04 # 0 to 4000 lux
ISL29003_REG_CONTROL_GAIN_0_16K			= 0x08 # 0 to 16000 lux
ISL29003_REG_CONTROL_GAIN_0_64K			= 0x0C # 0 to 64000 lux
ISL29003_REG_CONTROL_INTRCYCLE_1		= 0x00 # 1 Integration Cycle
ISL29003_REG_CONTROL_INTRCYCLE_4		= 0x01 # 4 Integration Cycles
ISL29003_REG_CONTROL_INTRCYCLE_8		= 0x02 # 8 Integration Cycles
ISL29003_REG_CONTROL_INTRCYCLE_16		= 0x03 # 16 Integration Cycles

class ISL29003():
	def __init__(self):
		self.write_command()
		time.sleep(0.5)
		self.write_control()
	
	def write_command(self):
		"""Select the command register configuration from the given provided values"""
		COMMAND_CONFIG = (ISL29003_REG_CMND_ADC_ENABLE | ISL29003_REG_CMND_ADCPD_NORMAL | ISL29003_REG_CMND_RES_16)
		bus.write_byte_data(ISL29003_DEFAULT_ADDRESS, ISL29003_REG_COMMAND, COMMAND_CONFIG)
	
	def write_control(self):
		"""Select the control register configuration from the given provided values"""
		CONTROL_CONFIG = (ISL29003_REG_CONTROL_INTRFLAG_NOTRIG | ISL29003_REG_CONTROL_GAIN_0_64K | ISL29003_REG_CONTROL_INTRCYCLE_1)
		bus.write_byte_data(ISL29003_DEFAULT_ADDRESS, ISL29003_REG_CONTROL, CONTROL_CONFIG)
	
	time.sleep(0.5)
	
	def read_luminance(self):
		"""Read data back from ISL29003_REG_SENSOR_LSB(0x04), 2 bytes, luminance LSB, luminance MSB"""
		data = bus.read_i2c_block_data(ISL29003_DEFAULT_ADDRESS, ISL29003_REG_SENSOR_LSB, 2)
		
		# Convert the data
		luminance = data[1] * 256 + data[0]
		
		return {'l' : luminance}

from ISL29003 import ISL29003
isl29003 = ISL29003()

while True:
	lum = isl29003.read_luminance()
	print "Ambient Light luminance : %d lux" %(lum['l'])
	print " ***************************************** "
	time.sleep(0.5)
