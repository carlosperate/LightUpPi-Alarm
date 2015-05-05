#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Unit test for the HardwareLightBulb module.
#
# Copyright (c) 2015 carlosperate https://github.com/carlosperate/
#
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
from __future__ import unicode_literals, absolute_import
import sys
import unittest
import time
try:
    from LightUpHardware.HardwareLightBulb import *
except ImportError:
    import os
    import sys
    file_dir = os.path.dirname(os.path.realpath(__file__))
    package_dir = os.path.dirname(os.path.dirname(file_dir))
    sys.path.insert(0, package_dir)
    from LightUpHardware.HardwareLightBulb import *


class HardwareSwitchTestCase(unittest.TestCase):
    """
    This is an extremely simple test to be able to quickly see the room light
    bulb working.
    """

    #
    # Tests
    #
    def test_gradual_light_on(self):
        run_time = 60
        start_time = time.time()
        gradual_light_on(run_time)
        end_time = time.time()
        # Large delta due to the initial time required to connect
        self.assertAlmostEqual(start_time + run_time, end_time, delta=10)


if __name__ == '__main__':
    unittest.main()
