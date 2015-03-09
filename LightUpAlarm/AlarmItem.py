#!/usr/bin/env python2
#
# Class to contain the data for a single alarm.
#
# Copyright (c) 2015 carlosperate https://github.com/carlosperate/
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
# Full description goes here
#
from __future__ import unicode_literals, absolute_import, print_function
from __builtin__ import property
import types
import sys


class AlarmItem(object):
    """
    .
    """
    #
    # constructor
    #
    def __init__(self, hour, minute,
                 days=(False, False, False, False, False, False, False),
                 active=True, alarm_id=None):
        """
        Constructor assigns the input data into the new alarm instance.
        First creates the private variables, then assigns values
        """
        # ID is only created at first save into db
        self.__id = None
        # Indicates if the alarm is active or not
        self.__active = False
        # Contains the days of the weeks that this alarm repeats
        self.__repeat = {'Monday': False,
                         'Tuesday': False,
                         'Wednesday': False,
                         'Thursday': False,
                         'Friday': False,
                         'Saturday': False,
                         'Sunday': False}
        # Alarm time
        self.__minute = 0
        self.__hour = 0

        # Assigning values using accessors
        self.hour = hour
        self.minute = minute
        self.repeat = days
        self.active = active
        if alarm_id is not None:
            self.id = alarm_id

    #
    # id accesor
    #
    def get_id(self):
        return self.__id

    def set_id(self, new_id):
        """
        Sets id value. Must be an integer.
        :param new_id: new ID for the alarm instance.
        """
        if isinstance(new_id, types.IntType):
            self.__id = new_id
        else:
            print('ERROR: Provided AlarmItem().id type is not an Integer' +
                  ': %s!' % new_id, file=sys.stderr)

    id = property(get_id, set_id)

    #
    # active accesor
    #
    def get_active(self):
        return self.__active

    def set_active(self, new_active):
        """
        Ensure new value is a boolean before setting the active state.
        :param new_active: new active state for the alarm instance.
        """
        if isinstance(new_active, types.BooleanType):
            self.__active = new_active
        else:
            print('ERROR: Provided AlarmItem().active type is not a boolean' +
                  ': %s!' % new_active, file=sys.stderr)

    active = property(get_active, set_active)

    #
    # minute accesor
    #
    def get_minute(self):
        return self.__minute

    def set_minute(self, new_minute):
        """
        Checks input is an integer and wraps around value to be between 0 - 59.
        :param new_minute: new alarm minutes for the alarm instance.
        """
        if isinstance(new_minute, types.IntType):
            while new_minute >= 60:
                new_minute %= 60
            self.__minute = new_minute
        else:
            print('ERROR: Provided AlarmItem().minute type is not an Integer' +
                  ': %s!' % new_minute, file=sys.stderr)

    minute = property(get_minute, set_minute)

    #
    # hour accesor
    #
    def get_hour(self):
        return self.__hour

    def set_hour(self, new_hour):
        """
        Checks input is an integer and wraps around value to be between 0 - 23.
        :param new_hour: new alarm hours for the alarm instance.
        """
        if isinstance(new_hour, types.IntType):
            while new_hour >= 24:
                new_hour %= 24
            self.__hour = new_hour
        else:
            print('ERROR: Provided AlarmItem().hour type is not an Integer' +
                  ': %s!' % new_hour, file=sys.stderr)

    hour = property(get_hour, set_hour)

    #
    # repeat accesor
    #
    def get_repeat(self):
        """
        Returns the days of the week alarm repetition in the form of a tuple.
        :return: Tuple with 7 booleans to indicate repetition for the weekdays.
        """
        repeat_tuple = (self.__repeat['Monday'], self.__repeat['Tuesday'],
                        self.__repeat['Wednesday'], self.__repeat['Thursday'],
                        self.__repeat['Friday'], self.__repeat['Saturday'],
                        self.__repeat['Sunday'])
        return repeat_tuple

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
                self.__repeat['Monday'] = new_repeat[0]
                self.__repeat['Tuesday'] = new_repeat[1]
                self.__repeat['Wednesday'] = new_repeat[2]
                self.__repeat['Thursday'] = new_repeat[3]
                self.__repeat['Friday'] = new_repeat[4]
                self.__repeat['Saturday'] = new_repeat[5]
                self.__repeat['Sunday'] = new_repeat[6]
        else:
            print('ERROR: The AlarmItem().repeat must be a list of 7 booleans!',
                  file=sys.stderr)

    repeat = property(get_repeat, set_repeat)

    def get_monday(self):
        return self.__repeat['Monday']

    def set_monday(self, new_monday):
        if isinstance(new_monday, types.BooleanType):
            self.__repeat['Monday'] = new_monday
        else:
            print('ERROR: New value for the AlarmItem().monday variable has ' +
                  'to be a Boolean !', file=sys.stderr)

    monday = property(get_monday, set_monday)

    def get_tuesday(self):
        return self.__repeat['Tuesday']

    def set_tuesday(self, new_tuesday):
        if isinstance(new_tuesday, types.BooleanType):
            self.__repeat['Tuesday'] = new_tuesday
        else:
            print('ERROR: New value for the AlarmItem().tuesday variable has ' +
                  'to be a Boolean !', file=sys.stderr)

    tuesday = property(get_tuesday, set_tuesday)

    def get_wednesday(self):
        return self.__repeat['Wednesday']

    def set_wednesday(self, new_wednesday):
        if isinstance(new_wednesday, types.BooleanType):
            self.__repeat['Wednesday'] = new_wednesday
        else:
            print('ERROR: New value for the AlarmItem().wednesday variable ' +
                  'has to be a Boolean !', file=sys.stderr)

    wednesday = property(get_wednesday,set_wednesday)

    def get_thursday(self):
        return self.__repeat['Thursday']

    def set_thursday(self, new_thursday):
        if isinstance(new_thursday, types.BooleanType):
            self.__repeat['Thursday'] = new_thursday
        else:
            print('ERROR: New value for the AlarmItem().thursday variable ' +
                  'has to be a Boolean !', file=sys.stderr)

    thursday = property(get_thursday, set_thursday)

    def get_friday(self):
        return self.__repeat['Friday']

    def set_friday(self, new_friday):
        if isinstance(new_friday, types.BooleanType):
            self.__repeat['Friday'] = new_friday
        else:
            print('ERROR: New value for the AlarmItem().friday variable has ' +
                  'to be a Boolean !', file=sys.stderr)

    friday = property(get_friday, set_friday)

    def get_saturday(self):
        return self.__repeat['Saturday']

    def set_saturday(self, new_saturday):
        if isinstance(new_saturday, types.BooleanType):
            self.__repeat['Saturday'] = new_saturday
        else:
            print('ERROR: New value for the AlarmItem().saturday variable ' +
                  'has to be a Boolean !', file=sys.stderr)

    saturday = property(get_saturday, set_saturday)

    def get_sunday(self):
        return self.__repeat['Sunday']

    def set_sunday(self, new_sunday):
        if isinstance(new_sunday, types.BooleanType):
            self.__repeat['Sunday'] = new_sunday
        else:
            print('ERROR: New value for the AlarmItem().sunday variable ' +
                  'has to be a Boolean !', file=sys.stderr)

    sunday = property(get_sunday, set_sunday)

    #
    # member methods
    #
