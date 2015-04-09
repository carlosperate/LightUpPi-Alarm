#!/usr/bin/env python2
#
# Entry point for the LightUpAlarm package.
#
# Copyright (c) 2015 carlosperate http://carlosperate.github.io
#
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
# Creates an instance of the AlarmCli class and runs it.
#
from __future__ import unicode_literals, absolute_import
import sys
try:
    from LightUpAlarm.AlarmCli import AlarmCli
except ImportError:
    from AlarmCli import AlarmCli


def main(argv=None):
    # Checking command line arguments
    if (argv is not None) and (len(argv) > 0):
        AlarmCli().onecmd(' '.join(argv[0:]))
    else:
        AlarmCli().cmdloop()


if __name__ == "__main__":
    main(sys.argv[1:])
