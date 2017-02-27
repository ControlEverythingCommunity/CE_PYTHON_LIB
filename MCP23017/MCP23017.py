# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MCP23017_REG_I2CR16G5LE
# This code is designed to work with the MCP23017_REG_I2CR16G5LE_10A I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Relay-Controller?sku=MCP23017_REG_I2CR16G5LE_10A#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
MCP23017_DEFAULT_ADDRESS				= 0x20

# MCP23017 Register Map
MCP23017_REG_IODIRA						= 0x00 # I/O DIRECTION-A Register
MCP23017_REG_IPOLA						= 0x02 # INPUT POLARITY PORT-A Register
MCP23017_REG_GPINTENA					= 0x04 # INTERRUPT-ON-CHANGE-A PINS
MCP23017_REG_DEFVALA					= 0x06 # DEFAULT VALUE-A Register
MCP23017_REG_INTCONA					= 0x08 # INTERRUPT-ON-CHANGE CONTROL-A Register
MCP23017_REG_IOCONA						= 0x0A # I/O EXPANDER CONFIGURATION-A Register
MCP23017_REG_GPPUA						= 0x0C # GPIO PULL-UP RESISTOR-A Register
MCP23017_REG_INTFA						= 0x0E # INTERRUPT FLAG-A Register
MCP23017_REG_INTCAPA					= 0x10 # INTERRUPT CAPTURED VALUE FOR PORT-A Register
MCP23017_REG_GPIOA						= 0x12 # GENERAL PURPOSE I/O PORT-A Register
MCP23017_REG_OLATA						= 0x14 # OUTPUT LATCH-A Register 0

MCP23017_REG_IODIRB						= 0x01 # I/O DIRECTION-B Register
MCP23017_REG_IPOLB						= 0x03 # INPUT POLARITY PORT-B Register
MCP23017_REG_GPINTENB					= 0x05 # INTERRUPT-ON-CHANGE-B PINS
MCP23017_REG_DEFVALB					= 0x07 # DEFAULT VALUE-B Register
MCP23017_REG_INTCONB					= 0x09 # INTERRUPT-ON-CHANGE CONTROL-B Register
MCP23017_REG_IOCONB						= 0x0B # I/O EXPANDER CONFIGURATION-B Register
MCP23017_REG_GPPUB						= 0x0D # GPIO PULL-UP RESISTOR-B Register
MCP23017_REG_INTFB						= 0x0F # INTERRUPT FLAG-B Register
MCP23017_REG_INTCAPB					= 0x11 # INTERRUPT CAPTURED VALUE FOR PORT-B Register
MCP23017_REG_GPIOB						= 0x13 # GENERAL PURPOSE I/O PORT-B Register
MCP23017_REG_OLATB						= 0x15 # OUTPUT LATCH-B Register 0

# MCP23017 I/O Direction Register Configuration
MCP23017_IODIR_PIN_7_INPUT				= 0x80 # Pin-7 is configured as an input
MCP23017_IODIR_PIN_6_INPUT				= 0x40 # Pin-6 is configured as an input
MCP23017_IODIR_PIN_5_INPUT				= 0x20 # Pin-5 is configured as an input
MCP23017_IODIR_PIN_4_INPUT				= 0x10 # Pin-4 is configured as an input
MCP23017_IODIR_PIN_3_INPUT				= 0x08 # Pin-3 is configured as an input
MCP23017_IODIR_PIN_2_INPUT				= 0x04 # Pin-2 is configured as an input
MCP23017_IODIR_PIN_1_INPUT				= 0x02 # Pin-1 is configured as an input
MCP23017_IODIR_PIN_0_INPUT				= 0x01 # Pin-0 is configured as an input
MCP23017_IODIR_PIN_INPUT				= 0xFF # All Pins are configured as an input
MCP23017_IODIR_PIN_OUTPUT				= 0x00 # All Pins are configured as an output

# MCP23017 Pull-Up Resistor Register Configuration
MCP23017_GPPU_PIN_7_EN					= 0x80 # Pull-up enabled on Pin-7
MCP23017_GPPU_PIN_6_EN					= 0x40 # Pull-up enabled on Pin-6
MCP23017_GPPU_PIN_5_EN					= 0x20 # Pull-up enabled on Pin-5
MCP23017_GPPU_PIN_4_EN					= 0x10 # Pull-up enabled on Pin-4
MCP23017_GPPU_PIN_3_EN					= 0x08 # Pull-up enabled on Pin-3
MCP23017_GPPU_PIN_2_EN					= 0x04 # Pull-up enabled on Pin-2
MCP23017_GPPU_PIN_1_EN					= 0x02 # Pull-up enabled on Pin-1
MCP23017_GPPU_PIN_0_EN					= 0x01 # Pull-up enabled on Pin-0
MCP23017_GPPU_PIN_EN					= 0xFF # Pull-up enabled on All Pins
MCP23017_GPPU_PIN_DS					= 0x00 # Pull-up disabled on All Pins

