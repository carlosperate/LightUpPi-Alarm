#!/usr/bin/env python2
#
# Starts the LightUp Alarm application.
#
# Copyright (c) 2015 carlosperate https://github.com/carlosperate/
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
# Full description goes here
#
from __future__ import unicode_literals, absolute_import
import sys
import getopt
import platform
from LightUpAlarm import AlarmCli


def parsing_args(argv):
    """
    Processes the command line arguments. Arguments supported:
    -h / --help
    -c / --cli
    -s / --server
    :return: dictionary with available options(keys) and value(value)
    """
    option_dict = {}
    try:
        opts, args = getopt.getopt(argv, "hsc", ["help", "server", "cli"])
    except getopt.GetoptError as e:
        print('There was a problem parsing the command line arguments:')
        print('\t%s' % e)
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('Choose between running the application in command line ' +
                  'interface or to launch the HTTP server.\n' +
                  '\t-c Command Line Interface\n\t-s Launch HTTP server')
            sys.exit(0)
        elif opt in ("-c", "--cli"):
                option_dict['cli'] = None
        elif opt in ("-s", "--server"):
                option_dict['server'] = None
        #if opt in ("-x", "--xxx"):
        else:
            print('Flag ' + opt + ' not recognised.')

        # It only takes the server or the cli flag, so check
        if 'server' in option_dict and 'cli' in option_dict:
            print('Both server and cli flags detected, include only one.')
            sys.exit(1)
    return option_dict


def main(argv):
    """
    Gets the argument flags and launches the server or command line interface.
    """
    # This variable is used to select between CLI or server
    launch_cli = True
    print('Running Python version ' + platform.python_version())

    # Checking command line arguments
    print('\n======= Parsing Command line arguments =======')
    if len(argv) > 0:

        arguments = parsing_args(argv)
        if 'server' in arguments:
            print('server selected')
            launch_cli = False
            pass
        elif 'cli' in arguments:
            print('cli selected')
            pass
    else:
        print('No flags defaults to the command line interface.')

    # Loading the settings
    print('\n\n=========== Launching LightUp Alarm ==========')
    if launch_cli is True:
        AlarmCli.AlarmCli().cmdloop()
    else:
        print('LightUp Server not yet implemented.')


if __name__ == "__main__":
    main(sys.argv[1:])
