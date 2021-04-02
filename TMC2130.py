import spidev
import Jetson.GPIO as GPIO
import numpy as np
import time

class TMC2130():

    def __init__(self, En_PinIn, Dir_PinIn, Step_PinIn,CS_PinIn,busIn=0, deviceIn=0):

        # Import pin and bus setup from input
        self.En_Pin = En_PinIn
        self.Dir_Pin = Dir_PinIn
        self.Step_Pin = Step_PinIn
        self.bus = busIn
        self.device = deviceIn
        self.CS_Pin = CS_PinIn

        #Define the register address
        self.WriteFlag      =        (1<<7)
        self.ReadFlag       =        (0<<7)
        self.Reg_GCONF      =        0x00
        self.Reg_GSTAT      =        0x01
        self.Reg_IHOLD_IRUN =        0x10
        self.Reg_CHOPCONF   =        0x6C
        self.Reg_DCCTRL     =        0x6D
        self.Reg_DRVSTAT    =        0x6F

        # Implement spi device object
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
        GPIO.setup(self.CS_Pin, GPIO.OUT, initial=GPIO.HIGH)


    def __del__(self):
        self.spi.close()
        GPIO.cleanup()

    def Write(self,Cmd,DatatoSend):
        Data = np.uint32(DatatoSend)

        Data_byte1 = int((Data >> 24) & 0xFF)
        Data_byte2 = int((Data >> 16) & 0xFF)
        Data_byte3 = int((Data >> 8) & 0xFF)
        Data_byte4 = int((Data >> 0) & 0xFF)

        #combine the data to send in a list
        data1 = [Cmd,Data_byte1,Data_byte2,Data_byte3,Data_byte4]

        #Transmit the data via spi bus
        self.spi.xfer3(data1)


    def Read(self,Cmd):

        ReadCmd = [Cmd,0x00,0x00,0x00,0x00]
        self.spi.xfer3(ReadCmd)
        Data_read = self.spi.readbytes(4)


        return Data_read

    def Enable(self):
        GPIO.output(self.En_Pin, GPIO.LOW)

    def Disable(self):
        GPIO.output(self.En_Pin, GPIO.HIGH)

    def OneStep(self):
        GPIO.output(self.Step_Pin, GPIO.HIGH)
        time.sleep(1/1000000)
        GPIO.output(self.Step_Pin, GPIO.LOW)
        time.sleep(1 / 1000000)

    def Shaft (self):
        GPIO.output(self.Dir_Pin, not GPIO.input(Dir_Pin))
        #MyTMC2130.Write(MyTMC2130.WriteFlag | MyTMC2130.Reg_GCONF, 1<<4 | 0x00000001)

if __name__ == "__main__":
    def ChangeDir():
        MyTMC2130.Shaft()
        print ("Hello\n")

    import time
    from threading import Timer
    En_Pin = 31
    Dir_Pin = 32
    Step_Pin = 33
    CS_Pin = 15
    try:

        MyTMC2130 = TMC2130(En_Pin,Dir_Pin,Step_Pin,CS_Pin)
        MyTMC2130.Write(MyTMC2130.WriteFlag | MyTMC2130.Reg_GCONF, 0x00000001) # voltage on AIN is current reference
        MyTMC2130.Write(MyTMC2130.WriteFlag | MyTMC2130.Reg_IHOLD_IRUN, 0x00001010) #IHOLD=0x10, IRUN=0x10
        #MyTMC2130.Write(MyTMC2130.WriteFlag | MyTMC2130.Reg_CHOPCONF, 0x00008008)  # 256 microstep, MRERS=1=24, TBL=1=24,TOFF=8
        #MyTMC2130.Write(MyTMC2130.WriteFlag | MyTMC2130.Reg_CHOPCONF, 0x01008008)  # 128 microstep, MRERS=1=24, TBL=1=24,TOFF=8
        #MyTMC2130.Write(MyTMC2130.WriteFlag | MyTMC2130.Reg_CHOPCONF, 0x02008008)  # 64  microstep, MRERS=1=24, TBL=1=24,TOFF=8
        #MyTMC2130.Write(MyTMC2130.WriteFlag | MyTMC2130.Reg_CHOPCONF, 0x03008008)  # 32  microstep, MRERS=1=24, TBL=1=24,TOFF=8
        #MyTMC2130.Write(MyTMC2130.WriteFlag | MyTMC2130.Reg_CHOPCONF, 0x04008008)  # 16  microstep, MRERS=1=24, TBL=1=24,TOFF=8
        #MyTMC2130.Write(MyTMC2130.WriteFlag | MyTMC2130.Reg_CHOPCONF, 0x05008008)  # 08  microstep, MRERS=1=24, TBL=1=24,TOFF=8
        #MyTMC2130.Write(MyTMC2130.WriteFlag | MyTMC2130.Reg_CHOPCONF, 0x06008008)  # 04  microstep, MRERS=1=24, TBL=1=24,TOFF=8
        #MyTMC2130.Write(MyTMC2130.WriteFlag | MyTMC2130.Reg_CHOPCONF, 0x07008008)  # 02 microstep, MRERS=1=24, TBL=1=24,TOFF=8
        MyTMC2130.Write(MyTMC2130.WriteFlag | MyTMC2130.Reg_CHOPCONF, 0x08008008)  # 01 microstep, MRERS=1=24, TBL=1=24,TOFF=8

        time.sleep(0.1)
        MyTMC2130.Enable()
        t1 = Timer(5,ChangeDir)
        t2 = Timer(8, ChangeDir)
        t1.start()
        t2.start()
        while True:
            MyTMC2130.OneStep()
            time.sleep(0.001)


    finally:
        MyTMC2130.Disable()
        MyTMC2130.__del__()
        pass


