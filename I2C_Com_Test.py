# Version : 20210906
# This program is to get link to the Upper board (AiWeighter_V2.0) via I2C

import smbus
import time
import Jetson.GPIO as GPIO
import os
import os

class JoeI2C:
    def __init__(self, address = 0x08,  busNum=0, ackPin=29):
        # Since the I2C protocol in Jetson nano just performs master mode, a ack pin is needed to tell arduino to read
        # something sent from jetson nano
        self.address = address
        self.busNum = busNum
        self.ackPin = ackPin
        # Nvidia Jetson Nano i2c Bus 0 (default)
        self.bus = smbus.SMBus(busNum)
        # default address of Arduino is 0x08
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
        GPIO.setup(self.ackPin,GPIO.IN)
        GPIO.add_event_detect(self.ackPin, GPIO.FALLING, callback=self.I2C_Event)

        ##========================================== Definition ================================#
        # Register number define
        self.REG_CURMODE        =   0x00    # (W/R)
        self.REG_JN_CORE_TEMP   =   0x01    # (W)
        self.REG_AVG_WEIGHT     =   0x02    # (W/R)
        self.REG_SHUTDOWN_CMD   =   0xFF    # (R) Read this Reg will trigger Atmega send Shutdown command

        # Mode define
        self.MODE_NONE          =   0x00    # No mode is selected
        self.MODE_MEASURE       =   0x01    # IN measuring mode
        self.MODE_SLEEP         =   0x02
        self.MODE_SHUTDOWN      =   0xFE

        # Jetson Nano Status
        self.JNSTAT_WORKWELL    =   0x00
        self.JNSTAT_RESET       =   0x01    # Jetson Nano has been reseted once
        self.JNSTAT_CAMERAFAIL  =   0x02
        self.JNSTAT_WIFIFAIL    =   0x03


    def I2C_Event(self, channel):
        GPIO.remove_event_detect(self.ackpin)
        print("I2C Int!!")
        command = bytes(self.readNumber(self.REG_SHUTDOWN_CMD,3))
        if command[0] == 0x15:
            if command[1] == 0x18:
                if command[2] == 0x65:
                    print("shutdown!!")
                    time.sleep(3)
                    os.system('shutdown -h now')

        print("0x" + command.hex())
        time.sleep(0.001)
        GPIO.add_event_detect(self.ackPin, GPIO.FALLING, callback=self.I2C_Event)

    def writeNumber(self,Reg, value):
        #bus.write_byte(address, value)
        self.bus.write_byte_data(self.address,0,value)
        return -1

    def readNumber(self, Cmd,NumBytes):
        number = self.bus.read_i2c_block_data(self.address,Cmd,NumBytes)
        # number = bus.read_byte_data(address, 1)
        return number
if __name__ == "__main__":
    try:
        myI2C = JoeI2C()
        myI2C.bus.write_byte_data(0x00, 0x02)
        while True:

            #bus.write_byte_data(address, 0x15, 0x85)
            time.sleep(0.5)
            #number = readNumber(0x85,3)
            #print(number)

        # This is the address we setup in the Arduino Program


    except KeyboardInterrupt:
        print("Exiting Program")

    except Exception as exception_error:
        print("Error occurred. Exiting Program")
        print("Error: " + str(exception_error))

    finally:
        # MySerial.Close()
        pass

