from TMC2130 import TMC2130
import time
from threading import Timer

D1_En_Pin = 31
D1_Dir_Pin = 32
D1_Step_Pin = 33
D2_En_Pin = 22
D2_Dir_Pin = 16
D2_Step_Pin = 18
try:
    # Create the TMC2130 object
    MyTMC2130_1 = TMC2130(D1_En_Pin, D1_Dir_Pin, D1_Step_Pin, 0, 0)
    MyTMC2130_2 = TMC2130(D2_En_Pin, D2_Dir_Pin, D2_Step_Pin, 0, 1)
    time.sleep(0.1)
    #MyTMC2130_1.Enable_Stop_Enable()
    #MyTMC2130_2.Enable_Stop_Enable()
    # Reset the device if not reset
    if (MyTMC2130_1.Is_Reset()):
        MyTMC2130_1.Reset()
    if (MyTMC2130_2.Is_Reset()):
        MyTMC2130_2.Reset()

    time.sleep(0.1)
    # Set up the config of TMC2130
    MyTMC2130_2.Write(MyTMC2130_2.Reg_GCONF, 0x00000004)  # EN_PWM_MODE=1
    MyTMC2130_2.Write(MyTMC2130_2.Reg_IHOLD_IRUN, 0x00001209)  # IHOLD_IRUN: IHOLD=9, IRUN=31(max), IHOLDDELAY=0
    MyTMC2130_2.Write(MyTMC2130_2.Reg_TPOWERDOWN, 0x0000000A)  # TPOWERDOWN=00 #Delay before power down in stand still
    MyTMC2130_2.Write(MyTMC2130_2.Reg_TRWMTHRS, 0x00000000)
    MyTMC2130_2.Write(MyTMC2130_2.Reg_TCOOLTHRS, 0x00000000)
    MyTMC2130_2.Write(MyTMC2130_2.Reg_THIGH, 0x00000000)
    MyTMC2130_2.Write(MyTMC2130_2.Reg_XDIRECT, 0x00000000)
    MyTMC2130_2.Write(MyTMC2130_2.Reg_VDCMIN, 0x00000000)
    MyTMC2130_2.Write(MyTMC2130_2.Reg_CHOPCONF, 0x08028008)  # CHOPCONF: MicroStep: full, TOFF=?, HSTRT=?,HEND=?,TBL=36(speadCycle)
    MyTMC2130_2.Write(MyTMC2130_2.Reg_COOLCONF, 0x00000000)
    # MyTMC2130_2.Write(MyTMC2130_2.Reg_TRWMTHRS  , 0x000001F4)   # TPWM_THRS=500 yields a switching velocity about 3500 = ca. 30RPM
    MyTMC2130_2.Write(MyTMC2130_2.Reg_PWMCONF,  0x00050480)  # PWM_CONF: AUTO=?, ? Fclk, Switch amplitude limit = ?, Grad=?
    MyTMC2130_2.Write(MyTMC2130_2.Reg_ENCM_CTRL, 0x00000000)
    MyTMC2130_2.Write(MyTMC2130_2.Reg_GCONF, 0x00000004)  # EN_PWM_MODE=1, Voltage on AIN is current reference
    time.sleep(0.1)

    # Set up the config of TMC2130
    MyTMC2130_1.Write(MyTMC2130_1.Reg_GCONF, 0x00000004)  # EN_PWM_MODE=1
    MyTMC2130_1.Write(MyTMC2130_1.Reg_IHOLD_IRUN, 0x00001209)  # IHOLD_IRUN: IHOLD=9, IRUN=31(max), IHOLDDELAY=0
    MyTMC2130_1.Write(MyTMC2130_1.Reg_TPOWERDOWN, 0x0000000A)  # TPOWERDOWN=00 #Delay before power down in stand still
    MyTMC2130_1.Write(MyTMC2130_1.Reg_TRWMTHRS, 0x00000000)
    MyTMC2130_1.Write(MyTMC2130_1.Reg_TCOOLTHRS, 0x00000000)
    MyTMC2130_1.Write(MyTMC2130_1.Reg_THIGH, 0x00000000)
    MyTMC2130_1.Write(MyTMC2130_1.Reg_XDIRECT, 0x00000000)
    MyTMC2130_1.Write(MyTMC2130_1.Reg_VDCMIN, 0x00000000)
    MyTMC2130_1.Write(MyTMC2130_1.Reg_CHOPCONF, 0x08028008)  # CHOPCONF: MicroStep: full, TOFF=?, HSTRT=?,HEND=?,TBL=36(speadCycle)
    MyTMC2130_1.Write(MyTMC2130_1.Reg_COOLCONF, 0x00000000)
    #MyTMC2130_1.Write(MyTMC2130_1.Reg_TRWMTHRS    , 0x000001F4)   # TPWM_THRS=500 yields a switching velocity about 3500 = ca. 30RPM
    MyTMC2130_1.Write(MyTMC2130_1.Reg_PWMCONF, 0x00050480)  # PWM_CONF: AUTO=?, ? Fclk, Switch amplitude limit = ?, Grad=?
    MyTMC2130_1.Write(MyTMC2130_1.Reg_ENCM_CTRL, 0x00000000)
    MyTMC2130_1.Write(MyTMC2130_1.Reg_GCONF, 0x00000004)  # EN_PWM_MODE=1, Voltage on AIN is current reference


    # Enable the Motor
    time.sleep(0.1)
    MyTMC2130_1.Enable()
    time.sleep(0.1)
    MyTMC2130_2.Enable()
    time.sleep(0.1)

    # Define Timers and the Events
    time.sleep(0.1)
    t1 = Timer(5, MyTMC2130_1.Shaft)
    t1.start()
    t2 = Timer(15, MyTMC2130_1.Shaft)
    t2.start()
    t3 = Timer(20, MyTMC2130_1.Emergency_Stop)
    t3.start()

    while True:
        # data = MyTMC2130_1.Read(MyTMC2130_1.Reg_GCONF)

        # print (hex(data))
        MyTMC2130_2.OneStep()
        MyTMC2130_1.OneStep()
        time.sleep(0.005)
        #DRVSTAT = MyTMC2130_1.Read(MyTMC2130_1.Reg_DRVSTAT)
        #print("Read Reg: " + "0x{:02X}".format(MyTMC2130_1.Reg_DRVSTAT) + " DRVSTAT: " + "0x{:08X}".format(DRVSTAT))



except KeyboardInterrupt:
    print("Exiting Program")

finally:
    MyTMC2130_1.__del__()
    pass

