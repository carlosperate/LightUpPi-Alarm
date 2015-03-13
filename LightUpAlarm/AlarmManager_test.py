#!/usr/bin/env python2
#
# Unit test for the AlarmManager class.
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
import threading
from LightUpAlarm.AlarmManager import AlarmManager
from LightUpAlarm.AlarmItem import AlarmItem


class AlarmManagerTestCase(unittest.TestCase):
    """ Tests for AlarmManager class. """

    def assert_alarm(self, alarm, alarm_id, hour, minute, days, active):
        self.assertEqual(alarm.id_, alarm_id)
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

    def create_alarms(self, alarm_mgr):
        """ Deletes all alarms and creates 5 with different data. """
        alarm_mgr.delete_all_alarms()
        alarm_mgr.add_alarm(  # id 1
            8, 30, (False, True, False, True, False, True, False), True)
        alarm_mgr.add_alarm(  # id 2
            9, 00, (False, False, True, False, False, True, False), True)
        alarm_mgr.add_alarm(  # id 3
            11, 15, (True, False, False, True, False, False, True), True)
        alarm_mgr.add_alarm(  # id 4
            13, 35, (False, True, False, False, True, False, False), True)
        alarm_mgr.add_alarm(  # id 5
            20, 45, (False, False, True, False, False, True, False), True)

    def test_add_alarm(self):
        """ Adds an alarm and checks it has been set correctly. """
        alarm_mgr = AlarmManager()
        alarm_mgr.delete_all_alarms()
        add_success = alarm_mgr.add_alarm(  # id 1
            8, 30, (False, True, False, True, False, True, False), True)
        self.assertTrue(add_success)
        all_alarms = AlarmManager.get_all_alarms()
        latest = len(all_alarms) - 1
        self.assert_alarm(
            all_alarms[latest], 1, 8, 30,
            (False, True, False, True, False, True, False), True)

    def test_add_alarm_error(self):
        """ Adds an alarm incorrectly and check for errors. """
        alarm_mgr = AlarmManager()
        add_success = alarm_mgr.add_alarm(  # id 1
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
        alarm_mgr = AlarmManager()
        alarm_mgr.delete_all_alarms()
        alarm_mgr.add_alarm(
            11, 20, (True, False, False, False, False, False, False), True)
        alarm_mgr.add_alarm(
            11, 15, (True, False, False, False, False, False, False), True)

        #             year, mon, mday, hour, min, sec, wday, yday, isdst
        time_tuple = (2015,  0,     0,   12,  30,  00,   0,    0,     0)
        mock_time.return_value = time.struct_time(time_tuple)
        next_alarm = AlarmManager.get_next_alarm()
        self.assertEqual(next_alarm.id_, 2)

        #             year, mon, mday, hour, min, sec, wday, yday, isdst
        time_tuple = (2015,  0,     0,   11,  17,  00,   0,    0,     0)
        mock_time.return_value = time.struct_time(time_tuple)
        next_alarm = AlarmManager.get_next_alarm()
        self.assertEqual(next_alarm.id_, 1)

        self.create_alarms(alarm_mgr)

        #             year, mon, mday, hour, min, sec, wday, yday, isdst
        time_tuple = (2015,  0,     0,   19,  30,  00,   1,    0,     0)
        mock_time.return_value = time.struct_time(time_tuple)
        next_alarm = AlarmManager.get_next_alarm()
        self.assertEqual(next_alarm.id_, 2)

        #             year, mon, mday, hour, min, sec, wday, yday, isdst
        time_tuple = (2015,  0,     0,   13,  00,  00,   4,    0,     0)
        mock_time.return_value = time.struct_time(time_tuple)
        next_alarm = AlarmManager.get_next_alarm()
        self.assertEqual(next_alarm.id_, 4)

        #             year, mon, mday, hour, min, sec, wday, yday, isdst
        time_tuple = (2015,  0,     0,   21,  45,  00,   5,    0,     0)
        mock_time.return_value = time.struct_time(time_tuple)
        next_alarm = AlarmManager.get_next_alarm()
        self.assertEqual(next_alarm.id_, 3)

        #             year, mon, mday, hour, min, sec, wday, yday, isdst
        time_tuple = (2015,  0,     0,   11,  15,  00,   6,    0,     0)
        mock_time.return_value = time.struct_time(time_tuple)
        next_alarm = AlarmManager.get_next_alarm()
        self.assertEqual(next_alarm.id_, 3)

    def test_edit_alarm(self):
        """
        Places 5 alarms into the database, it then retrieves one, edits it and
        confirms all edits were successful.
        """
        alarm_mgr = AlarmManager()
        # id 3 = 11, 15, (True, False, False, True, False, False, True), True
        self.create_alarms(alarm_mgr)

        # Check the alarm has the expected data before editing it
        retrieved_alarm = AlarmManager.get_alarm(3)
        self.assert_alarm(
            retrieved_alarm, 3, 11, 15,
            (True, False, False, True, False, False, True), True)

        # Edit it and check values
        edit_success = alarm_mgr.edit_alarm(
            retrieved_alarm.id_, 23, 34,
            (False, True, False, True, False, True, False), False)
        self.assertTrue(edit_success)
        retrieved_alarm = AlarmManager.get_alarm(retrieved_alarm.id_)
        self.assert_alarm(
            retrieved_alarm, 3, 23, 34,
            (False, True, False, True, False, True, False), False)

        # Ensure nothing changes if no edit arguments are added
        edit_success = alarm_mgr.edit_alarm(retrieved_alarm.id_)
        self.assertTrue(edit_success)
        retrieved_alarm = AlarmManager.get_alarm(retrieved_alarm.id_)
        self.assert_alarm(
            retrieved_alarm, 3, 23, 34,
            (False, True, False, True, False, True, False), False)

    def test_set_alarm_thread(self):
        """
        Test that the __set_alarm_thread private method will only launch an
        Alarm Thread if there is an active day and the active state is set.
        Ensure the thread has been launched successfully.
        This test accesses private methods.
        """
        time_now = time.localtime(time.time())
        alarm = AlarmItem(time_now.tm_hour - 1, 34,
                          (True, True, True, True, True, True, True), False, 96)
        alarm_mgr = AlarmManager()
        alarm_mgr.delete_all_alarms()
        numb_threads = threading.activeCount()
        launch_success = alarm_mgr._AlarmManager__set_alarm_thread(alarm)
        self.assertFalse(launch_success)
        self.assertEqual(threading.activeCount(), numb_threads)

        alarm.repeat = (False, False, False, False, False, False, False)
        alarm.active = True
        launch_success = alarm_mgr._AlarmManager__set_alarm_thread(alarm)
        self.assertFalse(launch_success)
        self.assertEqual(threading.activeCount(), numb_threads)

        alarm.wednesday = True
        launch_success = alarm_mgr._AlarmManager__set_alarm_thread(alarm)
        self.assertTrue(launch_success)
        self.assertGreater(threading.activeCount(), numb_threads)

    def test_set_alarm_thread_edit(self):
        pass

    def test_stop_alarm_thread(self):
        """
        Test that the __stop_alarm_thread private method will stop a running
        Alarm Thread, which due to the nature of the thread code can take up to
        10 seconds.
        This test accesses private methods.
        """
        time_now = time.localtime(time.time())
        alarm = AlarmItem(time_now.tm_hour - 1, 34,
                         (False, True, True, True, True, True, True), True, 96)
        alarm_mgr = AlarmManager()
        alarm_mgr.delete_all_alarms()
        numb_threads = threading.activeCount()
        launch_success = alarm_mgr._AlarmManager__set_alarm_thread(alarm)
        self.assertTrue(launch_success)
        self.assertGreater(threading.activeCount(), numb_threads)
        stop_success = alarm_mgr._AlarmManager__stop_alarm_thread(alarm.id_)
        self.assertTrue(stop_success)
        self.assertEqual(threading.activeCount(), numb_threads)

    # Needed to be able to test the thread callback
    thread_alert = False

    @staticmethod
    def c():
        AlarmManagerTestCase.thread_alert = True

    def test_alarm_trigger_callback(self):
        """
        Creates and alarm to trigger within a minute and check it has done so
        correctly.
        This test uses the static variable AlarmManagerTestCase.thread_alert to
        be be change it in the callback function, and exit an infinite loop.
        This test can take a maximum of 1 minute to complete.
        """
        time_now = time.localtime(time.time())
        # Set alarm for next minute. Better than current minute as it might pass
        # before the alarm thread is able to trigger.
        alarm = AlarmItem(
            time_now.tm_hour, time_now.tm_min + 1,
            (True, True, True, True, True, True, True), True, 96)
        alarm_mgr = AlarmManager(alarm_callback=AlarmManagerTestCase.c)
        alarm_mgr.delete_all_alarms()
        launch_success = alarm_mgr._AlarmManager__set_alarm_thread(alarm)
        self.assertTrue(launch_success)
        while AlarmManagerTestCase.thread_alert is False:
            # This loop will never finish if the thread does not callback
            time.sleep(0.001)
        self.assertTrue(AlarmManagerTestCase.thread_alert)


if __name__ == '__main__':
    unittest.main()
