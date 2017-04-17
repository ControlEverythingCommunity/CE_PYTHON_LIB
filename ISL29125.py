# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# ISL29125
# This code is designed to work with the ISL29125_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/products

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
ISL29125_DEFAULT_ADDRESS			= 0x44

# Register Map
ISL29125_REG_DEV_ID                 = 0x00
ISL29125_REG_CONFIG_1               = 0x01
ISL29125_REG_CONFIG_2               = 0x02
ISL29125_REG_CONFIG_3               = 0x03
ISL29125_REG_THRESHOLD_LL           = 0x04
ISL29125_REG_THRESHOLD_LH           = 0x05
ISL29125_REG_THRESHOLD_HL           = 0x06
ISL29125_REG_THRESHOLD_HH           = 0x07
ISL29125_REG_STATUS                 = 0x08
ISL29125_REG_GREEN_LOW              = 0x09
ISL29125_REG_GREEN_HIGH             = 0x0A
ISL29125_REG_RED_LOW                = 0x0B
ISL29125_REG_RED_HIGH               = 0x0C
ISL29125_REG_BLUE_LOW               = 0x0E
ISL29125_REG_BLUE_HIGH              = 0x0F

# Configuration Register 1
ISL29125_REG_CONFIG1_BITS_16        = 0x00  # 16 Bits
ISL29125_REG_CONFIG1_BITS_12        = 0x10  # 12 Bits
ISL29125_REG_CONFIG1_RNG_375LUX     = 0x00  # 375 lux
ISL29125_REG_CONFIG1_RNG_10KLUX     = 0x08  # 10,000 lux
ISL29125_REG_CONFIG1_MODE_POWERDOWN = 0x00  # Power Down (ADC conversion)
ISL29125_REG_CONFIG1_MODE_G         = 0x01  # GREEN Only
ISL29125_REG_CONFIG1_MODE_R         = 0x02  # RED Only
ISL29125_REG_CONFIG1_MODE_B         = 0x03  # BLUE Only
ISL29125_REG_CONFIG1_MODE_STANDBY   = 0x04  # Stand by (No ADC conversion)
ISL29125_REG_CONFIG1_MODE_RGB       = 0x05  # GREEN/RED/BLUE
ISL29125_REG_CONFIG1_MODE_RG        = 0x06  # GREEN/RED
ISL29125_REG_CONFIG1_MODE_GB        = 0x07  # GREEN/BLUE

# Configuration Register 2
ISL29125_REG_CONFIG2_IR_OFFSET_OFF  = 0x00  # INT pin Sets to Normal Mode
ISL29125_REG_CONFIG2_IR_OFFSET_ON   = 0x80  # INT pin Sets to Interrupt Mode
ISL29125_REG_CONFIG2_IR_ADJUST_LOW  = 0x00  # Low Amount of IR Filtering
ISL29125_REG_CONFIG2_IR_ADJUST_MID  = 0x20  # Medium Amount of IR Filtering
ISL29125_REG_CONFIG2_IR_ADJUST_HIGH = 0x3F  # High Amount of IR Filtering

# Configuration Register 3
ISL29125_REG_CONFIG3_CONVEN_DISABLE = 0x00  # Disable
ISL29125_REG_CONFIG3_CONVEN_ENABLE  = 0x10  # Enable
ISL29125_REG_CONFIG3_PRST_1         = 0x00  # No. of Integration Cycle: 1
ISL29125_REG_CONFIG3_PRST_2         = 0x04  # No. of Integration Cycles: 2
ISL29125_REG_CONFIG3_PRST_4         = 0x08  # No. of Integration Cycles: 4
ISL29125_REG_CONFIG3_PRST_8         = 0x0C  # No. of Integration Cycles: 8
ISL29125_REG_CONFIG3_INTSEL_NO_INT  = 0x00  # No Interrupt
ISL29125_REG_CONFIG3_INTSEL_G_INT   = 0x01  # GREEN Interrupt
ISL29125_REG_CONFIG3_INTSEL_R_INT   = 0x02  # RED Interrupt
ISL29125_REG_CONFIG3_INTSEL_B_INT   = 0x03  # BLUE Interrupt


class ISL29125():
	def __init__(self):
		self.color_command()
	
	def color_command(self):
		"""Set the Configuration for the Configuration Register 1 from the given provided values"""
		bus.write_byte_data(ISL29125_DEFAULT_ADDRESS, ISL29125_REG_CONFIG_1, ISL29125_REG_CONFIG1_SYNC_NORMAL| ISL29125_REG_CONFIG1_BITS_16 | ISL29125_REG_CONFIG1_RNG_10KLUX | ISL29125_REG_CONFIG1_MODE_RGB)
    
        """Set the Configuration for the Configuration Register 2 from the given provided values"""
        bus.write_byte_data(ISL29125_DEFAULT_ADDRESS, ISL29125_REG_CONFIG_2, ISL29125_REG_CONFIG2_IR_OFFSET_OFF| ISL29125_REG_CONFIG2_IR_ADJUST_LOW)
        
        """Set the Configuration for the Configuration Register 3 from the given provided values"""
        bus.write_byte_data(ISL29125_DEFAULT_ADDRESS, ISL29125_REG_CONFIG_3, ISL29125_REG_CONFIG3_CONVEN_ENABLE| ISL29125_REG_CONFIG3_PRST_1 | ISL29125_REG_CONFIG3_INTSEL_NO_INT)
	
	def read_color(self):
		"""Read data back from the device address, 6 bytes, green LSB, green MSB, red LSB, red MSB, blue LSB, blue MSB"""
		data = bus.read_i2c_block_data(ISL29125_DEFAULT_ADDRESS, ISL29125_REG_GREEN_LOW, 6)
		
		# Convert the data
		green = data[1] * 256 + data[0]
        red = data[3] * 256 + data[2]
        blue = data[5] * 256 + data[4]
		
		return {'g' : green, 'r' : red, 'b' : blue}

from ISL29125 import ISL29125
isl29125 = ISL29125()

while True:
	time.sleep(0.3)
	isl29125.color_command()
	time.sleep(0.3)
	lum = isl29125.read_color()
    print "Green Color Luminance : %d "%(lum['g'])
    print "Red Color Luminance : %d "%(lum['r'])
    print "Blue Color Luminance : %d "%(lum['b'])
	print " ******************************************* "
	time.sleep(0.5)
