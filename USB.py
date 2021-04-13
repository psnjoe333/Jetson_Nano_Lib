#!/usr/bin/python3
# type  "sudo chmod 777 /dev/ttyTHS1" to change the permisssion of ttyTHS1 temporary
# type "sudo usermod -aGdialout [Username]" to get permanent permission

# ===== How to reset USB port on Jetson =======#
#Check USB device:
#   sudo dmesg -c
#Run the following command to enable read/write options for the usb bind and unbind files:
#   sudo chmod 666 /sys/bus/usb/drivers/usb/bind
#   sudo chmod 666 /sys/bus/usb/drivers/usb/unbind
#Verify correct permissions are enabled by running the following command:
#   ls -lha /sys/bus/usb/drivers/usb/bind
#   ls -lha /sys/bus/usb/drivers/usb/unbind
#You will get an output similar to the following:
#   -rw-rw-rw- 1 root root 4,0K mar 26 16:25 /sys/bus/usb/drivers/usb/bind
#   -rw-rw-rw- 1 root root 4,0K mar 26 16:25 /sys/bus/usb/drivers/usb/unbind
#Once the device is in the condition where it needs to be reset, using the device ID we found on Identifying the USB device run the following commands:
#(in my case is USB 1-2.3)
#   echo "1-2.3" | sudo tee /sys/bus/usb/drivers/usb/unbind
#   echo "1-2.3" | sudo tee /sys/bus/usb/drivers/usb/bind


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