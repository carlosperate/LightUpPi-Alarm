#!/usr/bin/env python2
#
# Unicorn Hat light control functions
#
# Copyright (c) 2015 carlosperate http://carlosperate.github.io
#
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
import unicornhat
import time


brightness_start = 0.1
brightness_end = 0.9


def gradual_light_on(seconds):
    sleep_time = seconds / 200.0
    brightness_step = (brightness_end - brightness_start) / 200.0
    brightness_level = brightness_start

    # Set all the pixels to the yellowish colour
    for y in range(8):
        for x in range(8):
            unicornhat.set_pixel(x, y, 255, 200, 100)
    unicornhat.brightness(brightness_start)
    unicornhat.show()

    # Increase brightness gradually
    while brightness_level < brightness_end:
        unicornhat.brightness(brightness_level)
        unicornhat.show()
        brightness_level += brightness_step
        time.sleep(sleep_time)


if __name__ == '__main__':
    gradual_light_on(10)
