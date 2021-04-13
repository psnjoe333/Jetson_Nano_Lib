#!/usr/bin/python3
# type  "sudo chmod 777 /dev/ttyTHS1" to change the permisssion of ttyTHS1 temporary
# type "sudo usermod -aGdialout [Username]" to get permanent permission

import time
import serial

class JoeSerial:
    def __init__(self):

        self.serial_port = serial.Serial(
            #port="/dev/ttyTHS1",
            port="/dev/ttyUSB0",
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
        )
        # Wait a second to let the port initialize
        time.sleep(1)


if __name__ == "__main__":
    try:
        MySerial = JoeSerial()
       # read data via UART
        while True:
            if MySerial.serial_port.inWaiting() > 0:
                    data =MySerial.serial_port.read()
                    print(data)
                    MySerial.serial_port.write("recieve:".encode('utf-8'))
                    MySerial.serial_port.write(data)
                    MySerial.serial_port.write("\r\n".encode('utf-8'))

    except KeyboardInterrupt:
        print("Exiting Program")

    except Exception as exception_error:
        print("Error occurred. Exiting Program")
        print("Error: " + str(exception_error))

    finally:
        #MySerial.Close()
        pass