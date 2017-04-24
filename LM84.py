# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# LM84
# This code is designed to work with the LM84_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/products

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
LM84_DEFAULT_ADDRESS                = 0x18

# LM84 Register Map
LM84_REG_COMMAND_RLT                = 0x00 # Read Local Temperature
LM84_REG_COMMAND_RRT                = 0x01 # Read Remote Temperature
LM84_REG_COMMAND_RS                 = 0x02 # Read Status
LM84_REG_COMMAND_RC                 = 0x03 # Read Configuration
LM84_REG_COMMAND_RMID               = 0x04 # Manufacturers ID
LM84_REG_COMMAND_RLCS               = 0x05 # Read Local T_CRIT Setpoint
LM84_REG_COMMAND_RRCS               = 0x07 # Read Remote T_CRIT Setpoint
LM84_REG_COMMAND_WC                 = 0x09 # Write Configuration
LM84_REG_COMMAND_WLCS               = 0x0B # Write Local T_CRIT Setpoint
LM84_REG_COMMAND_WRCS               = 0x0D # Write Remote T_CRIT Setpoint

# LM84 Configuration Register
LM84_REG_COMMAND_WC_T_CRIT_A_0      = 0x00 # T_CRIT_A Interrupts are not Masked
LM84_REG_COMMAND_WC_T_CRIT_A_1      = 0x80 # T_CRIT_A Interrupts are Masked


class LM84():
	def __init__(self):
		self.temp_configuration()
	
	def temp_configuration(self):
		"""Select the temperature configuration from the given provided values"""
		TEMP_CONFIG = (LM84_REG_COMMAND_WC_T_CRIT_A_1)
		bus.write_byte_data(LM84_DEFAULT_ADDRESS, LM84_REG_COMMAND_WC, TEMP_CONFIG)
	
	def read_temp(self):
		"""Read data back from LM84_REG_COMMAND_RLT(0x00), 1 byte, local temp data"""
		data = bus.read_i2c_block_data(LM84_DEFAULT_ADDRESS, LM84_REG_COMMAND_RLT, 1)
		
		# Convert the data
		local_temp = data[0]
		if local_temp > 127 :
			local_temp -= 256
		local_cTemp = local_temp
		local_fTemp = local_cTemp * 1.8 + 32
            
        """Read data back from LM84_REG_COMMAND_RRT(0x01), 1 byte, remote temp data"""
        data = bus.read_i2c_block_data(LM84_DEFAULT_ADDRESS, LM84_REG_COMMAND_RRT, 1)
                
        # Convert the data
        remote_temp = data[0]
        if remote_temp > 127 :
            remote_temp -= 256
        remote_cTemp = remote_temp
        remote_fTemp = remote_cTemp * 1.8 + 32
                
        return {'lc' : local_cTemp, 'lf' : local_fTemp, 'rc' : remote_cTemp, 'rf' : remote_fTemp}

from LM84 import LM84
lm84 = LM84()

while True:
	temp = lm84.read_temp()
	print "Local Temperature in Celsius : %.2f C"%(temp['lc'])
	print "Local Temperature in Fahrenheit : %.2f F"%(temp['lf'])
    print "Remote Temperature in Celsius : %.2f C"%(temp['rc'])
    print "Remote Temperature in Fahrenheit : %.2f F"%(temp['rf'])
	print " ***************************************** "
	time.sleep(1)
