Introduction
============


.. image:: https://readthedocs.org/projects/tmp117/badge/?version=latest
    :target: https://tmp117.readthedocs.io/
    :alt: Documentation Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

MicroPython Driver for the TMP117 temperature sensor

Register reding based on
https://github.com/adafruit/Adafruit_CircuitPython_Register


On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/micropython-tmp117/>`_.
To install for current user:

.. code-block:: shell

    pip3 install micropython-tmp117

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install micropython-tmp117

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .env/bin/activate
    pip3 install micropython-tmp117
