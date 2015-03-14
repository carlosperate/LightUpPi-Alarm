#!/usr/bin/env python2
#
# Short description
#
# Copyright (c) 2015 carlosperate https://github.com/carlosperate/
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
# Full description goes here
#
from __future__ import unicode_literals, absolute_import, print_function
import sys
import time
import operator
from LightUpAlarm.AlarmDb import AlarmDb
from LightUpAlarm.AlarmItem import AlarmItem
from LightUpAlarm.AlarmThread import AlarmThread


class AlarmManager(object):
    """
    .
    """

    #
    # constructor
    #
    def __init__(self, alarm_callback=None):
        """
        On initialization we connect to the database and check if there are
        any alarms to load. If not, load a couple of dummy alarms.
        It also registers any alarms present in the database.
        :param alarm_callback: Optional argument to register a callback function
                               to be executed on an alarm alert.
        """
        # Save the alarm callback function as a private member variable
        self.__alarm_callback = alarm_callback
        # Create a private member list for the alarm threads
        self.__alarm_threads = []

        # Set dummy alarms if database empty
        if AlarmDb().get_number_of_alarms() == 0:
            self.load_dummy_alarms()

        # Register any enabled alarms from the database
        alarms = AlarmManager.get_all_enabled_alarms()
        for alarm in alarms:
            self.__set_alarm_thread(alarm)

    #
    # static methods to retrieve alarms
    #
    @staticmethod
    def get_all_alarms():
        """
        Static method, gets all the alarms from the database.
        :return: List of AlarmItems containing all alarms. Returns an empty list
                 if there aren't any.
        """
        return AlarmDb().get_all_alarms()

    @staticmethod
    def get_number_of_alarms():
        """
        Gets the number of alarms stored in the database.
        :return: Integer indicating the number of alarms in the db.
        """
        return AlarmDb().get_number_of_alarms()

    @staticmethod
    def get_all_enabled_alarms():
        """
        Gets all the enabled alarms from the database.
        :return: List of AlarmItems containing all enabled alarms. Returns an
                 empty list if there aren't any.
        """
        return AlarmDb().get_all_enabled_alarms()

    @staticmethod
    def get_alarm(alarm_id):
        """
        Get the alarm with the given ID from the database.
        :param alarm_id: Integer to indicate the primary key of the Alarm to get.
        :return: AlarmItem with the alarm data, or None if id could not be found.
        """
        return AlarmDb().get_alarm(alarm_id)

    @staticmethod
    def get_next_alarm():
        """
        Gets the current time and all the active alarms. For each of these
        alarms it calculates the elapsed time that will pass for its next alert.
        Then it sorts the list based on this value and returns closes.
        :return: AlarmItem of the next alarm to alert.
        """
        # now_time[3] = tm_hour, now_time[4] = tm_minute, now_time[6] = tm_wday
        now_time = time.localtime(time.time())

        all_alarms = AlarmManager.get_all_enabled_alarms()
        if len(all_alarms) > 0:
            for alarm in all_alarms:
                alarm.next_alert = alarm.minutes_to_alert(
                    now_time[3], now_time[4], now_time[6])
            sorted_alarms = sorted(
                all_alarms, key=operator.attrgetter('next_alert'))
            return sorted_alarms[0]
        else:
            return None

    #
    # member methods to add alarms
    #
    def add_alarm(self, hour, minute,
                  days=(False, False, False, False, False, False, False),
                  enabled=True):
        """
        Adds an alarm to the database with the input values.
        If saved successfully it is sent to __set_alarm_thread to see if it
        should be launched as an enabled alarm thread.
        :param hour: Integer to indicate the alarm hour.
        :param minute: Integer to indicate the alarm minute.
        :param days: 7-item list of booleans to indicate repeat weekdays.
        :param enabled: Boolean to indicate the alarm enabled state.
        :return: Boolean indicating the success of the 'edit' operation.
        """
        alarm = AlarmItem(hour, minute, days, enabled)
        alarm.id_ = AlarmDb().add_alarm(alarm)
        if alarm.id_ is not None:
            self.__set_alarm_thread(alarm)
            return True
        else:
            return False

    def load_dummy_alarms(self):
        """
        It loads 2 inactive dummy alarms into the database for demonstration
        purposes.
        """
        self.add_alarm(
            07, 10, (True, True, True, True, True, False, False), False)
        self.add_alarm(
            10, 30, (False, False, False, False, False, True, True), False)

    #
    # member methods to edit alarms
    #
    def edit_alarm(self, alarm_id, hour=None, minute=None, days=None,
                   enabled=None):
        """
        Edits an alarm from the database with the input data.
        It then
        Returns success status of the operation.
        :param hour: Integer to indicate the alarm hour.
        :param minute: Integer to indicate the alarm minute.
        :param days: 7-item list of booleans to indicate repeat weekdays.
        :param enabled: Boolean to indicate alarm enabled state.
        :return: Boolean indicating the success of the 'edit' operation.
        """
        success = True
        db = AlarmDb()
        # Parse optional parameters
        if hour is not None:
            individual_success = db.edit_alarm(alarm_id, hour=hour)
            if not individual_success:
                success = False
        # Parse minute variable
        if minute is not None:
            individual_success = db.edit_alarm(alarm_id, minute=minute)
            if not individual_success:
                success = False
        # Parse days variable
        if days is not None:
            individual_success = db.edit_alarm(alarm_id, days=days)
            if not individual_success:
                success = False
        # Parse enabled variable
        if enabled is not None:
            individual_success = db.edit_alarm(alarm_id, enabled=enabled)
            if not individual_success:
                success = False

        # If a successful edit was carried, then make sure the alarm is launched
        if success is True:
            self.__set_alarm_thread(AlarmManager.get_alarm(alarm_id))

        return success

    def delete_alarm(self, alarm_id):
        """
        Remove the alarm with the given ID from the database and remove its
        alarm thread.
        :param alarm_id: Integer to indicate the primary key of the Alarm to be
                         removed.
        :return: Boolean indicating the success of the 'delete alarm' operation.
        """
        # First we need to ensure it there is no alarm thread running for it
        self.__stop_alarm_thread(alarm_id)
        # Remove it from the database
        return AlarmDb().delete_alarm(alarm_id)

    def delete_all_alarms(self):
        """
        Removes all alarm threads and alarms from the database.
        :return: Boolean indicating the success of the 'delete all' operation.
        """
        # Ensure there are no alarm threads running anymore
        thread_success = self.__stop_all_alarm_threads()
        # Remove from database
        db_success = AlarmDb().delete_all_alarms()

        if thread_success is True and db_success is True:
            return True
        else:
            return False

    #
    # member methods to launch, edit and stop alarm events
    #
    def __set_alarm_thread(self, alarm):
        """
        Takes an input alarm and determines if is active, in order to be
        launched as an alarm thread, or if a thread should be changed due to
        the new alarm data.
        :param alarm: AlarmItem to launch, edited, or stop thread.
        :return: Boolean indicating if Alarm Thread is running.
        """
        thread_up = False
        # First check if the alarm to be register is already in the list
        for i, alarm_thread in enumerate(self.__alarm_threads):
            if alarm.id_ == alarm_thread.get_id():
                # Already set as launched, check if should be stopped or edited
                if (not alarm.enabled) or (not alarm.any_enabled_day()):
                    self.__stop_alarm_thread(alarm.id_)
                else:
                    alarm_thread.edit_alarm(alarm)
                    # It is meant to be up and running, check that it is
                    if alarm_thread.isAlive() is False:
                        self.__alarm_threads[i] = \
                            AlarmThread(alarm, self.__alarm_triggered)
                        self.__alarm_threads[i].start()
                    thread_up = alarm_thread.isAlive()
                break
        # Else only executes if no alarm with same ID was found
        else:
            # Before thread is launched, check if the alarm is active and has
            # repeat days selected
            if (alarm.enabled is True) and (alarm.any_enabled_day() is True):
                alarm_thread = AlarmThread(alarm, self.__alarm_triggered)
                self.__alarm_threads.append(alarm_thread)
                alarm_thread.start()
                thread_up = alarm_thread.isAlive()

        return thread_up

    def __stop_alarm_thread(self, alarm_id):
        """
        Stops an AlarmThread and removes item from the threads list.
        This method can take up to 10 seconds to run.
        :param alarm_id: ID of the AlarmItem for the alarm thread to stop.
        :return: Boolean indicating if the operation was successful.
        """
        success = False
        for alarm_thread in self.__alarm_threads:
            if alarm_id == alarm_thread.get_id():
                alarm_thread.stop()
                # Check that it has really stopped for a maximum period of 10s
                milliseconds_passed = 0
                while alarm_thread.isAlive() and (milliseconds_passed < 10000):
                    time.sleep(0.01)
                    milliseconds_passed += 10
                # isAlive returns False if it has stopped
                success = not alarm_thread.isAlive()
                if success is True:
                    self.__alarm_threads.remove(alarm_thread)
        return success

    def __stop_all_alarm_threads(self):
        """
        Stops all AlarmThreads and removes items from the threads list.
        This method can take up to 15 seconds to run.
        :return: Boolean indicating if the operation was successful.
        """
        for alarm_thread in self.__alarm_threads:
            alarm_thread.stop()

        # Check that all threads have really stopped for a maximum period of 15s
        milliseconds_passed = 0
        continue_trying = True
        while continue_trying and (milliseconds_passed < 15000):
            continue_trying = False
            # Need to iterate backwards in order to remove items safely
            for i in xrange(len(self.__alarm_threads) - 1, -1, -1):
                if self.__alarm_threads[i].isAlive() is True:
                    continue_trying = True
                else:
                    del self.__alarm_threads[i]
            time.sleep(0.01)
            milliseconds_passed += 10

        if self.__alarm_threads:
            return False
        else:
            return True

    def is_alarm_running(self, alarm_id):
        """
        Checks if the given alarm ID is running as a thread.
        :param alarm_id: ID of the AlarmItem for the alarm thread to check.
        :return:
        """
        for alarm_thread in self.__alarm_threads:
            if alarm_thread.get_id() == alarm_id:
                return alarm_thread.isAlive()
        return False

    def check_threads_state(self):
        """
        Retrieves all the alarms and checks if the are running or not as they
        should. Tries to correct any possible errors, and if it can't it prints
        an error into stderr.
        :return: Boolean indicating if everything was running correctly before
                 the method was called.
        """
        previously_correct = True
        running_counter = 0
        all_alarms = AlarmManager.get_all_alarms()
        for alarm in all_alarms:
            if alarm.enabled is True and alarm.any_enabled_day() is True:
                # This alarm should be running
                running_counter += 1
                if self.is_alarm_running(alarm.id_) is False:
                    self.__set_alarm_thread(alarm)
                    previously_correct = False
            else:
                # This alarm should not be running
                if self.is_alarm_running(alarm.id_) is True:
                    self.__stop_alarm_thread(alarm.id_)
                    previously_correct = False

        # Check we have as many threads as expected
        if len(self.__alarm_threads) != running_counter:
            previously_correct = False
            # We can only attempt to recover if there are extra threads not
            # meant to be running
            for alarm_thread in self.__alarm_threads:
                for alarm in all_alarms:
                    if alarm.id_ == alarm_thread.get_id():
                        break
                else:
                    self.__stop_alarm_thread(alarm_thread.get_id())

            if len(self.__alarm_threads) != running_counter:
                print('ERROR: Could not correct the alarm threads in' +
                      'AlarmManager().check_threads_state !',
                      file=sys.stderr)

        return previously_correct

    #
    # other member methods
    #
    def __alarm_triggered(self):
        """
        This method is sent as a callback to each Alarm threads. It is meant to
        be executed when the alarm alert is raised.
        It executes the callback indicated on AlertManger constructor.
        :return:
        """
        # run AlertManager callback event
        if self.__alarm_callback is not None:
            self.__alarm_callback()
            print('This is an alarm ALERT!!! ')


if __name__ == "__main__":
    # Do nothing
    pass
