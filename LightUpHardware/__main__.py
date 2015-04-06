#!/usr/bin/env python2
#
# Entry point for the LightUpHardware package.
#
# Copyright (c) 2015 carlosperate http://carlosperate.github.io
#
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
from __future__ import unicode_literals, absolute_import
import sys
try:
    from LightUpHardware.HardwareThread import HardwareThread
except ImportError:
    from HardwareThread import HardwareThread


def main(argv=None):
    # Checking command line arguments
    if (argv is not None) and (len(argv) > 0):
        pass

    temp = HardwareThread(
        lamp_time=0, room_light_time=2, coffee_time=5, total_time=35)
    temp.start()
    while temp.isAlive():
        pass
    print('finished!')


if __name__ == '__main__':
    main(sys.argv[1:])
