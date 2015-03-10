#!/usr/bin/env python2
#
# Unit test for the AlarmItem class.
#
# Copyright (c) 2015 carlosperate https://github.com/carlosperate/
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
# The following methods are basically a call to the AlarmDb class and do not
# need to be tested:
#  get_all_alarms, get_number_of_alarms, get_all_active_alarms, get_alarm,
#  delete_alarm, delete_all_alarms
#
from __future__ import unicode_literals, absolute_import
import unittest
import mock
import time
from LightUpAlarm.AlarmManager import AlarmManager


class AlarmManagerTestCase(unittest.TestCase):
    """ Tests for AlarmManager class. """

    def assert_alarm(self, alarm, alarm_id, hour, minute, days, active):
        self.assertEqual(alarm.id, alarm_id)
        self.assertEqual(alarm.hour, hour)
        self.assertEqual(alarm.minute, minute)
        self.assertEqual(alarm.monday, days[0])
        self.assertEqual(alarm.tuesday, days[1])
        self.assertEqual(alarm.wednesday, days[2])
        self.assertEqual(alarm.thursday, days[3])
        self.assertEqual(alarm.friday, days[4])
        self.assertEqual(alarm.saturday, days[5])
        self.assertEqual(alarm.sunday, days[6])
        self.assertEqual(alarm.active, active)

    def create_alarms(self):
        """ Deletes all alarms and creates 5 with different data. """
        AlarmManager.delete_all_alarms()
        AlarmManager.add_alarm(  # id 1
            8, 30, (False, True, False, True, False, True, False), True)
        AlarmManager.add_alarm(  # id 2
            9, 00, (False, False, True, False, False, True, False), True)
        AlarmManager.add_alarm(  # id 3
            11, 15, (True, False, False, True, False, False, True), True)
        AlarmManager.add_alarm(  # id 4
            13, 35, (False, True, False, False, True, False, False), True)
        AlarmManager.add_alarm(  # id 5
            20, 45, (False, False, True, False, False, True, False), True)

    def test_add_alarm(self):
        """ Adds an alarm and checks it has been set correctly. """
        AlarmManager.delete_all_alarms()
        add_success = AlarmManager.add_alarm(  # id 1
            8, 30, (False, True, False, True, False, True, False), True)
        self.assertTrue(add_success)
        all_alarms = AlarmManager.get_all_alarms()
        latest = len(all_alarms) - 1
        self.assert_alarm(
            all_alarms[latest], 1, 8, 30,
            (False, True, False, True, False, True, False), True)

    def test_add_alarm_error(self):
        """ Adds an alarm incorrectly and check for errors. """
        add_success = AlarmManager.add_alarm(  # id 1
            8, 30, (False, True, False, True, False, True, False), True)
        self.assertTrue(add_success)

    def test_dummy_alarms(self):
        """
        Tests that if the database is empty it will populate it with the dummy
        alarms.
        This also accesses the static methods from a AlarmManager() instacne.
        """
        alarm_mgr = AlarmManager()
        alarm_mgr.delete_all_alarms()
        self.assertEqual(alarm_mgr.get_number_of_alarms(), 0)
        alarm_mgr = AlarmManager()
        self.assertNotEqual(alarm_mgr.get_number_of_alarms(), 0)

    @mock.patch('LightUpAlarm.AlarmManager.time.localtime')
    def test_get_next_alarm(self, mock_time):
        """
        Creates 5 alarms with different settings. It then mocks the current time
        to get calculate the next alarm at different reference points.
        """
        AlarmManager.delete_all_alarms()
        AlarmManager.add_alarm(
            11, 20, (True, False, False, False, False, False, False), True)
        AlarmManager.add_alarm(
            11, 15, (True, False, False, False, False, False, False), True)

        #             year, mon, mday, hour, min, sec, wday, yday, isdst
        time_tuple = (2015,  0,     0,   12,  30,  00,   0,    0,     0)
        mock_time.return_value = time.struct_time(time_tuple)
        next_alarm = AlarmManager.get_next_alarm()
        self.assertEqual(next_alarm.id, 2)

        #             year, mon, mday, hour, min, sec, wday, yday, isdst
        time_tuple = (2015,  0,     0,   11,  17,  00,   0,    0,     0)
        mock_time.return_value = time.struct_time(time_tuple)
        next_alarm = AlarmManager.get_next_alarm()
        self.assertEqual(next_alarm.id, 1)

        self.create_alarms()

        #             year, mon, mday, hour, min, sec, wday, yday, isdst
        time_tuple = (2015,  0,     0,   19,  30,  00,   1,    0,     0)
        mock_time.return_value = time.struct_time(time_tuple)
        next_alarm = AlarmManager.get_next_alarm()
        self.assertEqual(next_alarm.id, 2)

        #             year, mon, mday, hour, min, sec, wday, yday, isdst
        time_tuple = (2015,  0,     0,   13,  00,  00,   4,    0,     0)
        mock_time.return_value = time.struct_time(time_tuple)
        next_alarm = AlarmManager.get_next_alarm()
        self.assertEqual(next_alarm.id, 4)

        #             year, mon, mday, hour, min, sec, wday, yday, isdst
        time_tuple = (2015,  0,     0,   21,  45,  00,   5,    0,     0)
        mock_time.return_value = time.struct_time(time_tuple)
        next_alarm = AlarmManager.get_next_alarm()
        self.assertEqual(next_alarm.id, 3)

        #             year, mon, mday, hour, min, sec, wday, yday, isdst
        time_tuple = (2015,  0,     0,   11,  15,  00,   6,    0,     0)
        mock_time.return_value = time.struct_time(time_tuple)
        next_alarm = AlarmManager.get_next_alarm()
        self.assertEqual(next_alarm.id, 3)

    def test_edit_alarm(self):
        """
        Places 5 alarms into the database, it then retrieves one, edits it and
        confirms all edits were successful.
        """
        # id 3 = 11, 15, (True, False, False, True, False, False, True), True
        self.create_alarms()

        # Check the alarm has the expected data before editing it
        retrieved_alarm = AlarmManager.get_alarm(3)
        self.assert_alarm(
            retrieved_alarm, 3, 11, 15,
            (True, False, False, True, False, False, True), True)

        # Edit it and check values
        edit_success = AlarmManager.edit_alarm(
            retrieved_alarm.id, 23, 34,
            (False, True, False, True, False, True, False), False)
        self.assertTrue(edit_success)
        retrieved_alarm = AlarmManager.get_alarm(retrieved_alarm.id)
        self.assert_alarm(
            retrieved_alarm, 3, 23, 34,
            (False, True, False, True, False, True, False), False)

        # Ensure nothing changes if no edit arguments are added
        edit_success = AlarmManager.edit_alarm(retrieved_alarm.id)
        self.assertTrue(edit_success)
        retrieved_alarm = AlarmManager.get_alarm(retrieved_alarm.id)
        self.assert_alarm(
            retrieved_alarm, 3, 23, 34,
            (False, True, False, True, False, True, False), False)


if __name__ == '__main__':
    unittest.main()
