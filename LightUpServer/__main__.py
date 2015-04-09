#!/usr/bin/env python2
#
# Entry point for the LightUpServer package.
#
# Copyright (c) 2015 carlosperate http://carlosperate.github.io
#
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
# Longer description.
#
from __future__ import unicode_literals, absolute_import
import sys
from LightUpServer import Server


def main(argv=None, alarm_mgr=None):
    # Checking command line arguments
    if (argv is not None) and (len(argv) > 0):
        pass

    Server.main(alarm_mgr)


if __name__ == '__main__':
    main(sys.argv[1:])
