#!/usr/bin/env python2
# #############################################################################
# Starts the LightUp Alarm application.
#
# Copyright (c) 2015 carlosperate https://github.com/carlosperate/
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
# Full description goes here
###############################################################################
from __future__ import unicode_literals, absolute_import
import sys
import os
import re
import getopt
import platform


def parsing_args(argv):
    """
    Processes the command line arguments. Arguments supported:
    -h / --help
    -s / --serverroot <working directory>
    :return: dictionary with available options(keys) and value(value)
    """
    option_dict = {}
    try:
        opts, args = getopt.getopt(argv, "hs:", ["help", "serverroot="])
    except getopt.GetoptError as e:
        print('There was a problem parsing the command line arguments:')
        print('\t%s' % e)
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('Include a server working directory using the flag:')
            print('\t -s <folder>')
            sys.exit(0)
        if opt in ("-s", "--serverroot"):
            # Windows only issue: In BlocklyRequestHandler, if chdir is fed
            # an 'incorrect' path like 'C:' instead of 'C:\' or C:/' it
            # fails silently maintaining the current working directory.
            # Use regular expressions to catch this corner case.
            if re.match("^[a-zA-Z]:$", arg):
                print('The windows drive letter needs to end in a slash, ' +
                      'eg. %s\\' % arg)
                sys.exit(1)
            # Check if the value is a valid directory
            if os.path.isdir(arg):
                option_dict['serverroot'] = arg
                print ('Parsed "' + opt + '" flag with "' + arg + '" value.')
            else:
                print('Invalid directory "' + arg + '".')
                sys.exit(1)
        else:
            print('Flag ' + opt + ' not recognised.')
    return option_dict


def main(argv):
    """
    Gets the argument flags and launches the server.
    """
    print('Running Python version ' + platform.python_version())

    # Checking command line arguments
    if len(argv) > 0:
        print("\n======= Parsing Command line arguments =======")
        arguments = parsing_args(argv)
        if 'serverroot' in arguments:
            # Nothing yet implemented, so do nothing
            pass

    # Loading the settings
    print("\n======= Doing something =======")


if __name__ == "__main__":
    main(sys.argv[1:])
