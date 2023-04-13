# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya

import time
from machine import Pin, I2C
import micropython_tmp117.tmp117 as tmp117

i2c = I2C(sda=Pin(8), scl=Pin(9))  # Correct I2C pins for UM FeatherS2
tmp = tmp117.TMP117(i2c)

for _ in range(3):
    temp = tmp.temperature
    print("Temperature: ", temp)
    print("----------")
    time.sleep(1)
