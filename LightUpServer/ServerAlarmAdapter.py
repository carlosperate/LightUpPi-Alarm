#!/usr/bin/env python2
#
# Adapter class to interface with the LightUpAlarm AlarmManager.
#
# Copyright (c) 2015 carlosperate https://github.com/carlosperate/
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
    # Alarm operations
    #
    def get_number_of_alarms(self):
        """
        Gets the number of alarms stored in the database.
        :return: Integer indicating the number of alarms in the db.
        """
        return self.alarm_mgr.get_number_of_alarms()

    def add_alarm(self, hour, minute,
                  days=(False, False, False, False, False, False, False),
                  enabled=True, label=''):
        """
        Adds an alarm by sending it to the AlamarManager class instance.
        Input sanitation is done at the AlamarManager method.
        :param hour: Integer to indicate the alarm hour.
        :param minute: Integer to indicate the alarm minute.
        :param days: 7-item list of booleans to indicate repeat weekdays.
        :param enabled: Boolean to indicate the alarm enabled state.
        :param label: Strong to contain the alarm label.
        :return: Integer indicating the newly created alarm ID, or None if fail.
        """
        return self.alarm_mgr.add_alarm(hour, minute, days, enabled, label)

    def edit_alarm(self, alarm_id, hour=None, minute=None, days=None,
                   enabled=None, label=None):
        """
        Edits an alarm from the database by sending the input data to the
        AlamarManager class instance.
        :param alarm_id: Integer to indicate the ID of the alarm to be edited.
        :param hour: Integer to indicate the alarm hour.
        :param minute: Integer to indicate the alarm minute.
        :param days: 7-item list of booleans to indicate repeat weekdays.
        :param enabled: Boolean to indicate alarm enabled state.
        :param label: Strong to contain the alarm label.
        :return: Boolean indicating the success of the 'edit' operation.
        """
        return self.alarm_mgr.add_alarm(
            alarm_id, hour, minute, days, enabled, label)

    def delete_alarm(self, alarm_id):
        """
        Remove the alarm with the given ID by sending it to the AlamarManager
        class instance.
        :param alarm_id: Integer to indicate ID of the Alarm to be removed.
        :return: Boolean indicating the success of the 'delete alarm' operation.
        """
        return self.alarm_mgr.delete_alarm(alarm_id)

    def delete_all_alarms(self):
        """
        Removes all alarms.
        :return: Boolean indicating the success of the 'delete all' operation.
        """
        return self.alarm_mgr.delete_all()

    #
    # convert to python generic data
    #
    @staticmethod
    def alarm_to_dict(alarm):
        return {'id': alarm.id_,
                'hour': alarm.hour,
                'minute': alarm.minute,
                'enabled': alarm.enabled,
                'label': alarm.label,
                'monday': alarm.monday,
                'tuesday': alarm.tuesday,
                'wednesday': alarm.wednesday,
                'thursday': alarm.thursday,
                'friday': alarm.friday,
                'saturday': alarm.saturday,
                'sunday': alarm.sunday}

    #
    # convert to json methods
    #
    def json_get_alarm(self, alarm_id):
        alarm = self.alarm_mgr.get_alarm(alarm_id)
        return json.dumps(
            ServerAlarmAdapter.alarm_to_dict(alarm),
            indent=4, separators=(',', ': '))

    def json_get_next_alarm(self, alarm_id):
        alarm = self.alarm_mgr.get_next_alarm()
        return json.dump(ServerAlarmAdapter.alarm_to_dict(alarm))

    def json_get_all_alarms(self):
        all_alarms = self.alarm_mgr.get_all_alarms()
        alarms_dicts = []
        for alarm in all_alarms:
            alarms_dicts.append(ServerAlarmAdapter.alarm_to_dict(alarm))
        alarms_dicts = {'size': len(alarms_dicts), 'alarms': alarms_dicts}
        return json.dumps(alarms_dicts, indent=4, separators=(',', ': '))
