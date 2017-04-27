# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# KXTF9-4100
# This code is designed to work with the KXTF9-4100_I2CS I2C Mini Module available from ControlEverything.com.
# https://shop.controleverything.com/

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
KXTF9_4100_DEFAULT_ADDRESS                  = 0x0F

# KXTF9_4100 Register Map
KXTF9_4100_REG_ACCEL_XOUT_HPF_L             = 0x00  # X-Axis High-Pass Filtered Accelerometer Output Least Significant Byte Register
KXTF9_4100_REG_ACCEL_XOUT_HPF_H             = 0x01  # X-Axis High-Pass Filtered Accelerometer Output Most Significant Byte Register
KXTF9_4100_REG_ACCEL_YOUT_HPF_L             = 0x02  # Y-Axis High-Pass Filtered Accelerometer Output Least Significant Byte Register
KXTF9_4100_REG_ACCEL_YOUT_HPF_H             = 0x03  # Y-Axis High-Pass Filtered Accelerometer Output Most Significant Byte Register
KXTF9_4100_REG_ACCEL_ZOUT_HPF_L             = 0x04  # Z-Axis High-Pass Filtered Accelerometer Output Least Significant Byte Register
KXTF9_4100_REG_ACCEL_ZOUT_HPF_H             = 0x05  # Z-Axis High-Pass Filtered Accelerometer Output Most Significant Byte Register
KXTF9_4100_REG_ACCEL_XOUT_L                 = 0x06  # X-Axis Accelerometer Output Least Significant Byte Register
KXTF9_4100_REG_ACCEL_XOUT_H                 = 0x07  # X-Axis Accelerometer Output Most Significant Byte Register
KXTF9_4100_REG_ACCEL_YOUT_L                 = 0x08  # Y-Axis Accelerometer Output Least Significant Byte Register
KXTF9_4100_REG_ACCEL_YOUT_H                 = 0x09  # Y-Axis Accelerometer Output Most Significant Byte Register
KXTF9_4100_REG_ACCEL_ZOUT_L                 = 0x0A  # Z-Axis Accelerometer Output Least Significant Byte Register
KXTF9_4100_REG_ACCEL_ZOUT_H                 = 0x0B  # Z-Axis Accelerometer Output Most Significant Byte Register
KXTF9_4100_REG_ACCEL_DCST_RESP              = 0x0C  # Integrated Circuit Functionality Register
KXTF9_4100_REG_ACCEL_WHO_AM_I               = 0x0F  # Supplier Recognition Register
KXTF9_4100_REG_ACCEL_TILT_POS_CUR           = 0x10  # Current Tilt Position Register
KXTF9_4100_REG_ACCEL_TILT_POS_PRE           = 0x11  # Previous Tilt Position Register
KXTF9_4100_REG_ACCEL_INT_SRC_REG1           = 0x15  # Latched Interrupt Source Information Register 1
KXTF9_4100_REG_ACCEL_INT_SRC_REG2           = 0x16  # Latched Interrupt Source Information Register 2
KXTF9_4100_REG_ACCEL_STATUS_REG             = 0x18  # Interrupt Status Register
KXTF9_4100_REG_ACCEL_INT_REL                = 0x1A  # Interrupt Clearance Register
KXTF9_4100_REG_ACCEL_CTRL_REG1              = 0x1B  # Main Feature Control Register
KXTF9_4100_REG_ACCEL_CTRL_REG2              = 0x1C  # Tilt Position State Enabling Control Register
KXTF9_4100_REG_ACCEL_CTRL_REG3              = 0x1D  # More Feature Set Control Register
KXTF9_4100_REG_ACCEL_INT_CTRL_REG1          = 0x1E  # Physical Interrupt Pin Control Setting Register
KXTF9_4100_REG_ACCEL_INT_CTRL_REG2          = 0x1F  # Motion Detection Axis Enabling Register
KXTF9_4100_REG_ACCEL_INT_CTRL_REG3          = 0x20  # Motion Detection Axis Enabling Register
KXTF9_4100_REG_ACCEL_DATA_CTRL_REG          = 0x21  # Acceleration Outputs Configuration Register
KXTF9_4100_REG_ACCEL_TILT_TIMER             = 0x28  # Tilt Position State Timer Count Register
KXTF9_4100_REG_ACCEL_WUF_TIMER              = 0x29  # Motion Detection Timer Count Register
KXTF9_4100_REG_ACCEL_TDT_TIMER              = 0x2B  # Double Tap Event Detection Register
KXTF9_4100_REG_ACCEL_TDT_H_THRESH           = 0x2C  # 9-bit Jerk High Threshold Tap Detection Register
KXTF9_4100_REG_ACCEL_TDT_L_THRESH           = 0x2D  # 7-bit Jerk Low Threshold Tap Detection Register
KXTF9_4100_REG_ACCEL_TDT_TAP_TIMER          = 0x2E  # Any Tap Detection Counter Information Register
KXTF9_4100_REG_ACCEL_TDT_TOTAL_TIMER        = 0x2F  # Double Tap Detection Counter Information Register
KXTF9_4100_REG_ACCEL_TDT_LATENCY_TIMER      = 0x30  # Tap Detection Counter Information Register
KXTF9_4100_REG_ACCEL_TDT_WINDOW_TIMER       = 0x31  # Single/Double Tap Detection Counter Information Register
KXTF9_4100_REG_ACCEL_SELF_TEST              = 0x3A  # Self-Test Register
KXTF9_4100_REG_ACCEL_WUF_THRESH             = 0x5A  # Acceleration Threshold Register
KXTF9_4100_REG_ACCEL_TILT_ANGLE             = 0x5C  # Tilt Angle Register
KXTF9_4100_REG_ACCEL_HYST_SET               = 0x5F  # Hysteresis Register

