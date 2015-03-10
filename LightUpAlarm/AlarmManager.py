#!/usr/bin/env python2
#
# Short description
#
# Copyright (c) 2015 carlosperate https://github.com/carlosperate/
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
# Full description goes here
#
from __future__ import unicode_literals, absolute_import
import time
import operator
from LightUpAlarm.AlarmItem import AlarmItem
from LightUpAlarm.AlarmDb import AlarmDb


class AlarmManager(object):
    """
    .
    """

    #
    # constructor
    #
    def __init__(self):
        """
        On initialization we connect to the database and check if there are
        any alarms to load. If not, load a couple of dummy alarms.
        """
        if AlarmDb().get_number_of_alarms() == 0:
            self.load_dummy_alarms()

    #
    # member methods to get alarms
    #
    @staticmethod
    def get_all_alarms():
        """
        Static method, gets all the alarms from the database.
        :return: List of AlarmItems containing all alarms. Returns an empty list
                 if there aren't any.
        """
        return AlarmDb().get_all_alarms()

    @staticmethod
    def get_number_of_alarms():
        """
        Gets the number of alarms stored in the database.
        :return: Integer indicating the number of alarms in the db.
        """
        return AlarmDb().get_number_of_alarms()

    @staticmethod
    def get_all_active_alarms():
        """
        Gets all the active alarms from the database.
        :return: List of AlarmItems containing all active alarms. Returns an
                 empty list if there aren't any.
        """
        return AlarmDb().get_all_active_alarms()

    @staticmethod
    def get_alarm(alarm_id):
        """
        Get the alarm with the given ID from the database.
        :param alarm_id: Integer to indicate the primary key of the Alarm to get.
        :return: AlarmItem with the alarm data, or None if id could not be found.
        """
        return AlarmDb().get_alarm(alarm_id)

    @staticmethod
    def get_next_alarm():
        """
        Gets the current time and all the active alarms. For each of these
        alarms it calculates the elapsed time that will pass for its next alert.
        Then it sorts the list based on this value and returns closes.
        :return: AlarmItem of the next alarm to alert.
        """
        # now_time[3] = tm_hour, now_time[4] = tm_minute, now_time[6] = tm_wday
        now_time = time.localtime(time.time())

        all_alarms = AlarmManager.get_all_active_alarms()
        if len(all_alarms) > 0:
            for alarm in all_alarms:
                alarm.next_alert = alarm.minutes_to_alert(
                    now_time[3], now_time[4], now_time[6])
            sorted_alarms = sorted(
                all_alarms, key=operator.attrgetter('next_alert'))
            return sorted_alarms[0]
        else:
            return None

    #
    # member methods to add alarms
    #
    @staticmethod
    def add_alarm(hour, minute,
                  days=(False, False, False, False, False, False, False),
                  active=True):
        """
        Adds an alarm to the database with the input values.
        :param hour: Integer to indicate the alarm hour.
        :param minute: Integer to indicate the alarm minute.
        :param days: 7-item list of booleans to indicate repeat weekdays.
        :param active: Boolean to indicate the alarm active state.
        :return: Boolean indicating the success of the 'edit' operation.
        """
        alarm = AlarmItem(hour, minute, days, active)
        alarm.id = AlarmDb().add_alarm(alarm)
        if alarm.id is not None:
            return True
        else:
            return False

    @staticmethod
    def load_dummy_alarms():
        """
        It loads 2 dummy alarms into the database for demonstration purposes.
        """
        AlarmManager.add_alarm(
            07, 10, (True, True, True, True, True, False, False))
        AlarmManager.add_alarm(
            10, 30, (False, False, False, False, False, True, True))

    #
    # member methods to edit alarms
    #
    @staticmethod
    def edit_alarm(alarm_id, hour=None, minute=None, days=None,
                   active=None):
        """
        Adds an alarm to the database with the input data. Returns the new row
        primary key.
        :param hour: Integer to indicate the alarm hour.
        :param minute: Integer to indicate the alarm minute.
        :param days: 7-item list of booleans to indicate repeat weekdays.
        :param active: Boolean to indicate alarm active state.
        :return: Boolean indicating the success of the 'edit' operation.
        """
        success = True
        db = AlarmDb()
        # Parse optional parameters
        if hour is not None:
            individual_success = db.edit_alarm(alarm_id, hour=hour)
            if not individual_success:
                success = False
        # Parse minute variable
        if minute is not None:
            individual_success = db.edit_alarm(alarm_id, minute=minute)
            if not individual_success:
                success = False
        # Parse days variable
        if days is not None:
            individual_success = db.edit_alarm(alarm_id, days=days)
            if not individual_success:
                success = False
        # Parse active variable
        if active is not None:
            individual_success = db.edit_alarm(alarm_id, active=active)
            if not individual_success:
                success = False
        return success

    @staticmethod
    def delete_alarm(alarm_id):
        """
        Remove the alarm with the given ID from the database.
        :param alarm_id: Integer to indicate the primary key of the Alarm to be
                         removed.
        :return: Boolean indicating the success of the 'delete alarm' operation.
        """
        return AlarmDb().delete_alarm(alarm_id)

    @staticmethod
    def delete_all_alarms():
        """
        Removes all the alarms from the database.
        :return: Boolean indicating the success of the 'delete all' operation.
        """
        return AlarmDb().delete_all_alarms()

    #
    # member methods to register and un-register alarm events
    #
    def register_alarm(self, alarm):
        pass


if __name__ == "__main__":
    # Do nothing
    pass
