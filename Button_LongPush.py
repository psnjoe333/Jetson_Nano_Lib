import Jetson.GPIO as GPIO
from threading import Timer

BTN_STATE_PUSH = 1
BTN_STATE_NO_PUSH = -1
DEFALT_BYN_STATE = BTN_STATE_NO_PUSH

def detect_power_button():

