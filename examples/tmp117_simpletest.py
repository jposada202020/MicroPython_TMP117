# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya

import time
from machine import Pin, I2C
from micropython_tmp117 import tmp117

i2c = I2C(sda=Pin(8), scl=Pin(9))  # Correct I2C pins for UM FeatherS2
tmp = tmp117.TMP117(i2c)

while True:
    print(f"Temperature: {tmp.temperature:.2f}°C")
    print("----------")
    time.sleep(1)
