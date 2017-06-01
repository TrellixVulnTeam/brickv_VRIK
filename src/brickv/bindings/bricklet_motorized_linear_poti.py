# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on 2017-05-31.      #
#                                                           #
# Python Bindings Version 2.1.13                            #
#                                                           #
# If you have a bugfix for this file and want to commit it, #
# please fix the bug in the generator. You can find a link  #
# to the generators git repository on tinkerforge.com       #
#############################################################

#### __DEVICE_IS_NOT_RELEASED__ ####

from collections import namedtuple

try:
    from .ip_connection import Device, IPConnection, Error, create_chunk_data
except ValueError:
    from ip_connection import Device, IPConnection, Error, create_chunk_data

GetPositionCallbackConfiguration = namedtuple('PositionCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'min', 'max'])
GetMotorPosition = namedtuple('MotorPosition', ['position', 'drive_mode', 'hold_position', 'position_reached'])
GetSPITFPErrorCount = namedtuple('SPITFPErrorCount', ['error_count_ack_checksum', 'error_count_message_checksum', 'error_count_frame', 'error_count_overflow'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletMotorizedLinearPoti(Device):
    """
    TODO
    """

    DEVICE_IDENTIFIER = 267
    DEVICE_DISPLAY_NAME = 'Motorized Linear Poti Bricklet'

    CALLBACK_POSITION = 4
    CALLBACK_POSITION_REACHED = 10


    FUNCTION_GET_POSITION = 1
    FUNCTION_SET_POSITION_CALLBACK_CONFIGURATION = 2
    FUNCTION_GET_POSITION_CALLBACK_CONFIGURATION = 3
    FUNCTION_SET_MOTOR_POSITION = 5
    FUNCTION_GET_MOTOR_POSITION = 6
    FUNCTION_CALIBRATE = 7
    FUNCTION_SET_POSITION_REACHED_CALLBACK_CONFIGURATION = 8
    FUNCTION_GET_POSITION_REACHED_CALLBACK_CONFIGURATION = 9
    FUNCTION_GET_SPITFP_ERROR_COUNT = 234
    FUNCTION_SET_BOOTLOADER_MODE = 235
    FUNCTION_GET_BOOTLOADER_MODE = 236
    FUNCTION_SET_WRITE_FIRMWARE_POINTER = 237
    FUNCTION_WRITE_FIRMWARE = 238
    FUNCTION_SET_STATUS_LED_CONFIG = 239
    FUNCTION_GET_STATUS_LED_CONFIG = 240
    FUNCTION_GET_CHIP_TEMPERATURE = 242
    FUNCTION_RESET = 243
    FUNCTION_WRITE_UID = 248
    FUNCTION_READ_UID = 249
    FUNCTION_GET_IDENTITY = 255

    THRESHOLD_OPTION_OFF = 'x'
    THRESHOLD_OPTION_OUTSIDE = 'o'
    THRESHOLD_OPTION_INSIDE = 'i'
    THRESHOLD_OPTION_SMALLER = '<'
    THRESHOLD_OPTION_GREATER = '>'
    DRIVE_MODE_FAST = 0
    DRIVE_MODE_SMOOTH = 1
    BOOTLOADER_MODE_BOOTLOADER = 0
    BOOTLOADER_MODE_FIRMWARE = 1
    BOOTLOADER_MODE_BOOTLOADER_WAIT_FOR_REBOOT = 2
    BOOTLOADER_MODE_FIRMWARE_WAIT_FOR_REBOOT = 3
    BOOTLOADER_MODE_FIRMWARE_WAIT_FOR_ERASE_AND_REBOOT = 4
    BOOTLOADER_STATUS_OK = 0
    BOOTLOADER_STATUS_INVALID_MODE = 1
    BOOTLOADER_STATUS_NO_CHANGE = 2
    BOOTLOADER_STATUS_ENTRY_FUNCTION_NOT_PRESENT = 3
    BOOTLOADER_STATUS_DEVICE_IDENTIFIER_INCORRECT = 4
    BOOTLOADER_STATUS_CRC_MISMATCH = 5
    STATUS_LED_CONFIG_OFF = 0
    STATUS_LED_CONFIG_ON = 1
    STATUS_LED_CONFIG_SHOW_HEARTBEAT = 2
    STATUS_LED_CONFIG_SHOW_STATUS = 3

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

        self.response_expected[BrickletMotorizedLinearPoti.FUNCTION_GET_POSITION] = BrickletMotorizedLinearPoti.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletMotorizedLinearPoti.FUNCTION_SET_POSITION_CALLBACK_CONFIGURATION] = BrickletMotorizedLinearPoti.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletMotorizedLinearPoti.FUNCTION_GET_POSITION_CALLBACK_CONFIGURATION] = BrickletMotorizedLinearPoti.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletMotorizedLinearPoti.CALLBACK_POSITION] = BrickletMotorizedLinearPoti.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletMotorizedLinearPoti.FUNCTION_SET_MOTOR_POSITION] = BrickletMotorizedLinearPoti.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletMotorizedLinearPoti.FUNCTION_GET_MOTOR_POSITION] = BrickletMotorizedLinearPoti.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletMotorizedLinearPoti.FUNCTION_CALIBRATE] = BrickletMotorizedLinearPoti.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletMotorizedLinearPoti.FUNCTION_SET_POSITION_REACHED_CALLBACK_CONFIGURATION] = BrickletMotorizedLinearPoti.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletMotorizedLinearPoti.FUNCTION_GET_POSITION_REACHED_CALLBACK_CONFIGURATION] = BrickletMotorizedLinearPoti.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletMotorizedLinearPoti.CALLBACK_POSITION_REACHED] = BrickletMotorizedLinearPoti.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletMotorizedLinearPoti.FUNCTION_GET_SPITFP_ERROR_COUNT] = BrickletMotorizedLinearPoti.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletMotorizedLinearPoti.FUNCTION_SET_BOOTLOADER_MODE] = BrickletMotorizedLinearPoti.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletMotorizedLinearPoti.FUNCTION_GET_BOOTLOADER_MODE] = BrickletMotorizedLinearPoti.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletMotorizedLinearPoti.FUNCTION_SET_WRITE_FIRMWARE_POINTER] = BrickletMotorizedLinearPoti.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletMotorizedLinearPoti.FUNCTION_WRITE_FIRMWARE] = BrickletMotorizedLinearPoti.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletMotorizedLinearPoti.FUNCTION_SET_STATUS_LED_CONFIG] = BrickletMotorizedLinearPoti.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletMotorizedLinearPoti.FUNCTION_GET_STATUS_LED_CONFIG] = BrickletMotorizedLinearPoti.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletMotorizedLinearPoti.FUNCTION_GET_CHIP_TEMPERATURE] = BrickletMotorizedLinearPoti.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletMotorizedLinearPoti.FUNCTION_RESET] = BrickletMotorizedLinearPoti.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletMotorizedLinearPoti.FUNCTION_WRITE_UID] = BrickletMotorizedLinearPoti.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletMotorizedLinearPoti.FUNCTION_READ_UID] = BrickletMotorizedLinearPoti.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletMotorizedLinearPoti.FUNCTION_GET_IDENTITY] = BrickletMotorizedLinearPoti.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletMotorizedLinearPoti.CALLBACK_POSITION] = 'H'
        self.callback_formats[BrickletMotorizedLinearPoti.CALLBACK_POSITION_REACHED] = 'H'


    def get_position(self):
        """
        Returns the position of the linear potentiometer. The value is
        between 0 (slider down) and 100 (slider up).
        """
        return self.ipcon.send_request(self, BrickletMotorizedLinearPoti.FUNCTION_GET_POSITION, (), '', 'H')

    def set_position_callback_configuration(self, period, value_has_to_change, option, min, max):
        """
        TODO
        """
        self.ipcon.send_request(self, BrickletMotorizedLinearPoti.FUNCTION_SET_POSITION_CALLBACK_CONFIGURATION, (period, value_has_to_change, option, min, max), 'I ! c H H', '')

    def get_position_callback_configuration(self):
        """
        TODO
        """
        return GetPositionCallbackConfiguration(*self.ipcon.send_request(self, BrickletMotorizedLinearPoti.FUNCTION_GET_POSITION_CALLBACK_CONFIGURATION, (), '', 'I ! c H H'))

    def set_motor_position(self, position, drive_mode, hold_position):
        """
        TODO
        """
        self.ipcon.send_request(self, BrickletMotorizedLinearPoti.FUNCTION_SET_MOTOR_POSITION, (position, drive_mode, hold_position), 'H B !', '')

    def get_motor_position(self):
        """
        TODO
        """
        return GetMotorPosition(*self.ipcon.send_request(self, BrickletMotorizedLinearPoti.FUNCTION_GET_MOTOR_POSITION, (), '', 'H B ! !'))

    def calibrate(self):
        """
        TODO
        """
        self.ipcon.send_request(self, BrickletMotorizedLinearPoti.FUNCTION_CALIBRATE, (), '', '')

    def set_position_reached_callback_configuration(self, enabled):
        """

        """
        self.ipcon.send_request(self, BrickletMotorizedLinearPoti.FUNCTION_SET_POSITION_REACHED_CALLBACK_CONFIGURATION, (enabled,), '!', '')

    def get_position_reached_callback_configuration(self):
        """

        """
        return self.ipcon.send_request(self, BrickletMotorizedLinearPoti.FUNCTION_GET_POSITION_REACHED_CALLBACK_CONFIGURATION, (), '', '!')

    def get_spitfp_error_count(self):
        """
        Returns the error count for the communication between Brick and Bricklet.

        The errors are divided into

        * ack checksum errors,
        * message checksum errors,
        * frameing errors and
        * overflow errors.

        The errors counts are for errors that occur on the Bricklet side. All
        Bricks have a similar function that returns the errors on the Brick side.
        """
        return GetSPITFPErrorCount(*self.ipcon.send_request(self, BrickletMotorizedLinearPoti.FUNCTION_GET_SPITFP_ERROR_COUNT, (), '', 'I I I I'))

    def set_bootloader_mode(self, mode):
        """
        Sets the bootloader mode and returns the status after the requested
        mode change was instigated.

        You can change from bootloader mode to firmware mode and vice versa. A change
        from bootloader mode to firmware mode will only take place if the entry function,
        device identifier und crc are present and correct.

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        return self.ipcon.send_request(self, BrickletMotorizedLinearPoti.FUNCTION_SET_BOOTLOADER_MODE, (mode,), 'B', 'B')

    def get_bootloader_mode(self):
        """
        Returns the current bootloader mode, see :func:`Set Bootloader Mode`.
        """
        return self.ipcon.send_request(self, BrickletMotorizedLinearPoti.FUNCTION_GET_BOOTLOADER_MODE, (), '', 'B')

    def set_write_firmware_pointer(self, pointer):
        """
        Sets the firmware pointer for func:`WriteFirmware`. The pointer has
        to be increased by chunks of size 64. The data is written to flash
        every 4 chunks (which equals to one page of size 256).

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        self.ipcon.send_request(self, BrickletMotorizedLinearPoti.FUNCTION_SET_WRITE_FIRMWARE_POINTER, (pointer,), 'I', '')

    def write_firmware(self, data):
        """
        Writes 64 Bytes of firmware at the position as written by
        :func:`Set Write Firmware Pointer` before. The firmware is written
        to flash every 4 chunks.

        You can only write firmware in bootloader mode.

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        return self.ipcon.send_request(self, BrickletMotorizedLinearPoti.FUNCTION_WRITE_FIRMWARE, (data,), '64B', 'B')

    def set_status_led_config(self, config):
        """
        Sets the status LED configuration. By default the LED shows
        communication traffic between Brick and Bricklet, it flickers once
        for every 10 received data packets.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is will show heartbeat by default.
        """
        self.ipcon.send_request(self, BrickletMotorizedLinearPoti.FUNCTION_SET_STATUS_LED_CONFIG, (config,), 'B', '')

    def get_status_led_config(self):
        """
        Returns the configuration as set by :func:`Set Status LED Config`
        """
        return self.ipcon.send_request(self, BrickletMotorizedLinearPoti.FUNCTION_GET_STATUS_LED_CONFIG, (), '', 'B')

    def get_chip_temperature(self):
        """
        Returns the temperature in °C as measured inside the microcontroller. The
        value returned is not the ambient temperature!

        The temperature is only proportional to the real temperature and it has bad
        accuracy. Practically it is only useful as an indicator for
        temperature changes.
        """
        return self.ipcon.send_request(self, BrickletMotorizedLinearPoti.FUNCTION_GET_CHIP_TEMPERATURE, (), '', 'h')

    def reset(self):
        """
        Calling this function will reset the Bricklet. All configurations
        will be lost.

        After a reset you have to create new device objects,
        calling functions on the existing ones will result in
        undefined behavior!
        """
        self.ipcon.send_request(self, BrickletMotorizedLinearPoti.FUNCTION_RESET, (), '', '')

    def write_uid(self, uid):
        """
        Writes a new UID into flash. If you want to set a new UID
        you have to decode the Base58 encoded UID string into an
        integer first.

        We recommend that you use Brick Viewer to change the UID.
        """
        self.ipcon.send_request(self, BrickletMotorizedLinearPoti.FUNCTION_WRITE_UID, (uid,), 'I', '')

    def read_uid(self):
        """
        Returns the current UID as an integer. Encode as
        Base58 to get the usual string version.
        """
        return self.ipcon.send_request(self, BrickletMotorizedLinearPoti.FUNCTION_READ_UID, (), '', 'I')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to,
        the position, the hardware and firmware version as well as the
        device identifier.

        The position can be 'a', 'b', 'c' or 'd'.

        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletMotorizedLinearPoti.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, id_, callback):
        """
        Registers a callback with ID *id* to the function *callback*.
        """
        if callback is None:
            self.registered_callbacks.pop(id_, None)
        else:
            self.registered_callbacks[id_] = callback

MotorizedLinearPoti = BrickletMotorizedLinearPoti # for backward compatibility
