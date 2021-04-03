#!/usr/bin/python3
# type  "sudo chmod 777 /dev/ttyTHS1" to change the permisssion of ttyTHS1

import time
import serial

class JoeSerial:
    def __init__(self):

        self.serial_port = serial.Serial(
            port="/dev/ttyTHS1",
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
        )
        # Wait a second to let the port initialize
        time.sleep(1)

    def __del__(self):
        self.Close()

    def Close(self):
        self.serial_port.close()

    def ReadWeight(self):

            data_dec = float()
            data = self.serial_port.read(7)
            data_dec = float(data)
            #print("{:.2f}".format(data_dec))
            return data_dec
    def IsBusInWaiting(self):

        if MySerial.serial_port.inWaiting() > 0:
            return True
        else:
            return False
    def IsValidData(self):

        if self.serial_port.read() == b'=':
            return True
        else:
            return False

if __name__ == "__main__":
    try:
        MySerial = JoeSerial()
       # read data via UART
        while True:
            if MySerial.IsBusInWaiting():
                if MySerial.IsValidData():
                    Weight = MySerial.ReadWeight()
                    print("{:.2f}".format(Weight))
                else:
                    continue

    except KeyboardInterrupt:
        print("Exiting Program")

    except Exception as exception_error:
        print("Error occurred. Exiting Program")
        print("Error: " + str(exception_error))

    finally:
        MySerial.Close()
        pass