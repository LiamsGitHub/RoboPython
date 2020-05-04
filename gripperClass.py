import pymodbus
import serial
from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient #initialize a serial RTU client instance
from pymodbus.transaction import ModbusRtuFramer

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.WARNING)

import time
import numpy as np


class gripper():
    def __init__(self, client, deviceAddress=0x01, serialPortLock=None) :
        self.deviceAddress = deviceAddress
        # self.client= ModbusClient(method = "rtu", port=self.serialport)
        self.client = client
        # self.connection = client.connect()
        self.position = None
        # print ( self.connection )

    def test2(self):

        # Write LSB angle
        result = self.client.write_register(0, 45, unit=self.deviceAddress)
        print ("Result write angle LSB reg0: ", result)

        result = self.client.read_holding_registers(0, count=1, unit=self.deviceAddress)
        print ("Result read reg0: ", result.registers)


    def test(self):

        print ("Wait 5 secs")
        time.sleep(5) ## Block the class until finished

        # Read starting status
        result = self.client.read_discrete_inputs(0, count=1, unit=self.deviceAddress)
        print ("Result read Discrete Status Register initial alignment: ", result.bits)
        time.sleep(0.5) ## Block the class until finished

        print ("Write/Read angles and transit time")

        # Write LSB angle
        result = self.client.write_register(0, 45, unit=self.deviceAddress)
        print ("Result write angle LSB reg0: ", result)
        result = self.client.read_holding_registers(0, count=1, unit=self.deviceAddress)
        print ("Result read reg0: ", result.registers)
        time.sleep(0.5) ## Block the class until finished

        # Write MSB angle
        result = self.client.write_register(1, 0, unit=self.deviceAddress)
        print ("Result write angle MSB reg1: ", result)
        result = self.client.read_holding_registers(1, count=1, unit=self.deviceAddress)
        print ("Result read reg1: ", result.registers)
        time.sleep(0.5) ## Block the class until finished

        # Write transit time
        result = self.client.write_register(2, 90, unit=self.deviceAddress)
        print ("Result write transit time   reg2: ", result)
        result = self.client.read_holding_registers(2, count=1, unit=self.deviceAddress)
        print ("Result read reg2: ", result.registers)
        time.sleep(0.5) ## Block the class until finished

        # Write Coil
        result = self.client.write_coil(0x00, 0x01, unit=self.deviceAddress)
        print ("Result write coil: ", result)
        time.sleep(0.5) ## Block the class until finished

        # Read status
        result = self.client.read_discrete_inputs(0, count=1, unit=self.deviceAddress)
        print ("Result read Discrete Status Register status immediate: ", result.bits)

        time.sleep(2) ## Block the class until finished
        result = self.client.read_discrete_inputs(0, count=1, unit=self.deviceAddress)
        print ("Result read Discrete Status Register status delayed 2 secs: ", result.bits)


    def home(self):
        print ("Home")
        result = self.client.read_discrete_inputs(0, count=1, unit=self.deviceAddress)
        print ("Result read Discrete Status Register status pre-home: ", result.bits)

        ## Goto Zero Position
        result = self.client.write_register(0, 0x000, unit=self.deviceAddress)
        result = self.client.write_register(1, 0x000, unit=self.deviceAddress)
        result = self.client.write_register(2, 999, unit=self.deviceAddress) ## Make the move in 1 second
        result = self.client.write_coil(0x00, 0x01, unit=self.deviceAddress)
        time.sleep(1) ## Block the class until finished
        self.position = 0

        result = self.client.read_discrete_inputs(0, count=1, unit=self.deviceAddress)
        print ("Result read Discrete Status Register status post-home: ", result.bits)

    def movePosition(self):
        print ("Move: ", self.position)
        low, high = self.highlow(self.position)
        result = self.client.write_registers(0, [low, high, 99], unit=self.deviceAddress  )
        result = self.client.write_coil( 0x00, 0x01, unit=self.deviceAddress)
        time.sleep(.099)

    def highlow(self, signedint):
        a = np.int32(signedint)
        low, high = a & 0xFFFF, a >> 16 & 0xFFFF
        return low, high

if __name__=='__main__':
    client = ModbusClient(method="rtu", port="/dev/tty.usbserial-AQ00CQDS")
    a = gripper(client, deviceAddress=0x01)
    a.home()
    a.position= 90
    a.movePosition()
