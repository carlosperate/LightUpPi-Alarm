#!/usr/bin/env python2
#
# Manages an Sqlite database for the alarms
#
# Copyright (c) 2015 carlosperate https://github.com/carlosperate/
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
# This class creates an Sqlite database with an 'alarms' table to contain all
# the alarms with the following columns:
#   id: primary key ID for the alarms row
#   hour: Indicates the hour value for the alarm. Integer from 0 to 23.
#   minute: Indicates the minute value for the alarm. Integer from 0 to 59.
#   monday: Indicates if the alarm repeats every monday. Boolean.
#   tuesday: Indicates if the alarm repeats every tuesday. Boolean.
#   wednesday: Indicates if the alarm repeats every wednesday. Boolean.
#   thursday: Indicates if the alarm repeats every thursday. Boolean.
#   friday: Indicates if the alarm repeats every friday. Boolean.
#   saturday: Indicates if the alarm repeats every saturday. Boolean.
#   sunday: Indicates if the alarm repeats every sunday. Boolean.
#   enabled: Indicates if the alarm is enabled (turned on). Boolean.
#
from __future__ import unicode_literals, absolute_import, print_function
import sys
import dataset
from LightUpAlarm.AlarmItem import AlarmItem


class AlarmDb(object):
    """ Creates and manages a Sqlite database to store and retrieve alarms. """

    #
    # constructor
    #
    def __init__(self, db_name=None):
        """
        AlarmDbHelper constructor.  It can take an argument to indicate the
        sqlite database filename.
        :param db_name: Optional string indicating the database filename.
        """
        if isinstance(db_name, str) or isinstance(db_name, basestring):
            self.db_file = 'sqlite:///%s.db' % db_name
        else:
            if db_name is not None:
                print('The database name inputted in the AlarmDbHelper ' +
                      'constructor is not a valid String !')
            self.db_file = 'sqlite:///alarmdatabase.db'

    #
    # db connection member functions
    #
    def __connect(self):
        """ Connecting to a SQLite database table 'alarms'. """
        alarms_table = dataset.connect(self.db_file)['alarms']
        return alarms_table

    #
    # member functions to retrieve data
    #
    def get_number_of_alarms(self):
        """
        Gets the number of alarms (db table rows) stored in the database.
        :return: Integer indicating the number of saved alarms.
        """
        alarms_table = self.__connect()
        return len(alarms_table)

    def get_all_alarms(self):
        """
        Returns all the alarms in a list of AlarmItems.
        :return: List of AlarmItems containing all alarms. Returns an empty list
                 if there aren't any.
        """
        alarms_table = self.__connect()
        alarm_list = []
        for alarm in alarms_table:
            alarm_list.append(
                AlarmItem(alarm['hour'], alarm['minute'],
                          (alarm['monday'], alarm['tuesday'],
                           alarm['wednesday'], alarm['thursday'],
                           alarm['friday'], alarm['saturday'], alarm['sunday']),
                          alarm['enabled'], alarm['id']))
        return alarm_list

    def get_all_enabled_alarms(self):
        """
        Returns all the alarms with an enabled state in a list of OrderedDicts.
        :return: List of AlarmItems containing all enabled alarms. Returns an
                 empty list if there aren't any.
        """
        alarms_table = self.__connect()
        alarm_list = []
        enabled_alarms = alarms_table.find(enabled=True)
        for alarm in enabled_alarms:
            alarm_list.append(
                AlarmItem(alarm['hour'], alarm['minute'],
                          (alarm['monday'], alarm['tuesday'],
                           alarm['wednesday'], alarm['thursday'],
                           alarm['friday'], alarm['saturday'], alarm['sunday']),
                          alarm['enabled'], alarm['id']))
        return alarm_list

    def get_all_disabled_alarms(self):
        """
        Returns all the alarms with an disabled state in a list of AlarmItems.
        :return: List of AlarmItems containing all disabled alarms. Returns an
                 empty list if there aren't any.
        """
        alarms_table = self.__connect()
        alarm_list = []
        disabled_alarms = alarms_table.find(enabled=False)
        for alarm in disabled_alarms:
            alarm_list.append(
                AlarmItem(alarm['hour'], alarm['minute'],
                          (alarm['monday'], alarm['tuesday'],
                           alarm['wednesday'], alarm['thursday'],
                           alarm['friday'], alarm['saturday'], alarm['sunday']),
                          alarm['enabled'], alarm['id']))
        return alarm_list

    def get_alarm(self, alarm_id):
        """
        Get the alarm with the given ID from the database.
        :param alarm_id: Integer to indicate the primary key of the row to get.
        :return: AlarmItem with the alarm data, or None if id could not be
                 found.
        """
        alarms_table = self.__connect()
        alarm_dict = alarms_table.find_one(id=alarm_id)

        if alarm_dict is None:
            return None
        else:
            return AlarmItem(alarm_dict['hour'], alarm_dict['minute'],
                             (alarm_dict['monday'], alarm_dict['tuesday'],
                              alarm_dict['wednesday'], alarm_dict['thursday'],
                              alarm_dict['friday'], alarm_dict['saturday'],
                              alarm_dict['sunday']),
                             alarm_dict['enabled'], alarm_dict['id'])

    #
    # member functions to add data
    #
    def add_alarm(self, alarm_item):
        """
        Adds an alarm to the database with the input AlarmItem. Returns the new
        row primary key. Uses the following AlarmItem member variables:
        hour: Integer to indicate the alarm hour.
        minute: Integer to indicate the alarm minute.
        days: 7-item list of booleans to indicate repeat weekdays.
        enabled: Boolean to indicate alarm enabled state.
        :return: Integer row primary key.
        """
        if not isinstance(alarm_item, AlarmItem):
            print('ERROR: Provided argument to AlarmDb().add_alarm must be of' +
                  'the AlarmItem type and not %s !' % type(alarm_item),
                  file=sys.stderr)
            return
        alarms_table = self.__connect()
        key = alarms_table.insert(
            dict(hour=alarm_item.hour, minute=alarm_item.minute,
                 monday=alarm_item.monday, tuesday=alarm_item.tuesday,
                 wednesday=alarm_item.wednesday, thursday=alarm_item.thursday,
                 friday=alarm_item.friday, saturday=alarm_item.saturday,
                 sunday=alarm_item.sunday, enabled=alarm_item.enabled))
        return key

    #
    # member functions to edit data
    #
    def edit_alarm(self, alarm_id, hour=None, minute=None, days=None,
                   enabled=None):
        """
        Edits an alarm to the database with the new input data.
        Uses the input sanitation of the AlarmItem class before the data is set.
        :param hour: Optional integer to indicate the new alarm hour.
        :param minute: Optional integer to indicate the new alarm minute.
        :param days: Optional 7-item list of booleans to indicate the new repeat
                     week days.
        :param enabled: Optional boolean to indicate new alarm enabled state.
        :return: Boolean indicating the success of the 'edit' operation.
        """
        alarms_table = self.__connect()
        success = True

        # Parse hour variable
        if hour is not None:
            alarm_item = AlarmItem(hour, 0)
            individual_success = alarms_table.update(
                dict(id=alarm_id, hour=alarm_item.hour), ['id'])
            if not individual_success:
                success = False

        # Parse minute variable
        if minute is not None:
            alarm_item = AlarmItem(0, minute)
            individual_success = alarms_table.update(
                dict(id=alarm_id, minute=alarm_item.minute), ['id'])
            if not individual_success:
                success = False

        # Parse days variable
        if days is not None:
            alarm_item = AlarmItem(0, 0, days=days)
            individual_success = alarms_table.update(
                dict(id=alarm_id, monday=alarm_item.monday,
                     tuesday=alarm_item.tuesday, wednesday=alarm_item.wednesday,
                     thursday=alarm_item.thursday, friday=alarm_item.friday,
                     saturday=alarm_item.saturday, sunday=alarm_item.sunday),
                ['id'])
            if not individual_success:
                success = False

        # Parse enabled variable
        if enabled is not None:
            alarm_item = AlarmItem(0, 0, enabled=enabled)
            individual_success = alarms_table.update(
                dict(id=alarm_id, enabled=alarm_item.enabled), ['id'])
            if not individual_success:
                success = False

        return success

    #
    # member functions to remove data
    #
    def delete_alarm(self, alarm_id):
        """
        Remove the alarm with the given ID from the database.
        :param alarm_id: Integer to indicate the primary key of the row to be
                         removed.
        :return: Boolean indicating the success of the 'delete' operation.
        """
        alarms_table = self.__connect()
        success = alarms_table.delete(id=alarm_id)
        return success

    def delete_all_alarms(self):
        """
        Remove all the alarms by dropping the table and creating it again.
        :return: Boolean indicating the success of the 'delete' operation.
        """
        alarms_table = self.__connect()
        success = alarms_table.delete()
        return success
