# Author : Liwan, Huang
# Date : April, 2021
# This program must wire the 4 lines of spi2 (/dev/SPI1.1)

import spidev
import Jetson.GPIO as GPIO
import numpy as np
import time

class TMC2130():

    def __init__(self, En_PinIn, Dir_PinIn, Step_PinIn, busIn=0, deviceIn=0):

        # Import pin and bus setup from input
        self.En_Pin = En_PinIn
        self.Dir_Pin = Dir_PinIn
        self.Step_Pin = Step_PinIn
        self.bus = busIn
        self.device = deviceIn

        #Define the register address
        self.WriteFlag      =        (1<<7)
        self.ReadFlag       =        (0<<7)
        self.Reg_GCONF      =        0x00
        self.Reg_GSTAT      =        0x01
        self.Reg_IOIN       =        0x04
        self.Reg_IHOLD_IRUN =        0x10
        self.Reg_TPOWERDOWN =        0x11
        self.Reg_TSTEP      =        0x12
        self.Reg_TRWMTHRS   =        0x13
        self.Reg_CHOPCONF   =        0x6C
        self.Reg_DCCTRL     =        0x6D
        self.Reg_DRVSTAT    =        0x6F
        self.Reg_PWMCONF    =        0x70

        #Implement and set up he spi device object
        self.spi = spidev.SpiDev()
        self.spi.open(self.bus, self.device)  # SPI2---->MOSI:37pin (/dev/SPI1.1)
        self.spi.max_speed_hz = 1000000
        self.spi.mode = 0b11
        self.spi.lsbfirst = False


        #Setup GPIO configuration
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.En_Pin, GPIO.OUT, initial=GPIO.HIGH) #LOW -> active
        GPIO.setup(self.Dir_Pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.Step_Pin, GPIO.OUT, initial=GPIO.LOW)


    def __del__(self):
        self.Disable()

        GPIO.cleanup()
        self.spi.close()


    def Write(self,Reg,DatatoSend):

        # Write command
        Cmd = self.WriteFlag | Reg

        Data = np.uint32(DatatoSend)
        Data_byte1 = int((Data >> 24) & 0xFF)
        Data_byte2 = int((Data >> 16) & 0xFF)
        Data_byte3 = int((Data >> 8) & 0xFF)
        Data_byte4 = int((Data >> 0) & 0xFF)

        #combine the data to send in a list
        data1 = [Cmd,Data_byte1,Data_byte2,Data_byte3,Data_byte4]

        #Transmit the data via spi bus
        self.spi.xfer3(data1)

        # Check data is correctly sent
        if Reg == self.Reg_GCONF:
            time.sleep(0.1)
        Data_Check = self.Read(Reg)
        Data_Check = Data_Check & 0xFFFFFFFF
        #print ("Write Reg: " + "0x{:02X}".format(Reg) + " Data_Check: " + "0x{:08X}".format(Data_Check))


    def Read(self,Reg):

        # Write command
        Cmd = self.ReadFlag | Reg
        Data = 0
        ReadCmd = [Cmd,0x00,0x00,0x00,0x00] #sen Read command and register to read to TMC2130
        Data_read = self.spi.xfer3(ReadCmd)
        Data_read = list(Data_read)
        Data |= ( Data_read[0]<<32 |  Data_read[1]<<24 | Data_read[2] <<16 | Data_read[3] <<  8 | Data_read[4])
        return Data

    def Enable(self):

        GPIO.output(self.En_Pin, GPIO.LOW)
        print("Enable!")

    def Disable(self):

        GPIO.output(self.En_Pin, GPIO.HIGH)
        print("Disable!")

    def OneStep(self):

        GPIO.output(self.Step_Pin, GPIO.HIGH)
        time.sleep(10 / 1000000)
        GPIO.output(self.Step_Pin, GPIO.LOW)

    def set_bit (self, value, bit):

        return value | (1<<bit)

    def clear_bit(self, value, bit):

        return value & ~(1<<bit)

    def Shaft (self):

        #GPIO.output(self.Dir_Pin, not GPIO.input(Dir_Pin))
        Data_Reg_GCONF = self.Read(self.Reg_GCONF)
        #print(hex(Data_Reg_GCONF))
        Shaft_Status = bool((0x01) & (Data_Reg_GCONF)>>4 )
        #print(Shaft_Status)
        if(Shaft_Status):
            New_Data_Reg_GCONF = self.clear_bit(Data_Reg_GCONF, 4)
        else:
            New_Data_Reg_GCONF = self.set_bit(Data_Reg_GCONF, 4)
        self.Write( self.Reg_GCONF, New_Data_Reg_GCONF)
        print("Shaft!")

    def Is_Reset(self):
        return bool(self.Read(self.Reg_GSTAT) & (1<<0))

    def Reset(self):

        self.Write(self.Reg_GSTAT, 0x00000001)
        print("Reset!!")
        time.sleep(0.1)

    def Is_Enable_Stop_Enable(self):

        return bool(self.Read(self.Reg_GSTAT) & (1 << 15))

    def Enable_Stop_Enable(self): # Emergency Stop

        Data_Reg_GCONF = self.Read(self.Reg_GCONF)
        New_Data_Reg_GCONF = self.set_bit(Data_Reg_GCONF,15)
        self.Write(self.Reg_GCONF, New_Data_Reg_GCONF)
        print("Enable_Stop_Enable!")

    def Disable_Stop_Enable(self): # Cancel Emergency Stop

        Data_Reg_GCONF = self.Read(self.Reg_GCONF)
        New_Data_Reg_GCONF = self.clear_bit(Data_Reg_GCONF, 15)
        self.Write(self.Reg_GCONF, New_Data_Reg_GCONF)
        print("Disable_Stop_Enable!")

    def Emergency_Stop(self):

        self.Disable()
        self.Enable_Stop_Enable()

    def Cancel_Emergency_Stop(self):

        self.Disable_Stop_Enable()


