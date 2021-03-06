# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MCP3428
# This code is designed to work with the MCP3428_I2CADC I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Analog-Digital-Converters?sku=MCP3428_I2CADC#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
MCP3428_DEFAULT_ADDRESS = 0x68

# MCP3428 Configuration Command Set
MCP3428_CMD_NEW_CNVRSN = 0x80  # Initiate a new conversion(One-Shot Conversion mode only)
MCP3428_CMD_CHNL_1 = 0x00  # Channel-1 Selected
MCP3428_CMD_CHNL_2 = 0x20  # Channel-2 Selected
MCP3428_CMD_CHNL_3 = 0x40  # Channel-3 Selected
MCP3428_CMD_CHNL_4 = 0x60  # Channel-4 Selected
MCP3428_CMD_MODE_CONT = 0x10  # Continuous Conversion Mode
MCP3428_CMD_MODE_ONESHOT = 0x00  # One-Shot Conversion Mode
MCP3428_CMD_SPS_240 = 0x00  # 240 SPS (12-bit)
MCP3428_CMD_SPS_60 = 0x04  # 60 SPS (14-bit)
MCP3428_CMD_SPS_15 = 0x08  # 15 SPS (16-bit)
MCP3428_CMD_GAIN_1 = 0x00  # PGA Gain = 1V/V
MCP3428_CMD_GAIN_2 = 0x01  # PGA Gain = 2V/V
MCP3428_CMD_GAIN_4 = 0x02  # PGA Gain = 4V/V
MCP3428_CMD_GAIN_8 = 0x03  # PGA Gain = 8V/V
MCP3428_CMD_READ_CNVRSN = 0x00  # Read Conversion Result Data


class MCP3428():
    def __init__(self):
        self.sps = MCP3428_CMD_SPS_15

    def config_command(self):
        """Select the Configuration Command from the given provided values"""
        if self.channel == 1:
            CONFIG_CMD = (MCP3428_CMD_MODE_CONT | self.sps | MCP3428_CMD_GAIN_1 | MCP3428_CMD_CHNL_1)
        elif self.channel == 2:
            CONFIG_CMD = (MCP3428_CMD_MODE_CONT | self.sps | MCP3428_CMD_GAIN_1 | MCP3428_CMD_CHNL_2)
        elif self.channel == 3:
            CONFIG_CMD = (MCP3428_CMD_MODE_CONT | self.sps | MCP3428_CMD_GAIN_1 | MCP3428_CMD_CHNL_3)
        elif self.channel == 4:
            CONFIG_CMD = (MCP3428_CMD_MODE_CONT | self.sps | MCP3428_CMD_GAIN_1 | MCP3428_CMD_CHNL_4)

        bus.write_byte(MCP3428_DEFAULT_ADDRESS, CONFIG_CMD)

    def read_adc(self):
        """Read data back from MCP3428_CMD_READ_CNVRSN(0x00), 2 bytes
        raw_adc MSB, raw_adc LSB"""
        data = bus.read_i2c_block_data(MCP3428_DEFAULT_ADDRESS, MCP3428_CMD_READ_CNVRSN, 2)

        print("data: {}".format(data))

        if self.sps == MCP3428_CMD_SPS_15:
            # Convert the data to 16-bits
            raw_adc = ((data[0] & 0xFF) * 256) + data[1]
            max_voltage_value = (29158 * 2)  # should be 65535
            # but measured was 29158
        elif self.sps == MCP3428_CMD_SPS_240:
            # Convert the data to 12-bits
            raw_adc = ((data[0] & 0x0F) * 256) + data[1]
            max_voltage_value = 4095
        elif self.sps == MCP3428_CMD_SPS_60:
            # Convert the data to 14-bits
            raw_adc = ((data[0] & 0x4F) * 256) + data[1]
            max_voltage_value = 16384

        voltage_value = 10.0 * (float(raw_adc) / (float(max_voltage_value) / 2.0))

        return {'r': raw_adc, 'v': voltage_value}


if __name__ == '__main__':

    mcp3428 = MCP3428()

    while True:
        for i in range(1, 5):
            mcp3428.channel = i
            mcp3428.config_command()
            time.sleep(0.2)
            adc = mcp3428.read_adc()
            print("Digital Value of Analog Input[{}] = {}, Volt = {} ".format(i, int(adc['r']), float(adc['v'])))
            print(" ********************************* ")
            time.sleep(0.8)