# MCP23017 General Purpose I/O Port Register
MCP23017_GPIO_PIN_7_HIGH				= 0x80 # Logic-high on Pin-7
MCP23017_GPIO_PIN_6_HIGH				= 0x40 # Logic-high on Pin-6
MCP23017_GPIO_PIN_5_HIGH				= 0x20 # Logic-high on Pin-5
MCP23017_GPIO_PIN_4_HIGH				= 0x10 # Logic-high on Pin-4
MCP23017_GPIO_PIN_3_HIGH				= 0x08 # Logic-high on Pin-3
MCP23017_GPIO_PIN_2_HIGH				= 0x04 # Logic-high on Pin-2
MCP23017_GPIO_PIN_1_HIGH				= 0x02 # Logic-high on Pin-1
MCP23017_GPIO_PIN_0_HIGH				= 0x01 # Logic-high on Pin-0
MCP23017_GPIO_PIN_HIGH					= 0xFF # Logic-high on All Pins
MCP23017_GPIO_PIN_LOW					= 0x00 # Logic-low on All Pins

class MCP23017():
	def select_port(self):
		"""Select the Port user want to use from 0-1
		0 : Port-A
		1 : Port-B"""
		self.port = int(input("Enter the Port No.(0-1) = "))
		while self.port > 1 :
			self.port = int(input("Enter the Port No.(0-1) = "))
		
		return self.port
	
	def select_relay(self):
		"""Select the Relay user want to use from 0-7
		0 : Relay-0
		1 : Relay-1
		2 : Relay-2
		3 : Relay-3
		4 : Relay-4
		5 : Relay-5
		6 : Relay-6
		7 : Relay-7
		8 : All Relay"""
		self.relay = int(input("Enter the Relay No.(0-8) = "))
		while self.relay > 8 :
			self.relay = int(input("Enter the Relay No.(0-8) = "))
		
		return self.relay
	
	def set_input_dir(self):
		"""Select the I/O Direction Register Configuration from the given provided value"""
		if self.port == 0 :
			if self.relay == 0 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_IODIRA, MCP23017_IODIR_PIN_0_INPUT)
			elif self.relay == 1 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_IODIRA, MCP23017_IODIR_PIN_1_INPUT)
			elif self.relay == 2 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_IODIRA, MCP23017_IODIR_PIN_2_INPUT)
			elif self.relay == 3 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_IODIRA, MCP23017_IODIR_PIN_3_INPUT)
			elif self.relay == 4 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_IODIRA, MCP23017_IODIR_PIN_4_INPUT)
			elif self.relay == 5 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_IODIRA, MCP23017_IODIR_PIN_5_INPUT)
			elif self.relay == 6 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_IODIRA, MCP23017_IODIR_PIN_6_INPUT)
			elif self.relay == 7 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_IODIRA, MCP23017_IODIR_PIN_7_INPUT)
			elif self.relay == 8 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_IODIRA, MCP23017_IODIR_PIN_INPUT)
		elif self.port == 1 :
			if self.relay == 0 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_IODIRB, MCP23017_IODIR_PIN_0_INPUT)
			elif self.relay == 1 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_IODIRB, MCP23017_IODIR_PIN_1_INPUT)
			elif self.relay == 2 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_IODIRB, MCP23017_IODIR_PIN_2_INPUT)
			elif self.relay == 3 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_IODIRB, MCP23017_IODIR_PIN_3_INPUT)
			elif self.relay == 4 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_IODIRB, MCP23017_IODIR_PIN_4_INPUT)
			elif self.relay == 5 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_IODIRB, MCP23017_IODIR_PIN_5_INPUT)
			elif self.relay == 6 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_IODIRB, MCP23017_IODIR_PIN_6_INPUT)
			elif self.relay == 7 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_IODIRB, MCP23017_IODIR_PIN_7_INPUT)
			elif self.relay == 8 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_IODIRB, MCP23017_IODIR_PIN_INPUT)
		
	
	def set_output_dir(self):
		"""Select the I/O Direction Register Configuration from the given provided value"""
		if self.port == 0 :
			bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_IODIRA, MCP23017_IODIR_PIN_OUTPUT)
		if self.port == 0 :
			bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_IODIRB, MCP23017_IODIR_PIN_OUTPUT)
	
	def pull_up_config(self):
		"""Select the Pull-Up Resistor Register Configuration from the given provided value"""
		if self.port == 0 :
			if self.relay == 0 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPPUA, MCP23017_GPPU_PIN_0_EN)
			elif self.relay == 1 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPPUA, MCP23017_GPPU_PIN_1_EN)
			elif self.relay == 2 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPPUA, MCP23017_GPPU_PIN_2_EN)
			elif self.relay == 3 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPPUA, MCP23017_GPPU_PIN_3_EN)
			elif self.relay == 4 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPPUA, MCP23017_GPPU_PIN_4_EN)
			elif self.relay == 5 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPPUA, MCP23017_GPPU_PIN_5_EN)
			elif self.relay == 6 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPPUA, MCP23017_GPPU_PIN_6_EN)
			elif self.relay == 7 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPPUA, MCP23017_GPPU_PIN_7_EN)
			elif self.relay == 8 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPPUA, MCP23017_GPPU_PIN_EN)
		elif self.port == 1 :
			if self.relay == 0 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPPUB, MCP23017_GPPU_PIN_0_EN)
			elif self.relay == 1 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPPUB, MCP23017_GPPU_PIN_1_EN)
			elif self.relay == 2 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPPUB, MCP23017_GPPU_PIN_2_EN)
			elif self.relay == 3 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPPUB, MCP23017_GPPU_PIN_3_EN)
			elif self.relay == 4 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPPUB, MCP23017_GPPU_PIN_4_EN)
			elif self.relay == 5 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPPUB, MCP23017_GPPU_PIN_5_EN)
			elif self.relay == 6 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPPUB, MCP23017_GPPU_PIN_6_EN)
			elif self.relay == 7 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPPUB, MCP23017_GPPU_PIN_7_EN)
			elif self.relay == 8 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPPUB, MCP23017_GPPU_PIN_EN)
	
	def checking_status(self):
		"""Checking Status of all GPIO pins before writing"""
		if self.port == 0 :
			self.status = bus.read_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPIOA)
		elif self.port == 1 :
			self.status = bus.read_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPIOB)
	
	def gpio_config(self):
		"""Select the Pull-Up Resistor Register Configuration from the given provided value"""
		if self.port == 0 :
			if self.relay == 0 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPIOA, self.status | MCP23017_GPIO_PIN_0_HIGH)
			elif self.relay == 1 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPIOA, self.status | MCP23017_GPIO_PIN_1_HIGH)
			elif self.relay == 2 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPIOA, self.status | MCP23017_GPIO_PIN_2_HIGH)
			elif self.relay == 3 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPIOA, self.status | MCP23017_GPIO_PIN_3_HIGH)
			elif self.relay == 4 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPIOA, self.status | MCP23017_GPIO_PIN_4_HIGH)
			elif self.relay == 5 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPIOA, self.status | MCP23017_GPIO_PIN_5_HIGH)
			elif self.relay == 6 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPIOA, self.status | MCP23017_GPIO_PIN_6_HIGH)
			elif self.relay == 7 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPIOA, self.status | MCP23017_GPIO_PIN_7_HIGH)
			elif self.relay == 8 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPIOA, self.status | MCP23017_GPIO_PIN_HIGH)
		elif self.port == 1 :
			if self.relay == 0 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPIOB, self.status | MCP23017_GPIO_PIN_0_HIGH)
			elif self.relay == 1 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPIOB, self.status | MCP23017_GPIO_PIN_1_HIGH)
			elif self.relay == 2 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPIOB, self.status | MCP23017_GPIO_PIN_2_HIGH)
			elif self.relay == 3 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPIOB, self.status | MCP23017_GPIO_PIN_3_HIGH)
			elif self.relay == 4 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPIOB, self.status | MCP23017_GPIO_PIN_4_HIGH)
			elif self.relay == 5 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPIOB, self.status | MCP23017_GPIO_PIN_5_HIGH)
			elif self.relay == 6 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPIOB, self.status | MCP23017_GPIO_PIN_6_HIGH)
			elif self.relay == 7 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPIOB, self.status | MCP23017_GPIO_PIN_7_HIGH)
			elif self.relay == 8 :
				bus.write_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPIOB, self.status | MCP23017_GPIO_PIN_HIGH)
	
	def check_status(self):
		"""Check Status of all GPIO pins"""
		if self.port == 0 :
			status = bus.read_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPIOA)
		elif self.port == 1 :
			status = bus.read_byte_data(MCP23017_DEFAULT_ADDRESS, MCP23017_REG_GPIOB)
		
		data = 0x01
		for MyData in range(0, 8):
			pin = status & data
			if pin == data:
				print "Status for Pin %d is High" %MyData
			else:
				print "Status for Pin %d is Low" %MyData
			data = data << 1
			time.sleep(0.3)
		
	