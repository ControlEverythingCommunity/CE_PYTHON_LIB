# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# KMX61
# This code is designed to work with the KMX61_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/products

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
KMX61_DEFAULT_ADDRESS                   = 0x0E

# KMX61 Accelerometer register
KMX61_OUT_X_L_A                         = 0x0A
KMX61_OUT_X_H_A                         = 0x0B
KMX61_OUT_Y_L_A                         = 0x0C
KMX61_OUT_Y_H_A                         = 0x0D
KMX61_OUT_Z_L_A                         = 0x0E
KMX61_OUT_Z_H_A                         = 0x0F
KMX61_OUT_Z_L_T                         = 0x10
KMX61_OUT_Z_H_T                         = 0x11
KMX61_OUT_X_L_M                         = 0x12
KMX61_OUT_X_H_M                         = 0x13
KMX61_OUT_Y_L_M                         = 0x14
KMX61_OUT_Y_H_M                         = 0x15
KMX61_OUT_Z_L_M                         = 0x16
KMX61_OUT_Z_H_M                         = 0x17
KMX61_STBY_REG                          = 0x29
KMX61_REG_CNTL1                         = 0x2A
KMX61_REG_ODCNTL                        = 0x2C


# Standby Status Register configuration
KMX61_REG_STBY_REG_ACT_STBY_0           = 0x00  # ASIC_AL Control Feature Disabled
KMX61_REG_STBY_REG_ACT_STBY_1           = 0x80  # ASIC_AL Control Feature Enabled

KMX61_REG_STBY_REG_MAG_STBY_0           = 0x00  # ASIC_AL's Magnetometer Control Feature Disabled
KMX61_REG_STBY_REG_MAG_STBY_1           = 0x02  # ASIC_AL's Magnetometer Control Feature Enabled

KMX61_REG_STBY_REG_ACCEL_STBY_0         = 0x00  # ASIC_AL's Accelerometer Control Feature Disabled
KMX61_REG_STBY_REG_ACCEL_STBY_1         = 0x01  # ASIC_AL's Accelerometer Control Feature Enabled

# Control Register 1 configuration
KMX61_REG_CNTL1_BTSE_DISABLE            = 0x00  # Back to Sleep Engine Disable
KMX61_REG_CNTL1_BTSE_ENABLE             = 0x80  # Back to Sleep Engine Enable

KMX61_REG_CNTL1_WUFE_DISABLE            = 0x00  # Wake up Engine Disable
KMX61_REG_CNTL1_WUFE_ENABLE             = 0x40  # Wake up Engine Enable

KMX61_REG_CNTL1_GSEL_2G                 = 0x00  # +/-2g
KMX61_REG_CNTL1_GSEL_4G                 = 0x00  # +/-4g
KMX61_REG_CNTL1_GSEL_8G                 = 0x00  # +/-8g
KMX61_REG_CNTL1_GSEL_8G_14BIT           = 0x00  # +/-8g: 12-bit


# Output Data Control Register configuration
# Rate at Which Data Samples from the Magnetometer will be Updated
KMX61_REG_ODCNTL_OSM_12_5               = 0x00  # Output Data Rate (Hz): 12.5
KMX61_REG_ODCNTL_OSM_25                 = 0x10  # Output Data Rate (Hz): 25
KMX61_REG_ODCNTL_OSM_50                 = 0x20  # Output Data Rate (Hz): 50
KMX61_REG_ODCNTL_OSM_100                = 0x30  # Output Data Rate (Hz): 100
KMX61_REG_ODCNTL_OSM_200                = 0x40  # Output Data Rate (Hz): 200
KMX61_REG_ODCNTL_OSM_400                = 0x50  # Output Data Rate (Hz): 400
KMX61_REG_ODCNTL_OSM_800                = 0x60  # Output Data Rate (Hz): 800
KMX61_REG_ODCNTL_OSM_1600               = 0x70  # Output Data Rate (Hz): 1600
KMX61_REG_ODCNTL_OSM_0_781              = 0x80  # Output Data Rate (Hz): 0.781
KMX61_REG_ODCNTL_OSM_1_583              = 0x90  # Output Data Rate (Hz): 1.583
KMX61_REG_ODCNTL_OSM_3_125              = 0xA0  # Output Data Rate (Hz): 3.125
KMX61_REG_ODCNTL_OSM_6_25               = 0xB0  # Output Data Rate (Hz): 6.25

# Rate at Which Data Samples from the Accelerometer will be Updated
KMX61_REG_ODCNTL_OSA_12_5               = 0x00  # Output Data Rate (Hz): 12.5
KMX61_REG_ODCNTL_OSA_25                 = 0x01  # Output Data Rate (Hz): 25
KMX61_REG_ODCNTL_OSA_50                 = 0x02  # Output Data Rate (Hz): 50
KMX61_REG_ODCNTL_OSA_100                = 0x03  # Output Data Rate (Hz): 100
KMX61_REG_ODCNTL_OSA_200                = 0x04  # Output Data Rate (Hz): 200
KMX61_REG_ODCNTL_OSA_400                = 0x05  # Output Data Rate (Hz): 400
KMX61_REG_ODCNTL_OSA_800                = 0x06  # Output Data Rate (Hz): 800
KMX61_REG_ODCNTL_OSA_1600               = 0x07  # Output Data Rate (Hz): 1600
KMX61_REG_ODCNTL_OSA_0_781              = 0x08  # Output Data Rate (Hz): 0.781
KMX61_REG_ODCNTL_OSA_1_583              = 0x09  # Output Data Rate (Hz): 1.583
KMX61_REG_ODCNTL_OSA_3_125              = 0x0A  # Output Data Rate (Hz): 3.125
KMX61_REG_ODCNTL_OSA_6_25               = 0x0B  # Output Data Rate (Hz): 6.25

