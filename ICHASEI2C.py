# Version : 20210906
# This program is to get link to the Upper board (AiWeighter_V2.0) via I2C

import smbus
import time
import Jetson.GPIO as GPIO
import numpy as np
import os
import requests

class JoeI2C:

    def __init__(self, address = 0x08,  busNum=0, ackPin=29):
        # Since the I2C protocol in Jetson nano just performs master mode, a ack pin is needed to tell arduino to read
        # something sent from jetson nano
        self.address = address
        self.busNum = busNum
        self.ackPin = ackPin
        # Nvidia Jetson Nano i2c Bus 0 (default)
        self.bus = smbus.SMBus(busNum)

        ##========================================== Definition ================================#
        # Register number define
        self.REG_CURMODE            =   0x00    # (W/R)
        self.REG_JN_CORE_TEMP       =   0x01    # (W)
        self.REG_AVG_WEIGHT         =   0x02    # (W/R)
        self.REG_CUR_TOTAL_WEIGHT   =   0x03    # (R)
        self.REG_OFFSET             =   0x04    # (R)
        self.REG_CAP_COUNT          =   0x05
        self.REG_CUR_JN_STAT        =   0xFE    # (W)
        self.REG_SHUTDOWN_CMD       =   0xFD    # (R) Read this Reg will trigger Atmega send Shutdown command

        # Mode define
        self.MODE_NONE              =   0x00    # No mode is selected
        self.MODE_MEASURE           =   0x01    # IN measuring mode
        self.MODE_SLEEP             =   0x02
        self.MODE_SHUTDOWN          =   0xFD

        #Cmd
        self.CMD_CONFIRM            =   0x65
        self.CMD_SHUTDOWN           =   0x15
        self.CMD_RESET              =   0x14
        self.CMD_READSTATUS         =   0x13
        self.CMD_CAP                =   0x12
        self.CMD_WIFIHOTSPOT         =  0x11

        # Jetson Nano Status
        self.JNSTAT_WORKWELL        =   0x00
        self.JNSTAT_RESET           =   0x01    # Jetson Nano has been reseted once
        self.JNSTAT_CAMERAFAIL      =   0x02
        self.JNSTAT_WIFIFAIL        =   0x03

        self.CurState               =   self.JNSTAT_WORKWELL
        self.isHotspotConnected     =   False

        # default address of Arduino is 0x08
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
        GPIO.setup(self.ackPin,GPIO.IN)
        GPIO.add_event_detect(self.ackPin, GPIO.FALLING, callback=self.I2C_Event)

        # Send msg to change the mode to MODE_MEASURE
        data = [0x00, self.MODE_MEASURE]
        self.bus.write_i2c_block_data(address, self.REG_CURMODE, data)


    def I2C_Event(self, channel):
        GPIO.remove_event_detect(self.ackPin)
        print("I2C Int!!")
        command = bytes(self.readNumber(self.REG_SHUTDOWN_CMD, 2))
        if command[0] == self.CMD_SHUTDOWN:
            print("Get Shutdown Cmd")
            if command[1] == self.CMD_CONFIRM:
                print("Shutdown!! Comfirmed ")
                time.sleep(3)
                os.system('shutdown -h now')
        elif command[0] == self.CMD_READSTATUS :
            if command[1] == self.CMD_CONFIRM:
                print("Check Status")
                data = [0x00, self.CurState ]
                self.bus.write_i2c_block_data(self.address, self.REG_CUR_JN_STAT, data )
        elif command[0] == self.CMD_CAP:
            if command[1] == self.CMD_CONFIRM:
                print("Capture!!")
                global is_Cap_request
                is_Cap_request = True
                #data = [0x00,0x65]
                #bus.write_i2c_block_data(address, REG_AVG_WEIGHT, data )
        elif command[0] == self.CMD_WIFIHOTSPOT:
            if command[1] == self.CMD_CONFIRM:
                if not self.isHotspotConnected:
                    print("Connect wifi hotspot")
                    os.system("nmcli connection up iChase")
                    self.isHotspotConnected = True
                else:
                    print("Disconnect wifi hotspot")
                    os.system("nmcli connection down iChase")
                    self.isHotspotConnected = False


        print("0x" + command.hex())
        time.sleep(0.001)
        GPIO.add_event_detect(self.ackPin, GPIO.FALLING, callback=self.I2C_Event)

    def writeNumber(self,Reg, value):
        #bus.write_byte(address, value)
        self.bus.write_byte_data(self.address, 0, value)
        return -1

    def readNumber(self, Cmd,NumBytes):
        number = self.bus.read_i2c_block_data(self.address, Cmd, NumBytes)
        # number = bus.read_byte_data(address, 1)
        return number

    def readWeight(self):
        Value = np.uint16(self.readNumber(self.REG_CUR_TOTAL_WEIGHT, 2))
        #print ("Value: " + "0x{:02X} ".format(Value[0]) + "0x{:02X} ".format(Value[1]))
        Temp = np.int16(((Value[0]<<8) & 0xFF00) | (Value[1] & 0x00FF))
        #print("Temp: " + str(Temp))
        Weight = float(Temp/100)
        #print("Weight :" + str(Weight))
        return Weight

    def writeAvgWeight(self, AvgWeight):
        #print("AvgWeight : " + str(AvgWeight))
        Data_toSend = np.uint16(AvgWeight*pow(10,2))
        #print("Data_toSend : " + str(Data_toSend))
        byte_High = int((Data_toSend>>8) & 0xFF)
        byte_Low = int((Data_toSend) & 0xFF)
        data = [byte_High, byte_Low]
        self.bus.write_i2c_block_data(self.address, self.REG_AVG_WEIGHT, data)
        print ("Value: " + "0x{:02X} ".format(byte_High) + "0x{:02X} ".format(byte_Low))
        
    def offset(self):
        success = self.readNumber(self.REG_OFFSET, 2)
        if success[0] == 0x13:
            if success[1] == 0x65:
                print("offset success!!") 

    def calibrate(self, value):
        Data_toSend = np.uint16(value*pow(10,2))
        #print("Data_toSend : " + str(Data_toSend))
        byte_High = int((Data_toSend>>8) & 0xFF)
        byte_Low = int((Data_toSend) & 0xFF)
        data = [byte_High, byte_Low]
        self.bus.write_i2c_block_data(self.address, self.REG_CALIB_WEIGHT, data)
        print ("Value: " + "0x{:02X} ".format(byte_High) + "0x{:02X} ".format(byte_Low))


if __name__ == "__main__":
    try:
        myI2C = JoeI2C()
        #myI2C.offset()
        #myI2C.calibrate(3.45)
        while True:
            #Weight = myI2C.readWeight()
            #print("Weight :" + str(Weight))
            #bus.write_byte_data(address, 0x15, 0x85)
            #time.sleep(0.1 )
            
            #number = readNumber(0x85,3)
            #print(number)
            timeout = 5
            url_test = "https://google.com"
            try:
                request = requests.get(url_test, timeout=timeout)
                print("Connected to the Internet")
                myI2C.CurState = myI2C.JNSTAT_CAMERAFAIL
            except (requests.ConnectionError, requests.Timeout) as exception:
                print("No internet connection.")
                myI2C.CurState = myI2C.JNSTAT_WIFIFAIL
                data = [0x00, myI2C.CurState ]
                myI2C.bus.write_i2c_block_data(myI2C.address, myI2C.REG_CUR_JN_STAT, data )
            time.sleep(1)

        # This is the address we setup in the Arduino Program


    except KeyboardInterrupt:
        print("Exiting Program")

    # except Exception as exception_error:
    #     print("Error occurred. Exiting Program")
    #     print("Error: " + str(exception_error))

    finally:
        # MySerial.Close()
        pass

