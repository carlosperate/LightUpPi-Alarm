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


class HardwareThread(object):
    """
    This class uses the singleton pattern to control the hardware connected to
    the system.
    The class static public variables are controlled using accessors, and are
    not accessible from class instances on purpose to highlight the fact that
    the data belongs to the class, so:
    instance = HardwareThread()          <-- returns a singleton instance
    HardwareThread.lamp_time             <-- correct
    instance.lamp_time                   <-- incorrect, AttributeError
    instance._HardwareThread__lamp_time  <-- works, but naughty
    """
    __singleton = None
    __lamp_time = None
    __lamp_duration = None
    __room_light_time = None
    __room_light_duration = None
    __coffee_time = None
    __total_time = None
    __running = False
    __thread = None
    __threads = []

    #
    # metaclass methods to apply singleton pattern and set accessors
    #
    class __HardwareThread_metaclass(type):
        """
        The property accesors of the HardwareThread class would only be applied
        to instance variables and not to the class static variables, so we set
        the  variables with accessors in the metaclass and they will be able
        act as HardwareThread class static variables with accessors for input
        sanitation and to stop editing the data while the thread is running.
        """
        def __new__(cls, name, bases, dct):
            hw_thread_instance = type.__new__(cls, name, bases, dct)

            # Set the metaclass variables and attach accessors
            cls.lamp_time = property(
                hw_thread_instance._HardwareThread__get_lamp_time.im_func,
                hw_thread_instance._HardwareThread__set_lamp_time.im_func)
            cls.lamp_duration = property(
                hw_thread_instance._HardwareThread__get_lamp_duration.im_func,
                hw_thread_instance._HardwareThread__set_lamp_duration.im_func)
            cls.room_light_time = property(
                hw_thread_instance._HardwareThread__get_room_light_time.im_func,
                hw_thread_instance._HardwareThread__set_room_light_time.im_func)
            cls.room_light_duration = property(
                hw_thread_instance._HardwareThread__get_room_light_duration.im_func,
                hw_thread_instance._HardwareThread__set_room_light_duration.im_func)
            cls.coffee_time = property(
                hw_thread_instance._HardwareThread__get_coffee_time.im_func,
                hw_thread_instance._HardwareThread__set_coffee_time.im_func)
            cls.total_time = property(
                hw_thread_instance._HardwareThread__get_total_time.im_func,
                hw_thread_instance._HardwareThread__set_total_time.im_func)

            return hw_thread_instance

    __metaclass__ = __HardwareThread_metaclass

    def __new__(cls, lamp=None, room_light=None, coffee_time=None,
                total_time=None):
        """
        The new constructor is edited directly to be able to control this class
        instance creation and apply a singleton pattern. Set strict control of
        the constructor arguments to:
        :param lamp: List or Tuple with the ime, in seconds, for the lamp
                     procedure to start and its duration.
        :param room_light: List or Tuple with the ime, in seconds, for the room
                           lights procedure to start and its duration
        :param coffee_time: Integer time, in seconds, for the coffee procedure
                            to start.
        :param total_time: Integer, total time for the entire entire hardware
                           control process to take.
        :return: HardwareThread singleton instance.
        """
        # Create singleton instance if __singleton is None
        if not cls.__singleton:
            cls.__singleton = super(HardwareThread, cls).__new__(cls)

            # Stop users from adding attributes, as they can accidentally add
            # the class static variables as instance attributes
            cls.__original_setattr = cls.__setattr__

            def set_attribute_filter(self, key, value):
                if key in ('lamp_time', 'lamp_duration', 'room_light_time',
                           'room_light_duration', 'coffee_time', 'total_time'):
                    raise AttributeError(
                        'Cannot add %s attribute to HardwareThread instance.' %
                        key)
                else:
                    self.__original_setattr(key, value)

            cls.__setattr__ = set_attribute_filter

        # The constructor arguments are optional and might change class
        # variables every time the singleton instance in invoked
        if lamp is not None:
            if (isinstance(lamp, types.TupleType) or
                    isinstance(lamp, types.ListType)) and (len(lamp) == 2):
                cls.lamp_time = lamp[0]
                cls.lamp_duration = lamp[1]
            else:
                print('ERROR: Provided lamp data is not list/tuple of the ' +
                      ('right format (launch time, duration): %s' % str(lamp)) +
                      ('\nKept default: (%s, %s)' %
                      (cls.lamp_time, cls.lamp_duration)), file=sys.stderr)
        if room_light is not None:
            if (isinstance(room_light, types.TupleType) or
                    isinstance(room_light, types.ListType)) and \
                    (len(room_light) == 2):
                cls.room_light_time = room_light[0]
                cls.room_light_duration = room_light[1]
            else:
                print('ERROR: Provided room light is not list/tuple of the ' +
                      ('right format (launch time, duration): %s' % str(lamp)) +
                      ('\nKept default: (%s, %s)' %
                      (cls.room_light_time, cls.room_light_duration)),
                      file=sys.stderr)
        if coffee_time is not None:
            cls.coffee_time = coffee_time
        if total_time is not None:
            cls.total_time = total_time

        return cls.__singleton

    def __init__(self, *args, **kwargs):
        """ No Initiliser, as everything taken care of in the constructor. """
        pass

    @classmethod
    def _drop(cls):
        """ Drop the instance and restore the set attribute method. """
        try:
            cls.__setattr__ = cls.__original_setattr
        except AttributeError:
            print('ERROR: Trying to drop singleton not initialised (setattr).',
                  file=sys.stderr)
        if cls.__singleton:
            cls.__singleton = None
        else:
            print('ERROR: Trying to drop singleton not initialised (instance).',
                  file=sys.stderr)
        cls.__lamp_time = None
        cls.__lamp_duration = None
        cls.__room_light_time = None
        cls.__room_light_duration = None
        cls.__coffee_time = None
        cls.__total_time = None
        cls.__running = False
        cls.__thread = None
        cls.__threads = []

    #
    # Accesors
    #
    @classmethod
    def __get_lamp_time(cls):
        return cls.__lamp_time

    @classmethod
    def __set_lamp_time(cls, new_lamp_time):
        """
        Only sets value if thread is not running. Checks input is an integer.
        :param new_lamp_time: New lamp time, in seconds, to trigger.
        """
        if cls.__thread and cls.__thread.isAlive():
            print('Cannot change properties while thread is running.')
        else:
            if isinstance(new_lamp_time, types.IntType):
                cls.__lamp_time = new_lamp_time
            else:
                print('ERROR: Provided lamp_time is not an integer: %s' %
                      new_lamp_time, file=sys.stderr)

    @classmethod
    def __get_lamp_duration(cls):
        return cls.__lamp_duration

    @classmethod
    def __set_lamp_duration(cls, new_lamp_duration):
        """
        Only sets value if thread is not running. Checks input is an integer.
        :param new_lamp_duration: New lamp duration, in seconds, to last.
        """
        if cls.__thread and cls.__thread.isAlive():
            print('Cannot change properties while thread is running.')
        else:
            if isinstance(new_lamp_duration, types.IntType):
                cls.__lamp_duration = new_lamp_duration
            else:
                print('ERROR: Provided lamp_duration is not an integer: %s' %
                      new_lamp_duration, file=sys.stderr)

    @classmethod
    def __get_room_light_time(cls):
        return cls.__room_light_time

    @classmethod
    def __set_room_light_time(cls, new_room_light_time):
        """
        Only sets value if thread is not running. Checks input is an integer.
        :param new_room_light_time: New room light time, in seconds, to trigger.
        """
        if cls.__thread and cls.__thread.isAlive():
            print('Cannot change properties while thread is running.')
        else:
            if isinstance(new_room_light_time, types.IntType):
                cls.__room_light_time = new_room_light_time
            else:
                print('ERROR: Provided room_light_time is not an integer: %s' %
                      new_room_light_time, file=sys.stderr)

    @classmethod
    def __get_room_light_duration(cls):
        return cls.__room_light_duration

    @classmethod
    def __set_room_light_duration(cls, new_room_light_duration):
        """
        Only sets value if thread is not running. Checks input is an integer.
        :param new_room_light_duration: New room light duration, in seconds, to
                                        last.
        """
        if cls.__thread and cls.__thread.isAlive():
            print('Cannot change properties while thread is running.')
        else:
            if isinstance(new_room_light_duration, types.IntType):
                cls.__room_light_duration = new_room_light_duration
            else:
                print('ERROR: Provided room_light_duration is not an integer:' +
                      ' %s' % new_room_light_duration, file=sys.stderr)

    @classmethod
    def __get_coffee_time(cls):
        return cls.__coffee_time

    @classmethod
    def __set_coffee_time(cls, new_coffee_time):
        """
        Only sets value if thread is not running. Checks input is an integer.
        :param new_coffee_time: New coffee time, in seconds, to trigger.
        """
        if cls.__thread and cls.__thread.isAlive():
            print('Cannot change properties while thread is running.')
        else:
            if isinstance(new_coffee_time, types.IntType):
                cls.__coffee_time = new_coffee_time
            else:
                print('ERROR: Provided coffee_time is not an integer: %s' %
                      new_coffee_time, file=sys.stderr)

    @classmethod
    def __get_total_time(cls):
        return cls.__total_time

    @classmethod
    def __set_total_time(cls, new_total_time):
        """
        Only sets value if thread is not running. Checks input is an integer.
        :param new_total_time: New total runtime, in seconds.
        """
        if cls.__thread and cls.__thread.isAlive():
            print('Cannot change properties while thread is running.')
        else:
            if isinstance(new_total_time, types.IntType):
                cls.__total_time = new_total_time
            else:
                print('ERROR: Provided total_time is not an integer: %s' %
                      new_total_time, file=sys.stderr)

    #
    # class member methods
    #
    @classmethod
    def _launch_lamp(cls):
        t = threading.Thread(
            name='LampThread',
            target=HardwareLamp.gradual_light_on,
            args=(cls.lamp_duration,))
        cls.__threads.append(t)
        t.start()

    @classmethod
    def _launch_room_light(cls):
        t = threading.Thread(
            name='LightThread',
            target=HardwareLightBulb.gradual_light_on,
            args=(cls.room_light_duration,))
        cls.__threads.append(t)
        t.start()

    @classmethod
    def _launch_coffee(cls):
        t = threading.Thread(
            name='SwitchThread',
            target=HardwareSwitch.safe_on)
        cls.__threads.append(t)
        t.start()

    @classmethod
    def check_variables(cls):
        """
        Checks that all variables are set to something
        :return: Boolean indicating the good state of the variables
        """
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

        return all_good

    #
    # Thread methods
    #
    @classmethod
    def __run(cls):
        """
        Infinite loop function to run during the total time, in seconds,
        indicated by total_time variable.
        This method checks the time variables have been set and locks reentry.
        """
        start_time = time.time()
        time_lamp = start_time + cls.lamp_time
        time_room = start_time + cls.room_light_time
        time_coffee = start_time + cls.coffee_time
        end_time = start_time + cls.total_time
        lamp_launched = False
        room_launched = False
        coffee_launched = False

        # Time controlled loop to launch the required hardware functions
        current_time = time.time()
        while current_time < end_time:
            if time_lamp < current_time and lamp_launched is False:
                lamp_launched = True
                cls._launch_lamp()
            if time_room < current_time and room_launched is False:
                room_launched = True
                cls._launch_room_light()
            if time_coffee < current_time and coffee_launched is False:
                coffee_launched = True
                cls._launch_coffee()
            time.sleep(0.1)
            current_time = time.time()

        # Don't wait for the threads to join, as it would overrun the requested
        # runtime. Ending this thread will kill its children.
        print('HardwareThread run finished.')

    @classmethod
    def start(cls):
        """
        """
        # First check if required variables are set
        variables_ok = cls.check_variables()
        if variables_ok is False:
            return

        # Setting a lock for no reentry
        if cls.__running is True:
            print("LightUpPi Hardware already running.")
            time.sleep(1)
        cls.__running = True

        # Launch thread
        cls.__thread = threading.Thread(
            name='HardwareThread run', target=cls.__run)
        cls.__thread.start()
        cls.__thread.join()

        cls.__running = False

    @classmethod
    def isAlive(cls):
        if cls.__thread:
            return cls.__thread.isAlive()
        else:
            return False
