# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on 2013-07-29.      #
#                                                           #
# Bindings Version 2.0.8                                    #
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

GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletTilt(Device):
    """
    Device for sensing inclination changes
    """

    DEVICE_IDENTIFIER = 239

    CALLBACK_TILT_STATE_CHANGED = 2

    FUNCTION_GET_TILT_STATE = 1
    FUNCTION_GET_IDENTITY = 255

    TILT_STATE_CLOSED = 0
    TILT_STATE_OPEN = 1

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

        self.response_expected[BrickletTilt.FUNCTION_GET_TILT_STATE] = BrickletTilt.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletTilt.CALLBACK_TILT_STATE_CHANGED] = BrickletTilt.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletTilt.FUNCTION_GET_IDENTITY] = BrickletTilt.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletTilt.CALLBACK_TILT_STATE_CHANGED] = 'B'

    def get_tilt_state(self):
        """
        
        """
        return self.ipcon.send_request(self, BrickletTilt.FUNCTION_GET_TILT_STATE, (), '', 'B')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to, 
        the position, the hardware and firmware version as well as the
        device identifier.
        
        The position can be 'a', 'b', 'c' or 'd'.
        
        The device identifiers can be found :ref:`here <device_identifier>`.
        
        .. versionadded:: 2.0.0~(Plugin)
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletTilt.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, id, callback):
        """
        Registers a callback with ID *id* to the function *callback*.
        """
        self.registered_callbacks[id] = callback

Tilt = BrickletTilt # for backward compatibility
