# -*- coding: utf-8 -*-
#
# Mock module for the Unicorn Hat package
#
# Copyright (c) 2015 carlosperate http://carlosperate.github.io
#
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
# This is a simple mock module that will print to screen the unicorn hat package
# calls. It is used to be able to do development in a non-raspberry pi system,
# as the Unicorn Hat package is the python code to control an LED matrix:
# http://shop.pimoroni.com/products/unicorn-hat
#
# Only the functions called within the HardwareLamp module will be defined here,
# to be expanded as development might require it.
#
from __future__ import unicode_literals, absolute_import

verbose = True
brightness_level = 0
verbose_counter = 0

def brightness(b=0.2):
    global brightness_level
    brightness_level = b
    if verbose is True:
        print('Unicorn brightness set to: %s' % b)


def set_pixel(x, y, r, g, b):
    if verbose is True:
        print('Unicorn pixel set x: %s; y: %s; rgb: %s %s %s' % (x, y, r, g, b))


def show():
    global verbose_counter
    verbose_counter += 1

    if verbose is False and (verbose_counter % 10 == 0):
        print('Unicorn updated, brightness %.3f' % brightness_level)
