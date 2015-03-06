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

    def test_constructor(self):
        """ Tests valid inputs to the constructor. """
        hour = 23
        minute = 59
        days = (False, True, True, False, False, False, False)

        # Check constructor with minimum arguments
        alarm_test = AlarmItem(hour, minute)
        self.assertEqual(hour, alarm_test.hour)
        self.assertEqual(minute, alarm_test.minute)
        for day in alarm_test._repeat:
            self.assertEqual(alarm_test._repeat[day], False)

        # Check constructor with minimum arguments + repeat days
        alarm_test = AlarmItem(hour, minute, days)
        self.assertEqual(days, alarm_test.repeat)

        # Check constructor with minimum arguments + repeat days + active
        alarm_test = AlarmItem(hour, minute, days, False)
        self.assertEqual(False, alarm_test.active)

    def test_constructor_loop_around(self):
        """
        Test constructor values for hours and minutes larger than 23 and 59
        respectively.
        """
        alarm_test = AlarmItem(24, 60)
        self.assertTrue(alarm_test.minute < 60)
        self.assertTrue(alarm_test.hour < 24)

    def test_hour_min_loop_around(self):
        """
        Test setting the hours and minutes values to larger than 23 and 59
        respectively to obtain a valid value.
        """
        alarm_test = AlarmItem(0, 0)
        alarm_test.minute = 60
        alarm_test.hour = 24
        self.assertTrue(alarm_test.minute < 60)
        self.assertTrue(alarm_test.minute == 0)
        self.assertTrue(alarm_test.hour < 24)
        self.assertTrue(alarm_test.hour == 0)

        alarm_test.minute = 120  # 0 + 60min + 60min
        alarm_test.hour = 48     # 0 + 24h + 24h
        self.assertTrue(alarm_test.minute == 0)
        self.assertTrue(alarm_test.hour == 0)

        alarm_test.minute = 212  # 32 + 60min + 60min + 60min
        alarm_test.hour = 87     # 15 + 24h + 24h + 24h
        self.assertTrue(alarm_test.minute == 32)
        self.assertTrue(alarm_test.hour < 24)

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

    def test_id(self):
        """ Test that the id member variable accessors work as expected. """
        alarm_test = AlarmItem(0, 0)
        alarm_test.id = 5
        self.assertEqual(5, alarm_test.id)

        # The accessor setter prints to stderr if bad data is encountered, so
        # we need to capture stderr to test it.
        with mock.patch('sys.stderr', new=io.StringIO()) as test_srderr:
            # First ensure that successful set does not write to stderr
            self.assertEqual(test_srderr.getvalue(), '')
            alarm_test.id = 10
            self.assertEqual(test_srderr.getvalue(), '')

            # String instead of integer
            alarm_test.id = 'String'
            self.assertNotEqual(test_srderr.getvalue(), '')

            # Float instead of integer
            test_srderr.truncate(0)
            test_srderr.write('')
            self.assertEqual(test_srderr.getvalue(), '')
            alarm_test.id = 10.4
            self.assertNotEqual(test_srderr.getvalue(), '')


if __name__ == '__main__':
    unittest.main()
