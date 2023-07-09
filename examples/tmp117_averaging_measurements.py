# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_tmp117 import tmp117

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
tmp = tmp117.TMP117(i2c)

tmp.averaging_measurements = tmp117.AVERAGE_64X

while True:
    for averaging_measurements in tmp117.averaging_measurements_values:
        print("Current Averaging measurements setting: ", tmp.averaging_measurements)
        for _ in range(10):
            print(f"Temperature: {tmp.temperature:.2f}°C")
            print()
            time.sleep(0.5)
        tmp.averaging_measurements = averaging_measurements
