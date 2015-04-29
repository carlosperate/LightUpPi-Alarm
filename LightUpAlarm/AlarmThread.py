#!/usr/bin/env python2
#
# Class to have alarms running on their own threads.
#
# Copyright (c) 2015 carlosperate http://carlosperate.github.io
#
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
    running checks the time every 5 seconds to determine if the Alarm (or any
    pre or post alert) should be triggered.

    This class does NOT edit the variables from the AlarmItem instance reference
    that it takes as constructor parameter. It does attach a callback function
    reference for the alert trigger in this thread, and it only uses the class
    instance data to determine if the alarm is meant to be trigger or not.

    If it reads old data while it is being modified by AlarmManger, it will read
    the new correct version at the next infinite loop iteration and not cause a
    problem.

    It is for this reason that locks are not required for the AlarmItem data or
    the __run private variable (modifiable by the externally accessible stop()
    method).
    """

    # This class variable blocks any alarm thread to execute the callback while
    # it is already running. This is because the callback is most likely to be
    # controlling hardware
    __alert_running = False

    #
    # metaclass methods
    #
    def __init__(self, alarm_item, alarm_callback=None, offset_alarm_time=None,
                 offset_callback=None):
        """
        AlarmThread initialiser. Takes an AlarmItem instance, a callback
        function and a pre or post alert time and callback to initialise the
        member variables.
        :param alarm_item: AlarmItem instance.
        :param alarm_callback: Callback function to execute when alarm triggers.
        :para offset_alarm_time: Indicates if a pre or post alarm alert shall
                                 be triggered. Input sanitation done at
                                 Alar.diff_alarm()
        :param offset_callback: If the offset_alarm_time is set, it will
                                execute this callback on the pre or post alert.
        """
        threading.Thread.__init__(self)
        self.daemon = True

        self.__alarm = alarm_item
        self.__id = self.__alarm.id_
        # Attach the callback to the alarm object for easy storage
        self.__alarm_callback = alarm_callback

        # Create a pre/post alarm alert. This is an alarm, not saved anywhere,
        # offset_alarm_time the same data as alarm_item except for a time offset
        # (in minutes)
        self.__offset_flag = False
        if offset_alarm_time is not None:
            self.__offset_time = offset_alarm_time
            self.__offset_callback = offset_callback
            self.__offset_alarm = self.__alarm.diff_alarm(self.__offset_time)
            if self.__offset_alarm is not None:
                self.__offset_flag = True

        self.__run = True

    #
    # control thread methods
    #
    def run(self):
        """
        Infinite loop function to run until it is stopped by calling the stop()
        method. It sleeps for 1 second between iterations.
        At each iteration it first determines if the alarm is enabled and set to
        trigger any day, if so it then checks if this time is the alarm time.
        """
        while self.__run:
            # Only check for the time if the Alarm is active
            if self.__alarm.is_active() is True:
                time_now = time.localtime(time.time())
                alert_triggered = False

                # Check if it is the alarm time
                if (self.__alarm.repeat[time_now.tm_wday] is True) and \
                        (self.__alarm.hour == time_now.tm_hour) and \
                        (self.__alarm.minute == time_now.tm_min):
                    self.alarm_alert(self.__alarm, self.__alarm_callback)
                    alert_triggered = True

                if self.__offset_flag is True:
                    # Sync and check if it is the pre/post alert time
                    self.sync_offset_alarm()
                    if (self.__offset_alarm.repeat[time_now.tm_wday] is True) \
                            and (self.__offset_alarm.hour == time_now.tm_hour) \
                            and (self.__offset_alarm.minute == time_now.tm_min):
                        self.alarm_alert(
                            self.__offset_alarm, self.__offset_callback)
                        alert_triggered = True

                if alert_triggered:
                    # Wait for the current minute to be over, in order to not
                    # execute the callback/s more than once
                    time_to_elapse = time_now
                    while (time_to_elapse.tm_hour == time_now.tm_hour) and \
                          (time_to_elapse.tm_min == time_now.tm_min):
                        time.sleep(1)
                        time_now = time.localtime(time.time())

            # Now just sleep for 5 seconds before checking again
            time.sleep(1)

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
        In most cases this will be unnecessary, as the input alarm is
        referencing the same instance, but there are cases where a new AlarmItem
        instance is created to represent the same alarm and this method needs
        to update the thread data.
        :param alarm_item: AlarmItem for the new Alarm instance.
        :return: Boolean indicating if the operation was successful.
        """
        # Only edit the alarm if it contains the same ID
        if alarm_item.id_ == self.__id == self.__alarm.id_:
            self.__alarm = alarm_item
            # Edit the offset alert if enabled
            if self.__offset_flag is True:
                self.__offset_alarm = \
                    self.__alarm.diff_alarm(self.__offset_time)
            success = True
        else:
            print('ERROR: Provided AlarmItem is not correct for this thread.\n'
                  + 'Provided Alarm ID: %s  |  Thread Alarm ID: %s !' %
                  (alarm_item.id_, self.__alarm.id_), file=sys.stderr)
            success = False
        return success

    def sync_offset_alarm(self):
        """
        This method will check if the alarm and the offset_alarm data are still
        the same. Required because the alarm instance can be edited outside of
        this class and the alarm data has to stay synchronised.
        This method edits the class member variable __offset_alarm directly.
        Doing these checks, instead of recreating the offset_alarm each time
        is about an order of magnitude faster.
        """
        if (self.__offset_alarm.hour != self.__alarm.hour) or \
                (self.__offset_alarm.minute != self.__alarm.minute) or \
                (self.__offset_alarm.repeat != self.__alarm.repeat) or \
                (self.__offset_alarm.enabled != self.__alarm.enabled):
            self.__offset_alarm = self.__alarm.diff_alarm(self.__offset_time)

    @classmethod
    def alarm_alert(cls, alarm_item, callback):
        """
        This method is executed when the alarm alert is raised.
        It executes the callback indicated on AlertThread constructor.
        """
        # Try to block reentry
        while cls.__alert_running is True:
            time.sleep(0.01)
        # Now should be safe to execute
        cls.__alert_running = True

        try:
            # run AlertManager callback event
            print('\nALERT for the Alarm %s, with label:"%s" !!!' %
                  (alarm_item.id_, alarm_item.label))
            if callback is not None:
                callback()
        finally:
            # Unblock
            cls.__alert_running = False