class KMX61():
    
    def standbystat(self):
        """Select the ASIC_AL to Control feature from the given provided values"""
        STANDBY = (KMX61_REG_STBY_REG_ACT_STBY_0 | KMX61_REG_STBY_REG_MAG_STBY_0 | KMX61_REG_STBY_REG_ACCEL_STBY_0)
        bus.write_byte_data(KMX61_DEFAULT_ADDRESS, KMX61_STBY_REG, STANDBY)

    def datarate(self):
		"""Select the data rate of the magnetometer and accelerometer from the given provided values"""
		DATARATE = (KMX61_REG_ODCNTL_OSM_12_5 | KMX61_REG_ODCNTL_OSA_12_5)
		bus.write_byte_data(KMX61_DEFAULT_ADDRESS, KMX61_REG_ODCNTL, DATARATE)
	
	def accl_scale_selection(self):
		"""Select the full-scale values of the accelerometer from the given provided values"""
		ACCL_SCALE = (KMX61_REG_CNTL1_GSEL_2G)
		bus.write_byte_data(KMX61_DEFAULT_ADDRESS, KMX61_REG_CNTL1, KMX61_REG_CNTL1_BTSE_DISABLE | KMX61_REG_CNTL1_WUFE_DISABLE | ACCL_SCALE)
	
	def readaccl(self):
		"""Read data back from KMX61_OUT_X_L_A(0x0A), 2 bytes
		X-Axis Accel LSB, X-Axis Accel MSB"""
		data0 = bus.read_byte_data(KMX61_DEFAULT_ADDRESS, KMX61_OUT_X_L_A)
		data1 = bus.read_byte_data(KMX61_DEFAULT_ADDRESS, KMX61_OUT_X_H_A)
		
		xAccl = ((data1 * 256) + (data0 & 0xF0)) / 16
        if xAccl > 2047 :
            xAccl -= 4096
		
		"""Read data back from KMX61_OUT_Y_L_M(0x0C), 2 bytes
		Y-Axis Accel LSB, Y-Axis Accel MSB"""
		data0 = bus.read_byte_data(KMX61_DEFAULT_ADDRESS, KMX61_OUT_Y_L_A)
		data1 = bus.read_byte_data(KMX61_DEFAULT_ADDRESS, KMX61_OUT_Y_H_A)
		
        yAccl = ((data1 * 256) + (data0 & 0xF0)) / 16
        if yAccl > 2047 :
            yAccl -= 4096
		
		"""Read data back from KMX61_OUT_Z_L_M(0x0E), 2 bytes
		Z-Axis Accel LSB, Z-Axis Accel MSB"""
		data0 = bus.read_byte_data(KMX61_DEFAULT_ADDRESS, KMX61_OUT_Z_L_A)
		data1 = bus.read_byte_data(KMX61_DEFAULT_ADDRESS, KMX61_OUT_Z_H_A)
		
        zAccl = ((data1 * 256) + (data0 & 0xF0)) / 16
        if zAccl > 2047 :
            zAccl -= 4096
		
		return {'x' : xAccl, 'y' : yAccl, 'z' : zAccl}
	
	def readmag(self):
		"""Read data back from KMX61_OUT_X_L_M(0x12), 2 bytes
		X-Axis Mag LSB, X-Axis Mag MSB"""
		data0 = bus.read_byte_data(KMX61_DEFAULT_ADDRESS, KMX61_OUT_X_H_M,)
		data1 = bus.read_byte_data(KMX61_DEFAULT_ADDRESS, KMX61_OUT_X_L_M,)
		
        xMag = ((data1 * 256) + (data0 & 0xFC)) / 4
        if xMag > 8191 :
            xMag -= 16384
                
        """Read data back from KMX61_OUT_Y_L_M(0x14), 2 bytes
        Y-Axis Mag LSB, Y-Axis Mag MSB"""
        data0 = bus.read_byte_data(KMX61_DEFAULT_ADDRESS, KMX61_OUT_Y_H_M,)
        data1 = bus.read_byte_data(KMX61_DEFAULT_ADDRESS, KMX61_OUT_Y_L_M,)
                    
        xMag = ((data1 * 256) + (data0 & 0xFC)) / 4
        if yMag > 8191 :
            yMag -= 16384
                                
        """Read data back from KMX61_OUT_Z_L_M(0x16), 2 bytes
		Z-Axis Mag LSB, Z-Axis Mag MSB"""
		data0 = bus.read_byte_data(KMX61_DEFAULT_ADDRESS, KMX61_OUT_Z_H_M,)
		data1 = bus.read_byte_data(KMX61_DEFAULT_ADDRESS, KMX61_OUT_Z_L_M,)
		
        zMag = ((data1 * 256) + (data0 & 0xFC)) / 4
        if zMag > 8191 :
            zMag -= 16384
		
		return {'x' : xMag, 'y' : yMag, 'z' : zMag}

from KMX61 import KMX61
kmx61 = KMX61()

while True:
	kmx61.datarate()
	kmx61.accl_scale_selection()
    kmx61.standbystat()
	accl = kmx61.readaccl()
	print "Acceleration in X-Axis : %d"%(accl['x'])
	print "Acceleration in Y-Axis : %d"%(accl['y'])
	print "Acceleration in Z-Axis : %d"%(accl['z'])
    mag = kmx61.readmag()
	print "Magnetic field in X-Axis : %d"%(mag['x'])
	print "Magnetic field in Y-Axis : %d"%(mag['y'])
	print "Magnetic field in Z-Axis : %d"%(mag['z'])
	print " ************************************* "
	time.sleep(0.8)
