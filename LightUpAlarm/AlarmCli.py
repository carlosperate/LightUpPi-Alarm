#!/usr/bin/env python2
#
# Command line interface for the LightUpAlarm package.
#
# Copyright (c) 2015 carlosperate https://github.com/carlosperate/
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
# The command line interface uses 80 vertical columns, exactly 80 in a lot of
# instances, but aims to never use more.
#
# Because the Unit test would basically require to manually write all the
# possible text that should be displayed as part of the CLI, and because the
# operations performed here are relatively straight forwards (minimum logic and
# calls to classes with full test coverage), no unit test has been developed.
#
from __future__ import unicode_literals, absolute_import
import os
import cmd
import sys
try:
    from LightUpAlarm.AlarmManager import AlarmManager
except ImportError:
    from AlarmManager import AlarmManager


class AlarmCli(cmd.Cmd):
    """
    Command processor class to control LightUpAlarm.
    The Pydoc comments do not include the 'param' and 'return' data because
    the class uses these comments for the command line help menu.
    """
    prompt = '\n(command): '
    doc_header = 'Available commands (for more info type "help <command>")'

    #
    # metaclass methods
    #
    def __init__(self):
        """ Instance constructor. """
        cmd.Cmd.__init__(self)
        self.alarm_mgr = AlarmManager()

    #
    # parent class methods
    #
    def preloop(self):
        """ Gets executed before the run loop. """
        self.show_header_only()

    def onecmd(self, s):
        """
        Parses and executes the command. Overwritten to added method to only
        show the header and current alarms at the top of the terminal and the
        current command output.
        """
        self.show_header_only()
        return cmd.Cmd.onecmd(self, s)

    #
    # command methods
    #
    def do_alarms(self, empty_str):
        """ Displays all the alarms. """
        pass

    def do_active(self, empty_str):
        """ Displays the active alarms currently running. """
        running_alarms = self.alarm_mgr.get_running_alarms()
        print('\nActive alarms running:\n' +
              '----------------------------------------' +
              '----------------------------------------')
        if not running_alarms:
            print('\tThere are not active alarms running.')
        else:
            for alarm in running_alarms:
                print(alarm)

    def do_add(self, alarm_str):
        """
        Add an alarm using the format (days follow the 3 letter format):
        'hh mm enable_boolean days_to_reap'
        eg. '9 00 True Mon Fri'
        """
        words = alarm_str.split(' ')
        try:
            hour = int(words[0])
        except ValueError:
            print('First item must be a number indicating the time !')
            return
        try:
            minute = int(words[1])
        except ValueError:
            print('First item must be a number indicating the time !')
            return
        if words[2] == 'enable' or words[2] == 'enabled':
            enable = True
        elif words[2] == 'disable' or words[2] == 'disabled':
            enable = False
        else:
            print('Third item must indicate if the alarm will be "enable" or ' +
                  '"disabled" !')
            return
        if words[3]:
            if words[3].lower() == 'all':
                repeats = (True, True, True, True, True, True, True)
            else:
                repeats = [False] * 7
                for i in xrange(len(words[3:])):
                    if words[i+3].lower() == 'mon':
                        repeats[0] = True
                    elif words[i+3].lower() == 'tue':
                        repeats[1] = True
                    elif words[i+3].lower() == 'wed':
                        repeats[2] = True
                    elif words[i+3].lower() == 'thu':
                        repeats[3] = True
                    elif words[i+3].lower() == 'fri':
                        repeats[4] = True
                    elif words[i+3].lower() == 'sat':
                        repeats[5] = True
                    elif words[i+3].lower() == 'sun':
                        repeats[6] = True
        else:
            repeats = (False, False, False, False, False, False, False)

        alarm_id = self.alarm_mgr.add_alarm(hour, minute, repeats, enable)
        if alarm_id is not None:
            self.show_header_only()
            print('\nCreated Alarm:\n' +
                  '----------------------------------------' +
                  '----------------------------------------\n' +
                  '%s' % AlarmManager.get_alarm(alarm_id))

    def do_edit(self, edit_str):
        """
        Edit an alarm using the following format:
        'id attribute new_value"
        eg. '1 enable False'
            '2 monday true'
            '3 hour 9'
        """
        pass

    def do_delete(self, alarm_id_string):
        """
        Delete an alarm identified by its id, eg:
        'delete 3'
        """
        try:
            alarm_id = int(alarm_id_string)
        except ValueError:
            print('After "delete" there must be a number indicating ' +
                  'the Alarm ID to be deleted !')
            return
        success = self.alarm_mgr.delete_alarm(alarm_id)
        if not success:
            print('The Alarm could not be deleted.')
        print('')  # Extra new line

    def do_exit(self, empty_str):
        """ Exists the LightUp Alarm program. """
        return True

    #
    # Command line interface methods
    #
    def show_header_only(self):
        if os.name == 'nt':
            os.system("cls")
        else:
            os.system('clear')
        print('========================================' +
              '========================================\n' +
              '=                               LightUp ' +
              'Alarm                                  =\n' +
              '=                                       ' +
              '                                       =\n' +
              '= Use the "help" command for information' +
              ' about how to use this program.        =\n' +
              '========================================' +
              '========================================')
        # Display the alarms below header
        all_alarms = self.alarm_mgr.get_all_alarms()
        print('\n\nAlarms:\n' +
              '----------------------------------------' +
              '----------------------------------------')
        if not all_alarms:
            print('\tThere are not saved alarms.')
        else:
            for alarm in all_alarms:
                print(alarm)
        print('')  # Extra new line


#
# Non-class methods
#
def main(argv=None):
    # Checking command line arguments
    if (argv is not None) and (len(argv) > 0):
        AlarmCli().onecmd(' '.join(argv[0:]))
    else:
        AlarmCli().cmdloop()


if __name__ == "__main__":
    main(sys.argv[1:])
