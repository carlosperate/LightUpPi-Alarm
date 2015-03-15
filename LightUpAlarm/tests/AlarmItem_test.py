#!/usr/bin/env python2
#
# Unit test for the AlarmItem class.
#
# Copyright (c) 2015 carlosperate https://github.com/carlosperate/
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
from __future__ import unicode_literals, absolute_import
import unittest
import mock
import io
from LightUpAlarm.AlarmItem import AlarmItem


class AlarmItemTestCase(unittest.TestCase):
    """ Tests for AlarmItem class. """

    def assert_repeat(self, alarm_test, days):
        self.assertEqual(alarm_test.monday, days[0])
        self.assertEqual(alarm_test.tuesday, days[1])
        self.assertEqual(alarm_test.wednesday, days[2])
        self.assertEqual(alarm_test.thursday, days[3])
        self.assertEqual(alarm_test.friday, days[4])
        self.assertEqual(alarm_test.saturday, days[5])
        self.assertEqual(alarm_test.sunday, days[6])

    def test_constructor(self):
        """ Tests valid inputs to the constructor. """
        hour = 23
        minute = 59
        days = (False, True, True, False, False, False, False)

        # Check constructor with minimum arguments
        alarm_test = AlarmItem(hour, minute)
        self.assertEqual(hour, alarm_test.hour)
        self.assertEqual(minute, alarm_test.minute)
        for day in alarm_test.repeat:
            self.assertEqual(alarm_test.repeat[day], False)

        # Check constructor with minimum arguments + repeat days
        alarm_test = AlarmItem(hour, minute, days)
        self.assertEqual(days, alarm_test.repeat)

        # Check constructor with minimum arguments + repeat days + enabled
        alarm_test = AlarmItem(hour, minute, days, False)
        self.assertEqual(False, alarm_test.enabled)

    def test_constructor_hour_min_range(self):
        """
        Test constructor values for hours and minutes to produce a None object
        if they are larger than 23 and 59 respectively.
        """
        # The accessor functions print to stderr if bad data is encountered, so
        # we need to capture stderr to test it.
        with mock.patch('sys.stderr', new=io.StringIO()) as test_srderr:
            # Invalid minute
            self.assertEqual(test_srderr.getvalue(), '')
            alarm_test = AlarmItem(23, 60)
            self.assertIsNone(alarm_test)
            self.assertNotEqual(test_srderr.getvalue(), '')

            # Invalid hour
            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test = AlarmItem(24, 59)
            self.assertIsNone(alarm_test)
            self.assertNotEqual(test_srderr.getvalue(), '')

            # Invalid hour and minute
            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test = AlarmItem(24, 60)
            self.assertIsNone(alarm_test)
            self.assertNotEqual(test_srderr.getvalue(), '')

    def test_hour_min_loop_around(self):
        """
        Test setting the hours and minutes accessors to not change values with
        invalid inputs.
        """
        alarm_test = AlarmItem(0, 1)
        # The accessor functions print to stderr if bad data is encountered, so
        # we need to capture stderr to test it.
        with mock.patch('sys.stderr', new=io.StringIO()) as test_srderr:
            self.assertEqual(test_srderr.getvalue(), '')
            alarm_test.hour = 12
            alarm_test.minute = 34
            self.assertEquals(alarm_test.hour, 12)
            self.assertEquals(alarm_test.minute, 34)
            self.assertEqual(test_srderr.getvalue(), '')

            # Invalid ints
            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test.minute = 60
            self.assertNotEqual(test_srderr.getvalue(), '')
            self.assertEquals(alarm_test.minute, 34)

            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test.hour = 24
            self.assertNotEqual(test_srderr.getvalue(), '')
            self.assertEquals(alarm_test.hour, 12)

    def test_hour_min_integers(self):
        """
        Test setting the hours and minutes values valid integers and non-integer
        values.
        """
        alarm_test = AlarmItem(0, 0)

        # The accessor functions print to stderr if bad data is encountered, so
        # we need to capture stderr to test it.
        with mock.patch('sys.stderr', new=io.StringIO()) as test_srderr:
            # First ensure that successful set does not write to stderr
            self.assertEqual(test_srderr.getvalue(), '')
            alarm_test.hour = 12
            alarm_test.minute = 34
            self.assertEqual(test_srderr.getvalue(), '')

            # Float instead of integer
            test_srderr.truncate(0)
            test_srderr.write('')
            self.assertEqual(test_srderr.getvalue(), '')
            alarm_test.hour = 12.34
            self.assertNotEqual(test_srderr.getvalue(), '')
            test_srderr.truncate(0)
            test_srderr.write('')
            self.assertEqual(test_srderr.getvalue(), '')
            alarm_test.minute = 34.56
            self.assertNotEqual(test_srderr.getvalue(), '')

            # String instead of integer
            test_srderr.truncate(0)
            test_srderr.write('')
            self.assertEqual(test_srderr.getvalue(), '')
            alarm_test.hour = 'minutes'
            self.assertNotEqual(test_srderr.getvalue(), '')
            test_srderr.truncate(0)
            test_srderr.write('')
            self.assertEqual(test_srderr.getvalue(), '')
            alarm_test.minute = 'hours'
            self.assertNotEqual(test_srderr.getvalue(), '')

    def test_repeat_list_strictness(self):
        """
        Test that the repeat list of booleans is filtered and catches invalid
        inputs. Including lists of not booleans, and boolean lists with and
        incorrect number of items.
        """
        alarm_test = AlarmItem(0, 0)
        valid_days = (False, True, True, False, False, False, False)

        # Setting a valid value
        self.assertNotEqual(valid_days, alarm_test.repeat)
        alarm_test.repeat = valid_days
        self.assertEqual(valid_days, alarm_test.repeat)

        # The accessor functions print to stderr if bad data is encountered, so
        # we need to capture stderr to test it.
        with mock.patch('sys.stderr', new=io.StringIO()) as test_srderr:
            # First ensure that successful set does not write to stderr
            self.assertEqual(test_srderr.getvalue(), '')
            alarm_test.repeat = valid_days
            self.assertEqual(test_srderr.getvalue(), '')

            # Too many arguments
            alarm_test.repeat = (
                False, True, True, False, False, False, False, False)
            self.assertNotEqual(test_srderr.getvalue(), '')

            # Too few arguments
            test_srderr.truncate(0)
            test_srderr.write('')
            self.assertEqual(test_srderr.getvalue(), '')
            alarm_test.repeat = (False, True, True, False, False, False)
            self.assertNotEqual(test_srderr.getvalue(), '')

            # Wrong arguments
            test_srderr.truncate(0)
            test_srderr.write('')
            self.assertEqual(test_srderr.getvalue(), '')
            alarm_test.repeat = (False, True, True, 0, False, False, True)
            self.assertNotEqual(test_srderr.getvalue(), '')

    def test_repeat_accessors_get(self):
        """
        Sets the repeat list at the constructor and variable level, and test
        that all the individual accessors for each day of the week works
        correctly.
        """
        days = [False, True, True, False, True, False, True]

        # Test constructor input
        alarm_test = AlarmItem(0, 0, days, False)
        self.assertEqual(alarm_test.repeat, tuple(days))
        self.assert_repeat(alarm_test, days)

        # Test repeat accesor with opposite repeat list
        for i in xrange(len(days)):
            days[i] = not days[i]
        alarm_test.repeat = days
        self.assertEqual(alarm_test.repeat, tuple(days))
        self.assert_repeat(alarm_test, days)

    def test_repeat_accessors_set(self):
        """
        Sets the repeat list and test that the individual set accessors work as
        expected, including throwing errors if values are not booleans.
        """
        alarm_test = AlarmItem(0, 0)
        days = [False, True, True, False, True, False, True]

        # Test with correct values
        alarm_test.monday = days[0]
        alarm_test.tuesday = days[1]
        alarm_test.wednesday = days[2]
        alarm_test.thursday = days[3]
        alarm_test.friday = days[4]
        alarm_test.saturday = days[5]
        alarm_test.sunday = days[6]
        self.assert_repeat(alarm_test, days)

        # To test the incorrect value, the accessor setter prints to stderr
        # if bad data is encountered, so we need to capture stderr to test it.
        with mock.patch('sys.stderr', new=io.StringIO()) as test_srderr:
            # First ensure that successful set does not write to stderr
            self.assertEqual(test_srderr.getvalue(), '')
            alarm_test.monday = days[0]
            self.assertEqual(test_srderr.getvalue(), '')

            # Monday
            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test.monday = 'monday'
            self.assertNotEqual(test_srderr.getvalue(), '')
            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test.monday = 1
            self.assertNotEqual(test_srderr.getvalue(), '')
            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test.monday = 2.3
            self.assertNotEqual(test_srderr.getvalue(), '')

            # Tuesday
            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test.tuesday = 'tuesday'
            self.assertNotEqual(test_srderr.getvalue(), '')
            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test.tuesday = 1
            self.assertNotEqual(test_srderr.getvalue(), '')
            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test.tuesday = 2.3
            self.assertNotEqual(test_srderr.getvalue(), '')

            # Wednesday
            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test.wednesday = 'wednesday'
            self.assertNotEqual(test_srderr.getvalue(), '')
            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test.wednesday = 1
            self.assertNotEqual(test_srderr.getvalue(), '')
            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test.wednesday = 2.3
            self.assertNotEqual(test_srderr.getvalue(), '')

            # Thursday
            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test.thursday = 'thursday'
            self.assertNotEqual(test_srderr.getvalue(), '')
            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test.thursday = 1
            self.assertNotEqual(test_srderr.getvalue(), '')
            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test.thursday = 2.3
            self.assertNotEqual(test_srderr.getvalue(), '')

            # Friday
            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test.friday = 'friday'
            self.assertNotEqual(test_srderr.getvalue(), '')
            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test.friday = 1
            self.assertNotEqual(test_srderr.getvalue(), '')
            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test.friday = 2.3
            self.assertNotEqual(test_srderr.getvalue(), '')

            # Saturday
            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test.saturday = 'saturday'
            self.assertNotEqual(test_srderr.getvalue(), '')
            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test.saturday = 1
            self.assertNotEqual(test_srderr.getvalue(), '')
            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test.saturday = 2.3
            self.assertNotEqual(test_srderr.getvalue(), '')

            # Sunday
            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test.sunday = 'sunday'
            self.assertNotEqual(test_srderr.getvalue(), '')
            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test.sunday = 1
            self.assertNotEqual(test_srderr.getvalue(), '')
            test_srderr.truncate(0)
            test_srderr.write('')
            alarm_test.sunday = 2.3

    def test_id(self):
        """ Tests the id member variable accessors filters non-integers. """
        alarm_test = AlarmItem(0, 0)
        alarm_test.id_ = 5
        self.assertEqual(5, alarm_test.id_)

        # The accessor setter prints to stderr if bad data is encountered, so
        # we need to capture stderr to test it.
        with mock.patch('sys.stderr', new=io.StringIO()) as test_srderr:
            # First ensure that successful set does not write to stderr
            self.assertEqual(test_srderr.getvalue(), '')
            alarm_test.id_ = 10
            self.assertEqual(test_srderr.getvalue(), '')
            # String instead of integer
            alarm_test.id_ = 'String'
            self.assertNotEqual(test_srderr.getvalue(), '')
            # Float instead of integer
            test_srderr.truncate(0)
            test_srderr.write('')
            self.assertEqual(test_srderr.getvalue(), '')
            alarm_test.id_ = 10.4
            self.assertNotEqual(test_srderr.getvalue(), '')

    def test_time_to_alarm(self):
        """
        Full tests coverage for the get_time_diff function. Good resource:
        http://www.timeanddate.com/date/timeduration.html
        """
        one_day = 1440
        test_alarm = AlarmItem(
            9, 30, (True, False, False, True, False, False, False), True)
        time_diff = test_alarm.minutes_to_alert(9, 30, 0)
        self.assertEqual(time_diff, 0)
        time_diff = test_alarm.minutes_to_alert(9, 29, 0)
        self.assertEqual(time_diff, 1)
        time_diff = test_alarm.minutes_to_alert(19, 55, 2)
        self.assertEqual(time_diff, 815)
        time_diff = test_alarm.minutes_to_alert(9, 30, 2)
        self.assertEqual(time_diff, one_day)
        time_diff = test_alarm.minutes_to_alert(9, 30, 1)
        self.assertEqual(time_diff, (one_day * 2))
        time_diff = test_alarm.minutes_to_alert(9, 31, 1)
        self.assertEqual(time_diff, ((one_day * 2) - 1))
        time_diff = test_alarm.minutes_to_alert(9, 29, 4)
        self.assertEqual(time_diff, ((one_day * 3) + 1))
        time_diff = test_alarm.minutes_to_alert(3, 15, 1)
        self.assertEqual(time_diff, ((one_day * 2) + (60 * 6) + 15))

        test_alarm.repeat = (True, False, False, False, False, False, False)
        time_diff = test_alarm.minutes_to_alert(9, 31, 0)
        self.assertEqual(time_diff, ((one_day * 7) - 1))
        time_diff = test_alarm.minutes_to_alert(13, 34, 1)
        self.assertEqual(time_diff, ((one_day * 5) + (60 * 19) + 56))
        time_diff = test_alarm.minutes_to_alert(4, 15, 2)
        self.assertEqual(time_diff, ((one_day * 5) + (60 * 5) + 15))

    def test_string_alarm(self):
        """ Checks the __str__ output is correct. """
        test_alarm = AlarmItem(
            9, 30, (True, False, False, True, False, False, True), True)
        test_alarm.id_ = 10
        out = 'Alarm ID:  10 | Time: 09:30 | Enabled: Yes | Repeat: ' +\
              'Mon --- --- Thu --- --- Sun '
        self.assertEqual(str(test_alarm), out)

    def test_any_enabled_day(self):
        """ Test any_day_enabled() returns False if all repeats are false. """
        test_alarm = AlarmItem(
            9, 30, (True, False, False, True, False, False, True), True)
        self.assertTrue(test_alarm.any_day_enabled())
        test_alarm.repeat = (False, False, False, False, False, False, False)
        self.assertFalse(test_alarm.any_day_enabled())


if __name__ == '__main__':
    unittest.main()
