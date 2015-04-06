#!/usr/bin/env python2
#
# Singleton Thread class to control the alarm alert hardware
#
# Copyright (c) 2015 carlosperate http://carlosperate.github.io
#
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
from __future__ import unicode_literals, absolute_import, print_function
import sys
import time
import types
import threading
try:
    from LightUpHardware import HardwareLightBulb
    from LightUpHardware import HardwareSwitch
    from LightUpHardware import HardwareLamp
except ImportError:
    import HardwareLightBulb
    import HardwareSwitch
    import HardwareLamp


class HardwareThread(threading.Thread):
    """ """
    __singleton = None
    __lamp_time = None
    __room_light_time = None
    __coffee_time = None
    __total_time = None
    __running = False
    __threads = []

    #
    # metaclass methods to apply singleton pattern
    #
    def __new__(cls, lamp_time=None, room_light_time=None, coffee_time=None,
                total_time=None):
        """
        The new constructor is edited directly to be able to control this class
        instance creation and apply a singleton patter.
        :param lamp_time: Time, in seconds, for the lamp procedure to start.
        :param room_light_time: Time, in seconds, for the room lights procedure
                                to start.
        :param coffee_time: Time, in seconds, for the coffee procedure to start.
        :param total_time: Total time for the entire entire hardware control
                           process to take.
        :return: HardwareThread singleton instance.
        """
        if not cls.__singleton:
            cls.__singleton = super(HardwareThread, cls).__new__(cls)
            cls.daemon = True
            threading.Thread.__init__(cls.__singleton)

        # The constructor arguments are optional and might change class
        # variables every time the singleton instance in invoked
        if lamp_time is not None:
            cls.lamp_time = lamp_time
        if room_light_time is not None:
            cls.room_light_time = room_light_time
        if coffee_time is not None:
            cls.coffee_time = coffee_time
        if total_time is not None:
            cls.total_time = total_time

        return cls.__singleton

    def __init__(self, *args, **kwargs):
        """ No Initiliser, as everything taken care of in the constructor. """
        pass

    def _drop(self):
        """ Drop the instance. """
        self.__singleton = None

    #
    # control thread methods
    #
    def run(self):
        """
        Infinite loop function to run during the total time, in seconds,
        indicated by total_time variable.
        This method checks the time variables have been set and locks reentry.
        """
        # First check if required variables are set
        self.check_variables()

        # Setting a lock for no reentry
        if self.__running is True:
            print("LightUpPi Hardware already running.")
            time.sleep(1)
        self.__running = True

        start_time = time.time()
        time_lamp = start_time + self.lamp_time
        time_room = start_time + self.room_light_time
        time_coffee = start_time + self.coffee_time
        end_time = start_time + self.total_time
        lamp_launched = False
        room_launched = False
        coffee_launched = False

        # Time controlled loop to launch the required hardware functions
        current_time = time.time()
        while current_time < end_time:
            if time_lamp < current_time and lamp_launched is False:
                lamp_launched = True
                HardwareThread._launch_lamp()
            if time_room < current_time and room_launched is False:
                room_launched = True
                HardwareThread._launch_room_light()
            if time_coffee < current_time and coffee_launched is False:
                coffee_launched = True
                HardwareThread._launch_coffee()
            time.sleep(0.1)
            current_time = time.time()

        # Don't wait for the threads to join, as it would overrun the requested
        # runtime. Ending this thread will kill its children.
        print('finished')
        self.__running = False

    #
    # Accesors
    #
    def __get_lamp_time(self):
        return self.__lamp_time

    def __set_lamp_time(self, new_lamp_time):
        """
        Only sets value if thread is not running. Checks input is an integer.
        :param new_lamp_time: New lamp time, in seconds, to trigger.
        """
        if self.isAlive():
            print('Cannot change properties while thread is running.')
        else:
            if isinstance(new_lamp_time, types.IntType):
                self.__lamp_time = new_lamp_time
            else:
                print('ERROR: Provided lamp_time is not an integer: %s' %
                      new_lamp_time, file=sys.stderr)

    lamp_time = property(__get_lamp_time, __set_lamp_time)

    def __get_room_light_time(self):
        return self.__room_light_time

    def __set_room_light_time(self, new_room_light_time):
        """
        Only sets value if thread is not running. Checks input is an integer.
        :param new_room_light_time: New room light time, in seconds, to trigger.
        """
        if self.isAlive():
            print('Cannot change properties while thread is running.')
        else:
            if isinstance(new_room_light_time, types.IntType):
                self.__room_light_time = new_room_light_time
            else:
                print('ERROR: Provided room_light_time is not an integer: %s' %
                      new_room_light_time, file=sys.stderr)

    room_light_time = property(__get_room_light_time, __set_room_light_time)

    def __get_coffee_time(self):
        return self.__coffee_time

    def __set_coffee_time(self, new_coffee_time):
        """
        Only sets value if thread is not running. Checks input is an integer.
        :param new_coffee_time: New coffee time, in seconds, to trigger.
        """
        if self.isAlive():
            print('Cannot change properties while thread is running.')
        else:
            if isinstance(new_coffee_time, types.IntType):
                self.__coffee_time = new_coffee_time
            else:
                print('ERROR: Provided coffee_time is not an integer: %s' %
                      new_coffee_time, file=sys.stderr)

    coffee_time = property(__get_coffee_time, __set_coffee_time)

    def __set_total_time(self, new_total_time):
        """
        Only sets value if thread is not running. Checks input is an integer.
        :param new_total_time: New total runtime, in seconds.
        """
        if self.isAlive():
            print('Cannot change properties while thread is running.')
        else:
            if isinstance(new_total_time, types.IntType):
                self.__total_time = new_total_time
            else:
                print('ERROR: Provided total_time is not an integer: %s' %
                      new_total_time, file=sys.stderr)

    total_time = property(__get_coffee_time, __set_coffee_time)

    #
    # class member methods
    #
    @classmethod
    def _launch_lamp(cls):
        t = threading.Thread(target=HardwareLamp.gradual_light_on)
        cls.__threads.append(t)
        t.start()

    @classmethod
    def _launch_room_light(cls):
        t = threading.Thread(
            target=HardwareLightBulb.gradual_light_on, args=[20])
        cls.__threads.append(t)
        t.start()

    @classmethod
    def _launch_coffee(cls):
        t = threading.Thread(target=HardwareSwitch.switch_on())
        cls.__threads.append(t)
        t.start()

    @classmethod
    def check_variables(cls):
        all_good = True
        if cls.lamp_time is None:
            print('HardwareThread ERROR: Variable lamp_time has not been set.',
                  file=sys.stderr)
            all_good = False
        if cls.room_light_time is None:
            print('HardwareThread ERROR: Variable room_light_time has not been '
                  'set.',file=sys.stderr)
            all_good = False
        if cls.coffee_time is None:
            print('HardwareThread ERROR: Variable coffee_time has not been '
                  'set.', file=sys.stderr)
            all_good = False
        if cls.total_time is None:
            print('HardwareThread ERROR: Variable total_time has not been set.',
                  file=sys.stderr)
            all_good = False
        if all_good is True:
            print('Running the Hardware Thread: runtime of %s seconds, lamp '
                  'trigger after %s seconds, room light triggered after %s '
                  'seconds, coffee triggered after %s seconds' %
                  (cls.total_time, cls.lamp_time, cls.room_light_time,
                   cls.coffee_time))
