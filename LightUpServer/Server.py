#!/usr/bin/env python2
#
# Server component from the LightUpServer package.
#
# Copyright (c) 2015 carlosperate https://github.com/carlosperate/
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
# Longer description.
#
from __future__ import unicode_literals, absolute_import
from flask import Flask
from flask import Response
from flask import request, redirect, jsonify, render_template, \
    send_from_directory, url_for
import datetime
import os
try:
    from LightUpServer.ServerAlarmAdapter import ServerAlarmAdapter
except ImportError:
    from ServerAlarmAdapter import ServerAlarmAdapter


# Creating flask instance
flask_server = Flask(__name__, static_url_path='/LightUpPi')

# Uninitialised AlarmManager instance
alarm_adapt = None


@flask_server.route('/')
def root_index_redirect():
    """ Redirects the LightUpPi dir directly to index.html """
    return redirect('/LightUpPi/', code=302)

@flask_server.route('/LightUpPi/')
def lightuppi_index_redirect():
    """ Redirects the LightUpPi dir directly to index.html """
    return send_from_directory(
        flask_server.static_folder, 'index.html')


@flask_server.route('/LightUpPi/test')
def template_test():
    """
    This is for the main.html static page entry point.
    :return:
    """
    now = datetime.datetime.now()
    timeString = now.strftime('%Y-%m-%d %H:%M')
    templateData = {
        'title' : 'HELLO!',
        'time': timeString
    }
    return render_template('main.html', **templateData)


@flask_server.route('/LightUpPi/alarms')
def get_all_alarms_json():
    global alarm_adapt
    alarms_json = alarm_adapt.json_get_all_alarms()
    return Response(alarms_json,  mimetype='application/json')


@flask_server.route('/LightUpPi/alarm', methods=['GET'])
def alarm_operations():
    global alarm_adapt
    message = {'message': 'nothing'}
    url_args = request.args.get('action')
    if url_args == 'get':
        alarm_id = int(request.args.get('id'))
        alarm_json = alarm_adapt.json_get_alarm(alarm_id)
        return Response(alarm_json,  mimetype='application/json')
    elif url_args == 'add':
        message['action'] = 'add'
    elif url_args == 'edit':
        message['action'] = 'edit'
    elif url_args == 'delete':
        message['action'] = 'delete'
    else:
        message['error'] = 'something'

    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return jsonify(message)
    #return Response(json.dumps(message),  mimetype='application/json')


def run(alarm_mgr_arg):
    global alarm_adapt
    alarm_adapt = ServerAlarmAdapter(alarm_mgr_arg)

    # Setting the static folder
    static_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
        'LightUpWeb')
    global flask_server
    flask_server.static_folder = static_dir

    # Run flask
    flask_server.run(host='0.0.0.0', port=80, debug=True)
