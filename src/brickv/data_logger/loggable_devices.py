# -*- coding: utf-8 -*-
"""
brickv (Brick Viewer)
Copyright (C) 2012, 2014 Roland Dudko <roland.dudko@gmail.com>
Copyright (C) 2012, 2014 Marvin Lutz <marvin.lutz.mail@gmail.com>

loggable_devices.py: Util classes for the data logger

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
"""

import time

# https://docs.google.com/spreadsheets/d/14p6N8rAg8M9Ozr1fmOZePPflvNJmgt0pSAebliDrasI/edit?usp=sharing
# Documented for Testing and Blueprints
# Bricklets ############################################################################################################
from brickv.bindings.bricklet_accelerometer import BrickletAccelerometer
from brickv.bindings.bricklet_ambient_light import BrickletAmbientLight
from brickv.bindings.bricklet_ambient_light_v2 import BrickletAmbientLightV2
from brickv.bindings.bricklet_analog_in import BrickletAnalogIn # config: range, averaging
from brickv.bindings.bricklet_analog_in_v2 import BrickletAnalogInV2 # config: moving_average
from brickv.bindings.bricklet_analog_out_v2 import BrickletAnalogOutV2
from brickv.bindings.bricklet_barometer import BrickletBarometer
from brickv.bindings.bricklet_color import BrickletColor # config: gain, integration_time
from brickv.bindings.bricklet_current12 import BrickletCurrent12
from brickv.bindings.bricklet_current25 import BrickletCurrent25
from brickv.bindings.bricklet_distance_ir import BrickletDistanceIR
from brickv.bindings.bricklet_distance_us import BrickletDistanceUS # config: moving_average
from brickv.bindings.bricklet_dual_button import BrickletDualButton
from brickv.bindings.bricklet_dust_detector import BrickletDustDetector # config: moving_average
from brickv.bindings.bricklet_gps import BrickletGPS
from brickv.bindings.bricklet_hall_effect import BrickletHallEffect # config: edge_type, debounce
from brickv.bindings.bricklet_humidity import BrickletHumidity
from brickv.bindings.bricklet_industrial_digital_in_4 import BrickletIndustrialDigitalIn4 # config: selection_mask, edge_type, debounce
from brickv.bindings.bricklet_industrial_dual_0_20ma import BrickletIndustrialDual020mA # config: sample_rate
from brickv.bindings.bricklet_industrial_dual_analog_in import BrickletIndustrialDualAnalogIn # config: sample_rate
from brickv.bindings.bricklet_io16 import BrickletIO16 # config: port_configuration
from brickv.bindings.bricklet_io4 import BrickletIO4 # config: port
from brickv.bindings.bricklet_joystick import BrickletJoystick
# from brickv.bindings.bricklet_laser_range_finder import BrickletLaserRangeFinder #NYI # config: mode, FIXME: special laser handling
from brickv.bindings.bricklet_led_strip import BrickletLEDStrip
from brickv.bindings.bricklet_line import BrickletLine
from brickv.bindings.bricklet_linear_poti import BrickletLinearPoti
from brickv.bindings.bricklet_load_cell import BrickletLoadCell # config: moving_average
from brickv.bindings.bricklet_moisture import BrickletMoisture # config: moving_average
from brickv.bindings.bricklet_motion_detector import BrickletMotionDetector
from brickv.bindings.bricklet_multi_touch import BrickletMultiTouch # config: electrode_config, electrode_sensitivity
from brickv.bindings.bricklet_ptc import BrickletPTC # config: wire_mode
from brickv.bindings.bricklet_rotary_encoder import BrickletRotaryEncoder
from brickv.bindings.bricklet_rotary_poti import BrickletRotaryPoti
# from brickv.bindings.bricklet_rs232 import BrickletRS232 #NYI FIXME: has to use read_callback to get all data
from brickv.bindings.bricklet_sound_intensity import BrickletSoundIntensity
from brickv.bindings.bricklet_temperature import BrickletTemperature # config: i2c_mode
from brickv.bindings.bricklet_temperature_ir import BrickletTemperatureIR # config: emissivity
from brickv.bindings.bricklet_tilt import BrickletTilt
from brickv.bindings.bricklet_voltage import BrickletVoltage
from brickv.bindings.bricklet_voltage_current import BrickletVoltageCurrent # config: averaging, voltage_conversion_time, current_conversion_time
# Bricks ###############################################################################################################
from brickv.bindings.brick_dc import BrickDC  # NYI
# from brickv.bindings.brick_stepper import BricklStepper #NYI

from brickv.data_logger.event_logger import EventLogger
import brickv.data_logger.utils as utils


# special_* functions are for special Bricks/Bricklets. Some device functions can
# return different values, depending on different situations, e.g. the GPS Bricklet.
# If the GPS Bricklet does not have a fix, then the function will return an Error
# instead of the specified return values.

# BrickletGPS
def special_get_gps_coordinates(device):
    if device.get_status()[0] == BrickletGPS.FIX_NO_FIX:
        raise Exception('No fix')
    else:
        return device.get_coordinates()

