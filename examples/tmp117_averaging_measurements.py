# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya

import time
from machine import Pin, I2C
import micropython_tmp117.tmp117 as tmp117

i2c = I2C(sda=Pin(8), scl=Pin(9))  # Correct I2C pins for UM FeatherS2
tmp = tmp117.TMP117(i2c)

tmp.averaging_measurements = tmp117.AVERAGE_64X
print("Averaging Measuremens:  ", tmp.averaging_measurements)

while True:
    print("Single measurement: %.2f C" % tmp.temperature)
    for i in range(10):
        print("One Shot Measurement mode: ", tmp.measurement_mode)
        print("Temperature: ", tmp.temperature)
        time.sleep(1)
    tmp117.measurement_mode = tmp117.CONTINUOUS_CONVERSION_MODE
    for i in range(10):
        print("Temperature: ", tmp.temperature)
        print("Continuos Measurement Mode: ", tmp.measurement_mode)
        time.sleep(1)
