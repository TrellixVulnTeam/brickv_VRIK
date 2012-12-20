# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on 2012-12-20.      #
#                                                           #
# If you have a bugfix for this file and want to commit it, #
# please fix the bug in the generator. You can find a link  #
# to the generator git on tinkerforge.com                   #
#############################################################

try:
    from collections import namedtuple
except ImportError:
    try:
        from .ip_connection import namedtuple
    except ValueError:
        from ip_connection import namedtuple

try:
    from .ip_connection import Device, IPConnection, Error
except ValueError:
    from ip_connection import Device, IPConnection, Error

GetCoordinates = namedtuple('Coordinates', ['latitude', 'ns', 'longitude', 'ew', 'pdop', 'hdop', 'vdop', 'epe'])
GetStatus = namedtuple('Status', ['fix', 'satellites_view', 'satellites_used'])
GetAltitude = namedtuple('Altitude', ['altitude', 'geoidal_separation'])
GetMotion = namedtuple('Motion', ['course', 'speed'])
GetDateTime = namedtuple('DateTime', ['date', 'time'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletGPS(Device):
    """
    Device for receiving GPS position
    """

    DEVICE_IDENTIFIER = 222

    CALLBACK_COORDINATES = 17
    CALLBACK_STATUS = 18
    CALLBACK_ALTITUDE = 19
    CALLBACK_MOTION = 20
    CALLBACK_DATE_TIME = 21

    FUNCTION_GET_COORDINATES = 1
    FUNCTION_GET_STATUS = 2
    FUNCTION_GET_ALTITUDE = 3
    FUNCTION_GET_MOTION = 4
    FUNCTION_GET_DATE_TIME = 5
    FUNCTION_RESTART = 6
    FUNCTION_SET_COORDINATES_CALLBACK_PERIOD = 7
    FUNCTION_GET_COORDINATES_CALLBACK_PERIOD = 8
    FUNCTION_SET_STATUS_CALLBACK_PERIOD = 9
    FUNCTION_GET_STATUS_CALLBACK_PERIOD = 10
    FUNCTION_SET_ALTITUDE_CALLBACK_PERIOD = 11
    FUNCTION_GET_ALTITUDE_CALLBACK_PERIOD = 12
    FUNCTION_SET_DATE_TIME_CALLBACK_PERIOD = 13
    FUNCTION_GET_DATE_TIME_CALLBACK_PERIOD = 14
    FUNCTION_SET_MOTION_CALLBACK_PERIOD = 15
    FUNCTION_GET_MOTION_CALLBACK_PERIOD = 16
    FUNCTION_GET_IDENTITY = 255

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (1, 0, 0)

        self.response_expected[BrickletGPS.FUNCTION_GET_COORDINATES] = BrickletGPS.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletGPS.FUNCTION_GET_STATUS] = BrickletGPS.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletGPS.FUNCTION_GET_ALTITUDE] = BrickletGPS.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletGPS.FUNCTION_GET_MOTION] = BrickletGPS.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletGPS.FUNCTION_GET_DATE_TIME] = BrickletGPS.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletGPS.FUNCTION_RESTART] = BrickletGPS.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletGPS.FUNCTION_SET_COORDINATES_CALLBACK_PERIOD] = BrickletGPS.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletGPS.FUNCTION_GET_COORDINATES_CALLBACK_PERIOD] = BrickletGPS.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletGPS.FUNCTION_SET_STATUS_CALLBACK_PERIOD] = BrickletGPS.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletGPS.FUNCTION_GET_STATUS_CALLBACK_PERIOD] = BrickletGPS.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletGPS.FUNCTION_SET_ALTITUDE_CALLBACK_PERIOD] = BrickletGPS.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletGPS.FUNCTION_GET_ALTITUDE_CALLBACK_PERIOD] = BrickletGPS.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletGPS.FUNCTION_SET_DATE_TIME_CALLBACK_PERIOD] = BrickletGPS.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletGPS.FUNCTION_GET_DATE_TIME_CALLBACK_PERIOD] = BrickletGPS.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletGPS.FUNCTION_SET_MOTION_CALLBACK_PERIOD] = BrickletGPS.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletGPS.FUNCTION_GET_MOTION_CALLBACK_PERIOD] = BrickletGPS.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletGPS.CALLBACK_COORDINATES] = BrickletGPS.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletGPS.CALLBACK_STATUS] = BrickletGPS.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletGPS.CALLBACK_ALTITUDE] = BrickletGPS.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletGPS.CALLBACK_MOTION] = BrickletGPS.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletGPS.CALLBACK_DATE_TIME] = BrickletGPS.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletGPS.FUNCTION_GET_IDENTITY] = BrickletGPS.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletGPS.CALLBACK_COORDINATES] = 'I c I c H H H H'
        self.callback_formats[BrickletGPS.CALLBACK_STATUS] = 'B B B'
        self.callback_formats[BrickletGPS.CALLBACK_ALTITUDE] = 'I I'
        self.callback_formats[BrickletGPS.CALLBACK_MOTION] = 'I I'
        self.callback_formats[BrickletGPS.CALLBACK_DATE_TIME] = 'I I'

    def get_coordinates(self):
        """
        Returns the GPS coordinates. Latitude and longitude are given in the
        DD.dddddd° format. The parameter ns and ew are the cardinal directions for
        latitude and logitude. Possible values for ns and ew are 'N', 'S', 'E'
        and 'W' (north, south, east and west).
        
        PDOP, HDOP and VDOP are the dilution of precision (DOP) values. They specify
        the additional multiplicative effect of GPS satellite geometry on GPS 
        precision. See 
        `here <http://en.wikipedia.org/wiki/Dilution_of_precision_(GPS)>`__
        for more information. The values are give in hundreths.
        
        EPE is the "Estimated Position Error". The EPE is given in cm. This is not the
        absolute maximum error, it is the error with a specific confidence. See
        `here <http://www.nps.gov/gis/gps/WhatisEPE.html>`__ for more information.
        """
        return GetCoordinates(*self.ipcon.send_request(self, BrickletGPS.FUNCTION_GET_COORDINATES, (), '', 'I c I c H H H H'))

    def get_status(self):
        """
        Returns the current fix status, the number of satellites that are in view and
        the number of satellites that are currently used.
        
        Possible fix status values can be:
        
        .. csv-table::
         :header: "Value", "Description"
         :widths: 10, 100
        
         "1", "No Fix"
         "2", "2D Fix"
         "3", "3D Fix"
        """
        return GetStatus(*self.ipcon.send_request(self, BrickletGPS.FUNCTION_GET_STATUS, (), '', 'B B B'))

    def get_altitude(self):
        """
        Returns the current altitude and corresponding geoidal separation.
        
        Both values are given in cm.
        """
        return GetAltitude(*self.ipcon.send_request(self, BrickletGPS.FUNCTION_GET_ALTITUDE, (), '', 'I I'))

    def get_motion(self):
        """
        Returns the current course and speed. Course is given in hundreths degree
        and speed is given in hundreths km/h.
        
        Please note that this only returns useful values if an actual movement
        is present.
        """
        return GetMotion(*self.ipcon.send_request(self, BrickletGPS.FUNCTION_GET_MOTION, (), '', 'I I'))

    def get_date_time(self):
        """
        Returns the current date and time. The date is
        given in the format ddmmyy and the time is given
        in the format hhmmss.sss
        """
        return GetDateTime(*self.ipcon.send_request(self, BrickletGPS.FUNCTION_GET_DATE_TIME, (), '', 'I I'))

    def restart(self, restart_type):
        """
        Restarts the GPS Bricklet, the following restart types are available:
        
        .. csv-table::
         :header: "Value", "Description"
         :widths: 10, 100
        
         "0", "Hot start (use all available data in the NV store)"
         "1", "Warm start (don't use ephemeris at restart)"
         "2", "Cold start (don't use time, position, almanacs and ephemeris at restart)"
         "3", "Factory reset (clear all system/user configurations at restart)"
        """
        self.ipcon.send_request(self, BrickletGPS.FUNCTION_RESTART, (restart_type,), 'B', '')

    def set_coordinates_callback_period(self, period):
        """
        Sets the period in ms with which the :func:`Coordinates` callback is triggered
        periodically. A value of 0 turns the callback off.
        
        :func:`Coordinates` is only triggered if the coordinates changed since the
        last triggering.
        
        The default value is 0.
        """
        self.ipcon.send_request(self, BrickletGPS.FUNCTION_SET_COORDINATES_CALLBACK_PERIOD, (period,), 'I', '')

    def get_coordinates_callback_period(self):
        """
        Returns the period as set by :func:`SetCoordinatesCallbackPeriod`.
        """
        return self.ipcon.send_request(self, BrickletGPS.FUNCTION_GET_COORDINATES_CALLBACK_PERIOD, (), '', 'I')

    def set_status_callback_period(self, period):
        """
        Sets the period in ms with which the :func:`Status` callback is triggered
        periodically. A value of 0 turns the callback off.
        
        :func:`Status` is only triggered if the status changed since the
        last triggering.
        
        The default value is 0.
        """
        self.ipcon.send_request(self, BrickletGPS.FUNCTION_SET_STATUS_CALLBACK_PERIOD, (period,), 'I', '')

    def get_status_callback_period(self):
        """
        Returns the period as set by :func:`SetStatusCallbackPeriod`.
        """
        return self.ipcon.send_request(self, BrickletGPS.FUNCTION_GET_STATUS_CALLBACK_PERIOD, (), '', 'I')

    def set_altitude_callback_period(self, period):
        """
        Sets the period in ms with which the :func:`Altitude` callback is triggered
        periodically. A value of 0 turns the callback off.
        
        :func:`Altitude` is only triggered if the altitude changed since the
        last triggering.
        
        The default value is 0.
        """
        self.ipcon.send_request(self, BrickletGPS.FUNCTION_SET_ALTITUDE_CALLBACK_PERIOD, (period,), 'I', '')

    def get_altitude_callback_period(self):
        """
        Returns the period as set by :func:`SetAltitudeCallbackPeriod`.
        """
        return self.ipcon.send_request(self, BrickletGPS.FUNCTION_GET_ALTITUDE_CALLBACK_PERIOD, (), '', 'I')

    def set_date_time_callback_period(self, period):
        """
        Sets the period in ms with which the :func:`DateTime` callback is triggered
        periodically. A value of 0 turns the callback off.
        
        :func:`DateTime` is only triggered if the date or time changed since the
        last triggering.
        
        The default value is 0.
        """
        self.ipcon.send_request(self, BrickletGPS.FUNCTION_SET_DATE_TIME_CALLBACK_PERIOD, (period,), 'I', '')

    def get_date_time_callback_period(self):
        """
        Returns the period as set by :func:`SetDateTimeCallbackPeriod`.
        """
        return self.ipcon.send_request(self, BrickletGPS.FUNCTION_GET_DATE_TIME_CALLBACK_PERIOD, (), '', 'I')

    def set_motion_callback_period(self, period):
        """
        Sets the period in ms with which the :func:`Motion` callback is triggered
        periodically. A value of 0 turns the callback off.
        
        :func:`Motion` is only triggered if the motion changed since the
        last triggering.
        
        The default value is 0.
        """
        self.ipcon.send_request(self, BrickletGPS.FUNCTION_SET_MOTION_CALLBACK_PERIOD, (period,), 'I', '')

    def get_motion_callback_period(self):
        """
        Returns the period as set by :func:`SetMotionCallbackPeriod`.
        """
        return self.ipcon.send_request(self, BrickletGPS.FUNCTION_GET_MOTION_CALLBACK_PERIOD, (), '', 'I')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to, 
        the position, the hardware and firmware version as well as the
        device identifier.
        
        The position can be 'a', 'b', 'c' or 'd'.
        
        The device identifiers are:
        
        .. csv-table::
         :header: "Device Identifier", "Device"
         :widths: 10, 100
        
         "11", "Brick DC"
         "12", "Brick Debug"
         "13", "Brick Master 2.0"
         "14", "Brick Servo"
         "15", "Brick Stepper"
         "16", "Brick IMU"
         "", ""
         "21", "Bricklet Ambient Light"
         "22", "Bricklet Breakout"
         "23", "Bricklet Current12"
         "24", "Bricklet Current25"
         "25", "Bricklet Distance IR"
         "26", "Bricklet Dual Relay"
         "27", "Bricklet Humidity"
         "28", "Bricklet IO-16"
         "29", "Bricklet IO-4"
         "210", "Bricklet Joystick"
         "211", "Bricklet LCD 16x2"
         "212", "Bricklet LCD 20x4"
         "213", "Bricklet Linear Poti"
         "214", "Bricklet Piezo Buzzer"
         "215", "Bricklet Rotary Poti"
         "216", "Bricklet Temperature"
         "217", "Bricklet Temperature IR"
         "218", "Bricklet Voltage"
         "219", "Bricklet Analog In"
         "220", "Bricklet Analog Out"
         "221", "Bricklet Barometer"
         "222", "Bricklet GPS"
         "223", "Bricklet Industrial Digital In 4"
         "224", "Bricklet Industrial Digital Out 4"
         "225", "Bricklet Industrial Quad Relay"
         "226", "Bricklet PTC"
         "227", "Bricklet Voltage/Current"
        
        .. versionadded:: 2.0.0~(Plugin)
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletGPS.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, id, callback):
        """
        Registers a callback with ID *id* to the function *callback*.
        """
        self.registered_callbacks[id] = callback

GPS = BrickletGPS # for backward compatibility
