#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Unit test for the AlarmThread class.
#
# Copyright (c) 2015 carlosperate https://github.com/carlosperate/
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
# This only tests the class methods in the current main thread. The Threading
# aspect is tested in the AlarmManager Unit test when the methods responsible
# to launch, stop and track the threads are tested.
#
from __future__ import unicode_literals, absolute_import
import io
import time
import mock
import unittest
from datetime import datetime, timedelta
try:
    from LightUpAlarm.AlarmItem import AlarmItem
    from LightUpAlarm.AlarmThread import AlarmThread
except ImportError:
    import os
    import sys
    file_dir = os.path.dirname(os.path.realpath(__file__))
    package_dir = os.path.dirname(os.path.dirname(file_dir))
    sys.path.insert(0, package_dir)
    from LightUpAlarm.AlarmItem import AlarmItem
    from LightUpAlarm.AlarmThread import AlarmThread


class AlarmThreadTestCase(unittest.TestCase):
    """ Tests for AlarmThread class. """
    @staticmethod
    def empty_callback():
        pass

    def test_constructor(self):
        """ Tests the class constructor. """
        alarm_test = AlarmItem(9, 34, enabled=False, alarm_id=96,
                               days=(True, True, True, True, True, True, True))
        # With minimum parameters
        alarm_thread = AlarmThread(alarm_test)
        self.assertIs(alarm_thread._AlarmThread__alarm, alarm_test)
        self.assertFalse(alarm_thread._AlarmThread__offset_flag)

        # With minimum parameters + callback
        alarm_thread = AlarmThread(
            alarm_test, alarm_callback=AlarmThreadTestCase.empty_callback)
        self.assertIs(alarm_thread._AlarmThread__alarm, alarm_test)
        self.assertIs(
            alarm_thread._AlarmThread__alarm_callback,
            AlarmThreadTestCase.empty_callback)
        self.assertFalse(alarm_thread._AlarmThread__offset_flag)

        # With minimum parameters + callback + offset
        alarm_thread = AlarmThread(
            alarm_test, alarm_callback=AlarmThreadTestCase.empty_callback,
            offset_alarm_time=15)
        self.assertIs(alarm_thread._AlarmThread__alarm, alarm_test)
        self.assertIs(
            alarm_thread._AlarmThread__alarm_callback,
            AlarmThreadTestCase.empty_callback)
        self.assertEqual(alarm_thread._AlarmThread__offset_time, 15)
        self.assertTrue(alarm_thread._AlarmThread__offset_flag)
        self.assertIsNotNone(alarm_thread._AlarmThread__offset_alarm)

        # With minimum parameters + callback + offset + offset callback
        alarm_thread = AlarmThread(
            alarm_test, alarm_callback=AlarmThreadTestCase.empty_callback,
            offset_callback=AlarmThreadTestCase.empty_callback,
            offset_alarm_time=15)
        self.assertIs(alarm_thread._AlarmThread__alarm, alarm_test)
        self.assertIs(
            alarm_thread._AlarmThread__alarm_callback,
            AlarmThreadTestCase.empty_callback)
        self.assertEqual(alarm_thread._AlarmThread__offset_time, 15)
        self.assertTrue(alarm_thread._AlarmThread__offset_flag)
        self.assertIsNotNone(alarm_thread._AlarmThread__offset_alarm)
        self.assertIs(
            alarm_thread._AlarmThread__offset_callback,
            AlarmThreadTestCase.empty_callback)

        # Incorrect offset_alarm_time
        alarm_thread = AlarmThread(alarm_test, offset_alarm_time="5")
        self.assertIs(alarm_thread._AlarmThread__alarm, alarm_test)
        self.assertFalse(alarm_thread._AlarmThread__offset_flag)
        self.assertIsNone(alarm_thread._AlarmThread__offset_alarm)

    def test_get_id(self):
        """ Tests the get_id() method. """
        alarm_test = AlarmItem(9, 34, enabled=False, alarm_id=36,
                               days=(True, True, True, True, True, True, True))
        alarm_thread = AlarmThread(
            alarm_test, alarm_callback=AlarmThreadTestCase.empty_callback)
        self.assertEqual(alarm_thread.get_id(), alarm_test.id_)

    def test_edit_alarm(self):
        """ Tests the edit_alarm() method. """
        # Carefully select the minutes to be different and > |offset_time|
        offset_minutes = -15
        old_minute = 35
        new_minute = 20

        alarm_test = AlarmItem(9, old_minute, enabled=False, alarm_id=36,
                               days=(True, True, True, True, True, True, True))
        new_alarm = AlarmItem(9, new_minute, enabled=False, alarm_id=96,
                              days=(True, True, True, True, True, True, True))

        alarm_thread = AlarmThread(
            alarm_test, alarm_callback=AlarmThreadTestCase.empty_callback,
            offset_alarm_time=offset_minutes)
        self.assertIs(alarm_thread._AlarmThread__alarm, alarm_test)

        # The edit_alarm method prints to stderr if wrong alarm if input, so
        # we need to capture stderr to test it.
        with mock.patch('sys.stderr', new=io.StringIO()) as test_srderr:
            # Test with wrong ID
            self.assertEqual(test_srderr.getvalue(), '')
            alarm_thread.edit_alarm(new_alarm)
            self.assertNotEqual(test_srderr.getvalue(), '')
            self.assertIsNot(alarm_thread._AlarmThread__alarm, new_alarm)
             # Check the offset alert has not been updated
            self.assertEqual(alarm_thread._AlarmThread__offset_alarm.minute,
                             old_minute + offset_minutes)

            # Test with correct ID
            new_alarm.id_ = 36
            test_srderr.truncate(0)
            test_srderr.write('')
            self.assertEqual(test_srderr.getvalue(), '')
            alarm_thread.edit_alarm(new_alarm)
            self.assertEqual(test_srderr.getvalue(), '')
            self.assertIs(alarm_thread._AlarmThread__alarm, new_alarm)
            # Check the offset alert has also been updated
            self.assertEqual(alarm_thread._AlarmThread__offset_alarm.minute,
                             new_minute + offset_minutes)

    def test_run(self):
        """
        Creates and alarm to trigger within a minute to instate AlarmThread,
        with an offset alert trigger of -1 minute.
        This test uses the member method AlarmManagerTestCase.c as the callback
        method. As the expected number of arguments is not 0, a TypeError is
        raised when executed, proving that the run method triggers on the alarm
        time and executes the callback.
        This test can take a little over 10 seconds in its worse case scenario.
        """
        def good_callback():
            pass

        def bad_callback(one, two, three):
            """
            Does nothing, but because it's it expects several argument it will
            throw an exception if they are not provided.
            """
            pass

        # Set alarm for current minute, but only if there is at least 10seconds
        # left for this minute. Better than setting it for the next minute.
        time_now = time.localtime(time.time())
        while time_now.tm_sec > 50:
            time.sleep(1)
            time_now = time.localtime(time.time())

        alarm_thread = AlarmThread(
            AlarmItem(
                time_now.tm_hour, time_now.tm_min, enabled=True, alarm_id=96,
                days=(True, True, True, True, True, True, True)),
            alarm_callback=bad_callback,
            offset_alarm_time=-1,
            offset_callback=good_callback)
        self.assertRaises(TypeError, alarm_thread.run)
        alarm_thread.stop()

        # This time test the pre/post alert
        time_now = time.localtime(time.time())
        while time_now.tm_sec > 50:
            time.sleep(1)
            time_now = time.localtime(time.time())

        alarm_time = datetime.now() + timedelta(minutes=1)
        alarm_thread = AlarmThread(
            AlarmItem(
                alarm_time.hour, alarm_time.minute, enabled=True, alarm_id=97,
                days=(True, True, True, True, True, True, True)),
            alarm_callback=good_callback,
            offset_alarm_time=-1,
            offset_callback=bad_callback)
        self.assertRaises(TypeError, alarm_thread.run)


if __name__ == '__main__':
    unittest.main()
