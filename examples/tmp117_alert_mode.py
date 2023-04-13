# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya

import time
from machine import Pin, I2C
import micropython_tmp117.tmp117 as tmp117

i2c = I2C(sda=Pin(8), scl=Pin(9))  # Correct I2C pins for UM FeatherS2
tmp = tmp117.TMP117(i2c)

tmp.high_limit = 23
tmp.low_limit = 20

print("Alert mode:", tmp.alert_mode)
print("High limit", tmp.high_limit)
print("Low limit", tmp.low_limit)


while True:
    print("Temperature: %.2f degrees C" % tmp.temperature)
    alert_status = tmp.alert_status
    if alert_status.high_alert:
        print("Temperature above high set limit!")
    if alert_status.low_alert:
        print("Temperature below low set limit!")
    print("Low alert:", alert_status.low_alert)
    time.sleep(1)
