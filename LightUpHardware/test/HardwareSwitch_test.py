#!/usr/bin/env python2
#
# Unit test for the HardwareSwitch class.
#
# Copyright (c) 2015 carlosperate https://github.com/carlosperate/
#
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
# These test require the Wemo Switch to be on the network at the defined IP
# address.
#
from __future__ import unicode_literals, absolute_import
import io
import mock
import unittest
from time import sleep
try:
    import LightUpHardware.HardwareSwitch as HardwareSwitch
    from LightUpHardware.pywemoswitch.WemoSwitch import WemoSwitch
except ImportError:
    import os
    import sys
    file_dir = os.path.dirname(os.path.realpath(__file__))
    package_dir = os.path.dirname(os.path.dirname(file_dir))
    sys.path.insert(0, package_dir)
    import LightUpHardware.HardwareSwitch as HardwareSwitch
    from LightUpHardware.pywemoswitch.WemoSwitch import WemoSwitch


class HardwareSwitchTestCase(unittest.TestCase):
    """
    Tests for HardwareSwitch functions.
    These test require the Wemo Switch to be on the network at the defined IP
    address.
    """

    #
    # Helper methods
    #
    def assert_stderr(self, test_srderr, equal=False):
        """ Checks the stderr error string and resets it for next test. """
        if equal is True:
            self.assertEqual(test_srderr.getvalue(), '')
        else:
            self.assertNotEqual(test_srderr.getvalue(), '')
        test_srderr.truncate(0)
        test_srderr.write('')
        self.assertEqual(test_srderr.getvalue(), '')

    #
    # Tests
    #
    def test__get_switch(self):
        """
        Tests if an error is set when a switch cannot be connected. Due to the
        connection timeout this test can take several seconds to complete.
        """
        # We capture stderr to check for invalid input IP
        with mock.patch('sys.stderr', new=io.StringIO()) as test_srderr:
            # Invalid _coffee_switch_name causes to print an error
            switch = HardwareSwitch._get_switch('127.0.0.1')
            self.assert_stderr(test_srderr)
            self.assertIsNone(switch)

        # Test that the default IP returns a connected switch instance
        switch = HardwareSwitch._get_switch()
        self.assertEqual(type(switch), WemoSwitch)

    def test_switch_on_off(self):
        """
        Tests the switch Turns ON and OFF with the default input and a given
        switch.
        """
        state = HardwareSwitch.switch_on()
        self.assertTrue(state)
        sleep(1)
        state = HardwareSwitch.switch_off()
        self.assertFalse(state)

        switch = HardwareSwitch._get_switch()
        state = HardwareSwitch.switch_on(switch)
        self.assertTrue(state)
        sleep(1)
        state = HardwareSwitch.switch_off(switch)
        self.assertFalse(state)

    def test_safe_on(self):
        """ Tests the default switch Turns ON only if already ON. """
        switch = HardwareSwitch._get_switch()
        switch_is_on = switch.get_state()
        if switch_is_on is True:
            switch.turn_off()
        switch_is_on = switch.get_state()
        self.assertFalse(switch_is_on)
        HardwareSwitch.safe_on()
        switch_is_on = switch.get_state()
        self.assertTrue(switch_is_on)

        # We capture stderr to check for swtich already ON when called and
        # mock the turn off method to check if it was called
        with mock.patch('sys.stderr', new=io.StringIO()) as test_srderr:
            with mock.patch('LightUpHardware.pywemoswitch.WemoSwitch') as \
                    mock_switch:
                self.assert_stderr(test_srderr, True)
                HardwareSwitch.safe_on()
                self.assertEqual(mock_switch.turn_off.call_count, 0)
                self.assert_stderr(test_srderr)
                switch_is_on = switch.get_state()
                self.assertTrue(switch_is_on)

        # to clean up, turn the switch off
        sleep(1)
        switch.turn_off()


if __name__ == '__main__':
    unittest.main()
