import time
import numpy as np
import Adafruit_MCP4725
import math
import smbus


DAC_X = Adafruit_MCP4725.MCP4725(address=0x60, busnum=0)
DAC_Y = Adafruit_MCP4725.MCP4725(address=0x61, busnum=0)
amplitude = 50
toprange = 500
data_x = list()
data_y = list()



offset_x = 1050
offset_y = 1050

for t in np.arange(0, 2 * math.pi, 0.1):
    size_x = toprange / (2 * amplitude)
    size_y = toprange / (2 * amplitude)

    x = amplitude * math.cos(t)
    y = amplitude * math.sin(t)
    new_x = offset_x + x * size_x
    new_y = offset_y + y * size_y

    # new_x = offset
    # new_y = offset

    print(new_y)
    data_x.append(new_x)
    data_y.append(new_y)



while True:
    for num in range(len(data_x)):
        DAC_X.set_voltage(int(data_x[num]))
        DAC_Y.set_voltage(int(data_y[num]))
        #time.sleep(0.0000001)