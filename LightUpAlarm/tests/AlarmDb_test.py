#!/usr/bin/env python2
#
# Unit test for the AlarmDb class.
#
# Copyright (c) 2015 carlosperate https://github.com/carlosperate/
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
from __future__ import unicode_literals, absolute_import
import unittest
import mock
import time
import json
import os
try:
    from LightUpAlarm.AlarmDb import AlarmDb
    from LightUpAlarm.AlarmItem import AlarmItem
except ImportError:
    import sys
    file_dir = os.path.dirname(os.path.realpath(__file__))
    package_dir = os.path.dirname(os.path.dirname(file_dir))
    sys.path.insert(0, package_dir)
    from LightUpAlarm.AlarmDb import AlarmDb
    from LightUpAlarm.AlarmItem import AlarmItem


class AlarmDbTestCase(unittest.TestCase):
    """ Tests for AlarmDb class. """

    # Database name to be used for the unit test
    db_name = 'AlarmDb_test_db'

    # just random repeat days to use for tests
    random_days = (False, False, True, False, False, True, False)

    #
    # Helper methods
    #
    def only_five_entries(self, alarm_db):
        """
        Removes all rows and adds 5 entries into the input alarm database.
        :param alarm_db: AlarmDb instance to add entries
        No return as the mutable argument changes remain after exit
        """
        alarm_db.delete_all_alarms()
        alarm_db.add_alarm(AlarmItem(
            13, 35, days=self.random_days, enabled=False, label=''))  # id 1
        alarm_db.add_alarm(AlarmItem(
            14, 36, days=self.random_days, enabled=False, label=''))  # id 2
        alarm_db.add_alarm(AlarmItem(
            15, 37, days=self.random_days, enabled=False, label=''))  # id 3
        alarm_db.add_alarm(AlarmItem(
            16, 38, days=self.random_days, enabled=False, label=''))  # id 4
        alarm_db.add_alarm(AlarmItem(
            17, 39, days=self.random_days, enabled=False, label=''))  # id 5

    #
    # Test methods
    #
    def test_create_instance(self):
        """
        Simply creates an instance with an input file and checks the database
        file has been created.
        """
        db_file = '%s.db' % self.db_name
        # Ensure the file is not there
        if os.path.isfile(db_file):
            os.remove(db_file)
        self.assertFalse(os.path.isfile(db_file))
        adh = AlarmDb(self.db_name)
        adh._AlarmDb__connect_alarms()
        self.assertTrue(os.path.isfile(db_file))

    @mock.patch('time.time')
    def test_entry(self, mock_time):
        """ Adds an entry to the database and deletes it. """
        hour = 13
        minute = 35
        mock_timestamp = 12341234
        mock_time.return_value = mock_timestamp
        adh = AlarmDb(self.db_name)

        # Test an entry with the minimum amount of arguments and check for
        # default values
        test_alarm = AlarmItem(hour, minute)
        test_alarm.id_ = adh.add_alarm(test_alarm)
        # Test that the alarm object inserted has its member variable edited
        # with the new timestamp
        self.assertEqual(mock_timestamp, test_alarm.timestamp)
        # Check variables with a new alarm with data retrieved directly from db
        retrieved_alarm = adh.get_alarm(test_alarm.id_)
        self.assertEqual(hour, retrieved_alarm.hour)
        self.assertEqual(minute, retrieved_alarm.minute)
        self.assertEqual(test_alarm.monday, retrieved_alarm.monday)
        self.assertEqual(test_alarm.tuesday, retrieved_alarm.tuesday)
        self.assertEqual(test_alarm.wednesday, retrieved_alarm.wednesday)
        self.assertEqual(test_alarm.thursday, retrieved_alarm.thursday)
        self.assertEqual(test_alarm.friday, retrieved_alarm.friday)
        self.assertEqual(test_alarm.saturday, retrieved_alarm.saturday)
        self.assertEqual(test_alarm.sunday, retrieved_alarm.sunday)
        self.assertEqual(test_alarm.enabled, retrieved_alarm.enabled)
        self.assertEqual(test_alarm.label, retrieved_alarm.label)
        self.assertEqual(mock_timestamp, retrieved_alarm.timestamp)

        # Test with all possible arguments
        days = (False, False, True, False, False, True, False)
        enabled = False
        label = 'Test alarm label'
        timestamp = 98765432
        test_alarm = AlarmItem(
            hour, minute, days=days, enabled=enabled, label=label,
            timestamp=timestamp)
        test_alarm.id_ = adh.add_alarm(test_alarm)
        # Check that the timestamp value from the alarm instance was not
        # modified with the present (in this case the mocked) timestamp
        self.assertEqual(timestamp, test_alarm.timestamp)
        # Check variables with a new alarm with data retrieved directly from db
        retrieved_alarm = adh.get_alarm(test_alarm.id_)
        self.assertEqual(hour, retrieved_alarm.hour)
        self.assertEqual(minute, retrieved_alarm.minute)
        self.assertEqual(days[0], retrieved_alarm.monday)
        self.assertEqual(days[1], retrieved_alarm.tuesday)
        self.assertEqual(days[2], retrieved_alarm.wednesday)
        self.assertEqual(days[3], retrieved_alarm.thursday)
        self.assertEqual(days[4], retrieved_alarm.friday)
        self.assertEqual(days[5], retrieved_alarm.saturday)
        self.assertEqual(days[6], retrieved_alarm.sunday)
        self.assertEqual(enabled, retrieved_alarm.enabled)
        self.assertEqual(label, retrieved_alarm.label)
        self.assertEqual(timestamp, retrieved_alarm.timestamp)

    def test_entry_error(self):
        """ Tries to add an entry with an incorrect number of arguments. """
        adh = AlarmDb(self.db_name)
        self.assertRaises(TypeError, adh.add_alarm, AlarmItem(0, 0), 0)
        self.assertRaises(TypeError, adh.add_alarm)

    def test_get_wrong_entry(self):
        """ Loads 5 alarms and then tries to access an invalid alarm. """
        adh = AlarmDb(self.db_name)
        self.only_five_entries(adh)
        # ID 7 does not exists
        alarm = adh.get_alarm(7)
        self.assertIsNone(alarm)

    def test_get_all_alarms(self):
        """
        Adds 5 alarms to the db, then checks all are retrieved.
        Also test the get_number_of_alarms method.
        """
        adh = AlarmDb(self.db_name)
        self.only_five_entries(adh)
        number_of_alarms = adh.get_number_of_alarms()
        all_alarms = adh.get_all_alarms()
        self.assertEqual(number_of_alarms, 5)
        self.assertEqual(number_of_alarms, len(all_alarms))
        hour = 13
        minute = 35
        for alarm in all_alarms:
            self.assertEqual(hour, alarm.hour)
            self.assertEqual(minute, alarm.minute)
            hour += 1
            minute += 1

    def test_get_alarm_and_delete(self):
        """
        Adds 5 alarms into the database, then it removes one, and then all the
        rest.
        """
        adh = AlarmDb(self.db_name)
        self.only_five_entries(adh)
        retrieved_alarm = adh.get_alarm(3)  # AlarmItem(15, 37) id=3
        self.assertEqual(retrieved_alarm.hour, 15)
        self.assertEqual(retrieved_alarm.minute, 37)
        delete_success = adh.delete_alarm(3)
        self.assertTrue(delete_success)
        retrieved_alarm = adh.get_alarm(3)  # AlarmItem(15, 37) id=3
        self.assertIsNone(retrieved_alarm)
        delete_success = adh.delete_all_alarms()
        self.assertTrue(delete_success)

    def test_empty_table_zero_alarms(self):
        """ Check that an empty table returns a 0 length list of items """
        adh = AlarmDb(self.db_name)
        adh.delete_all_alarms()
        number_of_alarms = adh.get_number_of_alarms()
        all_alarms = adh.get_all_alarms()
        self.assertEqual(number_of_alarms, 0)
        self.assertEqual(len(all_alarms), 0)

    def test_get_all_enable_alarms(self):
        """
        Adds 5 alarms into the database, 3 enabled and 2 disabled. Checks the
        enabled and disabled getters are working.
        """
        adh = AlarmDb(self.db_name)
        adh.delete_all_alarms()
        adh.add_alarm(
            AlarmItem(13, 35, days=self.random_days, enabled=True))   # id 1
        adh.add_alarm(
            AlarmItem(14, 36, days=self.random_days, enabled=False))  # id 2
        adh.add_alarm(
            AlarmItem(15, 37, days=self.random_days, enabled=True))   # id 3
        adh.add_alarm(
            AlarmItem(16, 38, days=self.random_days, enabled=False))  # id 4
        adh.add_alarm(
            AlarmItem(17, 39, days=self.random_days, enabled=True))   # id 5
        enabled_alarms = adh.get_all_enabled_alarms()
        disabled_alarms = adh.get_all_disabled_alarms()
        self.assertEqual(len(enabled_alarms), 3)
        self.assertEqual(len(disabled_alarms), 2)

    def test_edit_alarm(self):
        """ Creates an alarm and edits it. """
        adh = AlarmDb(self.db_name)
        adh.delete_all_alarms()
        alarm_test = AlarmItem(
            13, 35, days=(False, False, False, False, False, False, False),
            enabled=True, label='')

        # Check the timestamp changes on add_alarm
        original_timestamp = alarm_test.timestamp
        alarm_test.id_ = adh.add_alarm(alarm_test)
        self.assertNotEqual(alarm_test.timestamp, original_timestamp)

        # Edit alarm, check new data and different timestamp
        original_timestamp = alarm_test.timestamp
        time.sleep(1)
        edit_success = adh.edit_alarm(
            alarm_test.id_, 11, 22, enabled=False, label='New label',
            days=(True, True, True, True, True, True, True))
        self.assertEqual(edit_success, True)
        edited_alarm = adh.get_alarm(alarm_test.id_)
        self.assertGreater(edited_alarm.timestamp, original_timestamp)
        self.assertEqual(edited_alarm.hour, 11)
        self.assertEqual(edited_alarm.minute, 22)
        self.assertTrue(edited_alarm.monday)
        self.assertTrue(edited_alarm.tuesday)
        self.assertTrue(edited_alarm.wednesday)
        self.assertTrue(edited_alarm.thursday)
        self.assertTrue(edited_alarm.friday)
        self.assertTrue(edited_alarm.saturday)
        self.assertTrue(edited_alarm.sunday)
        self.assertFalse(edited_alarm.enabled)
        self.assertEqual(edited_alarm.label, 'New label')

    def test_edit_alarm_single(self):
        """
        Adds an alarm, edits a single value and checks all the others remain the
        same.
        """
        adh = AlarmDb(self.db_name)
        alarm_test = AlarmItem(
            13, 35, enabled=True, label='yes',
            days=(True, False, True, False, True, False, True))

        # Check the timestamp changes on add_alarm
        original_timestamp = alarm_test.timestamp
        alarm_test.id_ = adh.add_alarm(alarm_test)
        self.assertNotEqual(alarm_test.timestamp, original_timestamp)

        # Edit alarm, check new data and different timestamp
        original_timestamp = alarm_test.timestamp
        time.sleep(1)
        edit_success = adh.edit_alarm(alarm_test.id_, minute=0)
        self.assertTrue(edit_success)
        edited_alarm = adh.get_alarm(alarm_test.id_)
        self.assertGreater(edited_alarm.timestamp, original_timestamp)
        self.assertEqual(edited_alarm.hour, 13)
        self.assertEqual(edited_alarm.minute, 0)
        self.assertTrue(edited_alarm.monday)
        self.assertFalse(edited_alarm.tuesday)
        self.assertTrue(edited_alarm.wednesday)
        self.assertFalse(edited_alarm.thursday)
        self.assertTrue(edited_alarm.friday)
        self.assertFalse(edited_alarm.saturday)
        self.assertTrue(edited_alarm.sunday)
        self.assertTrue(edited_alarm.enabled)
        self.assertEqual(edited_alarm.label, 'yes')

        # Test with opposite initial values
        alarm_test = AlarmItem(
            10, 20, enabled=False, label='no',
            days=(False, True, False, True, False, True, False))
        alarm_test.id_ = adh.add_alarm(alarm_test)
        edit_success = adh.edit_alarm(alarm_test.id_, hour=0)
        self.assertTrue(edit_success)
        edited_alarm = adh.get_alarm(alarm_test.id_)
        self.assertEqual(edited_alarm.hour, 0)
        self.assertEqual(edited_alarm.minute, 20)
        self.assertFalse(edited_alarm.monday)
        self.assertTrue(edited_alarm.tuesday)
        self.assertFalse(edited_alarm.wednesday)
        self.assertTrue(edited_alarm.thursday)
        self.assertFalse(edited_alarm.friday)
        self.assertTrue(edited_alarm.saturday)
        self.assertFalse(edited_alarm.sunday)
        self.assertFalse(edited_alarm.enabled)
        self.assertEqual(edited_alarm.label, 'no')

    def test_update_alarm(self):
        """ Creates an alarm and update it. """
        adh = AlarmDb(self.db_name)
        adh.delete_all_alarms()
        alarm_test = AlarmItem(
            13, 35, days=(False, False, False, False, False, False, False),
            enabled=True, label='')
        original_timestamp = alarm_test.timestamp

        # Add the alarm to the database and check the timestamp has been set
        alarm_test.id_ = adh.add_alarm(alarm_test)
        self.assertNotEqual(alarm_test.timestamp, original_timestamp)
        original_timestamp = alarm_test.timestamp

        # Create a new AlarmItem with the same id and timestamp to update the db
        alarm_updated = AlarmItem(
            21, 12, days=(True, True, True, True, True, True, True),
            enabled=False, label='new label', alarm_id=alarm_test.id_,
            timestamp=original_timestamp)
        time.sleep(1)
        update_success = adh.update_alarm(alarm_updated)
        self.assertEqual(update_success, True)
        self.assertNotEqual(alarm_updated.timestamp, original_timestamp)

        # Check the new data has replaced the old,
        retrieved_alarm = adh.get_alarm(alarm_test.id_)
        self.assertEqual(retrieved_alarm.hour, 21)
        self.assertEqual(retrieved_alarm.minute, 12)
        self.assertTrue(retrieved_alarm.monday)
        self.assertTrue(retrieved_alarm.tuesday)
        self.assertTrue(retrieved_alarm.wednesday)
        self.assertTrue(retrieved_alarm.thursday)
        self.assertTrue(retrieved_alarm.friday)
        self.assertTrue(retrieved_alarm.saturday)
        self.assertTrue(retrieved_alarm.sunday)
        self.assertFalse(retrieved_alarm.enabled)
        self.assertEqual(retrieved_alarm.label, 'new label')
        self.assertEqual(retrieved_alarm.timestamp, alarm_updated.timestamp)
        self.assertGreater(retrieved_alarm.timestamp, original_timestamp)

    def test_export_alarms_json(self):
        """
        Tests that the test_export_alarms_json creates a correct json string
        for all the 5 alarms inputted into the database.
        """
        adh = AlarmDb(self.db_name)
        self.only_five_entries(adh)
        json_str = adh.export_alarms_json()
        alarms_parsed = json.loads(json_str)

        def test_alarm(test, alarm, hour, minute, monday, tuesday, wednesday,
                       thursday, friday, saturday, sunday, enabled, label):
            test.assertEqual(alarm.hour, hour)
            test.assertEqual(alarm.minute, minute)
            test.assertEqual(alarm.monday, monday)
            test.assertEqual(alarm.tuesday, tuesday)
            test.assertEqual(alarm.wednesday, wednesday)
            test.assertEqual(alarm.thursday, thursday)
            test.assertEqual(alarm.friday, friday)
            test.assertEqual(alarm.saturday, saturday)
            test.assertEqual(alarm.sunday, sunday)
            test.assertEqual(alarm.enabled, enabled)
            test.assertEqual(alarm.label, label)

        for i in range(0, 5):
            test_alarm(self, adh.get_alarm(i+1),
                       alarms_parsed['alarms'][i]['hour'],
                       alarms_parsed['alarms'][i]['minute'],
                       alarms_parsed['alarms'][i]['monday'],
                       alarms_parsed['alarms'][i]['tuesday'],
                       alarms_parsed['alarms'][i]['wednesday'],
                       alarms_parsed['alarms'][i]['thursday'],
                       alarms_parsed['alarms'][i]['friday'],
                       alarms_parsed['alarms'][i]['saturday'],
                       alarms_parsed['alarms'][i]['sunday'],
                       alarms_parsed['alarms'][i]['enabled'],
                       alarms_parsed['alarms'][i]['label'])

    def test_snooze_time(self):
        """ Test the accessor for the db snooze time setting. """
        adh = AlarmDb(self.db_name)
        # Valid data
        success = adh.set_snooze_time(5)
        self.assertTrue(success)
        self.assertEquals(adh.get_snooze_time(), 5)

        # Invalid data should maintain old value
        success = adh.set_snooze_time(-1)
        self.assertFalse(success)
        self.assertEquals(adh.get_snooze_time(), 5)

        success = adh.set_snooze_time(2.5)
        self.assertFalse(success)
        self.assertEquals(adh.get_snooze_time(), 5)

        success = adh.set_snooze_time('3')
        self.assertFalse(success)
        self.assertEquals(adh.get_snooze_time(), 5)

    def test_prealert_time(self):
        """ Test the accessor for the db prealert time setting. """
        adh = AlarmDb(self.db_name)

        # Valid negative data
        success = adh.set_prealert_time(-1)
        self.assertTrue(success)
        self.assertEquals(adh.get_prealert_time(), -1)

        # Valid positive data
        success = adh.set_prealert_time(5)
        self.assertTrue(success)
        self.assertEquals(adh.get_prealert_time(), 5)

        # Invalid data should maintain old value
        success = adh.set_prealert_time(2.5)
        self.assertFalse(success)
        self.assertEquals(adh.get_prealert_time(), 5)

        success = adh.set_prealert_time('3')
        self.assertFalse(success)
        self.assertEquals(adh.get_prealert_time(), 5)

    def test_reset_settings(self):
        """ Test reset settings. """
        adh = AlarmDb(self.db_name)
        success = adh.set_snooze_time(321)
        self.assertTrue(success)
        success = adh.set_prealert_time(123)
        self.assertTrue(success)
        self.assertEquals(adh.get_snooze_time(), 321)
        self.assertEquals(adh.get_prealert_time(), 123)

        success = adh.reset_settings()
        self.assertTrue(success)
        self.assertNotEquals(adh.get_snooze_time(), 321)
        self.assertNotEquals(adh.get_prealert_time(), 123)

if __name__ == '__main__':
    unittest.main()