if __name__ == "__main__":
    import time
    from threading import Timer
    En_Pin = 31
    Dir_Pin = 32
    Step_Pin = 33
    try:
        # Create the TMC2130 object
        MyTMC2130 = TMC2130(En_Pin,Dir_Pin,Step_Pin)
        time.sleep(0.1)

        # Reset the device if not reset
        if( MyTMC2130.Is_Reset()):
            MyTMC2130.Reset()

        # Set up the config of TMC2130
        MyTMC2130.Write(MyTMC2130.Reg_IHOLD_IRUN  , 0x00061F0A)   # IHOLD_IRUN: IHOLD=0x10, IRUN=0x31(max. current), IHOLDDELAY=6
        MyTMC2130.Write(MyTMC2130.Reg_CHOPCONF    , 0x080100C3)   # CHOPCONF: MicroStep: full, TOFF=3, HSTRT=4,HEND=2,TBL=0(speadCycle)
        MyTMC2130.Write(MyTMC2130.Reg_TPOWERDOWN  , 0x0000000A)   # TPOWERDOWN=10 #Delay before power down in stand still
        MyTMC2130.Write(MyTMC2130.Reg_TRWMTHRS    , 0x000001F4)   # TPWM_THRS=500 yields a switching velocity about 3500 = ca. 30RPM
        MyTMC2130.Write(MyTMC2130.Reg_PWMCONF     , 0x000401C8)   # PWM_CONF: AUTO=1, 2/1024 Fclk, Switch amplitude limit = 200, Grad=1
        MyTMC2130.Write(MyTMC2130.Reg_GCONF       , 0x00000005)   # EN_PWM_MODE=1, Voltage on AIN is current reference

        # Enable the Motor
        time.sleep(0.1)
        MyTMC2130.Enable()

        #Define Timers and the Events
        time.sleep(0.1)
        t1 = Timer(5,MyTMC2130.Shaft)
        t1.start()
        t2 = Timer(15,MyTMC2130.Shaft)
        t2.start()
        t3 = Timer(20,MyTMC2130.Emergency_Stop)
        t3.start()

        while True:
            #data = MyTMC2130.Read(MyTMC2130.Reg_GCONF)
            #print (hex(data))
            MyTMC2130.OneStep()
            time.sleep(0.001)


    except KeyboardInterrupt:
        print("Exiting Program")

    finally:
        MyTMC2130.__del__()
        pass


