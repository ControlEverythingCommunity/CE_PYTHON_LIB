# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# ITG3200
# This code is designed to work with the ITG-3200_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Gyro?sku=ITG-3200_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
ITG3200_DEFAULT_ADDRESS				= 0x68

# ITG3200 Register Map
ITG3200_WHO_AM_I					= 0x00 # Who Am I Register
ITG3200_SMPLRT_DIV					= 0x15 # Sample Rate Divider
ITG3200_DLPF_PS						= 0x16 # Digital Low Pass Filter Register
ITG3200_INT_CFG						= 0x17 # Interrupt Configuration
ITG3200_INT_STATUS					= 0x1A # Interrupt Status
ITG3200_TEMP_OUT_H					= 0x1B # Temperature High Byte
ITG3200_TEMP_OUT_L					= 0x1C # Temperature Low Byte
ITG3200_GYRO_XOUT_H					= 0x1D # X-Axis High Byte
ITG3200_GYRO_XOUT_L					= 0x1E # X-Axis Low Byte
ITG3200_GYRO_YOUT_H					= 0x1F # Y-Axis High Byte
ITG3200_GYRO_YOUT_L					= 0x20 # Y-Axis Low Byte
ITG3200_GYRO_ZOUT_H					= 0x21 # Z-Axis High Byte
ITG3200_GYRO_ZOUT_L					= 0x22 # Z-Axis Low Byte
ITG3200_PWR_MGM						= 0x3E # Power Management

# ITG3200 Digital Low Pass Filter Register
ITG3200_FULLSCALE_2000				= 0x18 # Gyro Full-Scale Range = +/-2000 per sec
ITG3200_DLPF_BW_256					= 0x00 # Bandwidth = 256Hz
ITG3200_DLPF_BW_188					= 0x01 # Bandwidth = 188Hz
ITG3200_DLPF_BW_98					= 0x02 # Bandwidth = 98Hz
ITG3200_DLPF_BW_42					= 0x03 # Bandwidth = 42Hz
ITG3200_DLPF_BW_20					= 0x04 # Bandwidth = 20Hz
ITG3200_DLPF_BW_10					= 0x05 # Bandwidth = 10Hz
ITG3200_DLPF_BW_5					= 0x06 # Bandwidth = 5Hz

# ITG3200 Power Management Register
ITG3200_PWR_H_RESET					= 0x80 # Reset device and internal registers to the power-up-default settings
ITG3200_PWR_SLEEP					= 0x40 # Enable low power sleep mode
ITG3200_PWR_NRML_X_Y_Z				= 0x00 # Put all gyro axis in normal mode
ITG3200_PWR_STBY_XG					= 0x20 # Put gyro X in standby mode
ITG3200_PWR_STBY_YG					= 0x10 # Put gyro Y in standby mode
ITG3200_PWR_STBY_ZG					= 0x08 # Put gyro Z in standby mode
ITG3200_CLOCK_INTERNAL				= 0x00 # Internal oscillator
ITG3200_CLOCK_PLL_XGYRO				= 0x01 # PLL with X Gyro reference
ITG3200_CLOCK_PLL_YGYRO				= 0x02 # PLL with Y Gyro reference
ITG3200_CLOCK_PLL_ZGYRO				= 0x03 # PLL with Z Gyro reference
ITG3200_CLOCK_PLL_EXT32K			= 0x04 # PLL with external 32.768kHz reference
ITG3200_CLOCK_PLL_EXT19M			= 0x05 # PLL with external 19.2MHz reference

class ITG3200():
	def __init__(self):
		self.power_configuration()
		self.fullscale_configuration()
	
	def power_configuration(self):
		"""Select the Power Management Register configuration of the gyroscope from the given provided values"""
		POWER_CONFIG = (ITG3200_CLOCK_PLL_XGYRO | ITG3200_PWR_NRML_X_Y_Z)
		bus.write_byte_data(ITG3200_DEFAULT_ADDRESS, ITG3200_PWR_MGM, POWER_CONFIG)
	
	def fullscale_configuration(self):
		"""Select the Digital Low Pass Filter Register configuration of the gyroscope from the given provided values"""
		FULLSCALE_CONFIG = (ITG3200_FULLSCALE_2000 | ITG3200_DLPF_BW_256)
		bus.write_byte_data(ITG3200_DEFAULT_ADDRESS, ITG3200_DLPF_PS, FULLSCALE_CONFIG)
	
	def read_gyro(self):
		"""Read data back from ITG3200_GYRO_XOUT_H(0x1D), 6 bytes
		X-Axis MSB, X-Axis LSB, Y-Axis MSB, Y-Axis LSB, Z-Axis MSB, Z-Axis LSB"""
		data = bus.read_i2c_block_data(ITG3200_DEFAULT_ADDRESS, ITG3200_GYRO_XOUT_H, 6)
		
		# Convert the data
		xGyro = data[0] * 256 + data[1]
		if xGyro > 32767 :
			xGyro -= 65536
		
		yGyro = data[2] * 256 + data[3]
		if yGyro > 32767 :
			yGyro -= 65536
		
		zGyro = data[4] * 256 + data[5]
		if zGyro > 32767 :
			zGyro -= 65536
		
		return {'x' : xGyro, 'y' : yGyro, 'z' : zGyro}

from ITG3200 import ITG3200
itg3200 = ITG3200()

while True :
	itg3200.power_configuration()
	itg3200.fullscale_configuration()
	time.sleep(0.5)
	gyro = itg3200.read_gyro()
	print "X-Axis of Rotation : %d" %(gyro['x'])
	print "Y-Axis of Rotation : %d" %(gyro['y'])
	print "Z-Axis of Rotation : %d" %(gyro['z'])
	print " ************************************* "
	time.sleep(0.5)
