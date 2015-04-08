#!/usr/bin/env python2
#
# Command line interface for the LightUpAlarm package.
#
# Copyright (c) 2015 carlosperate http://carlosperate.github.io
#
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
import time
import random
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
    # Class variable for a full line (80 chars) of dashes
    dashes_line = '----------------------------------------' + \
                  '----------------------------------------'

    #
    # metaclass methods
    #
    def __init__(self, alarm_mgr=None, callback=None):
        """
        Instance initialiser.
        Creates an AlarmManager instance and sets the alarm alert callback.
        """
        cmd.Cmd.__init__(self)
        self.callback = callback
        self.callback_running = False
        if alarm_mgr is None:
            self.alarm_mgr = AlarmManager(self.alarm_callback)
        else:
            self.alarm_mgr = alarm_mgr

    #
    # parent class methods and class variables
    #
    prompt = '(command): '
    doc_header = 'Available commands (for more info type "help <command>")'

    def preloop(self):
        """ Gets executed before the run loop. """
        self.show_header_only()
        self.display_alarms()

    def onecmd(self, s):
        """
        Parses and executes the command. Overwritten to added method to only
        show the header and current alarms at the top of the terminal and the
        current command output.
        """
        self.show_header_only()
        return cmd.Cmd.onecmd(self, s)

    def postcmd(self, stop, line):
        """
        Runs after the command is executed. Overwritten to add a couple of blank
        lines before the command input is displayed. Used for visual spacing.
        """
        print('\n')
        return cmd.Cmd.postcmd(self, stop, line)

    #
    # Alar command methods
    #
    def do_alarms(self, full_str):
        """Help alarms:
        Displays all the alarms.
        Use the keyword 'full' to display additional info.
        """
        if full_str == '':
            self.display_alarms()
        elif full_str == 'full':
            all_alarms = self.alarm_mgr.get_all_alarms()
            print('All Alarms:\n' + AlarmCli.dashes_line)
            if not all_alarms:
                print('\tThere are not saved alarms.')
            else:
                for alarm in all_alarms:
                    print('%s\n              | timestamp: %s      | label: %s\n'
                          % (alarm, alarm.timestamp, alarm.label))
        else:
            print('The only command that can follow alarms is "full"')

    def do_active(self, empty_str):
        """Help active:
        Displays the active alarms currently running.
        """
        self.display_alarms()
        running_alarms = self.alarm_mgr.get_running_alarms()
        print('Active Alarms running:\n' + AlarmCli.dashes_line)
        if not running_alarms:
            print('\tThere are not active alarms running.')
        else:
            for alarm in running_alarms:
                print(alarm)

    def do_next(self, empty_str):
        """Help next:
        Displays the next scheduled alarm to alert.
        """
        self.display_alarms()
        next_alarm = self.alarm_mgr.get_next_alarm()
        if next_alarm is not None:
            print('The next scheduled Alarm is:\n' + AlarmCli.dashes_line)
            print(next_alarm)
        else:
            print('\tThere are not active alarms running.')

    def do_add(self, alarm_str):
        """Help add:
        Add an alarm using the format (days follow the 3 letter format):
        'hh mm <enabled/disabled> <days to repeat>'
        e.g. 'add 9 00 enabled Mon Fri'
            'add 10 30 disabled sat sun'
            'add 7 10 enabled all'
            'add 22 55 disabled'
        """
        words = alarm_str.split(' ')
        # First check for enough items
        if len(words) < 2:
            print('Not enough data provided, for information about this ' +
                  'command use the "help add"\ncommand !')
            return

        # First word is the hour, mandatory
        try:
            hour = int(words[0])
        except ValueError:
            print('First item must be a number indicating the time !')
            return

        # Second word is the minute, mandatory
        try:
            minute = int(words[1])
        except ValueError:
            print('First item must be a number indicating the time !')
            return

        # Third word is the enable, optional
        if len(words) > 2:
            if words[2].lower() == 'enable' or words[2].lower() == 'enabled':
                enable = True
            elif words[2].lower() == 'disable' or \
                    words[2].lower() == 'disabled':
                enable = False
            else:
                print('Third item must indicate if the alarm will be ' +
                      '"enable" or "disabled" !')
                return
        else:
            # Defaults to enabled
            enable = True

        # Following words are the repeat days, optional
        if len(words) > 3:
            if words[3].lower() == 'all':
                repeats = (True, True, True, True, True, True, True)
            elif words[3].lower() == 'none':
                repeats = (False, False, False, False, False, False, False)
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
                        print(('Repeat day "%s" not recognised,' % words[i+3]) +
                              ' use the "help add" command for more info !')
                        return
        else:
            # Defaults to all days enabled
            repeats = (True, True, True, True, True, True, True)

        # Create the alarm and inform the user
        alarm_id = self.alarm_mgr.add_alarm(hour, minute, repeats, enable)
        if alarm_id is not None:
            self.display_alarms()
            print('Created Alarm:\n' + AlarmCli.dashes_line +
                  '\n%s' % AlarmManager.get_alarm(alarm_id))
        else:
            print('There was a problem creating the alarm.')

    def do_edit(self, edit_str):
        """Help edit command:
        Edit an alarm using the following format:
        'edit <alarm ID> <attribute> <new value>'
        e.g. 'edit 3 hour 9'
            'edit 4 minute 30'
            'edit 7 enabled no'
            'edit 1 repeat mon fri'
        """
        words = edit_str.split(' ')
        # First check for enough items
        if len(words) < 3:
            print('Not enough data provided, for information about this ' +
                  'command use the "help edit"\ncommand !')
            return

        # First word is the Alarm ID
        try:
            alarm_id = int(words[0])
        except ValueError:
            print('First item must be a the ID number of the alarm to edit!')
            return

        # Capture the original alarm, to check if it exits and later comparison
        original_alarm = self.alarm_mgr.get_alarm(alarm_id)
        if original_alarm is None:
            self.display_alarms()
            print('The Alarm with ID %s could not be found !' % alarm_id)
            return

        # Second word is the attribute to change, the third word parsed
        # immediately after each second word option.
        # Hours
        if words[1].lower() == 'hour' or words[2] == 'hours':
            try:
                hour = int(words[2])
            except ValueError:
                self.display_alarms()
                print('To edit the hour it must be followed a valid number !')
                return
            self.alarm_mgr.edit_alarm(alarm_id, hour=hour)
        # Minutes
        elif words[1].lower() == 'minute' or words[2] == 'minutes':
            try:
                minute = int(words[2])
            except ValueError:
                print('To edit the minute it must be followed a valid number !')
                return
            self.alarm_mgr.edit_alarm(alarm_id, minute=minute)
        # Enable
        elif words[1].lower() == 'enable' or words[1] == 'enabled':
            if words[2].lower() == 'yes':
                self.alarm_mgr.edit_alarm(alarm_id, enabled=True)
            elif words[2].lower() == 'no':
                self.alarm_mgr.edit_alarm(alarm_id, enabled=False)
            else:
                print('To edit the enable it must be followed by "yes" or ' +
                      '"No" !')
                return
        # Disable (should not really be an option, but accepted)
        elif words[1].lower() == 'disable' or words[1] == 'disabled':
            if words[2].lower() == 'yes':
                self.alarm_mgr.edit_alarm(alarm_id, enabled=False)
            elif words[2].lower() == 'no':
                self.alarm_mgr.edit_alarm(alarm_id, enabled=True)
            else:
                print('To edit the enable it must be followed by "yes" or ' +
                      '"No" !')
                return
        # Label
        elif words[1].lower() == 'label':
            label_str = ' '.join(str(x) for x in words[2:])
            self.alarm_mgr.edit_alarm(alarm_id, label=label_str)
        # Days
        elif words[1].lower() == 'repeat':
            if words[2].lower() == 'all':
                repeats = (True, True, True, True, True, True, True)
            elif words[2].lower() == 'none':
                repeats = (False, False, False, False, False, False, False)
            else:
                repeats = [False] * 7
                for i in xrange(len(words[2:])):
                    if words[i+2].lower() == 'mon':
                        repeats[0] = True
                    elif words[i+2].lower() == 'tue':
                        repeats[1] = True
                    elif words[i+2].lower() == 'wed':
                        repeats[2] = True
                    elif words[i+2].lower() == 'thu':
                        repeats[3] = True
                    elif words[i+2].lower() == 'fri':
                        repeats[4] = True
                    elif words[i+2].lower() == 'sat':
                        repeats[5] = True
                    elif words[i+2].lower() == 'sun':
                        repeats[6] = True
                    else:
                        print(('Repeat day "%s" not recognised,' % words[i+2]) +
                              ' use the "help edit" command for more info !')
                        return
            self.alarm_mgr.edit_alarm(alarm_id, days=repeats)
        else:
            # Invalid keyword
            print('Incorrect data provided, for information about this ' +
                  'command use the "help edit"\ncommand !')
            return

        # If this point has been reached, a success edit has been carried
        self.display_alarms()
        new_alarm = self.alarm_mgr.get_alarm(alarm_id)
        print(('Edited Alarm %s:\n' % alarm_id) + AlarmCli.dashes_line +
              ('\nOriginal:\n%s\n              | label: %s\n' %
               (original_alarm, original_alarm.label)) +
              ('\nNew:\n%s\n              | label: %s' %
               (new_alarm, new_alarm.label)))

    def do_delete(self, alarm_id_string):
        """
        Delete an alarm identified by its id, or all the alarms. E.g.:
        'delete 3'
        'delete all'
        """
        if alarm_id_string == 'all':
            success = self.alarm_mgr.delete_all_alarms()
            if success is True:
                print('All alarms have been deleted !')
        else:
            try:
                alarm_id = int(alarm_id_string)
            except ValueError:
                self.display_alarms()
                print('After "delete" there must be a number indicating ' +
                      'the Alarm ID to be deleted !')
                return
            alarm_string = str(AlarmManager.get_alarm(alarm_id))
            success = self.alarm_mgr.delete_alarm(alarm_id)
            if success is True:
                self.display_alarms()
                print('Alarm ID %s has been deleted:\n' % alarm_id +
                      AlarmCli.dashes_line + '\n%s' % alarm_string)

        if not success:
            self.display_alarms()
            print('Alarm/s "%s" could not be deleted.' % alarm_id_string)

    #
    # Settings command methods
    #
    def do_snooze(self, new_snooze_str):
        """Help snooze:
        Displays the currently set snooze time, or if accompanied by an integer
        it will change the snooze time and display the new value. E.g.:
        'snooze'
        'snooze 5'
        """
        snooze_text = 'Snooze time is:'
        if new_snooze_str:
            try:
                snooze_time = int(new_snooze_str)
            except ValueError:
                print('To edit the snooze time, the snooze command must be '
                      'followed a valid number !')
                return
            snooze_text = 'New snooze time is:'
            self.alarm_mgr.set_snooze_time(snooze_time)

        self.display_alarms()
        print(snooze_text + ' %s' % self.alarm_mgr.get_snooze_time())

    def do_prealert(self, new_prealert_str):
        """Help prealert:
        Displays the currently set pre-alert time, (time before the alarm alert
        is triggered and used to launch any kind of process), or if accompanied
        by an integer it will change the pre-alert time and display the new
        value. E.g.:
        'prealert'
        'prealert 5'
        """
        prealert_text = 'Pre-alert time is:'
        if new_prealert_str:
            try:
                new_prealert_str = int(new_prealert_str)
            except ValueError:
                print('To edit the pre-alert time, the prealert command must be'
                      'followed a valid number !')
                return
            prealert_text = 'New pre-alert time is:'
            self.alarm_mgr.set_prealert_time(new_prealert_str)

        self.display_alarms()
        print(prealert_text + ' %s' % self.alarm_mgr.get_prealert_time())

    #
    # General command methods
    #
    def do_exit(self, empty_str):
        """ Exists the LightUp Alarm program. """
        self.display_alarms()
        return True

    #
    # Command line interface methods
    #
    def show_header_only(self):
        """
        Clears the screen and displays the application header with next alarm.
        :return: All outputs for this method go straight to the stdout.
        """
        # First cleat the screen
        if os.name == 'nt':
            os.system("cls")
        else:
            os.system('clear')

        # Then print the header
        empty_line = '=                                       ' + \
                     '                                       =\n'
        print('========================================' +
              '========================================\n' + empty_line +
              '=                              LightUpPi' +
              ' Alarm                                 =')
        # If there are active alarms, print the next schedule time to alert
        next_alarm = self.alarm_mgr.get_next_alarm()
        if next_alarm is not None:
            print(empty_line + AlarmCli.dashes_line + '\n' + empty_line +
                  '=                   Next scheduled alert'
                  ' is for Alarm ID %3d                   =' % next_alarm.id_)
        print(empty_line + AlarmCli.dashes_line + '\n' + empty_line +
              '=    Use the "help" command for informat' +
              'ion about how to use this program.     =\n' +
              '=    This program must remain open for t' +
              'he alarms to be active and running.    =\n' + empty_line +
              '========================================' +
              '========================================')

        print('\n')  # Empty line for visual spacing

    def display_alarms(self):
        """
        Displays all the current alarms.
        :return: All outputs for this method go straight to the stdout
        """
        # And finally, display the alarms below the header
        all_alarms = self.alarm_mgr.get_all_alarms()
        print('All Alarms:\n' + AlarmCli.dashes_line)
        if not all_alarms:
            print('\tThere are not saved alarms.')
        else:
            for alarm in all_alarms:
                print(alarm)
        print('\n')  # Empty line for visual spacing

    #
    # callback method
    #
    def alarm_callback(self):
        """
        This is the command line interface Alarm Alert function. It will be
        executed every time an alarm alert is triggered.
        """
        # Try to prevent re-entry
        while self.callback_running is True:
            time.sleep(float(random.randint(1, 100)) / 1000.0)
        # Should be safe now
        self.callback_running = True
        print('\n\nRING RING RING!!!!')
        print('\a')  # Request terminal to beep
        time.sleep(0.8)
        print('\a')  # Request terminal to beep
        time.sleep(0.8)
        print('\a')  # Request terminal to beep
        if self.callback is not None:
            self.callback()
        # print without a new line, using sys to work on python 2 and 3
        sys.stdout.flush()
        sys.stdout.write('\n%s' % self.prompt)
        self.callback_running = False