# Accl Control Register 1 configuration
KXTF9_4100_PC1_STANDBY          = 0x00  # Stand-by Mode
KXTF9_4100_PC1_OPERATE          = 0x80  # Operating Mode
KXTF9_4100_RES_0                = 0x00  # Low Current, 8-bit Valid
KXTF9_4100_RES_1                = 0x40  # High Current, 12-bit Valid
KXTF9_4100_DRDYE_NOT            = 0x00  # Availability of New Acceleration Data Not Reflected on Interrupt Pin (7)
KXTF9_4100_DRDYE_NEW            = 0x20  # Availability of New Acceleration Data Reflected on Interrupt Pin (7)
KXTF9_4100_GSEL_2G              = 0x00  # Range: +/-2g
KXTF9_4100_GSEL_4G              = 0x08  # Range: +/-4g
KXTF9_4100_GSEL_8G              = 0x10  # Range: +/-8g
KXTF9_4100_TDTE_DISABLE         = 0x00  # Directional TapTM Function Disable
KXTF9_4100_TDTE_ENABLE          = 0x04  # Directional TapTM Function Enable
KXTF9_4100_WUFE_DISABLE         = 0x00  # Wake Up (Motion Detect) Function Disable
KXTF9_4100_WUFE_ENABLE          = 0x02  # Wake Up (Motion Detect) Function Enable
KXTF9_4100_TPE_DISABLE          = 0x00  # Tilt Position Function Disable
KXTF9_4100_TPE_ENABLE           = 0x01  # Tilt Position Function Enable


class KXTF9_4100():
	def __init__ (self):
		self.select_data_control()
	
	def select_data_control(self):
		"""Select the data configuration of the accelerometer from the given provided values"""
		DATA_CONTROL1 = (KXTF9_4100_PC1_OPERATE | KXTF9_4100_RES_1 | KXTF9_4100_DRDYE_NOT | KXTF9_4100_GSEL_8G | KXTF9_4100_TDTE_ENABLE | KXTF9_4100_WUFE_ENABLE | KXTF9_4100_TPE_ENABLE)
		bus.write_byte_data(KXTF9_4100_DEFAULT_ADDRESS, KXTF9_4100_REG_ACCEL_CTRL_REG1, DATA_CONTROL1)
	
	def read_accl(self):
		"""Read data back from KXTF9_4100_REG_ACCEL_XOUT_L(0x06), 2 bytes
		X-Axis Accl LSB, X-Axis Accl MSB"""
		data0 = bus.read_byte_data(KXTF9_4100_DEFAULT_ADDRESS, KXTF9_4100_REG_ACCEL_XOUT_L)
		data1 = bus.read_byte_data(KXTF9_4100_DEFAULT_ADDRESS, KXTF9_4100_REG_ACCEL_XOUT_H)
		
        xAccl = ((data1 * 256) + (data0 & 0xF0)) / 16
        if xAccl > 2047 :
            xAccl -= 4096
		
		"""Read data back from KXTF9_4100_REG_ACCEL_YOUT_L(0x08), 2 bytes
		Y-Axis Accl LSB, Y-Axis Accl MSB"""
		data0 = bus.read_byte_data(KXTF9_4100_DEFAULT_ADDRESS, KXTF9_4100_REG_ACCEL_YOUT_L)
		data1 = bus.read_byte_data(KXTF9_4100_DEFAULT_ADDRESS, KXTF9_4100_REG_ACCEL_YOUT_H)
		
        yAccl = ((data1 * 256) + (data0 & 0xF0)) / 16
        if yAccl > 2047 :
            yAccl -= 4096
		
		"""Read data back from KXTF9_4100_REG_ACCEL_ZOUT_L(0x0A), 2 bytes
		Z-Axis Accl LSB, Z-Axis Accl MSB"""
		data0 = bus.read_byte_data(KXTF9_4100_DEFAULT_ADDRESS, KXTF9_4100_REG_ACCEL_ZOUT_L)
		data1 = bus.read_byte_data(KXTF9_4100_DEFAULT_ADDRESS, KXTF9_4100_REG_ACCEL_ZOUT_H)
		
        zAccl = ((data1 * 256) + (data0 & 0xF0)) / 16
        if zAccl > 2047 :
            zAccl -= 4096
		
		return {'x' : xAccl, 'y' : yAccl, 'z' : zAccl}

from KXTF9_4100 import KXTF9_4100
kxtf9_4100 = KXTF9_4100()

while True:
	kxtf9_4100.select_data_control()
	time.sleep(0.1)
	accl = kxtf9_4100.read_accl()
	print "Acceleration in X-Axis : %d" %(accl['x'])
	print "Acceleration in Y-Axis : %d" %(accl['y'])
	print "Acceleration in Z-Axis : %d" %(accl['z'])
	print " ************************************ "
	time.sleep(1)
