#!/usr/bin/python2
#
# Class to control a Belkin Wemo Switch.
#
# Copyright (c) 2015 carlosperate http://carlosperate.github.io
# Code partially based on "wee.py" Copyright (c) 2014 froyomuffin
#  https://github.com/froyomuffin/wee.py
#
# Licensed under The MIT License (MIT), a copy can be found in the LICENSE file
#
# A useful resource for the UPnP SOAP XML data:
#   https://objectpartners.com/2014/03/25/a-groovy-time-with-upnp-and-wemo/
#
import socket
from xml.dom import minidom
import xml.etree.ElementTree as et
try:
    from httplib import HTTPConnection
except ImportError:
    from http.client import HTTPConnection


class WemoSwitch(object):
    """ Sends and receives UPnP messages to a Belkin Wemo. """

    ERROR_STATE = -1

    #
    # UPnP SOAP XML strings to compose messages
    #
    body_top = """
    <?xml version="1.0" encoding="utf-8"?>
    <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
       <s:Body>
    """

    body_bottom = """
       </s:Body>
    </s:Envelope>
    """

    body_status = body_top + """
          <u:GetBinaryState xmlns:u="urn:Belkin:service:basicevent:1"></u:GetBinaryState>
    """ + body_bottom

    body_on = body_top + """
          <u:SetBinaryState xmlns:u="urn:Belkin:service:basicevent:1">
             <BinaryState>1</BinaryState>
             <Duration></Duration>
             <EndAction></EndAction>
             <UDN></UDN>
          </u:SetBinaryState>
    """ + body_bottom

    body_off = body_top + """
          <u:SetBinaryState xmlns:u="urn:Belkin:service:basicevent:1">
             <BinaryState>0</BinaryState>
             <Duration></Duration>
             <EndAction></EndAction>
             <UDN></UDN>
          </u:SetBinaryState>
    """ + body_bottom

    headers_bot = {
        "Content-Type": "text/xml; charset=\"utf-8\"",
        "Accept": "",
        "User-Agent": "",
        "Connection": "close"
    }

    headers_get = dict(
        list({"SOAPAction":
                  "\"urn:Belkin:service:basicevent:1#GetBinaryState\""}.items())
        + list(headers_bot.items()))

    headers_set = dict(
        list({"SOAPAction":
                  "\"urn:Belkin:service:basicevent:1#SetBinaryState\""}.items())
        + list(headers_bot.items()))

    #
    # metaclass methods
    #
    def __init__(self, server):
        """
        Creates an instance of the class and attempts to connected to the switch
        within the predefine port range.
        :param server: String with the IP of the Belkin Wemo Switch.
        """
        self.server = server
        self.connected = False
        self.port = 49151

        # Wemo ports can change, most user list ports in the range 49152-49155,
        # so do a quick connection check and rotate if it fails
        response_status = 0
        while response_status != 200 and self.port < 49156:
            self.port += 1
            conn = HTTPConnection(self.server, self.port, timeout=0.5)
            try:
                conn.request('GET', '/setup.xml')
                response = conn.getresponse()
                response_status = response.status
            except socket.timeout:
                #print('timeout port %s' % self.port)
                pass
        conn.close()

        # Check if the connection was successful and set it into self.connected
        if response_status == 200:
            self.connected = True
        else:
            self.connected = False
            self.port = WemoSwitch.ERROR_STATE

    def __request(self, body, headers):
        """
        Creates an HTTP post request to the Switch with the given body and
        headers.
        :param body: POST message body
        :param headers: POST message headers
        :return: Boolean ON state of the switch. Returns -1 for Error state.
        """
        conn = HTTPConnection(self.server, self.port)
        conn.request("POST", "/upnp/control/basicevent1", body, headers)
        response = conn.getresponse()
        state = WemoSwitch.ERROR_STATE
        if response.status == 200:
            # Parse the received XML and search for 'BinaryState' element
            tree = et.fromstring(response.read().decode("utf-8"))
            binary_state = tree.find('.//BinaryState')
            if binary_state is not None:
                state = binary_state.text
            else:
                state = WemoSwitch.ERROR_STATE
        conn.close()
        # 0 = off, 1 = on, -1 or Error = error
        if state == '1':
            state = True
        elif state == '0':
            state = False
        else:
            state = WemoSwitch.ERROR_STATE
        return state

    def get_state(self):
        """
        Requests the state of the Switch.
        :return: Boolean indicating the ON state of the switch, or if an error
                 occurred it returns WemoSwitch.ERROR_STATE (-1).
        """
        if self.connected is True:
            return self.__request(
                WemoSwitch.body_status, WemoSwitch.headers_get)
        else:
            return WemoSwitch.ERROR_STATE

    def turn_on(self):
        """
        Turns on the Switch.
        :return: Boolean indicating the ON state of the switch, or if an error
                 occurred it returns WemoSwitch.ERROR_STATE (-1).
        """
        if self.connected is True:
            return self.__request(WemoSwitch.body_on, WemoSwitch.headers_set)
        else:
            return WemoSwitch.ERROR_STATE

    def turn_off(self):
        """
        Turns the switch off.
        :return: Boolean indicating the ON state of the switch, or if an error
                 occurred it returns WemoSwitch.ERROR_STATE (-1).
        """
        if self.connected is True:
            return self.__request(WemoSwitch.body_off, WemoSwitch.headers_set)
        else:
            return WemoSwitch.ERROR_STATE
