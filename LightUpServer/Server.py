#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Server component from the LightUpServer package.
#
# Copyright (c) 2015 carlosperate http://carlosperate.github.io
#
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
# Longer description.
#
from __future__ import unicode_literals, absolute_import
import os
import datetime
import logging
from flask import Flask
from flask import Response
from flask import request, redirect, jsonify, render_template, \
    send_from_directory
try:
    from LightUpServer.ServerAlarmAdapter import ServerAlarmAdapter
except ImportError:
    from ServerAlarmAdapter import ServerAlarmAdapter


# Creating flask instance
flask_server = Flask(__name__, static_url_path='/LightUpPi')

# Uninitialised AlarmManager instance
alarm_adapt = None

# Callback function to be executed every time there is an alarm change
callback_func = None


def callback():
    if callback_func is not None:
        callback_func()


@flask_server.route('/')
def root_index_redirect():
    """ Redirects the LightUpPi dir directly to /LightUpPi/ """
    return redirect('/LightUpPi/', code=302)


@flask_server.route('/LightUpPi/')
def lightuppi_index_redirect():
    """ Redirects the LightUpPi dir directly to index.html """
    return send_from_directory(
        flask_server.static_folder, 'index.html')


@flask_server.route('/LightUpPi/ping')
def ping_test():
    """
    This is used to check if the server is up and accessible, almost like a
    ping.
    :return: Empty string with a 200 response.
    """
    return ''

@flask_server.route('/LightUpPi/templateTest')
def template_test():
    """
    This is for the main.html static page entry point.
    :return: html page from the templates folder.
    """
    now = datetime.datetime.now()
    timeString = now.strftime('%Y-%m-%d %H:%M')
    templateData = {
        'title': 'HELLO!',
        'time': timeString
    }
    return render_template('main.html', **templateData)


@flask_server.route('/LightUpPi/getAlarm', methods=['GET'])
def get_alarm():
    callback()
    global alarm_adapt
    message = {'error': 'The \'id\' argument is required for \'getAlarm\''}
    alarm_id = request.args.get('id')
    if alarm_id is not None:
        if alarm_id == 'all':
            # /LightUpPi/getAlarm?id=all
            json_response = alarm_adapt.json_get_all_alarms()
            return Response(json_response,  mimetype='application/json')
        else:
            # /LightUpPi/getAlarm?id=<alarm_id>
            try:
                alarm_id = int(alarm_id)
                json_response = alarm_adapt.json_get_alarm(int(alarm_id))
                return Response(json_response,  mimetype='application/json')
            except ValueError:
                message['error'] = 'The \'id\' argument has to be an integer'

    # At this point credentials were invalid or request method was not GET
    return jsonify(message)


@flask_server.route('/LightUpPi/addAlarm', methods=['GET'])
def add_alarm():
    """
    Adding an alarm to the database and launching it if active.
    The hour and minute arguments are mandatory and the others are optional.
    The full request is:
    /LightUpPi/addAlarm?hour=<>&minute=<>&monday=<>&tuesday=<>&wedneday=<>
        &thursday=<>&friday=<>&saturday=<>&sunday=<>&enabled=<>&label=<>
        &timestamp=<>
    :return: JSON string with response data indicating success of operation.
    """
    global alarm_adapt

    # Parsing the hour argument, if not present or wrong return error message
    hour = request.args.get('hour')
    if hour is None:
        message = {'error': 'The \'hour\' argument is required to add alarm'}
        return jsonify(message)
    else:
        try:
            hour = int(hour)
        except ValueError:
            message = {'error': 'The \'hour\' argument must be an integer'}
            return jsonify(message)

    # Parsing the minute argument, if not present or wrong return error message
    minute = request.args.get('minute')
    if minute is None:
        message = {'error': 'The \'minute\' argument is required to add alarm'}
        return jsonify(message)
    else:
        try:
            minute = int(minute)
        except ValueError:
            message = {'error': 'The \'minute\' argument must be an integer'}
            return jsonify(message)

    def check_boolean(arg_str):
        """
        Internal function to simplify boolean arguments parsing.
        Set to True by default.
        """
        arg_value = request.args.get(arg_str)
        if arg_value is None:
            parse_success = True
            return_value = True
        elif arg_value.lower() in ("true", "yes", "enabled"):
            parse_success = True
            return_value = True
        elif arg_value.lower() in ("false", "no", "disabled"):
            parse_success = True
            return_value = False
        else:
            parse_success = False
            return_value = 'The \'%s\' argument has to be a bool' % arg_str
        return parse_success, return_value

    # Parsing the weekdays
    success, monday = check_boolean("monday")
    if success is False:
        return jsonify({'error': monday})
    success, tuesday = check_boolean("tuesday")
    if success is False:
        return jsonify({'error': tuesday})
    success, wednesday = check_boolean("wednesday")
    if success is False:
        return jsonify({'error': wednesday})
    success, thursday = check_boolean("thursday")
    if success is False:
        return jsonify({'error': thursday})
    success, friday = check_boolean("friday")
    if success is False:
        return jsonify({'error': friday})
    success, saturday = check_boolean("saturday")
    if success is False:
        return jsonify({'error': saturday})
    success, sunday = check_boolean("sunday")
    if success is False:
        return jsonify({'error': sunday})

    # Parsing the enabled argument, if not present or wrong return error message
    success, enabled = check_boolean("enabled")
    if success is False:
        return jsonify({'error': enabled})

    # Parsing the label argument
    label = request.args.get('label')
    if label is None:
        label = ''

    # Parsing the timestamp argument, if wrong data type return error
    timestamp = request.args.get('timestamp')
    if timestamp is not None:
        try:
            timestamp = long(timestamp)
        except ValueError:
            message = {'error': 'The \'timestamp\' argument must be an integer'}
            return jsonify(message)

    # At this point all arguments should be correct
    json_response = alarm_adapt.json_add_alarm(
        hour, minute, enabled=enabled, label=label, timestamp=timestamp,
        days=(monday, tuesday, wednesday, thursday, friday, saturday, sunday))
    return Response(json_response, mimetype='application/json')


