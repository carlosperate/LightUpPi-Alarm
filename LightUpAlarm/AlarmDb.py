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
# It also contains a 'settings' table to contain general alarm configuration
# settings. The rows and columns are predetermined to the following
# configuration for simple conversion to json.
#   row 1 -> column 'snooze_time', column 'prealert_time'
#
from __future__ import unicode_literals, absolute_import, print_function
import sys
import json
import types
import dataset
import StringIO
try:
    from LightUpAlarm.AlarmItem import AlarmItem
except ImportError:
    from AlarmItem import AlarmItem


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

        # Check if the settings table is empty
        settings_table = self.__connect_settings()
        rows = settings_table.all()
        if rows.count == 0:
            settings_table.insert(dict(snooze_time=3, prealert_time=15))

    #
    # db connection member functions
    #
    def __connect_alarms(self):
        """ Connecting to a SQLite database table 'alarms'. """
        alarms_table = dataset.connect(self.db_file)['alarms']
        return alarms_table

    def __connect_settings(self):
        """ Connecting to a SQLite database table 'settings'. """
        settings_table = dataset.connect(self.db_file)['settings']
        return settings_table

    #
    # member functions to set settings
    #
    def set_snooze_time(self, snooze_time):
        """
        Sets the snooze time in the settings table.
        :param snooze_time: Integer, new snooze time in minutes.
        :return: Boolean indicating the operation success.
        """
        if isinstance(snooze_time, types.IntType) and snooze_time >= 0:
            settings_table = self.__connect_settings()
            success = settings_table.update(
                dict(id=1, snooze_time=snooze_time), ['id'])
            return success
        else:
            return False

    def get_snooze_time(self):
        """
        Retrieves the alarm snooze time from the setting table
        :return: Integer, snooze time in minutes
        """
        settings_table = self.__connect_settings()
        settings_dict = settings_table.find_one(id=1)
        return settings_dict['snooze_time']

    def set_prealert_time(self, prealert_time):
        """
        Sets the prealert time (the time before the alarm alert is triggered),
        used to set some action before the alarm rings.
        :param prealert_time: Integer, prealert time in minutes.
        :return: Boolean indicating the operation success.
        """
        if isinstance(prealert_time, types.IntType) and prealert_time >= 0:
            settings_table = self.__connect_settings()
            success = settings_table.update(
                dict(id=1, prealert_time=prealert_time), ['id'])
            return success
        else:
            return False

    def get_prealert_time(self):
        """
        Retrieves from the settings table the prealeter time (the time before
        the alarm alert is triggered), used to set some action before the
        alarm rings.
        :return: Integer, the prealert time in minutes.
        """
        settings_table = self.__connect_settings()
        settings_dict = settings_table.find_one(id=1)
        return settings_dict['prealert_time']

    def reset_settings(self):
        """
        Resets the settings table to the default settings (3 min snooze time,
        and 15 min prealert time).
        :return: Boolean indicating the operation success.
        """
        settings_table = self.__connect_settings()
        success = settings_table.delete()
        if success is True:
            settings_table = self.__connect_settings()
            insert_success = settings_table.insert(
                dict(snooze_time=3, prealert_time=15))
            success = bool(insert_success)
        return success

    #
    # member functions to retrieve alarm data
    #
    def get_number_of_alarms(self):
        """
        Gets the number of alarms (db table rows) stored in the database.
        :return: Integer indicating the number of saved alarms.
        """
        alarms_table = self.__connect_alarms()
        return len(alarms_table)

    def get_all_alarms(self):
        """
        Returns all the alarms in a list of AlarmItems.
        :return: List of AlarmItems containing all alarms. Returns an empty list
                 if there aren't any.
        """
        alarms_table = self.__connect_alarms()
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
        alarms_table = self.__connect_alarms()
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
        alarms_table = self.__connect_alarms()
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
        alarms_table = self.__connect_alarms()
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

    def export_alarms_json(self):
        """
        Exports all the alarm data into a JSON string.
        The dataset.freeze() method exports the table into a file object, but
        it is going to be "tricked" into getting an string object to send back.
        Because it also closes the object file we need to overwrite the close
        function to retrieve the data and, then restore it back to normal.
        :return: String containing all the alarm data
        """
        def fake_close():
            pass
        out_iostr = StringIO.StringIO()
        original_close = out_iostr.close
        alarms_table = self.__connect_alarms()

        # Retrieve the db as a json StringIO without the close method
        out_iostr.close = fake_close
        dataset.freeze(alarms_table.all(), format='json', fileobj=out_iostr)
        out_str = out_iostr.getvalue()
        out_iostr.close = original_close
        out_iostr.close()

        # Get only the required data and format it
        alarms_dict = {'alarms': json.loads(out_str)['results']}

        # This commented out line would prettify the string
        #json.dumps(alarms_dict, indent=4, separators=(',', ': '))
        return json.dumps(alarms_dict)

    #
    # member functions to add alarm data
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
        alarms_table = self.__connect_alarms()
        key = alarms_table.insert(
            dict(hour=alarm_item.hour, minute=alarm_item.minute,
                 monday=alarm_item.monday, tuesday=alarm_item.tuesday,
                 wednesday=alarm_item.wednesday, thursday=alarm_item.thursday,
                 friday=alarm_item.friday, saturday=alarm_item.saturday,
                 sunday=alarm_item.sunday, enabled=alarm_item.enabled))
        return key

    #
    # member functions to edit alarm data
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
        alarms_table = self.__connect_alarms()
        success = True

        # Parse hour variable
        if hour is not None:
            alarm_item = AlarmItem(hour, 0)
            if alarm_item is not None:
                individual_success = alarms_table.update(
                    dict(id=alarm_id, hour=alarm_item.hour), ['id'])
                if not individual_success:
                    success = False
            else:
                success = False

        # Parse minute variable
        if minute is not None:
            alarm_item = AlarmItem(0, minute)
            if alarm_item is not None:
                individual_success = alarms_table.update(
                    dict(id=alarm_id, minute=alarm_item.minute), ['id'])
                if not individual_success:
                    success = False
            else:
                success = False

        # Parse days variable
        if days is not None:
            alarm_item = AlarmItem(0, 0, days=days)
            if alarm_item is not None:
                individual_success = alarms_table.update(
                    dict(id=alarm_id, monday=alarm_item.monday,
                         tuesday=alarm_item.tuesday,
                         wednesday=alarm_item.wednesday,
                         thursday=alarm_item.thursday,
                         friday=alarm_item.friday,
                         saturday=alarm_item.saturday,
                         sunday=alarm_item.sunday),
                    ['id'])
                if not individual_success:
                    success = False
            else:
                success = False

        # Parse enabled variable
        if enabled is not None:
            alarm_item = AlarmItem(0, 0, enabled=enabled)
            if alarm_item is not None:
                individual_success = alarms_table.update(
                    dict(id=alarm_id, enabled=alarm_item.enabled), ['id'])
                if not individual_success:
                    success = False
            else:
                success = False

        return success

    #
    # member functions to remove alarm data
    #
    def delete_alarm(self, alarm_id):
        """
        Remove the alarm with the given ID from the database.
        :param alarm_id: Integer to indicate the primary key of the row to be
                         removed.
        :return: Boolean indicating the success of the 'delete' operation.
        """
        alarms_table = self.__connect_alarms()
        success = alarms_table.delete(id=alarm_id)
        return success

    def delete_all_alarms(self):
        """
        Remove all the alarms by dropping the table and creating it again.
        :return: Boolean indicating the success of the 'delete' operation.
        """
        alarms_table = self.__connect_alarms()
        success = alarms_table.delete()
        return success
