# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`tmp117`
================================================================================

MicroPython Driver for the TMP117 temperature sensor


* Author(s): Jose D. Montoya

Implementation Notes
--------------------

**Software and Dependencies:**

This library depends on Micropython

"""

# pylint: disable=unused-argument, too-many-arguments

import time
from micropython import const

try:
    import struct
except ImportError:
    import ustruct as struct


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/micropython_TMP117.git"

_REG_WHOAMI = const(0x0F)
_TEMP_RESULT = const(0x00)
_CONFIGURATION = const(0x01)

_CONTINUOUS_CONVERSION_MODE = const(0b00)  # Continuous Conversion Mode
_ONE_SHOT_MODE = const(0b11)  # One Shot Conversion Mode
_SHUTDOWN_MODE = const(0b01)  # Shutdown Conversion Mode

_TMP117_RESOLUTION = const(0.0078125)


class CBits:
    """
    Changes bits from a byte register
    """

    def __init__(
        self,
        num_bits: int,
        register_address: int,
        start_bit: int,
        register_width=1,
        lsb_first=True,
    ) -> None:
        self.bit_mask = ((1 << num_bits) - 1) << start_bit
        self.register = register_address
        self.star_bit = start_bit
        self.lenght = register_width
        self.lsb_first = lsb_first

    def __get__(
        self,
        obj,
        objtype=None,
    ) -> int:

        mem_value = obj._i2c.readfrom_mem(obj._address, self.register, self.lenght)

        reg = 0
        order = range(len(mem_value) - 1, -1, -1)
        if not self.lsb_first:
            order = reversed(order)
        for i in order:
            reg = (reg << 8) | mem_value[i]

        reg = (reg & self.bit_mask) >> self.star_bit

        return reg

    def __set__(self, obj, value: int) -> None:

        memory_value = obj._i2c.readfrom_mem(obj._address, self.register, self.lenght)

        reg = 0
        order = range(len(memory_value) - 1, -1, -1)
        if not self.lsb_first:
            order = range(0, len(memory_value))
        for i in order:
            reg = (reg << 8) | memory_value[i]
        reg &= ~self.bit_mask

        value <<= self.star_bit
        reg |= value
        reg = reg.to_bytes(self.lenght, "big")

        obj._i2c.writeto_mem(obj._address, self.register, reg)


class RegisterStruct:
    """
    Register Struct
    """

    def __init__(self, register_address: int, form: str, lenght=1) -> None:
        self.format = form
        self.register = register_address
        self.lenght = struct.calcsize(form)

    def __get__(
        self,
        obj,
        objtype=None,
    ):

        if self.lenght <= 2:
            value = struct.unpack(
                self.format,
                memoryview(
                    obj._i2c.readfrom_mem(obj._address, self.register, self.lenght)
                ),
            )[0]
        else:
            value = struct.unpack(
                self.format,
                memoryview(
                    obj._i2c.readfrom_mem(obj._address, self.register, self.lenght)
                ),
            )
        return value

    def __set__(self, obj, value):

        obj._i2c.writeto_mem(obj._address, self.register, bytes([value]))


class TMP117:
    """Main class for the Sensor

    :param ~machine.I2C i2c: The I2C bus the TMP117 is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x48`

    :raises RuntimeError: if the sensor is not found


    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`TMP117` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        from machine import Pin, I2C
        import tmp117

    Once this is done you can define your `machine.I2C` object and define your sensor object

    .. code-block:: python

        i2c = I2C(sda=Pin(8), scl=Pin(9))
        tmp117 = tmp117.TMP117(i2c)

    Now you have access to the :attr:`temperature` attribute

    .. code-block:: python

        temp = tmp117.temperature

    """

    _device_id = RegisterStruct(_REG_WHOAMI, ">H")
    _configuration = RegisterStruct(_CONFIGURATION, ">H")
    _raw_temperature = RegisterStruct(_TEMP_RESULT, ">h")

    # Register 0x01
    # HIGH_Alert|LOW_Alert|Data_Ready|EEPROM_Busy| MOD1(2) |   MOD0(1)    | CONV2(1) |CONV1(1)
    # ----------------------------------------------------------------------------------------
    # CONV0(1)  | AVG1(1) |AVG0(1)   |T/nA(1)    |POL(1)   |DR/Alert(1)   |Soft_Reset|   —
    _data_ready = CBits(1, _CONFIGURATION, 13, 2, False)
    _mode = CBits(2, _CONFIGURATION, 10, 2, False)
    _soft_reset = CBits(1, _CONFIGURATION, 1, 2, False)

    def __init__(self, i2c, address=0x48):
        self._i2c = i2c
        self._address = address

        if self._device_id != 0x117:
            raise RuntimeError("Failed to find TMP117!")

        self._reset = True

        self._mode = _CONTINUOUS_CONVERSION_MODE
        while not self._data_ready:
            time.sleep(0.001)
        self._read_temperature()

    def _read_temperature(self):
        return self._raw_temperature * _TMP117_RESOLUTION

    @property
    def temperature(self):
        """The current measured temperature in Celsius"""

        return self._read_temperature()
