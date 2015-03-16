#!/usr/bin/env python2
#
# Class to have alarms running on their own threads.
#
# Copyright (c) 2015 carlosperate https://github.com/carlosperate/
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
# This file only contains a class definition, which description can be found in
# its docstring.
#
from __future__ import unicode_literals, absolute_import, print_function
import sys
import time
import threading


class AlarmThread(threading.Thread):
    """
    This thread class contains an instance to an AlarmItem and when it is
    running checks the time every 5 seconds to determine if the Alarm should be
    triggered.

    This class does NOT edit the AlarmItem instance it takes, it only uses its
    data to determine if the alarm is meant to be trigger or not. If it reads
    old data while it is being modified by AlarmManger, it will read the new
    correct version at the next infinite loop iteration and not cause a problem.
    It is for this reason that locks are not required for the AlarmItem data or
    the __run private variable (modifiable by the externally accessible stop()
    method).
    """
    #
    # metaclass methods
    #
    def __init__(self, alarm_item, alarm_callback=None):
        """
        AlarmThread constructor. Takes an AlarmItem instance and a callback
        function to initialise the member variables.
        :param alarm_item: AlarmItem instance.
        :param alarm_callback: Callback function to execute when alarm triggers.
        """
        threading.Thread.__init__(self)
        self.daemon = True

        self.__alarm = alarm_item
        self.__id = self.__alarm.id_
        self.__alarm_callback = alarm_callback
        self.alert_running = False
        self.__run = True

    #
    # control thread methods
    #
    def run(self):
        """
        Infinite loop function to run until it is stopped by calling the stop()
        method. It sleeps for 5 seconds between iterations.
        At each iteration it first determines if the alarm is enabled and set to
        trigger any day, if so it then checks if this time is the alarm time.
        """
        while self.__run:
            # Only check for the time if the Alarm is active
            if self.__alarm.is_active() is True:
                # Check if it is the alarm time
                time_now = time.localtime(time.time())
                if (self.__alarm.repeat[time_now.tm_wday] is True) and \
                   (self.__alarm.hour == time_now.tm_hour) and \
                   (self.__alarm.minute == time_now.tm_min):
                    self.alarm_alert()
                    # Wait for the current minute to be over, in order to not
                    # execute the callback more than once
                    while (self.__alarm.hour == time_now.tm_hour) and \
                          (self.__alarm.minute == time_now.tm_min):
                        time.sleep(1)
                        time_now = time.localtime(time.time())

            # Now just sleep for 5 seconds before checking again
            time.sleep(5)

            # debugging test
            #print('Alarm %s %s %02d:%02d | ' %
            #      (self.__alarm.id_, self.getName(), self.__alarm.hour,
            #       self.__alarm.minute))

    def stop(self):
        """
        Stops the infinite loop in run method and causes the thread to exit once
        the current operation finishes.
        """
        self.__run = False

    #
    # member methods
    #
    def get_id(self):
        """
        :return: The AlarmItem id, which is also used to identified this thread.
        """
        return self.__id

    def edit_alarm(self, alarm_item):
        """
        Edits the alarm instance to a new one, if the IDs are the same.
        This could be unnecessary, as the input alarm is probably referencing
        the same instance, but there could be a case where a new AlarmItem
        instance is created to represent the same alarm.
        :param alarm_item: AlarmItem for the new Alarm instance.
        :return: Boolean indicating if the operation was successful.
        """
        # Only edit the alarm if it contains the same ID
        if alarm_item.id_ == self.__id == self.__alarm.id_:
            self.__alarm = alarm_item
            success = True
        else:
            print('ERROR: Provided AlarmItem is not correct for this thread.\n'
                  + 'Provided Alarm ID: %s  |  Thread Alarm ID: %s !' %
                  (alarm_item.id_, self.__alarm.id_), file=sys.stderr)
            success = False
        return success

    def alarm_alert(self):
        """
        This method is executed when the alarm alert is raised.
        It executes the callback indicated on AlertThread constructor.
        """
        # Try to block reentry
        while self.alert_running is True:
            time.sleep(0.01)

        # Should be safe to execute
        self.alert_running = True
        # run AlertManager callback event
        print('\nThis is the Alarm %s ALERT !!!' % self.__alarm.id_)
        if self.__alarm_callback is not None:
            self.__alarm_callback()
        self.alert_running = False