def special_get_gps_altitude(device):
    if device.get_status()[0] != BrickletGPS.FIX_3D_FIX:
        raise Exception('No 3D fix')
    else:
        return device.get_altitude()

def special_get_gps_motion(device):
    if device.get_status()[0] == BrickletGPS.FIX_NO_FIX:
        raise Exception('No fix')
    else:
        return device.get_motion()

# BrickletPTC
def special_get_ptc_resistance(device):
    if not device.is_sensor_connected():
        raise Exception('No sensor')
    else:
        return device.get_resistance()

def special_get_ptc_temperature(device):
    if not device.is_sensor_connected():
        raise Exception('No sensor')
    else:
        return device.get_temperature()


'''
/*---------------------------------------------------------------------------
                                Identifier
 ---------------------------------------------------------------------------*/
 '''


class Identifier(object):
    """
        This class is used to identify supported Bricks and Bricklets. The
        DEVICE_DEFINITIONS contains a Blueprint for each supported device.
        This Blueprint is used in the config file and the GUI.
    """
    # Devices
    DEVICES = "devices"

    # config list access strings
    DD_NAME = "name"
    DD_CLASS = "class"
    DD_UID = "uid"
    DD_VALUES = "values"
    DD_VALUES_INTERVAL = "interval"
    # Device Definitions Keys
    DD_GETTER = "getter"
    DD_SUBVALUES = "subvalues"

    DD_UID_DEFAULT = "Enter UID"

    # Device Definitons(DD)
    DEVICE_DEFINITIONS = {
        ########################
        # Bricklets Start Here #
        ########################
        BrickletAccelerometer.DEVICE_DISPLAY_NAME: {
            'class': BrickletAccelerometer,
            'values': [
                {
                    'name': 'Acceleration',
                    'getter': lambda device: device.get_acceleration(),
                    'subvalues': ['X', 'Y', 'Z'],
                    'unit': ['g/1000', 'g/1000', 'g/1000'],
                    'advanced': False
                },
                {
                    'name': 'Temperature',
                    'getter': lambda device: device.get_temperature(),
                    'subvalues': None,
                    'unit': '°C',
                    'advanced': True
                }
            ],
            'options_setter': lambda device, data_rate, full_scale, filter_bandwidth: device.set_configuration(data_rate, full_scale, filter_bandwidth),
            'options': [
                {
                    'name': 'Data Rate',
                    'type': 'choice',
                    'values': [('Off', BrickletAccelerometer.DATA_RATE_OFF),
                               ('3Hz', BrickletAccelerometer.DATA_RATE_3HZ),
                               ('6Hz', BrickletAccelerometer.DATA_RATE_6HZ),
                               ('12Hz', BrickletAccelerometer.DATA_RATE_12HZ),
                               ('25Hz', BrickletAccelerometer.DATA_RATE_25HZ),
                               ('50Hz', BrickletAccelerometer.DATA_RATE_50HZ),
                               ('100Hz', BrickletAccelerometer.DATA_RATE_100HZ),
                               ('400Hz', BrickletAccelerometer.DATA_RATE_400HZ),
                               ('800Hz', BrickletAccelerometer.DATA_RATE_800HZ),
                               ('1600Hz', BrickletAccelerometer.DATA_RATE_1600HZ)],
                    'default': '100Hz'
                },
                {
                    'name': 'Full Scale',
                    'type': 'choice',
                    'values': [('2g', BrickletAccelerometer.FULL_SCALE_2G),
                               ('4g', BrickletAccelerometer.FULL_SCALE_4G),
                               ('6g', BrickletAccelerometer.FULL_SCALE_6G),
                               ('8g', BrickletAccelerometer.FULL_SCALE_8G),
                               ('16g', BrickletAccelerometer.FULL_SCALE_16G)],
                    'default': '4g'
                },
                {
                    'name': 'Filter Bandwidth',
                    'type': 'choice',
                    'values': [('800Hz', BrickletAccelerometer.FILTER_BANDWIDTH_800HZ),
                               ('400Hz', BrickletAccelerometer.FILTER_BANDWIDTH_400HZ),
                               ('200Hz', BrickletAccelerometer.FILTER_BANDWIDTH_200HZ),
                               ('50Hz', BrickletAccelerometer.FILTER_BANDWIDTH_50HZ)],
                    'default': '200Hz'
                }
            ]
        },
        BrickletAmbientLight.DEVICE_DISPLAY_NAME: {
            'class': BrickletAmbientLight,
            'values': [
                {
                    'name': 'Analog Value',
                    'getter': lambda device: device.get_analog_value(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': True
                },
                {
                    'name': 'Illuminance',
                    'getter': lambda device: device.get_illuminance(),
                    'subvalues': None,
                    'unit': 'lx/10',
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': None
        },
        BrickletAmbientLightV2.DEVICE_DISPLAY_NAME: {
            'class': BrickletAmbientLightV2,
            'values': [
                {
                    'name': 'Illuminance',
                    'getter': lambda device: device.get_illuminance(),
                    'subvalues': None,
                    'unit': 'lx/100',
                    'advanced': False
                }
            ],
            'options_setter': lambda device, illuminance_range, integration_time: device.set_configuration(illuminance_range, integration_time),
            'options': [
                {
                    'name': 'Illuminance Range',
                    'type': 'choice',
                    'values': [('Unlimited', BrickletAmbientLightV2.ILLUMINANCE_RANGE_UNLIMITED),
                               ('64000Lux', BrickletAmbientLightV2.ILLUMINANCE_RANGE_64000LUX),
                               ('32000Lux', BrickletAmbientLightV2.ILLUMINANCE_RANGE_32000LUX),
                               ('16000Lux', BrickletAmbientLightV2.ILLUMINANCE_RANGE_16000LUX),
                               ('8000Lux', BrickletAmbientLightV2.ILLUMINANCE_RANGE_8000LUX),
                               ('1300Lux', BrickletAmbientLightV2.ILLUMINANCE_RANGE_1300LUX),
                               ('600Lux', BrickletAmbientLightV2.ILLUMINANCE_RANGE_600LUX)],
                    'default': '8000Lux'
                },
                {
                    'name': 'Integration Time',
                    'type': 'choice',
                    'values': [('50ms', BrickletAmbientLightV2.INTEGRATION_TIME_50MS),
                               ('100ms', BrickletAmbientLightV2.INTEGRATION_TIME_100MS),
                               ('150ms', BrickletAmbientLightV2.INTEGRATION_TIME_150MS),
                               ('200ms', BrickletAmbientLightV2.INTEGRATION_TIME_200MS),
                               ('250ms', BrickletAmbientLightV2.INTEGRATION_TIME_350MS),
                               ('300ms', BrickletAmbientLightV2.INTEGRATION_TIME_300MS),
                               ('350ms', BrickletAmbientLightV2.INTEGRATION_TIME_350MS),
                               ('400ms', BrickletAmbientLightV2.INTEGRATION_TIME_400MS)],
                    'default': '200ms'
                }
            ]
        },
        BrickletAnalogIn.DEVICE_DISPLAY_NAME: {
            'class': BrickletAnalogIn,
            'values': [
                {
                    'name': 'Analog Value',
                    'getter': lambda device: device.get_analog_value(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': True
                },
                {
                    'name': 'Voltage',
                    'getter': lambda device: device.get_voltage(),
                    'subvalues': None,
                    'unit': 'mV',
                    'advanced': False
                }
            ],
            'options_setter': lambda device, voltage_range, average_length: [device.set_range(voltage_range), device.set_averaging(average_length)],
            'options': [
                {
                    'name': 'Voltage Range',
                    'type': 'choice',
                    'values': [('Automatic', BrickletAnalogIn.RANGE_AUTOMATIC),
                               ('3.30V', BrickletAnalogIn.RANGE_UP_TO_3V),
                               ('6.05V', BrickletAnalogIn.RANGE_UP_TO_6V),
                               ('10.32V', BrickletAnalogIn.RANGE_UP_TO_10V),
                               ('36.30V', BrickletAnalogIn.RANGE_UP_TO_36V),
                               ('45.00V', BrickletAnalogIn.RANGE_UP_TO_45V)],
                    'default': 'Automatic'
                },
                {
                    'name': 'Average Length',
                    'type': 'int',
                    'minimum': 0,
                    'maximum': 255,
                    'suffix': None,
                    'default': 50
                }
            ]
        },
        BrickletAnalogInV2.DEVICE_DISPLAY_NAME: {
            'class': BrickletAnalogInV2,
            'values': [
                {
                    'name': 'Analog Value',
                    'getter': lambda device: device.get_analog_value(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': True
                },
                {
                    'name': 'Voltage',
                    'getter': lambda device: device.get_voltage(),
                    'subvalues': None,
                    'unit': 'mV',
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletAnalogOutV2.DEVICE_DISPLAY_NAME: {
            'class': BrickletAnalogOutV2,
            'values': [
                {
                    'name': 'Input Voltage',
                    'getter': lambda device: device.get_input_voltage(),
                    'subvalues': None,
                    'unit': 'mV',
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletBarometer.DEVICE_DISPLAY_NAME: {
            'class': BrickletBarometer,
            'values': [
                {
                    'name': 'Air Pressure',
                    'getter': lambda device: device.get_air_pressure(),
                    'subvalues': None,
                    'unit': 'mbar/1000',
                    'advanced': False
                },
                {
                    'name': 'Altitude',
                    'getter': lambda device: device.get_altitude(),
                    'subvalues': None,
                    'unit': 'cm',
                    'advanced': False
                },
                {
                    'name': 'Chip Temperature',
                    'getter': lambda device: device.get_chip_temperature(),
                    'subvalues': None,
                    'unit': '°C/100',
                    'advanced': False
                }
            ],
            'options_setter': lambda device, reference_air_pressure, moving_average_length_air_pressure, average_length_air_pressure, average_length_temperature: \
                              [device.set_reference_air_pressure(int(reference_air_pressure * 1000.0)),
                               device.set_averaging(moving_average_length_air_pressure, average_length_air_pressure, average_length_temperature)],
            'options': [
                {
                    'name': 'Reference Air Pressure',
                    'type': 'float',
                    'minimum': 10.0,
                    'maximum': 1200.0,
                    'decimals': 3,
                    'suffix': ' mbar',
                    'default': 1013.25
                },
                {
                    'name': 'Moving Average Length (Air Pressure)',
                    'type': 'int',
                    'minimum': 0,
                    'maximum': 25,
                    'suffix': None,
                    'default': 25
                },
                {
                    'name': 'Average Length (Air Pressure)',
                    'type': 'int',
                    'minimum': 0,
                    'maximum': 10,
                    'suffix': None,
                    'default': 10
                },
                {
                    'name': 'Average Length (Temperature)',
                    'type': 'int',
                    'minimum': 0,
                    'maximum': 255,
                    'suffix': None,
                    'default': 10
                }
            ]
        },
        BrickletColor.DEVICE_DISPLAY_NAME: {
            'class': BrickletColor,
            'values': [
                {
                    'name': 'Color',
                    'getter': lambda device: device.get_color(),
                    'subvalues': ['Red', 'Green', 'Blue', 'Clear'],
                    'unit': [None, None, None, None],
                    'advanced': False
                },
                {
                    'name': 'Illuminance',
                    'getter': lambda device: device.get_illuminance(), # FIXME: need to apply formula: illuminance * 700 / gain / integration_time
                    'subvalues': None,
                    'unit': 'lx',
                    'advanced': False
                },
                {
                    'name': 'Color Temperature',
                    'getter': lambda device: device.get_color_temperature(),
                    'subvalues': None,
                    'unit': 'K',
                    'advanced': False
                }
            ],
            'options': [
            ]
        },
        BrickletCurrent12.DEVICE_DISPLAY_NAME: {
            'class': BrickletCurrent12,
            'values': [
                {
                    'name': 'Analog Value',
                    'getter': lambda device: device.get_analog_value(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': True
                },
                {
                    'name': 'Current',
                    'getter': lambda device: device.get_current(),
                    'subvalues': None,
                    'unit': 'mA',
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': None
        },
        BrickletCurrent25.DEVICE_DISPLAY_NAME: {
            'class': BrickletCurrent25,
            'values': [
                {
                    'name': 'Analog Value',
                    'getter': lambda device: device.get_analog_value(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': True
                },
                {
                    'name': 'Current',
                    'getter': lambda device: device.get_current(),
                    'subvalues': None,
                    'unit': 'mA',
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': None
        },
        BrickletDistanceIR.DEVICE_DISPLAY_NAME: {
            'class': BrickletDistanceIR,
            'values': [
                {
                    'name': 'Analog Value',
                    'getter': lambda device: device.get_analog_value(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': True
                },
                {
                    'name': 'Distance',
                    'getter': lambda device: device.get_distance(),
                    'subvalues': None,
                    'unit': 'mm',
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': None
        },
        BrickletDistanceUS.DEVICE_DISPLAY_NAME: {
            'class': BrickletDistanceUS,
            'values': [
                {
                    'name': 'Distance Value',
                    'getter': lambda device: device.get_distance_value(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletDualButton.DEVICE_DISPLAY_NAME: {
            'class': BrickletDualButton,
            'values': [
                {
                    'name': 'Button State',
                    'getter': lambda device: device.get_button_state(),
                    'subvalues': ['Left', 'Right'],
                    'unit': [None, None], # FIXME: constants?
                    'advanced': False
                },
                {
                    'name': 'LED State',
                    'getter': lambda device: device.get_led_state(),
                    'subvalues': ['Left', 'Right'],
                    'unit': [None, None], # FIXME: constants?
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': None
        },
        BrickletDustDetector.DEVICE_DISPLAY_NAME: {
            'class': BrickletDustDetector,
            'values': [
                {
                    'name': 'Dust Density',
                    'getter': lambda device: device.get_dust_density(),
                    'subvalues': None,
                    'unit': 'µg/m³',
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletGPS.DEVICE_DISPLAY_NAME: {
            'class': BrickletGPS,
            'values': [
                {
                    'name': 'Altitude',
                    'getter': special_get_gps_altitude,
                    'subvalues': ['Altitude', 'Geoidal Separation'],
                    'unit': ['cm', 'cm'],
                    'advanced': False
                },
                {
                    'name': 'Coordinates',
                    'getter': special_get_gps_coordinates,
                    'subvalues': ['Latitude', 'NS', 'Longitude', 'EW', 'PDOP', 'HDOP', 'VDOP', 'EPE'],
                    'unit': ['deg/1000000', None, 'deg/1000000', None, '1/100', '1/100', '1/100', 'cm'],
                    'advanced': False
                },
                {
                    'name': 'Date Time',
                    'getter': lambda device: device.get_date_time(),
                    'subvalues': ['Date', 'Time'],
                    'unit': ['ddmmyy', 'hhmmss|sss'],
                    'advanced': False
                },
                {
                    'name': 'Motion',
                    'getter': special_get_gps_motion,
                    'subvalues': ['Course', 'Speed'],
                    'unit': ['deg/100', '10m/h'],
                    'advanced': False
                },
                {
                    'name': 'Status',
                    'getter': lambda device: device.get_status(),
                    'subvalues': ['Fix', 'Satellites View', 'Satellites Used'],
                    'unit': [None, None, None], # FIXME: fix constants?
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletHallEffect.DEVICE_DISPLAY_NAME: {
            'class': BrickletHallEffect,
            'values': [
                {
                    'name': 'Edge Count',
                    'getter': lambda device: device.get_edge_count(False),
                    'subvalues': None,
                    'unit': None,
                    'advanced': False
                },
                {
                    'name': 'Value',
                    'getter': lambda device: device.get_value(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletHumidity.DEVICE_DISPLAY_NAME: {
            'class': BrickletHumidity,
            'values': [
                {
                    'name': 'Analog Value',
                    'getter': lambda device: device.get_analog_value(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': True
                },
                {
                    'name': 'Humidity',
                    'getter': lambda device: device.get_humidity(),
                    'subvalues': None,
                    'unit': '%RH/10',
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': None
        },
        BrickletIndustrialDigitalIn4.DEVICE_DISPLAY_NAME: {
            'class': BrickletIndustrialDigitalIn4,
            'values': [
                {
                    'name': 'Edge Count (Pin 0)',
                    'getter': lambda device: device.get_edge_count(0, False),
                    'subvalues': None,
                    'unit': None,
                    'advanced': True
                },
                {
                    'name': 'Edge Count (Pin 1)',
                    'getter': lambda device: device.get_edge_count(1, False),
                    'subvalues': None,
                    'unit': None,
                    'advanced': True
                },
                {
                    'name': 'Edge Count (Pin 2)',
                    'getter': lambda device: device.get_edge_count(2, False),
                    'subvalues': None,
                    'unit': None,
                    'advanced': True
                },
                {
                    'name': 'Edge Count (Pin 3)',
                    'getter': lambda device: device.get_edge_count(3, False),
                    'subvalues': None,
                    'unit': None,
                    'advanced': True
                },
                {
                    'name': 'Value',
                    'getter': lambda device: device.get_value(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletIndustrialDual020mA.DEVICE_DISPLAY_NAME: {
            'class': BrickletIndustrialDual020mA,
            'values': [
                {
                    'name': 'Current (Sensor 0)',
                    'getter': lambda device: device.get_current(0),
                    'subvalues': None,
                    'unit': 'nA',
                    'advanced': False
                },
                {
                    'name': 'Current (Sensor 1)',
                    'getter': lambda device: device.get_current(1),
                    'subvalues': None,
                    'unit': 'nA',
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletIndustrialDualAnalogIn.DEVICE_DISPLAY_NAME: {
            'class': BrickletIndustrialDualAnalogIn,
            'values': [
                {
                    'name': 'ADC Values',
                    'getter': lambda device: device.get_adc_values(),
                    'subvalues': ['Channel 0', 'Channel 1'],
                    'unit': [None, None],
                    'advanced': True
                },
                {
                    'name': 'Voltage (Channel 0)',
                    'getter': lambda device: device.get_voltage(0),
                    'subvalues': None,
                    'unit': 'mV',
                    'advanced': False
                },
                {
                    'name': 'Voltage (Channel 1)',
                    'getter': lambda device: device.get_voltage(1),
                    'subvalues': None,
                    'unit': 'mV',
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletIO16.DEVICE_DISPLAY_NAME: {
            'class': BrickletIO16,
            'values': [
                {
                    'name': 'Edge Count (Pin A0)',
                    'getter': lambda device: device.get_edge_count(0, False),
                    'subvalues': None,
                    'unit': None,
                    'advanced': True
                },
                {
                    'name': 'Edge Count (Pin A1)',
                    'getter': lambda device: device.get_edge_count(1, False),
                    'subvalues': None,
                    'unit': None,
                    'advanced': True
                },
                {
                    'name': 'Port A',
                    'getter': lambda device: device.get_port('a'),
                    'subvalues': None,
                    'unit': None,
                    'advanced': False
                },
                {
                    'name': 'Port B',
                    'getter': lambda device: device.get_port('b'),
                    'subvalues': None,
                    'unit': None,
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletIO4.DEVICE_DISPLAY_NAME: {
            'class': BrickletIO4,
            'values': [
                {
                    'name': 'Edge Count (Pin 0)',
                    'getter': lambda device: device.get_edge_count(0, False),
                    'subvalues': None,
                    'unit': None,
                    'advanced': True
                },
                {
                    'name': 'Edge Count (Pin 1)',
                    'getter': lambda device: device.get_edge_count(1, False),
                    'subvalues': None,
                    'unit': None,
                    'advanced': True
                },
                {
                    'name': 'Edge Count (Pin 2)',
                    'getter': lambda device: device.get_edge_count(2, False),
                    'subvalues': None,
                    'unit': None,
                    'advanced': True
                },
                {
                    'name': 'Edge Count (Pin 3)',
                    'getter': lambda device: device.get_edge_count(3, False),
                    'subvalues': None,
                    'unit': None,
                    'advanced': True
                },
                {
                    'name': 'Value',
                    'getter': lambda device: device.get_value(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletJoystick.DEVICE_DISPLAY_NAME: {
            'class': BrickletJoystick,
            'values': [
                {
                    'name': 'Analog Value',
                    'getter': lambda device: device.get_analog_value(),
                    'subvalues': ['X', 'Y'],
                    'unit': [None, None],
                    'advanced': True
                },
                {
                    'name': 'Position',
                    'getter': lambda device: device.get_position(),
                    'subvalues': ['X', 'Y'],
                    'unit': [None, None],
                    'advanced': False
                },
                {
                    'name': 'Pressed',
                    'getter': lambda device: device.is_pressed(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletLEDStrip.DEVICE_DISPLAY_NAME: {
            'class': BrickletLEDStrip,
            'values': [
                {
                    'name': 'Supply Voltage',
                    'getter': lambda device: device.get_supply_voltage(),
                    'subvalues': None,
                    'unit': 'mV',
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletLine.DEVICE_DISPLAY_NAME: {
            'class': BrickletLine,
            'values': [
                {
                    'name': 'Reflectivity',
                    'getter': lambda device: device.get_reflectivity(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletLinearPoti.DEVICE_DISPLAY_NAME: {
            'class': BrickletLinearPoti,
            'values': [
                {
                    'name': 'Analog Value',
                    'getter': lambda device: device.get_analog_value(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': True
                },
                {
                    'name': 'Position',
                    'getter': lambda device: device.get_position(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletLoadCell.DEVICE_DISPLAY_NAME: {
            'class': BrickletLoadCell,
            'values': [
                {
                    'name': 'Weight',
                    'getter': lambda device: device.get_weight(),
                    'subvalues': None,
                    'unit': 'gram',
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletMoisture.DEVICE_DISPLAY_NAME: {
            'class': BrickletMoisture,
            'values': [
                {
                    'name': 'Moisture Value',
                    'getter': lambda device: device.get_moisture_value(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletMotionDetector.DEVICE_DISPLAY_NAME: {
            'class': BrickletMotionDetector,
            'values': [
                {
                    'name': 'Motion Detected',
                    'getter': lambda device: device.get_motion_detected(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletMultiTouch.DEVICE_DISPLAY_NAME: {
            'class': BrickletMultiTouch,
            'values': [
                {
                    'name': 'State',
                    'getter': lambda device: device.get_touch_state(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletPTC.DEVICE_DISPLAY_NAME: {
            'class': BrickletPTC,
            'values': [
                {
                    'name': 'Resistance',
                    'getter': special_get_ptc_resistance,
                    'subvalues': None,
                    'unit': None,
                    'advanced': True
                },
                {
                    'name': 'Temperature',
                    'getter': special_get_ptc_temperature,
                    'subvalues': None,
                    'unit': '°C/100',
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletRotaryEncoder.DEVICE_DISPLAY_NAME: {
            'class': BrickletRotaryEncoder,
            'values': [
                {
                    'name': 'Count',
                    'getter': lambda device: device.get_count(False),
                    'subvalues': None,
                    'unit': None,
                    'advanced': False
                },
                {
                    'name': 'Pressed',
                    'getter': lambda device: device.is_pressed(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletRotaryPoti.DEVICE_DISPLAY_NAME: {
            'class': BrickletRotaryPoti,
            'values': [
                {
                    'name': 'Analog Value',
                    'getter': lambda device: device.get_analog_value(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': True
                },
                {
                    'name': 'Position',
                    'getter': lambda device: device.get_position(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletSoundIntensity.DEVICE_DISPLAY_NAME: {
            'class': BrickletSoundIntensity,
            'values': [
                {
                    'name': 'Intensity',
                    'getter': lambda device: device.get_intensity(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletTemperature.DEVICE_DISPLAY_NAME: {
            'class': BrickletTemperature,
            'values': [
                {
                    'name': 'Temperature',
                    'getter': lambda device: device.get_temperature(),
                    'subvalues': None,
                    'unit': '°C/100',
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletTemperatureIR.DEVICE_DISPLAY_NAME: {
            'class': BrickletTemperatureIR,
            'values': [
                {
                    'name': 'Ambient Temperature',
                    'getter': lambda device: device.get_ambient_temperature(),
                    'subvalues': None,
                    'unit': '°C/10',
                    'advanced': False
                },
                {
                    'name': 'Object Temperature',
                    'getter': lambda device: device.get_object_temperature(),
                    'subvalues': None,
                    'unit': '°C/10',
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletTilt.DEVICE_DISPLAY_NAME: {
            'class': BrickletTilt,
            'values': [
                {
                    'name': 'State',
                    'getter': lambda device: device.get_tilt_state(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletVoltage.DEVICE_DISPLAY_NAME: {
            'class': BrickletVoltage,
            'values': [
                {
                    'name': 'Analog Value',
                    'getter': lambda device: device.get_analog_value(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': True
                },
                {
                    'name': 'Voltage',
                    'getter': lambda device: device.get_voltage(),
                    'subvalues': None,
                    'unit': 'mV',
                    'advanced': False
                },
            ],
            'options_setter': None,
            'options': [
            ]
        },
        BrickletVoltageCurrent.DEVICE_DISPLAY_NAME: {
            'class': BrickletVoltageCurrent,
            'values': [
                {
                    'name': 'Current',
                    'getter': lambda device: device.get_current(),
                    'subvalues': None,
                    'unit': 'mA',
                    'advanced': False
                },
                {
                    'name': 'Voltage',
                    'getter': lambda device: device.get_voltage(),
                    'subvalues': None,
                    'unit': 'mV',
                    'advanced': False
                },
                {
                    'name': 'Power',
                    'getter': lambda device: device.get_power(),
                    'subvalues': None,
                    'unit': 'mW',
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        },
        #####################
        # Bricks Start Here #
        #####################
        BrickDC.DEVICE_DISPLAY_NAME: {
            'class': BrickDC,
            'values': [
                {
                    'name': 'Velocity',
                    'getter': lambda device: device.get_velocity(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': False
                },
                {
                    'name': 'Current Velocity',
                    'getter': lambda device: device.get_current_velocity(),
                    'subvalues': None,
                    'unit': None,
                    'advanced': False
                },
                {
                    'name': 'Acceleration',
                    'getter': lambda device: device.get_acceleration(),
                    'subvalues': None,
                    'unit': 'velocity/s',
                    'advanced': False
                },
                {
                    'name': 'Stack Input Voltage',
                    'getter': lambda device: device.get_stack_input_voltage(),
                    'subvalues': None,
                    'unit': 'mV',
                    'advanced': False
                },
                {
                    'name': 'External Input Voltage',
                    'getter': lambda device: device.get_external_input_voltage(),
                    'subvalues': None,
                    'unit': 'mV',
                    'advanced': False
                },
                {
                    'name': 'Current Consumption',
                    'getter': lambda device: device.get_current_consumption(),
                    'subvalues': None,
                    'unit': 'mA',
                    'advanced': False
                },
                {
                    'name': 'Chip Temperature',
                    'getter': lambda device: device.get_chip_temperature(),
                    'subvalues': None,
                    'unit': '°C/10',
                    'advanced': False
                }
            ],
            'options_setter': None,
            'options': [
            ]
        }
    }

'''
/*---------------------------------------------------------------------------
                                AbstractDevice
 ---------------------------------------------------------------------------*/
 '''

class AbstractDevice(object):
    """DEBUG and Inheritance only class"""

    def __init__(self, data, datalogger):
        self.datalogger = datalogger
        self.data = data
        self.identifier = None

        self.__name__ = "AbstractDevice"

    def start_timer(self):
        """
        Starts all timer for all loggable variables of the devices.
        """
        EventLogger.debug(self.__str__())

    def _try_catch(self, func):
        """
        Creates a simple try-catch for a specific funtion.
        """
        value = "[NYI-FAIL-TIMER]"
        # err = 0
        try:
            value = func()
        except Exception as e:
            value = self._exception_msg(e.value, e.description)
            # err = 1
        return value

    def _exception_msg(self, value, msg):
        """
        For a uniform creation of Exception messages.
        """
        return "ERROR[" + str(value) + "]: " + str(msg)

    def __str__(self):
        """
        Representation String of the class. For simple overwiev.
        """
        return "[" + str(self.__name__) + "]"

'''
/*---------------------------------------------------------------------------
                                DeviceImpl
 ---------------------------------------------------------------------------*/
 '''

class DeviceImpl(AbstractDevice):
    """
    A SimpleDevice is every device, which only has funtion with one return value.
    """

    def __init__(self, data, datalogger):
        AbstractDevice.__init__(self, data, datalogger)

        self.device_name = self.data[Identifier.DD_NAME]
        self.device_uid = self.data[Identifier.DD_UID]
        self.device_definition = Identifier.DEVICE_DEFINITIONS[self.device_name]
        device_class = self.device_definition[Identifier.DD_CLASS]
        self.device = device_class(self.device_uid, self.datalogger.ipcon)
        self.identifier = self.device_name

        self.__name__ = Identifier.DEVICES + ":" + str(self.device_name)

    def start_timer(self):
        AbstractDevice.start_timer(self)

        for value in self.data[Identifier.DD_VALUES]:
            interval = self.data[Identifier.DD_VALUES][value][Identifier.DD_VALUES_INTERVAL]
            func_name = "_timer"
            var_name = value

            self.datalogger.timers.append(utils.LoggerTimer(interval, func_name, var_name, self))

    def apply_options(self):
        options_setter = self.device_definition['options_setter']
        option_specs = self.device_definition['options']

        if options_setter != None and option_specs != None:
            EventLogger.debug('Applying options for "{0}" with UID "{1}"'.format(self.device_name, self.device_uid))

            args = []

            for option_spec in option_specs:
                for option_name in self.data['options']:
                    if option_name == option_spec['name']:
                        option_value = self.data['options'][option_name]['value']

                        if option_spec['type'] == 'choice':
                            for option_value_spec in option_spec['values']:
                                if option_value == option_value_spec[0]:
                                    args.append(option_value_spec[1])
                        elif option_spec['type'] == 'int':
                            args.append(option_value)
                        elif option_spec['type'] == 'float':
                            args.append(option_value)

            try:
                options_setter(self.device, *tuple(args))
            except Exception as e:
                EventLogger.warning('Could not apply options for "{0}" with UID "{1}": {2}'
                                    .format(self.device_name, self.device_uid, e))

    def _timer(self, var_name):
        """
        This function is used by the LoggerTimer to get the variable values from the brickd.
        In SimpleDevices the get-functions only return one value.
        """

        for value_spec in self.device_definition[Identifier.DD_VALUES]:
            if value_spec['name'] == var_name:
                break

        getter = value_spec['getter']
        subvalue_names = value_spec['subvalues']
        unit = value_spec['unit']
        now = time.time()
        time_format = self.datalogger._config['data']['time_format']

        if time_format == 'de':
            timestamp = utils.timestamp_to_de(now)
        elif time_format == 'us':
            timestamp = utils.timestamp_to_us(now)
        elif time_format == 'iso':
            timestamp = utils.timestamp_to_iso(now)
        else:
            timestamp = utils.timestamp_to_unix(now)

        try:
            value = getter(self.device)
        except Exception as e:
            value = self._exception_msg(str(self.identifier) + "-" + str(var_name), e)
            self.datalogger.add_to_queue(utils.CSVData(timestamp,
                                                       self.identifier,
                                                       self.device_uid,
                                                       var_name,
                                                       value,
                                                       ''))
            # log_exception(timestamp, value_name, e)
            return

        try:
            if subvalue_names is None:
                if unit == None:
                    unit_str = ''
                else:
                    unit_str = unit

                # log_value(value_name, value)
                self.datalogger.add_to_queue(utils.CSVData(timestamp,
                                                           self.identifier,
                                                           self.device_uid,
                                                           var_name,
                                                           value,
                                                           unit_str))
            else:
                subvalue_bool = self.data[Identifier.DD_VALUES][var_name][Identifier.DD_SUBVALUES]
                for i in range(len(subvalue_names)):
                    if not isinstance(subvalue_names[i], list):
                        try:
                            if subvalue_bool[subvalue_names[i]]:
                                if unit[i] == None:
                                    unit_str = ''
                                else:
                                    unit_str = unit[i]
                                self.datalogger.add_to_queue(utils.CSVData(timestamp,
                                                                           self.identifier,
                                                                           self.device_uid,
                                                                           str(var_name) + "-" + str(subvalue_names[i]),
                                                                           value[i],
                                                                           unit_str))
                        except Exception as e:
                            value = self._exception_msg(str(self.identifier) + "-" + str(var_name), e)
                            self.datalogger.add_to_queue(utils.CSVData(timestamp,
                                                                       self.identifier,
                                                                       self.device_uid,
                                                                       str(var_name) + "-" + str(subvalue_names[i]),
                                                                       value[i],
                                                                       ''))
                            return
                    else:
                        for k in range(len(subvalue_names[i])):
                            try:
                                if subvalue_bool[subvalue_names[i][k]]:
                                    if unit[i][k] == None:
                                        unit_str = ''
                                    else:
                                        unit_str = unit[i][k]
                                    self.datalogger.add_to_queue(utils.CSVData(timestamp,
                                                                               self.identifier,
                                                                               self.device_uid,
                                                                               str(var_name) + "-" + str(subvalue_names[i][k]),
                                                                               value[i][k],
                                                                               unit_str))
                            except Exception as e:
                                value = self._exception_msg(str(self.identifier) + "-" + str(var_name), e)
                                self.datalogger.add_to_queue(utils.CSVData(timestamp,
                                                                           self.identifier,
                                                                           self.device_uid,
                                                                           str(var_name) + "-" + str(subvalue_names[i][k]),
                                                                           value[i][k],
                                                                           ''))
                                return
        except Exception as e:
            value = self._exception_msg(str(self.identifier) + "-" + str(var_name), e)
            self.datalogger.add_to_queue(utils.CSVData(timestamp,
                                                       self.identifier,
                                                       self.device_uid,
                                                       var_name,
                                                       value,
                                                       ''))
