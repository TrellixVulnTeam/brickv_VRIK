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

class BrickletRemoteSwitch(Device):
    """
    Device that controls mains switches remotely
    """

    DEVICE_IDENTIFIER = 235

    CALLBACK_SWITCHING_DONE = 3

    FUNCTION_SWITCH_SOCKET = 1
    FUNCTION_GET_SWITCHING_STATE = 2
    FUNCTION_SET_TRIES = 4
    FUNCTION_GET_TRIES = 5
    FUNCTION_GET_IDENTITY = 255

    SWITCH_TO_OFF = 0
    SWITCH_TO_ON = 1
    SWITCHINGSTATE_READY = 0
    SWITCHINGSTATE_BUSY = 1

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

        self.response_expected[BrickletRemoteSwitch.FUNCTION_SWITCH_SOCKET] = BrickletRemoteSwitch.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletRemoteSwitch.FUNCTION_GET_SWITCHING_STATE] = BrickletRemoteSwitch.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRemoteSwitch.CALLBACK_SWITCHING_DONE] = BrickletRemoteSwitch.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletRemoteSwitch.FUNCTION_SET_TRIES] = BrickletRemoteSwitch.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletRemoteSwitch.FUNCTION_GET_TRIES] = BrickletRemoteSwitch.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRemoteSwitch.FUNCTION_GET_IDENTITY] = BrickletRemoteSwitch.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletRemoteSwitch.CALLBACK_SWITCHING_DONE] = ''

    def switch_socket(self, house_code, receiver_code, switch_to):
        """
        
        """
        self.ipcon.send_request(self, BrickletRemoteSwitch.FUNCTION_SWITCH_SOCKET, (house_code, receiver_code, switch_to), 'B B B', '')

    def get_switching_state(self):
        """
        
        """
        return self.ipcon.send_request(self, BrickletRemoteSwitch.FUNCTION_GET_SWITCHING_STATE, (), '', 'B')

    def set_tries(self, tries):
        """
        The default value is 5.
        """
        self.ipcon.send_request(self, BrickletRemoteSwitch.FUNCTION_SET_TRIES, (tries,), 'B', '')

    def get_tries(self):
        """
        Returns the number of tries as set by :func:`SetTries`.
        """
        return self.ipcon.send_request(self, BrickletRemoteSwitch.FUNCTION_GET_TRIES, (), '', 'B')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to, 
        the position, the hardware and firmware version as well as the
        device identifier.
        
        The position can be 'a', 'b', 'c' or 'd'.
        
        The device identifiers can be found :ref:`here <device_identifier>`.
        
        .. versionadded:: 2.0.0~(Plugin)
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletRemoteSwitch.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, id, callback):
        """
        Registers a callback with ID *id* to the function *callback*.
        """
        self.registered_callbacks[id] = callback

RemoteSwitch = BrickletRemoteSwitch # for backward compatibility
