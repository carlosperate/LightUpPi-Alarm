#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Starts the LightUpPi Alarm application.
#
# Copyright (c) 2015 carlosperate https://github.com/carlosperate/
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
# The entry point for the LightUpPi Alarm application. It can take command line
# arguments to select the command line interface, the server only run, or to
# have both running at the same time.
#
from __future__ import unicode_literals, absolute_import, print_function
import sys
import getopt
import thread
import platform
import threading
from time import sleep
from LightUpAlarm import AlarmCli
from LightUpAlarm import AlarmManager
from LightUpServer import Server
from LightUpHardware import HardwareThread


class CliThread(threading.Thread):
    """
    Simple thread class for launching command line ui in its own process (to be
    able to run alongside the server, which needs to be in the main thread)
    """
    def __init__(self):
        self.cli_instance = None
        threading.Thread.__init__(self)
        self.daemon = True

    def attach_alarm_mgr(self, alarm_mgr):
        self.cli_instance = AlarmCli.AlarmCli(alarm_mgr=alarm_mgr)

    def run(self):
        if self.cli_instance is None:
            print('ERROR: Need to attach an AlarmManager instance using the '
                  'attach_alarm_mgr method.', file=sys.stderr)
            return
        self.cli_instance.cmdloop()
        # Exit from cli returns here. User has requested the app to exit, and
        # this thread needs to request a keyboard interrupt to the main thread.
        thread.interrupt_main()

    def callback_event(self):
        """ Updates the cli data, to be used as a server callback. """
        self.cli_instance.onecmd('alarms')
        sys.stdout.flush()
        sys.stdout.write('\n%s' % self.cli_instance.prompt)

    def alarm_alert(self):
        # '\a' is a request to the terminal to beep
        print('\n\nRING RING RING!!!!\a')
        sleep(0.8)
        print('\a')
        sleep(0.8)
        print('\a')
        sys.stdout.write(self.cli_instance.prompt)


def alarm_offset_alert():
    """ Function executed as the 'offset alert' as a AlarmManager callback. """
    minutes = lambda x: x * 60
    hw_alert = HardwareThread.HardwareThread(
        lamp=(0, minutes(3)),
        room_light=(minutes(2), minutes(13)),
        coffee_time=minutes(10),
        total_time=minutes(15))
    hw_alert.start()


def parsing_args(argv):
    """
    Processes the command line arguments. Arguments supported:
    -h / --help
    -c / --cli
    -s / --server
    -b / --both
    :return: dictionary with available options(keys) and value(value)
    """
    option_dict = {}
    try:
        opts, args = getopt.getopt(
            argv, 'hscb', ['help', 'server', 'cli', 'both'])
    except getopt.GetoptError as e:
        print('There was a problem parsing the command line arguments:')
        print('\t%s' % e)
        sys.exit(1)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('Choose between running the application in command line ' +
                  'interface, to launch the HTTP server, or both.\n' +
                  '\t-c Command Line Interface\n\t-s Launch HTTP server\n'
                  '\t-b Both command line and server')
            sys.exit(0)
        elif opt in ('-c', '--cli'):
                option_dict['cli'] = None
        elif opt in ('-s', '--server'):
                option_dict['server'] = None
        elif opt in ('-b', '--both'):
                option_dict['both'] = None
        else:
            print('Flag ' + opt + ' not recognised.')

        # It only takes the server or the cli flag, so check
        if 'server' in option_dict and 'cli' in option_dict:
            print('Both server and cli flags detected, you can use the flag '
                  '-b/--both for both.')
    return option_dict


def main(argv):
    """
    Gets the argument flags and launches the server or command line interface.
    """
    print('Running Python version ' + platform.python_version())

    # This variable is used to select between the different modes, defaults both
    start = 'both'

    # Checking command line arguments in order of priority
    print('\n======= Parsing Command line arguments =======')
    if len(argv) > 0:
        arguments = parsing_args(argv)
        if 'both' in arguments:
            print('Command line and server selected')
            start = 'both'
        elif 'cli' in arguments:
            print('Command line selected')
            start = 'cli'
        elif 'server' in arguments:
            print('Server selected')
            start = 'server'
    else:
        print('No flags defaults to the command line interface.')

    # Loading the settings
    print('\n=========== Launching LightUpPi Alarm ==========')
    if start == 'server':
        # For the server we only set the offset alarm, as it is meant to be run
        # headless and nothing else will be connected to ring/alert
        alarm_mgr = AlarmManager.AlarmManager(
            offset_alert_callback=alarm_offset_alert)
        Server.run(alarm_mgr_arg=alarm_mgr)
    else:
        # The command line interface running on its own thread is common to
        # the 'cli' and 'both' options.
        cli_thread = CliThread()
        alarm_mgr = AlarmManager.AlarmManager(
            alert_callback=cli_thread.alarm_alert,
            offset_alert_callback=alarm_offset_alert)
        cli_thread.attach_alarm_mgr(alarm_mgr)
        cli_thread.start()
        # Infinite loop can be the Flask server, or just a loop
        try:
            if start == 'both':
                Server.run(
                    alarm_mgr_arg=alarm_mgr,
                    silent=True,
                    callback_arg=cli_thread.callback_event)
            else:
                while cli_thread.isAlive():
                    sleep(0.2)
        except (KeyboardInterrupt, SystemExit):
            # Allow the clean exit from the CLI interface to execute
            if cli_thread.isAlive():
                sleep(1)


if __name__ == '__main__':
    main(sys.argv[1:])
