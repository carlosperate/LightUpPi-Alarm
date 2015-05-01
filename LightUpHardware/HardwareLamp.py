#!/usr/bin/env python2
#
# Unicorn Hat light control functions
#
# Copyright (c) 2015 carlosperate http://carlosperate.github.io
#
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
from __future__ import unicode_literals, absolute_import
import time
import colorsys
try:
    import unicornhat
except ImportError:
    print('The unicornhat package needs to be installed !\n' +
          'The LightUpHardware folder contains a README file with more info.')
    try:
        from LightUpHardware import unicornhatmock as unicornhat
    except ImportError:
        import unicornhatmock as unicornhat
    unicornhat.verbose = False
    print('Mock unicornhat module imported.')


brightness_start = 0.1
brightness_end = 0.9


def gradual_light_on(seconds):
    sleep_time = seconds / 200.0
    brightness_step = (brightness_end - brightness_start) / 200.0
    brightness_level = brightness_start

    # Set all the pixels to the yellowish colour
    r, g, b = colorsys.hsv_to_rgb(0.108, 0.6, 1.0)
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    for y in range(8):
        for x in range(8):
            unicornhat.set_pixel(x, y, r, g, b)
    unicornhat.brightness(brightness_start)
    unicornhat.show()

    # Increase brightness gradually
    while brightness_level < brightness_end:
        unicornhat.brightness(brightness_level)
        unicornhat.show()
        brightness_level += brightness_step
        time.sleep(sleep_time)
