# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MMA7660FC
# This code is designed to work with the MMA7660FC_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Accelorometer?sku=MMA7660FC_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
MMA7660FC_DEFAULT_ADDRESS			= 0x4C

# MMA7660FC Register Map
MMA7660FC_XOUT						= 0x00 # Output Value X
MMA7660FC_YOUT						= 0x01 # Output Value Y
MMA7660FC_ZOUT						= 0x02 # Output Value Z
MMA7660FC_TILT						= 0x03 # Tilt Status
MMA7660FC_SRST						= 0x04 # Sampling Rate Status
MMA7660FC_SPCNT						= 0x05 # Sleep Count
MMA7660FC_INTSU						= 0x06 # Interrupt Status
MMA7660FC_MODE						= 0x07 # Mode Register
MMA7660FC_SR						= 0x08 # Sample Rate Register
MMA7660FC_PDET						= 0x09 # Tap/Pulse Detection Register
MMA7660FC_PD						= 0x0A # Tap/Pulse Debounce Count Register

# MMA7660FC Mode Register
MMA7660FC_MODE_STANDBY				= 0x00 # Standby Mode
MMA7660FC_MODE_TEST					= 0x04 # Test Mode
MMA7660FC_MODE_ACTIVE				= 0x01 # Active Mode
MMA7660FC_AWE_EN					= 0x08 # Auto-Wake Enabled
MMA7660FC_AWE_DS					= 0x00 # Auto-Wake Disabled
MMA7660FC_ASE_EN					= 0x10 # Auto-Sleep Enabled
MMA7660FC_ASE_DS					= 0x00 # Auto-Sleep Disabled
MMA7660FC_SCPS_16					= 0x20 # Prescaler is divide by 16
MMA7660FC_SCPS_1					= 0x00 # Prescaler is divide by 1
MMA7660FC_IPP_OPEN					= 0x00 # Interrupt output INT is open-drain
MMA7660FC_IPP_PUSH					= 0x40 # Interrupt output INT is push-pull
MMA7660FC_IAH_LOW					= 0x00 # Interrupt output INT is active low
MMA7660FC_IAH_HIGH					= 0x80 # Interrupt output INT is active high

# MMA7660FC Sample Rate Register
MMA7660FC_AMSR_120					= 0x00 # 120 Samples/Second Active and Auto-Sleep Mode
MMA7660FC_AMSR_64					= 0x01 # 64 Samples/Second Active and Auto-Sleep Mode
MMA7660FC_AMSR_32					= 0x02 # 32 Samples/Second Active and Auto-Sleep Mode
MMA7660FC_AMSR_16					= 0x03 # 16 Samples/Second Active and Auto-Sleep Mode
MMA7660FC_AMSR_8					= 0x04 # 8 Samples/Second Active and Auto-Sleep Mode
MMA7660FC_AMSR_4					= 0x05 # 4 Samples/Second Active and Auto-Sleep Mode
MMA7660FC_AMSR_2					= 0x06 # 2 Samples/Second Active and Auto-Sleep Mode
MMA7660FC_AMSR_1					= 0x07 # 1 Samples/Second Active and Auto-Sleep Mode
MMA7660FC_AWSR_32					= 0x00 # 32 Samples/Second Auto-Wake Mode
MMA7660FC_AWSR_16					= 0x08 # 16 Samples/Second Auto-Wake Mode
MMA7660FC_AWSR_8					= 0x10 # 8 Samples/Second Auto-Wake Mode
MMA7660FC_AWSR_1					= 0x18 # 1 Samples/Second Auto-Wake Mode

class MMA7660FC():
	def __init__(self):
		self.mode_config()
		self.sample_rate_config()
	
	def mode_config(self):
		"""Select the mode control register of the accelerometer from the given provided values"""
		MODE_CONTROL = (MMA7660FC_MODE_ACTIVE | MMA7660FC_AWE_DS | MMA7660FC_ASE_DS | MMA7660FC_SCPS_1 | MMA7660FC_IAH_LOW)
		bus.write_byte_data(MMA7660FC_DEFAULT_ADDRESS, MMA7660FC_MODE, MODE_CONTROL)
	
	def sample_rate_config(self):
		"""Select the sample rate register of the accelerometer from the given provided values"""
		SAMPLE_RATE = (MMA7660FC_AMSR_2)
		bus.write_byte_data(MMA7660FC_DEFAULT_ADDRESS, MMA7660FC_SR, SAMPLE_RATE)
	
	def read_accl(self):
		"""Read data back from MMA7660FC_XOUT(0x00), 3 bytes
		X-Axis Accl, Y-Axis Accl, Z-Axis Accl"""
		data = bus.read_i2c_block_data(MMA7660FC_DEFAULT_ADDRESS, MMA7660FC_XOUT, 3)
		
		# Convert the data to 6-bits
		xAccl = data[0] & 0x3F
		if xAccl > 31 :
			xAccl -= 64
		
		yAccl = data[1] & 0x3F
		if yAccl > 31 :
			yAccl -= 64
		
		zAccl = data[2] & 0x3F
		if zAccl > 31 :
			zAccl -= 64
		
		return {'x' : xAccl, 'y' : yAccl, 'z' : zAccl}

from MMA7660FC import MMA7660FC
mma7660fc = MMA7660FC()

while True :
	mma7660fc.mode_config()
	mma7660fc.sample_rate_config()
	time.sleep(0.1)
	accl = mma7660fc.read_accl()
	print "Acceleration in X-Axis : %d"%(accl['x'])
	print "Acceleration in Y-Axis : %d"%(accl['y'])
	print "Acceleration in Z-Axis : %d"%(accl['z'])
	print " ************************************* "
	time.sleep(1)
