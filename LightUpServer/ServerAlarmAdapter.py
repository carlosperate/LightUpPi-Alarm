#!/usr/bin/env python2
#
# Adapter class to interface with the LightUpAlarm AlarmManager.
#
# Copyright (c) 2015 carlosperate http://carlosperate.github.io
#
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
# Uses the class structures defined in:
#   LightUpAlarm.AlarmItem
#   LightUpAlarm.AlarmManager
#
from __future__ import unicode_literals, absolute_import
import json
#try:
#    from LightUpAlarm.AlarmManager import AlarmManager
#except ImportError:
#    from ..LightUpAlarm.AlarmManager import AlarmManager


class ServerAlarmAdapter(object):
    """
    Object Adapter for the LightUpAlarm.AlarmManager class.
    It provides data conversion from AlarmManager data to web-friendly formats.
    This is an Object Adapter, rather than a Class adapter, to reduce coopling
    and dependency on the parent class and simplify the possible replacement
    of the LightUpPi Alarm system.
    """

    #
    # metaclass methods
    #
    def __init__(self, alarm_mgr):
        """
        ServerAlarmAdapter initialiser. Takes an instance to
        LightUpAlarm.AlarmManager class and produces server
        :param alarm_mgr:
        :return:
        """
        self.alarm_mgr = alarm_mgr

    #
    # Alarm operations with normal python data
    #
    def get_number_of_alarms(self):
        """
        Gets the number of alarms stored in the database.
        :return: Integer indicating the number of alarms in the db.
        """
        return self.alarm_mgr.get_number_of_alarms()

    @staticmethod
    def alarm_to_dict(alarm):
        return {'id': alarm.id_,
                'hour': alarm.hour,
                'minute': alarm.minute,
                'enabled': alarm.enabled,
                'label': alarm.label,
                'timestamp': alarm.timestamp,
                'monday': alarm.monday,
                'tuesday': alarm.tuesday,
                'wednesday': alarm.wednesday,
                'thursday': alarm.thursday,
                'friday': alarm.friday,
                'saturday': alarm.saturday,
                'sunday': alarm.sunday}

    def get_alarm_repeat(self, alarm_id):
        alarm = self.alarm_mgr.get_alarm(alarm_id)
        return alarm.repeat

    #
    # retrieve alarm data in json format
    #
    def json_get_alarm(self, alarm_id):
        alarm = self.alarm_mgr.get_alarm(alarm_id)
        return json.dumps(
            ServerAlarmAdapter.alarm_to_dict(alarm),
            indent=4, separators=(',', ': '))

    def json_get_next_alarm(self):
        alarm = self.alarm_mgr.get_next_alarm()
        return json.dump(ServerAlarmAdapter.alarm_to_dict(alarm))

    def json_get_all_alarms(self):
        all_alarms = self.alarm_mgr.get_all_alarms()
        alarms_dicts = []
        for alarm in all_alarms:
            alarms_dicts.append(ServerAlarmAdapter.alarm_to_dict(alarm))
        alarms_dicts = {'dataType': 'All alarms',
                        'size': len(alarms_dicts),
                        'alarms': alarms_dicts}
        return json.dumps(alarms_dicts, indent=4, separators=(',', ': '))

    #
    # Perform operations to the alarms (add, edit, delete) returning json data
    #
    def json_add_alarm(self, hour, minute,
                       days=(False, False, False, False, False, False, False),
                       enabled=True, label='', timestamp=None):
        """
        Adds an alarm by sending it to the AlarmManager class instance.
        Input sanitation is done at the AlarmManager method.
        :param hour: Integer to indicate the alarm hour.
        :param minute: Integer to indicate the alarm minute.
        :param days: 7-item list of booleans to indicate repeat weekdays.
        :param enabled: Boolean to indicate the alarm enabled state.
        :param label: Strong to contain the alarm label.
        :param timestamp: Time, in seconds since 1970, that this alarm was last
                          modified. This value can be added in order to be
                          able to synchronise alarms between different systems.
        :return: Integer indicating the newly created alarm ID, or None if fail.
        """
        alarm_id = self.alarm_mgr.add_alarm(
            hour, minute, days=days, enabled=enabled, label=label,
            timestamp=timestamp)

        return_dict = {'dataType': 'Add alarm'}
        if alarm_id is not None:
            retrieved_alarm = self.alarm_mgr.get_alarm(alarm_id)
            return_dict['id'] = alarm_id
            return_dict['success'] = True
            return_dict['timestamp'] = retrieved_alarm.timestamp
        else:
            return_dict['success'] = False
        return json.dumps(return_dict, indent=4, separators=(',', ': '))

    def json_edit_alarm(self, alarm_id, hour=None, minute=None, days=None,
                        enabled=None, label=None):
        """
        Edits an alarm from the database by sending the input data to the
        AlarmManager class instance.
        :param alarm_id: Integer to indicate the ID of the alarm to be edited.
        :param hour: Integer to indicate the alarm hour.
        :param minute: Integer to indicate the alarm minute.
        :param days: 7-item list of booleans to indicate repeat weekdays.
        :param enabled: Boolean to indicate alarm enabled state.
        :param label: Strong to contain the alarm label.
        :return: Boolean indicating the success of the 'edit' operation.
        """
        success = self.alarm_mgr.edit_alarm(
            alarm_id, hour=hour, minute=minute, days=days, enabled=enabled,
            label=label)
        retrieved_alarm = self.alarm_mgr.get_alarm(alarm_id)
        return_dict = {'dataType': 'Edit alarm',
                       'success': success,
                       'timestamp': retrieved_alarm.timestamp}
        return json.dumps(return_dict, indent=4, separators=(',', ': '))

    def json_delete_alarm(self, alarm_id):
        """
        Remove the alarm with the given ID.
        :param alarm_id: Integer to indicate ID of the Alarm to be removed.
        :return: JSON string containing the data type, deleted alarm ID, and
                 success information.
        """
        success = self.alarm_mgr.delete_alarm(alarm_id)
        return_dict = {'dataType': 'Deleted alarm',
                       'id': alarm_id,
                       'success': success}
        return json.dumps(return_dict, indent=4, separators=(',', ': '))

    def json_delete_all_alarms(self):
        """
        Removes all alarms.
        :return: JSON string containing the data type, and success information.
        """
        success = self.alarm_mgr.delete_all()
        return_dict = {'dataType': 'Deleted all alarms',
                       'id': alarm_id,
                       'success': success}
        return json.dumps(return_dict, indent=4, separators=(',', ': '))
