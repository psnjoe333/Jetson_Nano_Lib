import Adafruit_PCA9685
import time


def set_servo_angle(channel, angle):
    date = (int)(587 + (angle - 0) * (1300 / 180))
    pwm.set_pwm(channel, 0, date)
    print("date = " + str(date))
    pwm.set_pwm_freq(200)
    # print(date)


pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)
pwm.set_pwm_freq(200)
time.sleep(.1)


set_servo_angle (0,0)
time.sleep(1)
set_servo_angle (0,90)
time.sleep(1)
set_servo_angle (0,180)