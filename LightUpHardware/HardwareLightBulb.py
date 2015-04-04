#!/usr/bin/env python2
#
# Functions to control the room Philips Hue light bulb
#
# Copyright (c) 2015 carlosperate http://carlosperate.github.io
#
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
from __future__ import unicode_literals, absolute_import
import time
try:
    from LightUpHardware.phue.phue import *
except ImportError:
    from phue.phue import *

# The Philips Hue light ID for the bedroom
ROOM_LIGHT_BULB_ID = 4


def gradual_light_on(seconds):
    """
    Gradually increases the light brightness from minimum to maximum in inputted
    amount of time.
    :param seconds: Time in seconds for the entire procedure to take.
    """
    sleep_time = seconds / 255.0

    light_bulb = Light(__connected_bridge(), ROOM_LIGHT_BULB_ID)
    if light_bulb.reachable is False:
        print("Light %s switch is OFF" % ROOM_LIGHT_BULB_ID)
    else:
        light_bulb.brightness = 0
        if light_bulb.on is False:
            light_bulb.on = True
        print('Increasing the light brightness for %s seconds.' % seconds)
        for x in range(1, 254):
            time.sleep(sleep_time)
            light_bulb.brightness = x


def __connected_bridge():
    bridge = None
    while True:
        try:
            bridge = Bridge('192.168.0.10')
            break
        except PhueRegistrationException as e:
            connect_str = "This application needs to be registered in the " \
                          "bridge. This only has to be done once.\nPlease " \
                          "press the button on the Bridge then hit Enter to " \
                          "try again."
            if sys.version_info[0] > 2:
                input(connect_str)
            else:
                raw_input(connect_str)
    return bridge
