#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Unit test for the HardwareLamp module.
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
    from LightUpHardware.HardwareLamp import *
except ImportError:
    import os
    import sys
    file_dir = os.path.dirname(os.path.realpath(__file__))
    package_dir = os.path.dirname(os.path.dirname(file_dir))
    sys.path.insert(0, package_dir)
    from LightUpHardware.HardwareLamp import *


class HardwareSwitchTestCase(unittest.TestCase):
    """
    This is an extremely simple test to be able to quickly see the lamp light
    up.
    """

    #
    # Tests
    #
    def test_gradual_light_on(self):
        run_time = 5
        start_time = time.time()
        gradual_light_on(run_time)
        end_time = time.time()
        self.assertAlmostEqual(start_time + run_time, end_time, delta=0.5)


if __name__ == '__main__':
    unittest.main()
