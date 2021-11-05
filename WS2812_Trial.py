#Ref: https://qiita.com/seitomatsubara/items/dfe7e353879c37d5569c

from typing import Sequence
import spidev
import sys

class SPItoWS():
    RGB_RED = [255,0,0]
    RGB_ORANGE = [255,97,0]
    RGB_YELLOW = [255,255,0]
    RGB_GREEN = [0,255,0]
    RGB_BLUE = [0,0,255]
    RGB_INDIGO = [111,0,255]
    RGB_PURPLE = [255,0,255]
    RGB_VOID = [0,0,0]

    def __init__(self, ledc):

        self.led_count = ledc

        self.X = ''  # X is signal of WS281x
        for i in range(self.led_count):
            self.X = self.X + "100100100100100100100100100100100100100100100100100100100100100100100100"
        self.spi = spidev.SpiDev()
        self.spi.open(1, 1)  # SPI2---->MOSI:37pin (/dev/SPI1.1)
        self.spi.max_speed_hz = 2400000

    def __init__(self, ledc , busIn=1, deviceIn=1):

        self.led_count = ledc
        self.bus = busIn
        self.device = deviceIn
        self.X = '' # X is signal of WS281x
        for i in range(self.led_count):
            self.X = self.X + "100100100100100100100100100100100100100100100100100100100100100100100100"
        self.spi = spidev.SpiDev()
        self.spi.open(self.bus, self.device)     #SPI2---->MOSI:37pin (/dev/SPI1.1)
        self.spi.max_speed_hz = 2400000

    def __del__(self):
        self.spi.close()

    def _Bytesto3Bytes(self, num, RGB): # num is number of signal, RGB is 8 bits (1 byte) str
        for i in range(8):
            if RGB[i] == '0':
                self.X = self.X[:num * 3 * 8 + i * 3] + '100' + self.X[num * 3 * 8 + i * 3 + 3:]
            elif RGB[i] == '1':
                self.X = self.X[:num * 3 * 8 + i * 3] + '110' + self.X[num * 3 * 8 + i * 3 + 3:]

    def _BytesToHex(self, Bytes):
        return ''.join(["0x%02X " % x for x in Bytes]).strip()

    def LED_show(self):
            Y = []
            for i in range(self.led_count * 9):
                Y.append(int(self.X[i*8:(i+1)*8],2))
            WS = self._BytesToHex(Y)
            self.spi.xfer3(Y, 2400000,0,8)

    def RGBto3Bytes(self, led_num, R, G, B):
        if (R > 255 or G > 255 or B > 255):
            print("Invalid Value: RGB is over 255\n")
            sys.exit(1)
        if (led_num > self.led_count - 1):
            print("Invalid Value: The number is over the number of LED")
            sys.exit(1)
        RR = format(R, '08b')
        GG = format(G, '08b')
        BB = format(B, '08b')
        self._Bytesto3Bytes(led_num * 3, GG)
        self._Bytesto3Bytes(led_num * 3 + 1, RR)
        self._Bytesto3Bytes(led_num * 3 + 2, BB)

    def LED_OFF_ALL(self):
        self.X = ''
        for i in range(self.led_count):
            self.X = self.X + "100100100100100100100100100100100100100100100100100100100100100100100100"
        self.LED_show()

    def Set_Color_RGB(self, led_num, R, G, B):
        if R>255  : R = 255
        if G>255 : G = 255
        if B>255 : B = 255
        if R<0 : R = 0
        if G<0 : G = 0
        if B<0 : B = 0 
        self.RGBto3Bytes(led_num, R, G, B)

    def Set_Color(self, led_num, RGB):
        R = RGB[0]
        G = RGB[1]
        B = RGB[2]
        self.Set_Color_RGB(led_num, R, G, B)
    
    def Show_Color(self, RGB):
        for i in range(self.led_count):
            self.Set_Color(RGB)
        self.LED_show()

    def Turn_off_slowly(self, CurR, CurG, CurB, Step,delay_swith):
        if Step < 0: Step = Step
        d_R = int(CurR/Step)
        R_R = CurR - d_R*Step
        d_G = int(CurG/Step)
        R_G = CurG - d_G*Step
        d_B = int(CurB/Step)
        R_B = CurB - d_B*Step        
        for i in range(Step):
            if not R_R==0 : 
                CurR = CurR - d_R - 1
                R_R = R_R-1
            else:CurR = CurR - d_R 

            if not R_G ==0 : 
                CurG = CurG - d_G - 1
                R_G = R_G-1
            else : CurG = CurG - d_G 

            if not R_B ==0 : 
                CurB = CurB - d_B - 1
                R_B = R_B-1
            else : CurB = CurB - d_B
            # print('CurR : ', CurR)
            # print('CurG : ', CurG)
            # print('CurB : ', CurB)
            for i in range(self.led_count):                
                self.Set_Color_RGB(i, CurR, CurG, CurB)
                time.sleep(delay_swith)
            self.LED_show()
    
    def Show_Slowly(self, FinR, FinG, FinB, Step,delay_swith):
        if Step < 0: Step = Step
        d_R = int(FinR/Step)
        R_R = FinR - d_R*Step
        d_G = int(FinG/Step)
        R_G = FinG - d_G*Step
        d_B = int(FinB/Step)
        R_B = FinB - d_B*Step      
        CurR = CurG = CurB = 0
        for i in range(Step):
            if not R_R==0 : 
                CurR = CurR + d_R + 1
                R_R = R_R-1
            else: CurR = CurR + d_R 

            if not R_G ==0 : 
                CurG = CurG + d_G + 1
                R_G = R_G-1
            else : CurG = CurG + d_G 

            if not R_B ==0 : 
                CurB = CurB + d_B + 1
                R_B = R_B-1
            else : CurB = CurB + d_B
            # print('CurR : ', CurR)
            # print('CurG : ', CurG)
            # print('CurB : ', CurB)
            for i in range(self.led_count):                
                self.Set_Color_RGB(i, CurR, CurG, CurB)
                time.sleep(delay_swith)
            self.LED_show()
    
    def Show_Breath_RGB(self, R, G, B, Step_Show=50, Step_Off=50,delay_open=1, delay_close = 1,delay_swith=0.0001):
        self.Show_Slowly(R, G, B, Step_Show,delay_swith)
        time.sleep(delay_open)
        self.Turn_off_slowly(R, G, B, Step_Off,delay_swith)
        time.sleep(delay_close)

    def Show_Breath(self, RGB, Step_Show=50, Step_Off=50,delay_open=1,delay_swith=0.0001):
        self.Show_Breath_RGB( RGB[0], RGB[1], RGB[2], Step_Show, Step_Off,delay_open,delay_swith)
        
    def Show_Meteor(self, circle_count):
        Array_Meteor = [self.RGB_RED,self.RGB_ORANGE,self.RGB_YELLOW, self.RGB_GREEN, self.RGB_BLUE, self.RGB_INDIGO, self.RGB_PURPLE,self.RGB_VOID]
        Array_Update = [0]*( len(Array_Meteor))
        Array_temp  = [0]*( len(Array_Meteor))
        Cur_Pos = 0
        for circle in range (circle_count):
            for update_count in range(self.led_count+len(Array_Meteor)):
                if Cur_Pos < len(Array_Update):
                    for Cur_Cell_Count in range(Cur_Pos+1):
                        Array_Update[Cur_Cell_Count] = Cur_Pos - Cur_Cell_Count 
                    Cur_Pos = Cur_Pos +1           
                elif Cur_Pos >= len(Array_Update) and Cur_Pos < self.led_count: 
                    for Cur_Cell_Count in range(len(Array_Update)):
                        Array_Update[Cur_Cell_Count] = Cur_Pos - Cur_Cell_Count 
                    Cur_Pos = Cur_Pos +1
                elif  Cur_Pos >= self.led_count and Cur_Pos <=self.led_count+len(Array_Meteor) :
                    Num_2Update = update_count - Cur_Pos
                    for Cur_Cell_Count in range(Num_2Update,len(Array_Update) ):
                        Array_Update[Cur_Cell_Count] = update_count - Cur_Cell_Count-1

                if update_count == self.led_count+len(Array_Meteor) - 1:
                    Cur_Pos = 0

                for i in range(len(Array_Update)):
                    self.Set_Color(Array_Update[i], Array_Meteor[i])            
                self.LED_show()                
                time.sleep(0.05)
            

if __name__ == "__main__":
    import time
    LED_COUNT = 24
    sig = SPItoWS(LED_COUNT)
    while(True):
        RGB = [255,50,0]
        #sig.Show_Breath(sig.RGB_ORANGE,delay_swith=0.01)
        #sig.Show_Slowly(R,G,B,50)
        # for LED_NUM in range(LED_COUNT):
        #     sig.RGBto3Bytes(LED_NUM, 255, 255, 255)
        #     sig.LED_show()
        #     time.sleep(.1)
        #sig.LED_OFF_ALL()
        #sig.Turn_off_slowly(R,G,B,50)
        time.sleep(0.1)
        sig.Show_Meteor(4)
        quit()
