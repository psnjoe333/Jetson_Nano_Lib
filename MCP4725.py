import time
import numpy as np
import Adafruit_MCP4725
import math
import smbus


DAC_X = Adafruit_MCP4725.MCP4725(address=0x60, busnum=0)
DAC_Y = Adafruit_MCP4725.MCP4725(address=0x62, busnum=0)
amplitude = 10
toprange = 100
data_x = list()
data_y = list()
offset = 1560

for x in np.arange(0 , 2*math.pi , 0.1):

    size_x = toprange / (2*math.pi)
    size_y = toprange / (2*amplitude)

    y = amplitude * math.sin(x)
    #new_x = offset + x*size_x
    #new_y = offset + y*size_y

    new_x = offset
    new_y = offset

    print(new_y)
    data_x.append(new_x)
    data_y.append(new_y)

for x in np.arange(2 * math.pi , 0, -0.1):
    size_x = toprange / (2 * math.pi)
    size_y = -toprange / (2 * amplitude)
    y = amplitude * math.sin(x)

    #new_x = offset + x * size_x
    #new_y = offset + y * size_y

    new_x = offset
    new_y = offset

    print(new_y)
    data_x.append(new_x)
    data_y.append(new_y)

while True:
    for num in range(len(data_x)):
        DAC_X.set_voltage(int(data_x[num]))
        DAC_Y.set_voltage(int(data_y[num]))
        #time.sleep(0.00000001)