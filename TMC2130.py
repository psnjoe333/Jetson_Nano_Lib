import spidev
import Jetson.GPIO as GPIO
import numpy as np

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
        GPIO.setup(self.En_Pin, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.Dir_Pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.Step_Pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.CS_Pin, GPIO.OUT, initial=GPIO.HIGH)


    def __del__(self):
        self.spi.close()
        GPIO.cleanup()

    def Write(self,Cmd,DataIn):
        Data = np.uint32(DataIn)

        Data_byte1 = int((Data >> 24) & 0xFF)
        Data_byte2 = int((Data >> 16) & 0xFF)
        Data_byte3 = int((Data >> 8) & 0xFF)
        Data_byte4 = int((Data >> 0) & 0xFF)

        #combine the data to send in a list
        data1 = [Cmd,Data_byte1,Data_byte2,Data_byte3,Data_byte4]

        #Transmit the data via spi bus
        GPIO.output(self.CS_Pin, GPIO.LOW)
        self.spi.xfer3(data1)
        GPIO.output(self.CS_Pin, GPIO.HIGH)


if __name__ == "__main__":
    import time
    En_Pin = 31
    Dir_Pin = 32
    Step_Pin = 33
    CS_Pin = 36
    MyTMC2130 = TMC2130(En_Pin,Dir_Pin,Step_Pin,CS_Pin)

    while True:
        TestData = 0x85154855
        MyTMC2130.Write(MyTMC2130.WriteFlag | MyTMC2130.Reg_GCONF,TestData)

