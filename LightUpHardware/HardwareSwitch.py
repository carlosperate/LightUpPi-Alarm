#!/usr/bin/env python2
#
# Functions to control the coffee Belkin Wemo mains switch
#
# Copyright (c) 2015 carlosperate http://carlosperate.github.io
#
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
from __future__ import unicode_literals, absolute_import
from ouimeaux.environment import Environment
from ouimeaux.device.switch import Switch

# The Belkin Wemo Switch name for the coffee machine
coffee_switch_name = None


def __on_switch(switch):
    global coffee_switch_name
    print('Switch found! %s' % switch.name)
    coffee_switch_name = switch.name


def switch_on():
    env = Environment(__on_switch)
    env.start()
    env.discover(seconds=3)

    global coffee_switch_name
    coffee_switch = env.get_switch(coffee_switch_name)
    coffee_switch.on()
