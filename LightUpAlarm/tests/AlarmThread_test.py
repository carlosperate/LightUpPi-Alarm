#!/usr/bin/env python2
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

        alarm_test = AlarmItem(
            9, 34, (True, True, True, True, True, True, True), False, 96)
        alarm_thread = AlarmThread(alarm_test, AlarmThreadTestCase.empty_callback)
        self.assertIs(alarm_thread._AlarmThread__alarm, alarm_test)
        self.assertIs(
            alarm_thread._AlarmThread__alarm_callback,
            AlarmThreadTestCase.empty_callback)

    def test_get_id(self):
        """ Tests the get_id() method. """
        alarm_test = AlarmItem(
            9, 34, (True, True, True, True, True, True, True), False, 36)
        alarm_thread = AlarmThread(
            alarm_test, AlarmThreadTestCase.empty_callback)
        self.assertEqual(alarm_thread.get_id(), alarm_test.id_)

    def test_edit_alarm(self):
        """ Tests the edit_alarm() method. """
        alarm_test = AlarmItem(
            9, 34, (True, True, True, True, True, True, True), False, 36)
        new_alarm = AlarmItem(
            9, 34, (True, True, True, True, True, True, True), False, 96)
        alarm_thread = AlarmThread(
            alarm_test, AlarmThreadTestCase.empty_callback)
        self.assertIs(alarm_thread._AlarmThread__alarm, alarm_test)
        # The edit_alarm method prints to stderr if wrong alarm if input, so
        # we need to capture stderr to test it.
        with mock.patch('sys.stderr', new=io.StringIO()) as test_srderr:
            # Test with wrong ID
            self.assertEqual(test_srderr.getvalue(), '')
            alarm_thread.edit_alarm(new_alarm)
            self.assertNotEqual(test_srderr.getvalue(), '')
            self.assertIsNot(alarm_thread._AlarmThread__alarm, new_alarm)
            # Test with correct ID
            new_alarm.id_ = 36
            test_srderr.truncate(0)
            test_srderr.write('')
            self.assertEqual(test_srderr.getvalue(), '')
            alarm_thread.edit_alarm(new_alarm)
            self.assertEqual(test_srderr.getvalue(), '')
            self.assertIs(alarm_thread._AlarmThread__alarm, new_alarm)

    def test_run(self):
        """
        Creates and alarm to trigger within a minute to instate AlarmThread.
        This test uses the member method AlarmManagerTestCase.c as the callback
        method. As the expected number of arguments is not 0, a TypeError is
        raised when executed, proving that the run method triggers on the alarm
        time and executes the callback.
        This test can take a little over 10 seconds in its worse case scenario.
        """
        def callback(one, two, three):
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
                time_now.tm_hour, time_now.tm_min,
                (True, True, True, True, True, True, True), True, 96),
            callback)
        self.assertRaises(TypeError, alarm_thread.run)


if __name__ == '__main__':
    unittest.main()
