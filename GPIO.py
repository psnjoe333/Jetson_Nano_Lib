import Jetson.GPIO as GPIO
import time

output_pin = 15  #BOARD PIN = 12  BCM = 14

GPIO.setmode(GPIO.BOARD)
GPIO.setup(output_pin,GPIO.OUT, initial = GPIO.LOW)

while(1):
    GPIO.output(output_pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(output_pin, GPIO.LOW)
    time.sleep(1)

