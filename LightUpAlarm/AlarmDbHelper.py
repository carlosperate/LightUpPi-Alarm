#!/usr/bin/env python2
#
# Short description
#
# Copyright (c) 2015 carlosperate https://github.com/carlosperate/
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
# Full description goes here
# AlarmDbHelper is only called from AlarmManager, which does all input
# sanitation with the AlarmItem class.
#
from __future__ import unicode_literals, absolute_import
import dataset


class AlarmDbHelper(object):
    """
    Class description goes here.
    """
    # Contains the filename for the database file
    db_file = None
    # Database table for the alarms
    alarms_table = None

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
            self.db_file = 'sqlite:///mydatabase.db'

    #
    # db connection member functions
    #
    def _connect(self):
        """ Connecting to a SQLite database table 'alarms'. """
        self.alarms_table = dataset.connect(self.db_file)['alarms']

    #
    # member functions to retrieve data
    #
    def get_number_of_alarms(self):
        """
        Gets the number of alarms (db table rows) stored in the database.
        :return: Integer indicating the number of saved alarms.
        """
        self._connect()
        total_number = len(self.alarms_table)
        return total_number

    def get_all_alarms(self):
        """
        Returns all the alarms in a list of OrderedDicts.
        :return: List of OrderedDicts containing all alarms table rows.
        """
        self._connect()
        alarm_list = []
        for alarm in self.alarms_table:
            alarm_list.append(alarm)
        return alarm_list

    def get_all_active_alarms(self):
        """
        Returns all the alarms with an active state in a list of OrderedDicts.
        :return: List of OrderedDicts containing all active alarms.
        """
        self._connect()
        alarm_list = []
        active_alarms = self.alarms_table.find(active=True)
        for alarm in active_alarms:
            alarm_list.append(alarm)
        return alarm_list

    def get_all_inactive_alarms(self):
        """
        Returns all the alarms with an active state in a list of OrderedDicts.
        :return: List of OrderedDicts containing all active alarms.
        """
        self._connect()
        alarm_list = []
        active_alarms = self.alarms_table.find(active=False)
        for alarm in active_alarms:
            alarm_list.append(alarm)
        return alarm_list

    def get_alarm(self, alarm_id):
        """
        Get the alarm with the given ID from the database.
        :param alarm_id: integer to indicate the primary key of the row to get.
        :return: Ordered Dictionary with the alarm data, or None if id could
                 not be found.
        """
        self._connect()
        alarm = self.alarms_table.find_one(id=alarm_id)
        return alarm

    #
    # member functions to add data
    #
    def add_alarm(self, hour, minute, days, active):
        """
        Adds an alarm to the database with the input data. Returns the new row
        primary key.
        :param hour: integer to indicate the alarm hour.
        :param minute: integer to indicate the alarm minute.
        :param days: 7-item list of booleans to indicate repeat weekdays.
        :param active: boolean alarm active state.
        :return: integer row primary key.
        """
        self._connect()
        key = self.alarms_table.insert(
            dict(hour=hour, minute=minute, monday=days[0], tuesday=days[1],
                 wednesday=days[2], thursday=days[3], friday=days[4],
                 saturday=days[5], sunday=days[6], active=active))
        return key

    #
    # member functions to edit data
    #
    def edit_alarm(self, alarm_id, hour=None, minute=None, days=None,
                   active=None):
        """
        Edits an alarm to the database with the new input data.
        :param hour: Optional integer to indicate the new alarm hour.
        :param minute: Optional integer to indicate the new alarm minute.
        :param days: Optional 7-item list of booleans to indicate the new repeat
                     week days.
        :param active: Optional boolean to indicate new alarm active state.
        """
        self._connect()
        success = True

        # Parse hour variable
        if hour is not None:
            individual_success = self.alarms_table.update(
                dict(id=alarm_id, hour=hour), ['id'])
            if not individual_success:
                success = False

        # Parse minute variable
        if minute is not None:
            individual_success = self.alarms_table.update(
                dict(id=alarm_id, minute=minute), ['id'])
            if not individual_success:
                success = False

        # Parse days variable
        if days is not None:
            individual_success = self.alarms_table.update(
                dict(id=alarm_id, monday=days[0], tuesday=days[1],
                     wednesday=days[2], thursday=days[3], friday=days[4],
                     saturday=days[5], sunday=days[6]), ['id'])
            if not individual_success:
                success = False

        # Parse active variable
        if active is not None:
            individual_success = self.alarms_table.update(
                dict(id=alarm_id, active=active), ['id'])
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
        """
        self._connect()
        success = self.alarms_table.delete(id=alarm_id)
        return success

    def delete_all_alarms(self):
        """
        Remove all the alarms by dropping the table and creating it again.
        """
        self._connect()
        sucess = self.alarms_table.delete()
        return sucess


if __name__ == "__main__":
    # Do nothing for now, run test otherwise?
    pass
