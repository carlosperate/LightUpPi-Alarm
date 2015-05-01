#!/usr/bin/env python2
#
# Entry point for the LightUpHardware package.
#
# Copyright (c) 2015 carlosperate http://carlosperate.github.io
#
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
from __future__ import unicode_literals, absolute_import
from time import sleep
try:
    from LightUpHardware.HardwareThread import HardwareThread
except ImportError:
    from HardwareThread import HardwareThread


def main():
    minutes = lambda x: x * 60

    hardware_alert = HardwareThread(
        lamp=(0, minutes(3)),
        room_light=(minutes(2), minutes(13)),
        coffee_time=minutes(10),
        total_time=minutes(15))

    hardware_alert.start()
    while hardware_alert.isAlive():
        sleep(1)
    print('Main LightUpHardware finished!')


if __name__ == '__main__':
    main()
