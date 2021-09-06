import smbus
import time
import Jetson.GPIO as GPIO
import os
import os

def I2C_Event(channel):
    GPIO.remove_event_detect(29)
    print("I2C Int!!")
    command = bytes(readNumber(MODE_SHUTDOWN,2))
    if command[0] == 0x15:
        if command[1] == 0x65:
            print("shutdown!!")
            time.sleep(3)
            os.system('shutdown -h now')

    print("0x" + command.hex())
    time.sleep(0.001)
    GPIO.add_event_detect(29, GPIO.FALLING, callback=I2C_Event)

# Nvidia Jetson Nano i2c Bus 0
bus = smbus.SMBus(0)

# Register number define
REG_CURMODE            =   0x00    # (W/R)
REG_JN_CORE_TEMP       =   0x01    # (W)
REG_AVG_WEIGHT         =   0x02    # (W/R)
REG_CUR_TOTAL_WEIGHT   =   0x03    # (R)
REG_CUR_JN_STAT        =   0xFE    # (W)
REG_SHUTDOWN_CMD       =   0xFF    # (R) Read this Reg will trigger Atmega send Shutdown command

# Mode define
MODE_NONE          =   0x00    # No mode is selected
MODE_MEASURE       =   0x01    # IN measuring mode
MODE_SLEEP         =   0x02
MODE_SHUTDOWN      =   0xFE

# Jetson Nano Status
JNSTAT_WORKWELL    =   0x00
JNSTAT_RESET       =   0x01    # Jetson Nano has been reseted once
JNSTAT_CAMERAFAIL  =   0x02
JNSTAT_WIFIFAIL    =   0x03

# This is the address we setup in the Arduino Program
GPIO.setwarnings(False)
address = 0x08
GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
GPIO.setup(29,GPIO.IN)
GPIO.add_event_detect(29, GPIO.FALLING, callback=I2C_Event)



def writeNumber(value):
    #bus.write_byte(address, value)
    bus.write_byte_data(address, 0, value)
    return -1

def readNumber(Cmd,NumBytes):
    number = bus.read_i2c_block_data(address,Cmd,NumBytes)
    # number = bus.read_byte_data(address, 1)
    return number
data = [0x0,MODE_MEASURE ]
bus.write_i2c_block_data(address, REG_CURMODE, data )

while True:

    #bus.write_byte_data(address, 0x15, 0x85)
    time.sleep(0.5)
    #number = readNumber(0x85,3)
    #print(number)