@flask_server.route('/LightUpPi/editAlarm', methods=['GET'])
def edit_alarm():
    """
    Edit an alarm to the database and launching it if active.
    The id arguments is mandatory and the others are optional.
    The full possible request is:
    /LightUpPi/addAlarm?id=<>&hour=<>&minute=<>&monday=<>&tuesday=<>
        &wedneday=<>&thursday=<>&friday=<>&saturday=<>&sunday=<>&enabled=<>
        &label=<>
    :return: JSON string with response data indicating success of operation.
    """
    global alarm_adapt

    # Parsing the id argument, if not present or wrong return error message
    id_ = request.args.get('id')
    if id_ is None:
        message = {'error': 'The \'id\' argument is required to edit alarm'}
        return jsonify(message)
    else:
        try:
            id_ = int(id_)
        except ValueError:
            message = {'error': 'The \'id\' argument must be an integer'}
            return jsonify(message)

    # Parsing the hour argument
    hour = request.args.get('hour')
    if hour is not None:
        try:
            hour = int(hour)
        except ValueError:
            message = {'error': 'The \'hour\' argument must be an integer'}
            return jsonify(message)

    # Parsing the minute argument
    minute = request.args.get('minute')
    if minute is not None:
        try:
            minute = int(minute)
        except ValueError:
            message = {'error': 'The \'minute\' argument must be an integer'}
            return jsonify(message)

    def check_boolean(arg_str):
        """ Internal function to simplify boolean arguments parsing. """
        return_value = request.args.get(arg_str)
        parse_success = True
        if return_value is not None:
            if return_value.lower() in ("true", "yes", "enabled"):
                parse_success = True
                return_value = True
            elif return_value.lower() in ("false", "no", "disabled"):
                parse_success = True
                return_value = False
            else:
                parse_success = False
                return_value = 'The \'%s\' argument has to be a bool' % arg_str
        return parse_success, return_value

    # Parsing the weekdays
    success, monday = check_boolean("monday")
    if success is False:
        return jsonify({'error': monday})
    success, tuesday = check_boolean("tuesday")
    if success is False:
        return jsonify({'error': tuesday})
    success, wednesday = check_boolean("wednesday")
    if success is False:
        return jsonify({'error': wednesday})
    success, thursday = check_boolean("thursday")
    if success is False:
        return jsonify({'error': thursday})
    success, friday = check_boolean("friday")
    if success is False:
        return jsonify({'error': friday})
    success, saturday = check_boolean("saturday")
    if success is False:
        return jsonify({'error': saturday})
    success, sunday = check_boolean("sunday")
    if success is False:
        return jsonify({'error': sunday})

    alarm_repeat = None
    if any([monday, tuesday, wednesday, thursday, friday, saturday, sunday]):
        alarm_repeat = list(alarm_adapt.get_alarm_repeat(id_))
        if monday is not None:
            alarm_repeat[0] = monday
        if tuesday is not None:
            alarm_repeat[1] = tuesday
        if wednesday is not None:
            alarm_repeat[2] = wednesday
        if thursday is not None:
            alarm_repeat[3] = thursday
        if friday is not None:
            alarm_repeat[4] = friday
        if saturday is not None:
            alarm_repeat[5] = saturday
        if sunday is not None:
            alarm_repeat[6] = sunday

    # Parsing the enabled argument, if wrong return error message
    success, enabled = check_boolean("enabled")
    if success is False:
        return jsonify({'error': enabled})

    # Parsing the label argument
    label = request.args.get('label')

    # At this point all arguments should be correct
    json_response = alarm_adapt.json_edit_alarm(
        alarm_id=id_, hour=hour, minute=minute, enabled=enabled, label=label,
        days=alarm_repeat)
    return Response(json_response, mimetype='application/json')


@flask_server.route('/LightUpPi/deleteAlarm', methods=['GET'])
def delete_alarm():
    global alarm_adapt
    message = {'error': 'The \'id\' argument is required for \'deleteAlarm\''}
    alarm_id = request.args.get('id')
    if alarm_id is not None:
        if alarm_id == 'all':
            # /LightUpPi/getAlarm?id=all
            json_response = alarm_adapt.json_delete_all_alarms()
            return Response(json_response,  mimetype='application/json')
        else:
            # /LightUpPi/getAlarm?id=<alarm_id>
            try:
                alarm_id = int(alarm_id)
                json_response = alarm_adapt.json_delete_alarm(int(alarm_id))
                return Response(json_response,  mimetype='application/json')
            except ValueError:
                message['error'] = 'The \'id\' argument has to be an integer'

    # At this point credentials were invalid or request method was not GET
    return jsonify(message)


def run(alarm_mgr_arg, silent=False, callback_arg=None):
    global alarm_adapt, callback_func
    alarm_adapt = ServerAlarmAdapter(alarm_mgr_arg)
    callback_func = callback_arg

    # Set up logging
    if silent is True:
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

    # Setting the static folder
    static_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
        'LightUpWeb')
    global flask_server
    flask_server.static_folder = static_dir

    # Run flask
    flask_server.run(host='0.0.0.0', port=80, debug=False)
