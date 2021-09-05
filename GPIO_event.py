import Jetson.GPIO as GPIO
import time

# Pin Definitions:
btn_pin = 37

def GPIO_event_Handler(channel):
    print(channel)
    print("INT!!")

# setting
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(btn_pin, GPIO.IN)
GPIO.add_event_detect(btn_pin, GPIO.FALLING, callback=GPIO_event_Handler, bouncetime=10)

while(1):
    print("1")
    time.sleep(0.01)

