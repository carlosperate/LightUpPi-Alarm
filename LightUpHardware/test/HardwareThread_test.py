#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Unit test for the HardwareThread class.
#
# Copyright (c) 2015 carlosperate https://github.com/carlosperate/
#
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
from __future__ import unicode_literals, absolute_import
import io
import time
import mock
import types
import unittest
import threading
try:
    from LightUpHardware.HardwareThread import HardwareThread
except ImportError:
    import os
    import sys
    file_dir = os.path.dirname(os.path.realpath(__file__))
    package_dir = os.path.dirname(os.path.dirname(file_dir))
    sys.path.insert(0, package_dir)
    print("path added: %s" % package_dir)
    from LightUpHardware.HardwareThread import HardwareThread


class HardwareThreadTestCase(unittest.TestCase):
    """ Tests for HardwareThread class. """

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
    # Test methods
    #
    def test_singleton(self):
        """ Testing if singleton is working. """
        if HardwareThread._HardwareThread__singleton is not None:
            HardwareThread._drop()
        self.assertIsNone(HardwareThread._HardwareThread__singleton)
        instance_1 = HardwareThread()
        instance_2 = HardwareThread()
        self.assertIsNotNone(HardwareThread._HardwareThread__singleton)
        self.assertIsNotNone(instance_1)
        self.assertIsNotNone(instance_2)
        self.assertEqual(id(instance_1), id(instance_2))
        self.assertEqual(id(instance_1),
                         id(HardwareThread._HardwareThread__singleton))

    def test_destructor(self):
        """ Testing if destructor is working. """
        # Dropping from instance
        instance = HardwareThread()
        self.assertIsNotNone(instance)
        instance._drop()
        self.assertIsNone(instance._HardwareThread__singleton)
        self.assertIsNone(HardwareThread._HardwareThread__singleton)

        # Dropping from class
        instance = HardwareThread()
        self.assertIsNotNone(instance)
        HardwareThread._drop()
        self.assertIsNone(instance._HardwareThread__singleton)
        self.assertIsNone(HardwareThread._HardwareThread__singleton)

        # Trying to drop a not instantiated singleton should print stderr
        with mock.patch('sys.stderr', new=io.StringIO()) as test_srderr:
            HardwareThread._drop()
            self.assert_stderr(test_srderr)

    def test_constructor(self):
        """
        Tests the class constructor saving data correctly and outputting errors
        if required.
        """
        if HardwareThread._HardwareThread__singleton is not None:
            HardwareThread._drop()

        # Ensure the default values are None
        self.assertIsNone(HardwareThread._HardwareThread__lamp_time)
        self.assertIsNone(HardwareThread._HardwareThread__lamp_duration)
        self.assertIsNone(HardwareThread._HardwareThread__room_light_time)
        self.assertIsNone(HardwareThread._HardwareThread__room_light_duration)
        self.assertIsNone(HardwareThread._HardwareThread__coffee_time)
        self.assertIsNone(HardwareThread._HardwareThread__total_time)

        self.assertIsNone(HardwareThread.lamp_time)
        self.assertIsNone(HardwareThread.lamp_duration)
        self.assertIsNone(HardwareThread.room_light_time)
        self.assertIsNone(HardwareThread.room_light_duration)
        self.assertIsNone(HardwareThread.coffee_time)
        self.assertIsNone(HardwareThread.total_time)

        # Check constructor with no arguments does not affect default values
        hw_thread_instance = HardwareThread()
        self.assertIsNotNone(hw_thread_instance)

        self.assertIsNone(hw_thread_instance._HardwareThread__lamp_time)
        self.assertIsNone(hw_thread_instance._HardwareThread__lamp_duration)
        self.assertIsNone(hw_thread_instance._HardwareThread__room_light_time)
        self.assertIsNone(
            hw_thread_instance._HardwareThread__room_light_duration)
        self.assertIsNone(hw_thread_instance._HardwareThread__coffee_time)
        self.assertIsNone(hw_thread_instance._HardwareThread__total_time)

        self.assertIsNone(HardwareThread._HardwareThread__lamp_time)
        self.assertIsNone(HardwareThread._HardwareThread__lamp_duration)
        self.assertIsNone(HardwareThread._HardwareThread__room_light_time)
        self.assertIsNone(HardwareThread._HardwareThread__room_light_duration)
        self.assertIsNone(HardwareThread._HardwareThread__coffee_time)
        self.assertIsNone(HardwareThread._HardwareThread__total_time)

        self.assertIsNone(HardwareThread.lamp_time)
        self.assertIsNone(HardwareThread.lamp_duration)
        self.assertIsNone(HardwareThread.room_light_time)
        self.assertIsNone(HardwareThread.room_light_duration)
        self.assertIsNone(HardwareThread.coffee_time)
        self.assertIsNone(HardwareThread.total_time)

        # Test that the argument inputs are saved in the class static variables
        hw_thread_instance = HardwareThread(
            lamp=(1, 2),
            room_light=(3, 4),
            coffee_time=5,
            total_time=6)
        self.assertEqual(1, hw_thread_instance._HardwareThread__lamp_time)
        self.assertEqual(1, HardwareThread._HardwareThread__lamp_time)
        self.assertEqual(1, HardwareThread.lamp_time)
        self.assertEqual(2, hw_thread_instance._HardwareThread__lamp_duration)
        self.assertEqual(2, HardwareThread._HardwareThread__lamp_duration)
        self.assertEqual(2, HardwareThread.lamp_duration)
        self.assertEqual(3, hw_thread_instance._HardwareThread__room_light_time)
        self.assertEqual(3, HardwareThread._HardwareThread__room_light_time)
        self.assertEqual(3, HardwareThread.room_light_time)
        self.assertEqual(
            4, hw_thread_instance._HardwareThread__room_light_duration)
        self.assertEqual(
            4, HardwareThread._HardwareThread__room_light_duration)
        self.assertEqual(
            4, HardwareThread.room_light_duration)
        self.assertEqual(5, hw_thread_instance._HardwareThread__coffee_time)
        self.assertEqual(5, HardwareThread._HardwareThread__coffee_time)
        self.assertEqual(5, HardwareThread.coffee_time)
        self.assertEqual(6, hw_thread_instance._HardwareThread__total_time)
        self.assertEqual(6, HardwareThread._HardwareThread__total_time)
        self.assertEqual(6, HardwareThread.total_time)

        # lamp and room light can also take lists
        hw_thread_instance = HardwareThread(
            lamp=[7, 8],
            room_light=[9, 10])
        self.assertEqual(7, hw_thread_instance._HardwareThread__lamp_time)
        self.assertEqual(7, HardwareThread._HardwareThread__lamp_time)
        self.assertEqual(7, HardwareThread.lamp_time)
        self.assertEqual(8, hw_thread_instance._HardwareThread__lamp_duration)
        self.assertEqual(8, HardwareThread._HardwareThread__lamp_duration)
        self.assertEqual(8, HardwareThread.lamp_duration)
        self.assertEqual(9, hw_thread_instance._HardwareThread__room_light_time)
        self.assertEqual(9, HardwareThread._HardwareThread__room_light_time)
        self.assertEqual(9, HardwareThread.room_light_time)
        self.assertEqual(
            10, hw_thread_instance._HardwareThread__room_light_duration)
        self.assertEqual(
            10, HardwareThread._HardwareThread__room_light_duration)
        self.assertEqual(
            10, HardwareThread.room_light_duration)

        # Test invalid arguments printing to stderr, so need to capture it
        with mock.patch('sys.stderr', new=io.StringIO()) as test_srderr:
            # Wrong lamp, constructor only checks for list/touple and length
            hw_thread_instance = HardwareThread(lamp=(0, 1, 2))
            self.assertIsNotNone(hw_thread_instance)
            self.assert_stderr(test_srderr)
            hw_thread_instance = HardwareThread(lamp=(1,))
            self.assertIsNotNone(hw_thread_instance)
            self.assert_stderr(test_srderr)
            hw_thread_instance = HardwareThread(lamp=[0, 1, 2])
            self.assertIsNotNone(hw_thread_instance)
            self.assert_stderr(test_srderr)
            hw_thread_instance = HardwareThread(lamp=[1])
            self.assertIsNotNone(hw_thread_instance)
            self.assert_stderr(test_srderr)

            # Wrong room_light,constructor only checks for list/touple and len
            hw_thread_instance = HardwareThread(room_light=(0, 1, 2))
            self.assertIsNotNone(hw_thread_instance)
            self.assert_stderr(test_srderr)
            hw_thread_instance = HardwareThread(room_light=(1,))
            self.assertIsNotNone(hw_thread_instance)
            self.assert_stderr(test_srderr)
            hw_thread_instance = HardwareThread(room_light=[0, 1, 2])
            self.assertIsNotNone(hw_thread_instance)
            self.assert_stderr(test_srderr)
            hw_thread_instance = HardwareThread(room_light=[1])
            self.assertIsNotNone(hw_thread_instance)
            self.assert_stderr(test_srderr)

            # The lamp_time, lamp_duration, room_light_time, room_light_duration
            # coffee_time, and total_time error checking are done as part of
            # the accessors

    def test_lamp_time(self):
        """ Tests the lamp_time accessors. """
        if HardwareThread._HardwareThread__singleton is not None:
            HardwareThread._drop()

        # Get current original value (None) and ensure getter returns the same
        original_lamp_time = \
            HardwareThread._HardwareThread__lamp_time
        self.assertEqual(original_lamp_time,
                         HardwareThread.lamp_time)
        self.assertIsNone(HardwareThread.lamp_time)

        # Set the value without a class instance created
        HardwareThread.lamp_time = 1
        self.assertEqual(1, HardwareThread._HardwareThread__lamp_time)
        self.assertEqual(1, HardwareThread.lamp_time)

        # Create the instance with empty constructor and ensure untouched
        hw_thread_instance = HardwareThread()
        self.assertEqual(1, hw_thread_instance._HardwareThread__lamp_time)
        self.assertEqual(1, HardwareThread._HardwareThread__lamp_time)
        self.assertEqual(1, HardwareThread.lamp_time)

        # Test invalid arguments print to stderr, so need to capture it
        with mock.patch('sys.stderr', new=io.StringIO()) as test_srderr:
            HardwareThread.lamp_time = 0.0
            self.assert_stderr(test_srderr)
            HardwareThread.lamp_time = 'String'
            self.assert_stderr(test_srderr)

    def test_lamp_duration(self):
        """ Tests the lamp_duration accessors. """
        if HardwareThread._HardwareThread__singleton is not None:
            HardwareThread._drop()

        # Get current original value (None) and ensure getter returns the same
        original_lamp_duration = \
            HardwareThread._HardwareThread__lamp_duration
        self.assertEqual(original_lamp_duration,
                         HardwareThread.lamp_duration)
        self.assertIsNone(HardwareThread.lamp_duration)

        # Set the value without a class instance created
        HardwareThread.lamp_duration = 1
        self.assertEqual(1, HardwareThread._HardwareThread__lamp_duration)
        self.assertEqual(1, HardwareThread.lamp_duration)

        # Create the instance with empty constructor and ensure untouched
        hw_thread_instance = HardwareThread()
        self.assertEqual(1, hw_thread_instance._HardwareThread__lamp_duration)
        self.assertEqual(1, HardwareThread._HardwareThread__lamp_duration)
        self.assertEqual(1, HardwareThread.lamp_duration)

        # Test invalid arguments print to stderr, so need to capture it
        with mock.patch('sys.stderr', new=io.StringIO()) as test_srderr:
            HardwareThread.lamp_duration = 0.0
            self.assert_stderr(test_srderr)
            HardwareThread.lamp_duration = 'String'
            self.assert_stderr(test_srderr)

    def test_room_light_time(self):
        """ Tests the  room_light_time accessors. """
        if HardwareThread._HardwareThread__singleton is not None:
            HardwareThread._drop()

        # Get current original value (None) and ensure getter returns the same
        original_room_light_time = \
            HardwareThread._HardwareThread__room_light_time
        self.assertEqual(original_room_light_time,
                         HardwareThread.room_light_time)
        self.assertIsNone(HardwareThread.room_light_time)

        # Set the value without a class instance created
        HardwareThread.room_light_time = 1
        self.assertEqual(1, HardwareThread._HardwareThread__room_light_time)
        self.assertEqual(1, HardwareThread.room_light_time)

        # Create the instance with empty constructor and ensure untouched
        hw_thread_instance = HardwareThread()
        self.assertEqual(1, hw_thread_instance._HardwareThread__room_light_time)
        self.assertEqual(1, HardwareThread._HardwareThread__room_light_time)
        self.assertEqual(1, HardwareThread.room_light_time)

        # Test invalid arguments print to stderr, so need to capture it
        with mock.patch('sys.stderr', new=io.StringIO()) as test_srderr:
            HardwareThread.room_light_time = 0.0
            self.assert_stderr(test_srderr)
            HardwareThread.room_light_time = 'String'
            self.assert_stderr(test_srderr)

    def test_room_light_duration(self):
        """ Tests the  room_light_duration accessors. """
        if HardwareThread._HardwareThread__singleton is not None:
            HardwareThread._drop()

        # Get current original value (None) and ensure getter returns the same
        original_room_light_duration = \
            HardwareThread._HardwareThread__room_light_duration
        self.assertEqual(original_room_light_duration,
                         HardwareThread.room_light_duration)
        self.assertIsNone(HardwareThread.room_light_duration)

        # Set the value without a class instance created
        HardwareThread.room_light_duration = 1
        self.assertEqual(1, HardwareThread._HardwareThread__room_light_duration)
        self.assertEqual(1, HardwareThread.room_light_duration)

        # Create the instance with empty constructor and ensure untouched
        hw_thread_instance = HardwareThread()
        self.assertEqual(
            1, hw_thread_instance._HardwareThread__room_light_duration)
        self.assertEqual(1, HardwareThread._HardwareThread__room_light_duration)
        self.assertEqual(1, HardwareThread.room_light_duration)

        # Test invalid arguments print to stderr, so need to capture it
        with mock.patch('sys.stderr', new=io.StringIO()) as test_srderr:
            HardwareThread.room_light_duration = 0.0
            self.assert_stderr(test_srderr)
            HardwareThread.room_light_duration = 'String'
            self.assert_stderr(test_srderr)

    def test_coffee_time(self):
        """ Tests the  coffee_time accessors. """
        if HardwareThread._HardwareThread__singleton is not None:
            HardwareThread._drop()

        # Get current original value (None) and ensure getter returns the same
        original_coffee_time = \
            HardwareThread._HardwareThread__coffee_time
        self.assertEqual(original_coffee_time,
                         HardwareThread.coffee_time)
        self.assertIsNone(HardwareThread.coffee_time)

        # Set the value without a class instance created
        HardwareThread.coffee_time = 1
        self.assertEqual(1, HardwareThread._HardwareThread__coffee_time)
        self.assertEqual(1, HardwareThread.coffee_time)

        # Create the instance with empty constructor and ensure untouched
        hw_thread_instance = HardwareThread()
        self.assertEqual(1, hw_thread_instance._HardwareThread__coffee_time)
        self.assertEqual(1, HardwareThread._HardwareThread__coffee_time)
        self.assertEqual(1, HardwareThread.coffee_time)

        # Test invalid arguments print to stderr, so need to capture it
        with mock.patch('sys.stderr', new=io.StringIO()) as test_srderr:
            HardwareThread.coffee_time = 0.0
            self.assert_stderr(test_srderr)
            HardwareThread.coffee_time = 'String'
            self.assert_stderr(test_srderr)

    def test_total_time(self):
        """ Tests the  total_time accessors. """
        if HardwareThread._HardwareThread__singleton is not None:
            HardwareThread._drop()

        # Get current original value (None) and ensure getter returns the same
        original_total_time = \
            HardwareThread._HardwareThread__total_time
        self.assertEqual(original_total_time,
                         HardwareThread.total_time)
        self.assertIsNone(HardwareThread.total_time)

        # Set the value without a class instance created
        HardwareThread.total_time = 1
        self.assertEqual(1, HardwareThread._HardwareThread__total_time)
        self.assertEqual(1, HardwareThread.total_time)

        # Create the instance with empty constructor and ensure untouched
        hw_thread_instance = HardwareThread()
        self.assertEqual(1, hw_thread_instance._HardwareThread__total_time)
        self.assertEqual(1, HardwareThread._HardwareThread__total_time)
        self.assertEqual(1, HardwareThread.total_time)

        # Test invalid arguments print to stderr, so need to capture it
        with mock.patch('sys.stderr', new=io.StringIO()) as test_srderr:
            HardwareThread.total_time = 0.0
            self.assert_stderr(test_srderr)
            HardwareThread.total_time = 'String'
            self.assert_stderr(test_srderr)

    def test_setattr(self):
        """
        As the class static variables have accesors set in the metaclass the
        instance of the class could have attributes set with the same name and
        cause undesired effects. The setattr method has been edited to stop this
        behaviour and it is tested here.
        """
        hw_thread_instance = HardwareThread()

        # lamp_time
        def invalid_add_attribute():
            hw_thread_instance.lamp_time = 5
        self.assertRaises(AttributeError, invalid_add_attribute)

        def invalid_read_attribute():
            a = hw_thread_instance.lamp_time
        self.assertRaises(AttributeError, invalid_read_attribute)

        # lamp_duration
        def invalid_add_attribute():
            hw_thread_instance.lamp_duration = 5
        self.assertRaises(AttributeError, invalid_add_attribute)

        def invalid_read_attribute():
            a = hw_thread_instance.lamp_duration
        self.assertRaises(AttributeError, invalid_read_attribute)

        # room_light_time
        def invalid_add_attribute():
            hw_thread_instance.room_light_time = 5
        self.assertRaises(AttributeError, invalid_add_attribute)

        def invalid_read_attribute():
            a = hw_thread_instance.room_light_time
        self.assertRaises(AttributeError, invalid_read_attribute)

        # room_light_duration
        def invalid_add_attribute():
            hw_thread_instance.room_light_duration = 5
        self.assertRaises(AttributeError, invalid_add_attribute)

        def invalid_read_attribute():
            a = hw_thread_instance.room_light_duration
        self.assertRaises(AttributeError, invalid_read_attribute)

        # coffee_time
        def invalid_add_attribute():
            hw_thread_instance.coffee_time = 5
        self.assertRaises(AttributeError, invalid_add_attribute)

        def invalid_read_attribute():
            a = hw_thread_instance.coffee_time
        self.assertRaises(AttributeError, invalid_read_attribute)

        # total_time
        def invalid_add_attribute():
            hw_thread_instance.total_time = 5
        self.assertRaises(AttributeError, invalid_add_attribute)

        def invalid_read_attribute():
            a = hw_thread_instance.total_time
        self.assertRaises(AttributeError, invalid_read_attribute)

        # other key
        try:
            hw_thread_instance.new_key = 5
        except AttributeError:
            self.fail('Cannot set new attribute to HardwareThread instance.')
        try:
            a = hw_thread_instance.new_key
            self.assertEqual(a, 5)
        except AttributeError:
            self.fail('Cannot get new attribute to HardwareThread instance.')

    def test_run(self):
        """
        Because this unit test is designed to not require the hardware running,
        the methods that launch the threads to control the hw will be mocked.
        This also allows to check if the methods are called at the requested
        intervals.
        This test will take over 5 seconds.
        """
        if HardwareThread._HardwareThread__singleton is not None:
            HardwareThread._drop()

        lamp_start = 0
        lamp_duration = 2
        room_start = 1
        room_duration = 2
        coffee_time = 3
        total_time = 5
        start_time = 0

        # Mocking the _launch_lamp method
        def mock_launch_lamp(cls):
            self.launch_lamp_counter += 1
            now = time.time()
            self.assertAlmostEqual(now, start_time + lamp_start, delta=0.2)
        self.launch_lamp_counter = 0
        HardwareThread._launch_lamp = \
            types.MethodType(mock_launch_lamp, HardwareThread)

        # Mocking the _launch_room_light method
        def mock_launch_room_light(cls):
            self.launch_room_light_counter += 1
            now = time.time()
            self.assertAlmostEqual(now, start_time + room_start, delta=0.2)
        self.launch_room_light_counter = 0
        HardwareThread._launch_room_light = \
            types.MethodType(mock_launch_room_light, HardwareThread)

        # Mocking the _launch_coffee method
        def mock_launch_coffee(cls):
            self.launch_coffee_counter += 1
            now = time.time()
            self.assertAlmostEqual(now, start_time + coffee_time, delta=0.2)
        self.launch_coffee_counter = 0
        HardwareThread._launch_coffee = \
            types.MethodType(mock_launch_coffee, HardwareThread)

        def assert_thread_not_running():
            start_time = time.time()
            hw_thread_instance.start()
            while hw_thread_instance.isAlive():
                pass
            self.assertEqual(self.launch_lamp_counter, 0)
            self.assertEqual(self.launch_room_light_counter, 0)
            self.assertEqual(self.launch_coffee_counter, 0)

        # Test that thread will not run if variables are not set, stderr output
        hw_thread_instance = HardwareThread()
        with mock.patch('sys.stderr', new=io.StringIO()) as test_srderr:
            assert_thread_not_running()

            HardwareThread.lamp_time = lamp_start
            assert_thread_not_running()
            self.assert_stderr(test_srderr)

            HardwareThread.lamp_duration = lamp_duration
            assert_thread_not_running()
            self.assert_stderr(test_srderr)

            HardwareThread.room_light_time = room_start
            assert_thread_not_running()
            self.assert_stderr(test_srderr)

            HardwareThread.room_light_duration = room_duration
            assert_thread_not_running()
            self.assert_stderr(test_srderr)

            HardwareThread.coffee_time = coffee_time
            assert_thread_not_running()
            self.assert_stderr(test_srderr)

        HardwareThread.total_time = total_time

        # Now all variables set, it should run correctly
        start_time = time.time()
        hw_thread_instance.start()
        while hw_thread_instance.isAlive():
            pass
        end_time = time.time()
        self.assertAlmostEqual(total_time, end_time - start_time, delta=0.1)

        self.assertEqual(self.launch_lamp_counter, 1)
        self.assertEqual(self.launch_room_light_counter, 1)
        self.assertEqual(self.launch_coffee_counter, 1)

    def test_multirun(self):
        """
        Tests that the HardwareThread can be launched several times and that
        if one instance launches the thread, and another tries to do the same it
        will wait until it is done.
        This test can take over 8 seconds (2s per thread launch, 4 launches)
        """
        # These thread last 2 seconds
        hw_thread_instance_one = HardwareThread(
            lamp=(0, 1), room_light=(0, 1), coffee_time=0, total_time=2)
        hw_thread_instance_two = HardwareThread()

        # Mocking the hardware threads, they will finish as soon as they are
        # launched
        def mock_hw(cls):
            pass
        HardwareThread._launch_lamp = \
            types.MethodType(mock_hw, HardwareThread)
        HardwareThread._launch_room_light = \
            types.MethodType(mock_hw, HardwareThread)
        HardwareThread._launch_coffee = \
            types.MethodType(mock_hw, HardwareThread)

        # Launch the hardware thread, ensure it lasts 2 seconds
        start_time = time.time()
        hw_thread_instance_one.start()
        while hw_thread_instance_one.isAlive():
            pass
        end_time = time.time()
        self.assertAlmostEqual(2, end_time - start_time, delta=0.1)

        # Ensure the hardware thread can be launched multiple times
        start_time = time.time()
        hw_thread_instance_one.start()
        while hw_thread_instance_one.isAlive():
            pass
        end_time = time.time()
        self.assertAlmostEqual(2, end_time - start_time, delta=0.1)

        # Ensure the hardware thread can only be launched once at a time
        original_numb_threads = threading.activeCount()
        start_time = time.time()

        hw_thread_instance_one.start()
        time.sleep(0.2)  # Enough time for child threads launch and end
        hw_thread_count = threading.activeCount()
        self.assertEqual(original_numb_threads + 1, hw_thread_count)

        hw_thread_instance_two.start()
        self.assertEqual(hw_thread_count, threading.activeCount())
        while hw_thread_instance_two.isAlive():
            pass

        end_time = time.time()
        self.assertAlmostEqual(2*2, end_time - start_time, delta=0.1*2)


if __name__ == '__main__':
    unittest.main()
