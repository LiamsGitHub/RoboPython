from gripperClass import gripper
import pymodbus
import serial
from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient #initialize a serial RTU client instance
from pymodbus.client.sync import ModbusTcpClient as ModbusTcpClient #initialize a serial TCPIP client instance
from pymodbus.transaction import ModbusRtuFramer
import time

#import logging
#logging.basicConfig()
#log = logging.getLogger()
#log.setLevel(logging.DEBUG)


#client = ModbusClient(method="rtu", port="/dev/cu.usbserial-AQ00CQDS")
#client = ModbusClient(method="rtu", port="/dev/tty.usbserial-AQ00CQDS")
#client = ModbusClient(method="rtu", port="/dev/ttyUSB0") # Mac or RaPi client
client = ModbusClient(method="rtu", port="com4", stopbits = 1, bytesize = 8, parity = 'N', baudrate= 19200) # PC

#host = '172.16.0.45'
#port = 502
#client = ModbusTcpClient(host, port) # TCP client
#client.connect()

angles = [0, 45, 90, 135, 180, 225, 270, 315]

a_motor = gripper(client, deviceAddress=0x01)
a_motor.home() # Move the motor to the power on position
time.sleep(5)

while (1):

    for posn in angles:
        print ("Going to ", posn)
        a_motor.position = posn
        a_motor.movePosition() # Move the motor
        time.sleep(1)
