#!/usr/bin/env python2
#
# Short description
#
# Copyright (c) 2015 carlosperate https://github.com/carlosperate/
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
# Full description goes here
#
from __future__ import unicode_literals, absolute_import, print_function
import sys
import dataset
from LightUpAlarm.AlarmItem import AlarmItem


class AlarmDb(object):
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
            self.db_file = 'sqlite:///alarmdatabase.db'

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
        return len(self.alarms_table)

    def get_all_alarms(self):
        """
        Returns all the alarms in a list of AlarmItems.
        :return: List of AlarmItems containing all alarms. Returns an empty list
                 if there aren't any.
        """
        self._connect()
        alarm_list = []
        for alarm in self.alarms_table:
            alarm_list.append(
                AlarmItem(alarm['hour'], alarm['minute'],
                          (alarm['monday'], alarm['tuesday'],
                           alarm['wednesday'], alarm['thursday'],
                           alarm['friday'], alarm['saturday'], alarm['sunday']),
                          alarm['active'], alarm['id']))
        return alarm_list

    def get_all_active_alarms(self):
        """
        Returns all the alarms with an active state in a list of OrderedDicts.
        :return: List of AlarmItems containing all active alarms. Returns an
                 empty list if there aren't any.
        """
        self._connect()
        alarm_list = []
        active_alarms = self.alarms_table.find(active=True)
        for alarm in active_alarms:
            alarm_list.append(
                AlarmItem(alarm['hour'], alarm['minute'],
                          (alarm['monday'], alarm['tuesday'],
                           alarm['wednesday'], alarm['thursday'],
                           alarm['friday'], alarm['saturday'], alarm['sunday']),
                          alarm['active'], alarm['id']))
        return alarm_list

    def get_all_inactive_alarms(self):
        """
        Returns all the alarms with an active state in a list of AlarmItems.
        :return: List of AlarmItems containing all active alarms. Returns an
                 empty list if there aren't any.
        """
        self._connect()
        alarm_list = []
        active_alarms = self.alarms_table.find(active=False)
        for alarm in active_alarms:
            alarm_list.append(
                AlarmItem(alarm['hour'], alarm['minute'],
                          (alarm['monday'], alarm['tuesday'],
                           alarm['wednesday'], alarm['thursday'],
                           alarm['friday'], alarm['saturday'], alarm['sunday']),
                          alarm['active'], alarm['id']))
        return alarm_list

    def get_alarm(self, alarm_id):
        """
        Get the alarm with the given ID from the database.
        :param alarm_id: integer to indicate the primary key of the row to get.
        :return: AlarmItem with the alarm data, or None if id could
                 not be found.
        """
        self._connect()
        alarm_dict = self.alarms_table.find_one(id=alarm_id)

        if alarm_dict is None:
            return None
        else:
            return AlarmItem(alarm_dict['hour'], alarm_dict['minute'],
                             (alarm_dict['monday'], alarm_dict['tuesday'],
                              alarm_dict['wednesday'], alarm_dict['thursday'],
                              alarm_dict['friday'], alarm_dict['saturday'],
                              alarm_dict['sunday']),
                             alarm_dict['active'], alarm_dict['id'])

    #
    # member functions to add data
    #
    def add_alarm(self, alarm_item):
        """
        Adds an alarm to the database with the input AlarmItem. Returns the new
        row primary key. Uses the following AlarmItem member variables:
        hour: integer to indicate the alarm hour.
        minute: integer to indicate the alarm minute.
        days: 7-item list of booleans to indicate repeat weekdays.
        active: boolean alarm active state.
        :return: integer row primary key.
        """
        if not isinstance(alarm_item, AlarmItem):
            print('ERROR: Provided argument to AlarmDb().add_alarm must be of' +
                  'the AlarmItem type and not %s !' % type(alarm_item),
                  file=sys.stderr)
            return
        self._connect()
        key = self.alarms_table.insert(
            dict(hour=alarm_item.hour, minute=alarm_item.minute,
                 monday=alarm_item.monday, tuesday=alarm_item.tuesday,
                 wednesday=alarm_item.wednesday, thursday=alarm_item.thursday,
                 friday=alarm_item.friday, saturday=alarm_item.saturday,
                 sunday=alarm_item.sunday, active=alarm_item.active))
        return key

    #
    # member functions to edit data
    #
    def edit_alarm(self, alarm_id, hour=None, minute=None, days=None,
                   active=None):
        """
        Edits an alarm to the database with the new input data.
        Uses the input sanitation of the AlarmItem class before the data is set.
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
            alarm_item = AlarmItem(hour, 0)
            individual_success = self.alarms_table.update(
                dict(id=alarm_id, hour=alarm_item.hour), ['id'])
            if not individual_success:
                success = False

        # Parse minute variable
        if minute is not None:
            alarm_item = AlarmItem(0, minute)
            individual_success = self.alarms_table.update(
                dict(id=alarm_id, minute=alarm_item.minute), ['id'])
            if not individual_success:
                success = False

        # Parse days variable
        if days is not None:
            alarm_item = AlarmItem(0, 0, days=days)
            individual_success = self.alarms_table.update(
                dict(id=alarm_id, monday=alarm_item.monday,
                     tuesday=alarm_item.tuesday, wednesday=alarm_item.wednesday,
                     thursday=alarm_item.thursday, friday=alarm_item.friday,
                     saturday=alarm_item.saturday, sunday=alarm_item.sunday),
                ['id'])
            if not individual_success:
                success = False

        # Parse active variable
        if active is not None:
            alarm_item = AlarmItem(0, 0, active=active)
            individual_success = self.alarms_table.update(
                dict(id=alarm_id, active=alarm_item.active), ['id'])
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
