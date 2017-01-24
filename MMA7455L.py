# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MMA7455L
# This code is designed to work with the MMA7455L_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Accelorometer?sku=MMA7455L_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
MMA7455L_DEFAULT_ADDRESS			= 0x1D

# MMA7455L Register Map
MMA7455L_XOUTL						= 0x00 # Output Value X LSB
MMA7455L_XOUTH						= 0x01 # Output Value X MSB
MMA7455L_YOUTL						= 0x02 # Output Value Y LSB
MMA7455L_YOUTH						= 0x03 # Output Value Y MSB
MMA7455L_ZOUTL						= 0x04 # Output Value Z LSB
MMA7455L_ZOUTH						= 0x05 # Output Value Z MSB
MMA7455L_XOUT8						= 0x06 # Output Value X 8 bits
MMA7455L_YOUT8						= 0x07 # Output Value Y 8 bits
MMA7455L_ZOUT8						= 0x08 # Output Value Z 8 bits
MMA7455L_STATUS						= 0x09 # Status Register
MMA7455L_DETSRC						= 0x0A # Detection Source Register
MMA7455L_TOUT						= 0x0B # Temperature Output Value (Optional)
MMA7455L_I2CAD						= 0x0D # I2C Device Address
MMA7455L_USRINF						= 0x0E # User Information (Optional)
MMA7455L_WHOAMI						= 0x0F # "Who am I" value (Optional)
MMA7455L_XOFFL						= 0x10 # Offset Drift X LSB
MMA7455L_XOFFH						= 0x11 # Offset Drift X MSB
MMA7455L_YOFFL						= 0x12 # Offset Drift Y LSB
MMA7455L_YOFFH						= 0x13 # Offset Drift Y MSB
MMA7455L_ZOFFL						= 0x14 # Offset Drift Z LSB
MMA7455L_ZOFFH						= 0x15 # Offset Drift Z MSB
MMA7455L_MCTL						= 0x16 # Mode Control Register
MMA7455L_INTRST						= 0x17 # Interrupt Latch Reset
MMA7455L_CTL1						= 0x18 # Control 1 Register
MMA7455L_CTL2						= 0x19 # Control 2 Register
MMA7455L_LDTH						= 0x1A # Level Detection Threshold Limit Value
MMA7455L_PDTH						= 0x1B # Pulse Detection Threshold Limit Value
MMA7455L_PD							= 0x1C # Pulse Duration Value
MMA7455L_LT							= 0x1D # Latency Time Value (between pulses)
MMA7455L_TW							= 0x1E # Time Window for Second Pulse Value

# MMA7455L Status Register
MMA7455L_STATUS_DRDY_R				= 0x01 # Data is ready
MMA7455L_STATUS_DRDY_NR				= 0x00 # Data is not ready
MMA7455L_STATUS_DOVR_W				= 0x02 # Data is over written
MMA7455L_STATUS_DOVR_NW				= 0x00 # Data is not over written
MMA7455L_STATUS_PERR_D				= 0x04 # Parity error is detected in trim data
MMA7455L_STATUS_PERR_ND				= 0x00 # Parity error is not detected in trim data

# MMA7455L Mode Control Register
MMA7455L_MCTL_MODE_STANDBY			= 0x00 # Standby Mode
MMA7455L_MCTL_MODE_MEASUREMENT		= 0x01 # Measurement Mode
MMA7455L_MCTL_MODE_LEVEL			= 0x02 # Level Detection Mode
MMA7455L_MCTL_MODE_PULSE			= 0x03 # Pulse Detection Mode
MMA7455L_MCTL_GLVL_8				= 0x00 # 8g is selected for measurement range
MMA7455L_MCTL_GLVL_4				= 0x08 # 4g is selected for measurement range
MMA7455L_MCTL_GLVL_2				= 0x04 # 2g is selected for measurement range
MMA7455L_MCTL_STON_EN				= 0x10 # Self-Test enabled
MMA7455L_MCTL_STON_DS				= 0x00 # Self-Test is not enabled
MMA7455L_MCTL_SPI_3W				= 0x20 # SPI is 3 wire mode
MMA7455L_MCTL_SPI_4W				= 0x00 # SPI is 4 wire mode
MMA7455L_MCTL_DRPD_O				= 0x00 # Data ready status is output to INT1/DRDY PIN
MMA7455L_MCTL_DRPD_NO				= 0x40 # Data ready status is not output to INT1/DRDY PIN

class MMA7455L():
	def __init__(self):
		self.mode_configuration()
	
	def mode_configuration(self):
		"""Select the mode control register of the accelerometer from the given provided values"""
		MODE_CONTROL = (MMA7455L_MCTL_MODE_MEASUREMENT | MMA7455L_MCTL_GLVL_8 | MMA7455L_MCTL_STON_DS | MMA7455L_MCTL_SPI_4W | MMA7455L_MCTL_DRPD_O)
		bus.write_byte_data(MMA7455L_DEFAULT_ADDRESS, MMA7455L_MCTL, MODE_CONTROL)
	
	def read_accl(self):
		"""Read data back from MMA7455L_XOUTL(0x00), 6 bytes
		X-Axis LSB, X-Axis MSB, Y-Axis LSB, Y-Axis MSB, Z-Axis LSB, Z-Axis MSB"""
		data = bus.read_i2c_block_data(MMA7455L_DEFAULT_ADDRESS, MMA7455L_XOUTL, 6)
		
		# Convert the data to 10-bits
		xAccl = (data[1] & 0x03) * 256 + data [0]
		if xAccl > 511 :
			xAccl -= 1024
		
		yAccl = (data[3] & 0x03) * 256 + data [2]
		if yAccl > 511 :
			yAccl -= 1024
		
		zAccl = (data[5] & 0x03) * 256 + data [4]
		if zAccl > 511 :
			zAccl -= 1024
		
		return {'x' : xAccl, 'y' : yAccl, 'z' : zAccl}

from MMA7455L import MMA7455L
mma7455l = MMA7455L()

while True :
	mma7455l.mode_configuration()
	time.sleep(0.3)
	accl = mma7455l.read_accl()
	print "Acceleration in X-Axis : %d"%(accl['x'])
	print "Acceleration in Y-Axis : %d"%(accl['y'])
	print "Acceleration in Z-Axis : %d"%(accl['z'])
	print " ************************************* "
	time.sleep(1)
