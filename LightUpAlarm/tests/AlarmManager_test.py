#!/usr/bin/env python2
#
# Unit test for the AlarmManager class.
#
# Copyright (c) 2015 carlosperate https://github.com/carlosperate/
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
# The following methods are basically a call to the AlarmDb class and do not
# need to be tested:
#  get_all_alarms, get_number_of_alarms, get_all_enabled_alarms, get_alarm,
#
from __future__ import unicode_literals, absolute_import
import io
import mock
import time
import types
import unittest
import threading
from LightUpAlarm.AlarmDb import AlarmDb
from LightUpAlarm.AlarmItem import AlarmItem
from LightUpAlarm.AlarmManager import AlarmManager


class AlarmManagerTestCase(unittest.TestCase):
    """ Tests for AlarmManager class. """

    def assert_alarm(self, alarm, alarm_id, hour, minute, days, enabled):
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
        self.assertEqual(alarm.enabled, enabled)

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
        self.assertIsInstance(add_success, types.IntType)
        all_alarms = AlarmManager.get_all_alarms()
        latest = len(all_alarms) - 1
        self.assert_alarm(
            all_alarms[latest], 1, 8, 30,
            (False, True, False, True, False, True, False), True)

    def test_add_alarm_error(self):
        """ Adds an alarm incorrectly and check for errors. """
        alarm_mgr = AlarmManager()
        # We capture stderr to stop unit test from printing all errors
        # No need to check stderr as returning None is proof enough
        with mock.patch('sys.stderr', new=io.StringIO()) as test_srderr:
            # Test hour
            add_success = alarm_mgr.add_alarm(
                26, 0, (False, True, False, True, False, True, False), True)
            self.assertIsNone(add_success)
            add_success = alarm_mgr.add_alarm(
                22.5, 0, (False, True, False, True, False, True, False), True)
            self.assertIsNone(add_success)
            add_success = alarm_mgr.add_alarm(
                '22', 0, (False, True, False, True, False, True, False), True)
            self.assertIsNone(add_success)
            add_success = alarm_mgr.add_alarm(
                -2, 0, (False, True, False, True, False, True, False), True)
            self.assertIsNone(add_success)

            # Test minute
            add_success = alarm_mgr.add_alarm(
                22, 60, (False, True, False, True, False, True, False), True)
            self.assertIsNone(add_success)
            add_success = alarm_mgr.add_alarm(
                22, 35.5, (False, True, False, True, False, True, False), True)
            self.assertIsNone(add_success)
            add_success = alarm_mgr.add_alarm(
                22, '25', (False, True, False, True, False, True, False), True)
            self.assertIsNone(add_success)
            add_success = alarm_mgr.add_alarm(
                22, -20, (False, True, False, True, False, True, False), True)
            self.assertIsNone(add_success)

            # Test days
            add_success = alarm_mgr.add_alarm(
                8, 30, (False, True, False, True, False, True, False, True), True)
            self.assertIsNone(add_success)
            add_success = alarm_mgr.add_alarm(
                8, 30, (False, True, False, True, False, True), True)
            self.assertIsNone(add_success)
            add_success = alarm_mgr.add_alarm(
                22, 0, (False, True, False, 'True', False, True, False), True)
            self.assertIsNone(add_success)

            # Test enabled
            add_success = alarm_mgr.add_alarm(
                8, 30, (False, True, False, True, False, True, False), -1)
            self.assertIsNone(add_success)
            add_success = alarm_mgr.add_alarm(
                8, 30, (False, True, False, True, False, True, False), '3')
            self.assertIsNone(add_success)
            add_success = alarm_mgr.add_alarm(
                8, 30, (False, True, False, True, False, True, False), 2.3)
            self.assertIsNone(add_success)

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

    def test_delete_alarm(self):
        """
        Adds 5 alarms to the database, checks it is able to retrieve one of
        them and proceeds to delete and check it has been deleted.
        """
        alarm_mgr = AlarmManager()
        self.create_alarms(alarm_mgr)
        numb_alarms = AlarmManager.get_number_of_alarms()
        self.assertGreater(numb_alarms, 0)
        all_alarms = AlarmManager.get_all_alarms()
        alarm_retrieved = AlarmManager.get_alarm(all_alarms[0].id_)
        self.assertIsNotNone(alarm_retrieved)
        delete_success = alarm_mgr.delete_alarm(1)
        self.assertTrue(delete_success)
        self.assertLess(AlarmManager.get_number_of_alarms(), numb_alarms)
        alarm_retrieved = AlarmManager.get_alarm(alarm_retrieved.id_)
        self.assertIsNone(alarm_retrieved)

    def test_delete_all_alarms(self):
        """
        Adds 5 alarms to the database, checks there are alarms in the db and
        proceeds to delete them all and check.
        """
        alarm_mgr = AlarmManager()
        self.create_alarms(alarm_mgr)
        numb_alarms = AlarmManager.get_number_of_alarms()
        self.assertGreater(numb_alarms, 0)
        delete_success = alarm_mgr.delete_all_alarms()
        self.assertTrue(delete_success)
        self.assertEqual(AlarmManager.get_number_of_alarms(), 0)

    def test_get_all_active_alarms(self):
        """ Test the get_all_active_alarms method. """
        alarm_mgr = AlarmManager()
        # First test with 5 active alarms
        self.create_alarms(alarm_mgr)
        active_alarms = AlarmManager.get_all_active_alarms()
        self.assertEquals(len(active_alarms), 5)
        # Deactivate a couple of alarms and try again
        edit_success = alarm_mgr.edit_alarm(1, enabled=False)
        self.assertTrue(edit_success)
        edit_success = alarm_mgr.edit_alarm(
            3, days=(False, False, False, False, False, False, False))
        self.assertTrue(edit_success)
        active_alarms = AlarmManager.get_all_active_alarms()
        self.assertEquals(len(active_alarms), 3)
        # Check it returns an empty list if no ative alarms
        alarm_mgr.delete_all_alarms()
        active_alarms = AlarmManager.get_all_active_alarms()
        self.assertEqual(len(active_alarms), 0)

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
        Alarm Thread if there is an active alarm.
        Ensure the thread has been launched successfully.
        This test accesses private methods.
        """
        time_now = time.localtime(time.time())
        alarm = AlarmItem(time_now.tm_hour - 1, 34,
                          (True, True, True, True, True, True, True), False, 96)
        alarm_mgr = AlarmManager()
        alarm_mgr.delete_all_alarms()
        numb_threads = threading.activeCount()

        # Test setting inactive alarm
        launch_success = alarm_mgr._AlarmManager__set_alarm_thread(alarm)
        self.assertFalse(launch_success)
        self.assertEqual(threading.activeCount(), numb_threads)

        # Test enabled alarm with no repeats
        alarm.repeat = (False, False, False, False, False, False, False)
        alarm.enabled = True
        launch_success = alarm_mgr._AlarmManager__set_alarm_thread(alarm)
        self.assertFalse(launch_success)
        self.assertEqual(threading.activeCount(), numb_threads)

        # Test fully active alarm
        alarm.wednesday = True
        launch_success = alarm_mgr._AlarmManager__set_alarm_thread(alarm)
        self.assertTrue(launch_success)
        self.assertGreater(threading.activeCount(), numb_threads)

    def test_set_alarm_thread_edit(self):
        """
        Tests the __set_alarm_thread when an existing alarm thread is inputted.
        No need to check for input with wrong ID as that gets dealt with in the
        AlarmThread class and unit test.
        """
        time_now = time.localtime(time.time())
        first_alarm = AlarmItem(
            time_now.tm_hour - 1, 34,
            (True, True, True, True, True, True, True), True, 96)
        new_alarm = AlarmItem(
            time_now.tm_hour - 1, 34,
            (False, False, False, False, False, False, False), False, 96)
        alarm_mgr = AlarmManager()
        alarm_mgr.delete_all_alarms()
        numb_threads = threading.activeCount()
        launch_success = alarm_mgr._AlarmManager__set_alarm_thread(first_alarm)
        self.assertTrue(launch_success)
        self.assertGreater(threading.activeCount(), numb_threads)

        # Editing to the new alarm data should stop the thread as it is inactive
        launch_success = alarm_mgr._AlarmManager__set_alarm_thread(new_alarm)
        self.assertFalse(launch_success)
        self.assertEqual(threading.activeCount(), numb_threads)

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

    def test_stop_all_alarm_threads(self):
        """
        Launches 2 alarms threads, checks they are running and them stops them
        all and checks again.
        """
        time_now = time.localtime(time.time())
        alarm_one = AlarmItem(
            time_now.tm_hour - 1, 34,
            (False, False, False, False, False, False, True), True, 31)
        alarm_two = AlarmItem(
            time_now.tm_hour - 1, 34,
            (False, False, False, False, False, False, True), True, 32)
        alarm_mgr = AlarmManager()
        # There is a bit of circular dependency here as delete all will execute
        # __stop_all_alarm_threads
        alarm_mgr.delete_all_alarms()
        launch_success = alarm_mgr._AlarmManager__set_alarm_thread(alarm_one)
        self.assertTrue(launch_success)
        launch_success = alarm_mgr._AlarmManager__set_alarm_thread(alarm_two)
        self.assertTrue(launch_success)
        numb_threads = threading.activeCount()
        self.assertGreaterEqual(numb_threads, 2)
        delete_success = alarm_mgr._AlarmManager__stop_all_alarm_threads()
        self.assertTrue(delete_success)
        self.assertEqual(threading.activeCount(), numb_threads - 2)

    def test_get_running_alarms(self):
        """
        Tests get_running_alarms returns a list of the running alarms (active
        alarms with a running thread), or an empty list.
        """
        alarm_mgr = AlarmManager()
        # All these alarms are active
        self.create_alarms(alarm_mgr)
        running_alarms = alarm_mgr.get_running_alarms()
        self.assertGreater(len(running_alarms), 0)
        alarm_mgr.edit_alarm(1, enabled=False)
        alarm_mgr.edit_alarm(3, enabled=False)
        self.assertEqual(
            len(running_alarms) - 2, len(alarm_mgr.get_running_alarms()))
        alarm_mgr.delete_all_alarms()
        running_alarms = alarm_mgr.get_running_alarms()
        self.assertEqual(len(running_alarms), 0)

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
        This test can take over 10 seconds in its worse case scenario.
        """
        # Set alarm for current minute, but only if there is at least 10 seconds
        # left for this minute. Better than setting it for the next minute.
        time_now = time.localtime(time.time())
        while time_now.tm_sec > 50:
            time.sleep(1)
            time_now = time.localtime(time.time())
        alarm = AlarmItem(
            time_now.tm_hour, time_now.tm_min,
            (True, True, True, True, True, True, True), True, 96)
        alarm_mgr = AlarmManager(alarm_callback=AlarmManagerTestCase.c)
        alarm_mgr.delete_all_alarms()
        launch_success = alarm_mgr._AlarmManager__set_alarm_thread(alarm)
        self.assertTrue(launch_success)
        while AlarmManagerTestCase.thread_alert is False:
            # This loop will never finish if the thread does not callback
            time.sleep(0.001)
        self.assertTrue(AlarmManagerTestCase.thread_alert)

    def test_is_alarm_running(self):
        """ Adds a couple of alarms and tests the is_alarm_running() method. """
        time_now = time.localtime(time.time())
        alarm_active = AlarmItem(
            time_now.tm_hour -1 , time_now.tm_min,
            (True, True, True, True, True, True, True), True, 96)
        alarm_inactive = AlarmItem(
            time_now.tm_hour -1 , time_now.tm_min,
            (False, False, False, False, False, False, False), False, 86)
        alarm_mgr = AlarmManager()
        alarm_mgr.delete_all_alarms()
        launch_success = alarm_mgr._AlarmManager__set_alarm_thread(alarm_active)
        self.assertTrue(launch_success)
        launch_success = alarm_mgr._AlarmManager__set_alarm_thread(
            alarm_inactive)
        self.assertFalse(launch_success)
        # Now everything is set up, test the is_alarm_running method
        self.assertTrue(alarm_mgr.is_alarm_running(alarm_active.id_))
        self.assertFalse(alarm_mgr.is_alarm_running(alarm_inactive.id_))

    def test_check_threads_state(self):
        """ Test almost all pathways of check_threads_state. """
        alarm_mgr = AlarmManager()
        self.create_alarms(alarm_mgr)
        check_result = alarm_mgr.check_threads_state()
        self.assertTrue(check_result)

        # Now that everything is working correctly, sneak around AlarmManager
        # and edit a running thread by editing an AlarmItem using the
        # AlarmThread internal reference to the AlarmItem instance (which does
        # not do the extra checks for tracking like AlarmManager does).
        # Also edit the database entry for that alarm bypassing AlarmManager.
        alarm_bypass = \
            alarm_mgr._AlarmManager__alarm_threads[0]._AlarmThread__alarm
        alarm_bypass.enabled = False
        alarm_id = alarm_bypass.id_
        AlarmDb().edit_alarm(alarm_id, enabled=False)
        check_result = alarm_mgr.check_threads_state()
        self.assertFalse(check_result)
        # Executing check_threads_state should have return false as there was
        # an issue, but if fixed correctly the second time should return true
        check_result = alarm_mgr.check_threads_state()
        self.assertTrue(check_result)

        # Now the thread for alarm 'alarm_bypass' with ID 'alarm_id' has been
        # stopped, we can bypass AlarmManager again to activate it and check
        # if check_threads_state recovers again.
        alarm_bypass.enabled = True
        AlarmDb().edit_alarm(alarm_bypass.id_, enabled=True)
        check_result = alarm_mgr.check_threads_state()
        self.assertFalse(check_result)
        check_result = alarm_mgr.check_threads_state()
        self.assertTrue(check_result)

        # Now that everything is working correctly once more, add extra thread
        time_now = time.localtime(time.time())
        alarm_test = AlarmItem(
            time_now.tm_hour -1, time_now.tm_min,
            (True, True, True, True, True, True, True), True, 96)
        launch_success = alarm_mgr._AlarmManager__set_alarm_thread(alarm_test)
        self.assertTrue(launch_success)
        check_result = alarm_mgr.check_threads_state()
        self.assertFalse(check_result)
        check_result = alarm_mgr.check_threads_state()
        self.assertTrue(check_result)

        # Now we stop a running thread bypassing AlarmManager public methods
        alarm_mgr._AlarmManager__alarm_threads[0].stop()
        while alarm_mgr._AlarmManager__alarm_threads[0].isAlive():
            time.sleep(0.1)
        check_result = alarm_mgr.check_threads_state()
        self.assertFalse(check_result)
        check_result = alarm_mgr.check_threads_state()
        self.assertTrue(check_result)

        # To test the last path, which is less threads running than expected,
        # we would need to kill a thread before running check_threads_state
        # and then somehow stop the recovery of such thread. So for now, it is
        # not tested.


if __name__ == '__main__':
    unittest.main()
