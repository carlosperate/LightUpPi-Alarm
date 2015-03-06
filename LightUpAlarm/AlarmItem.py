#!/usr/bin/env python2
#
# Class to contain the data for a single alarm.
#
# Copyright (c) 2015 carlosperate https://github.com/carlosperate/
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
# Full description goes here
#
from __future__ import unicode_literals, absolute_import
from __future__ import print_function
from __builtin__ import property
import types
import sys


class AlarmItem(object):
    """
    .
    """
    # ID is only created at first save into db
    _id = None

    # Indicates if the alarm is active or not
    _active = False

    # Contains the days of the weeks that this alarm repeats
    _repeat = {'Monday': False,
               'Tuesday': False,
               'Wednesday': False,
               'Thursday': False,
               'Friday': False,
               'Saturday': False,
               'Sunday': False}

    # Alarm time
    _minute = 0
    _hour = 0

    #
    # id accesor
    #
    def get_id(self):
        return self._id

    def set_id(self, new_id):
        """
        Sets id value. Must be an integer.
        :param new_id: new ID for the alarm instance.
        """
        if isinstance(new_id, types.IntType):
            self._id = new_id
        else:
            print('ERROR: Provided AlarmItem().id type is not an Integer' +
                  ': %s!' % new_id, file=sys.stderr)

    id = property(get_id, set_id)

    #
    # active accesor
    #
    def get_active(self):
        return self._active

    def set_active(self, new_active):
        """
        Wraps around input value to be within 0 and 23.
        :param new_active: new active state for the alarm instance.
        """
        if isinstance(new_active, types.BooleanType):
            self._active = new_active
        else:
            print('ERROR: Provided AlarmItem().active type is not a boolean' +
                  ': %s!' % new_active, file=sys.stderr)

    active = property(get_active, set_active)

    #
    # minute accesor
    #
    def get_minute(self):
        return self._minute

    def set_minute(self, new_minute):
        """
        Wraps around input value to be within 0 and 59.
        :param new_minute: new alarm minutes for the alarm instance.
        """
        while new_minute >= 60:
            new_minute %= 60
        self._minute = new_minute

    minute = property(get_minute, set_minute)

    #
    # hour accesor
    #
    def get_hour(self):
        return self._hour

    def set_hour(self, new_hour):
        """
        Wraps around input value to be within 0 and 23.
        :param new_hour: new alarm hours for the alarm instance.
        """
        while new_hour >= 24:
            new_hour %= 24
        self._hour = new_hour

    hour = property(get_hour, set_hour)

    #
    # repeat accesor
    #
    def get_repeat(self):
        """
        Returns the days of the week alarm repetition in the form of a tuple.
        :return: Tuple with 7 booleans to indicate repetition for the weekdays.
        """
        repeat_return = []
        for day in self._repeat:
            repeat_return.append(self._repeat[day])
        return tuple(repeat_return)

    def set_repeat(self, new_repeat):
        """
        Checks that it is a list/tuple of 7 booleans and if so assigns them to
        the _repeat dictionary.
        :param new_repeat: List of containing 7 booleans to indicate the days
                           of the week the alarm repeats.
        """
        if len(new_repeat) == 7:
            for day in new_repeat:
                if isinstance(day, types.BooleanType) is False:
                    print('ERROR: All items in the AlarmItem().repeat list ' +
                          'have to be Booleans!', file=sys.stderr)
                    break
            else:
                self._repeat = new_repeat
        else:
            print('ERROR: The AlarmItem().repeat must be a list of 7 booleans!',
                  file=sys.stderr)

    repeat = property(get_repeat, set_repeat)

    def __init__(self, hour, minute,
                 days=(False, False, False, False, False, False, False),
                 active=True, alarm_id=None):
        """
        Constructor assigns the input data into the new alarm instance.
        """
        self.hour = hour
        self.minute = minute
        self.repeat = days
        self.active = active
        if alarm_id is not None:
            self.id = alarm_id
