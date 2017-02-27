# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MCP23017_REG_I2CR16G5LE
# This code is designed to work with the MCP23017_REG_I2CR16G5LE_10A I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Relay-Controller?sku=MCP23017_REG_I2CR16G5LE_10A#tabs-0-product_tabset-2

import time

from MCP23017 import MCP23017
mcp23017 = MCP23017()

while True :
	mcp23017.select_port()
	mcp23017.select_relay()
	mcp23017.set_output_dir()
	mcp23017.checking_status()
	mcp23017.gpio_config()
	mcp23017.check_status()
	print " ******************************* "
	time.sleep(0.2)
