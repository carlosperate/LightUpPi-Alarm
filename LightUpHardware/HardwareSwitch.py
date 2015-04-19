#!/usr/bin/env python2
#
# Functions to control the coffee Belkin Wemo mains switch
#
# Copyright (c) 2015 carlosperate http://carlosperate.github.io
#
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
# For simplicity, this file is kept as a set of functions with global variables,
# instead of a singleton class, to maintain the singularity of the switch.
#
# For now this is designed to find a single switch on the network to
# automatically assign it as the coffee machine switch. If more switches are
# added, a specific switch can be found by IP.
#
from __future__ import unicode_literals, absolute_import, print_function
import sys
from time import sleep
try:
    from LightUpHardware.pywemoswitch.WemoSwitch import WemoSwitch
except ImportError:
    from pywemoswitch.WemoSwitch import WemoSwitch

# The Belkin Wemo Switch ip
_coffee_switch_ip = '192.168.0.16'


def _get_switch(input_switch_ip=None):
    """
    If not done so already it initialises the ouimeaux environment, if a switch
    name is not given it finds a Wemo Switch on the network.
    It connects to the switch and returns the Switch instance.
    :param input_switch_ip: String with the IP of the switch to connect. If
                            none given it will use global default.
    """
    if input_switch_ip is not None:
        switch_ip = input_switch_ip
    else:
        switch_ip = _coffee_switch_ip

    switch = WemoSwitch(switch_ip)
    counter = 0
    while (switch.connected is False) and (counter < 3):
        sleep(2)
        switch = WemoSwitch(switch_ip)
        counter += 1
    if switch.connected is True:
        print("Connected to wemo switch on %s:%s" %
              (switch.server, switch.port))
        return switch
    else:
        print("Unable to connect to Switch on %s" % switch.server,
              file=sys.stderr)
        return None


def switch_on(input_switch=None):
    """
    Turns ON the given switch, or the default switch.
    :return: Current state of the switch
    """
    state = False
    if isinstance(input_switch, WemoSwitch):
        switch_to_turn = input_switch
    else:
        switch_to_turn = _get_switch()
    if switch_to_turn is not None:
        switch_to_turn.turn_on()
        state = switch_to_turn.get_state()
    return state


def switch_off(input_switch=None):
    """
    Turns OFF the given switch, or the default switch.
    :return: Current state of the switch
    """
    state = False
    if isinstance(input_switch, WemoSwitch):
        switch_to_turn = input_switch
    else:
        switch_to_turn = _get_switch()
    if switch_to_turn is not None:
        switch_to_turn.turn_off()
        state = switch_to_turn.get_state()
    return state


def test_switch():
    """
    Simple test that turns ON the default switch (las switch found on the
    network), waits 5 seconds, and turns it off.
    """
    state = switch_on()
    print("Switch is now %s" % ("ON" if state else "OFF"))
    sleep(5)
    state = switch_off()
    print("Switch is now %s" % ("ON" if state else "OFF"))


if __name__ == '__main__':
    test_switch()

