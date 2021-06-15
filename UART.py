#!/usr/bin/python3
# type  "sudo chmod 777 /dev/ttyTHS1" to change the permisssion of ttyTHS1 temporary
# type "sudo usermod -aGdialout [Username]" to get permanent permission

import time
import serial

class JoeSerial:
    def __init__(self):

        self.serial_port = serial.Serial(
            port="/dev/ttyTHS1",
            #port="/dev/ttyUSB0",
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


if __name__ == "__main__":
    try:
        MySerial = JoeSerial()
        i=-00.150

       # read data via UART
        while True:
            print_data = round(i, 2)
            #MySerial.serial_port.write("B".encode("ASCII"))
            MySerial.serial_port.write((str(print_data)+"\n\r").encode('utf-8'))
            time.sleep(0.5)
            #MySerial.serial_port.write("\n".encode('utf-8'))
            #time.sleep(2)
            if MySerial.serial_port.inWaiting() > 0:
                    ReadString=(MySerial.serial_port.read())
                    print(ReadString)
                    #MySerial.serial_port.writelines(ReadString)
                    #MySerial.serial_port.write("\r\n".encode('utf-8'))

            i = i+0.01
    except KeyboardInterrupt:
        print("Exiting Program")

    except Exception as exception_error:
        print("Error occurred. Exiting Program")
        print("Error: " + str(exception_error))

    finally:
        #MySerial.Close()
        pass