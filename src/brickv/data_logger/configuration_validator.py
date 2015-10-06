# -*- coding: utf-8 -*-
"""
brickv (Brick Viewer)
Copyright (C) 2012, 2014 Roland Dudko <roland.dudko@gmail.com>
Copyright (C) 2012, 2014 Marvin Lutz <marvin.lutz.mail@gmail.com>

configuration_validator.py: Data logger configuration validator

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

import codecs
import json

from brickv.data_logger.event_logger import EventLogger
from brickv.data_logger.utils import DataLoggerException, Utilities
from brickv.data_logger.loggable_devices import Identifier as Idf

def load_and_validate_config(filename):
    EventLogger.info('Loading config from file: {0}'.format(filename))

    with codecs.open(filename, 'rb', 'UTF-8') as f:
        try:
            config = json.load(f)
        except Exception as e:
            EventLogger.critical('Could not parse config file as JSON: {0}'.format(e))
            return None

    if not ConfigValidator(config).validate():
        return None

    EventLogger.info('Config successfully loaded from: {0}'.format(filename))

    return config

def save_config(config, filename):
    EventLogger.info('Saving config to file: {0}'.format(filename))

    try:
        with open(filename, 'wb') as f:
            json.dump(config, f, sort_keys=True, indent=2)
    except Exception:
        EventLogger.critical('Could not write config file as JSON: {0}'.format(e))
        return False

    EventLogger.info('Config successfully saved to: {0}'.format(filename))

    return True

""""
/*---------------------------------------------------------------------------
                                ConfigValidator
 ---------------------------------------------------------------------------*/
"""


class ConfigValidator(object):
    """
    This class validates the (JSON) config file
    """
    MIN_INTERVAL = 0

    def __init__(self, config):
        self._error_count = 0
        self._config = config

        # FIXME: dont access the config before its validated. also this code should not be here
        # but somewhere else. it has nothing to do with validation
        #file_count = self._config['data']['csv']['file_count']
        #file_size = self._config['data']['csv']['file_size']
        #self._log_space_counter = LogSpaceCounter(file_count, file_size)

    def _report_error(self, message):
        self._error_count += 1
        EventLogger.critical(message)

    def validate(self):
        """
        This function performs the validation of the various sections of the JSON
        configuration file
        """
        EventLogger.info("Validating config file")

        self._validate_hosts()
        self._validate_data()
        self._validate_events()
        self._validate_devices()

        if self._error_count > 0:
            EventLogger.critical("Validation found {0} errors".format(self._error_count))
        else:
            EventLogger.info("Validation successful")

        #logging_time = self._log_space_counter.calculate_time()
        #if self._log_space_counter.file_size != 0:
        #    EventLogger.info("Logging time until old data will be overwritten.")
        #    EventLogger.info("Days: " + str(logging_time[0]) +
        #                     " Hours: " + str(logging_time[1]) +
        #                     " Minutes: " + str(logging_time[2]) +
        #                     " Seconds: " + str(logging_time[3]))
        #EventLogger.info("Will write about " + str(
        #    int(self._log_space_counter.lines_per_second + 0.5)) + " lines per second into the log-file.")

        return self._error_count == 0

    def _validate_hosts(self):
        try:
            hosts = self._config['hosts']
        except KeyError:
            self._report_error('Config has no "hosts" section')
            return

        if not isinstance(hosts, dict):
            self._report_error('"hosts" section is not a dict')
            return

        try:
            hosts['default']
        except KeyError:
            self._report_error('Config has no default host')

        for host_id, host in hosts.items():
            # name
            try:
                name = host['name']
            except KeyError:
                self._report_error('Host "{0}" has no name'.format(host_id))
            else:
                if not isinstance(name, basestring):
                    self._report_error('Name of host "{0}" is not a string'.format(host_id))
                elif len(name) == 0:
                    self._report_error('Name of host "{0}" is empty'.format(host_id))

            # port
            try:
                port = host['port']
            except KeyError:
                self._report_error('Host "{0}" has no port'.format(host_id))
            else:
                if not isinstance(port, int):
                    self._report_error('Port of host "{0}" is not an int'.format(host_id))
                elif port < 1 or port > 65535:
                    self._report_error('Port of host "{0}" is out-of-range'.format(host_id))

    def _validate_data(self):
        try:
            data = self._config['data']
        except KeyError:
            self._report_error('Config has no "data" section')
            return

        # time_format
        try:
            time_format = data['time_format']
        except KeyError:
            self._report_error('"data" section has no "time_format" member')
        else:
            if not isinstance(time_format, basestring):
                self._report_error('"data/time_format" is not a string')
            elif time_format not in ['de', 'us', 'iso', 'unix']:
                self._report_error('Invalid "data/time_format" value: {0}'.format(time_format))

        self._validate_data_csv()

    def _validate_data_csv(self):
        try:
            csv = self._config['data']['csv']
        except KeyError:
            self._report_error('Config has no "data/csv" section')
            return

        # enabled
        try:
            enabled = csv['enabled']
        except KeyError:
            self._report_error('"data/csv" section has no "enabled" member')
        else:
            if not isinstance(enabled, bool):
                self._report_error('"data/csv/enabled" is not an bool')

        # file_name
        try:
            file_name = csv['file_name']
        except KeyError:
            self._report_error('"data/csv" section has no "file_name" member')
        else:
            if not isinstance(file_name, basestring):
                self._report_error('"data/csv/file_name" is not an string')
            elif len(file_name) == 0:
                self._report_error('"data/csv/file_name" is empty')

        # file_count
        try:
            file_count = csv['file_count']
        except KeyError:
            self._report_error('"data/csv" section has no "file_count" member')
        else:
            if not isinstance(file_count, int):
                self._report_error('"data/csv/file_count" is not an integer')
            elif file_count < 1 or file_count > 65535:
                self._report_error('"data/csv/file_count" is out-of-range')

        # file_size
        try:
            file_size = csv['file_size']
        except KeyError:
            self._report_error('"data/csv" section has no "file_size" member')
        else:
            if not isinstance(file_size, int):
                self._report_error('"data/csv/file_size" is not an integer')
            elif file_size < 0 or file_size > 2097152:
                self._report_error('"data/csv/file_size" is out-of-range')

    def _validate_events(self):
        try:
            events = self._config['events']
        except KeyError:
            self._report_error('Config has no "events" section')
            return

        # time_format
        try:
            time_format = events['time_format']
        except KeyError:
            self._report_error('"events" section has no "time_format" member')
        else:
            if not isinstance(time_format, basestring):
                self._report_error('"events/time_format" is not a string')
            elif time_format not in ['de', 'us', 'iso', 'unix']:
                self._report_error('Invalid "events/time_format" value: {0}'.format(time_format))

        self._validate_events_log()

    def _validate_events_log(self):
        try:
            log = self._config['events']['log']
        except KeyError:
            self._report_error('Config has no "events/log" section')
            return

        # enabled
        try:
            enabled = log['enabled']
        except KeyError:
            self._report_error('"events/log" section has no "enabled" member')
        else:
            if not isinstance(enabled, bool):
                self._report_error('"events/log/enabled" is not an bool')

        # file_name
        try:
            file_name = log['file_name']
        except KeyError:
            self._report_error('"events/log" section has no "file_name" member')
        else:
            if not isinstance(file_name, basestring):
                self._report_error('"events/log/file_name" is not an string')
            elif len(file_name) == 0:
                self._report_error('"events/log/file_name" is empty')

        # level
        try:
            level = log['level']
        except KeyError:
            self._report_error('"events/log" section has no "level" member')
        else:
            if not isinstance(level, basestring):
                self._report_error('"events/log/level" is not an integer')
            elif level not in ['debug', 'info', 'warning', 'error', 'critical']:
                self._report_error('Invalid "events/log/level" value: {0}'.format(level))

    def _validate_devices(self):
        try:
            devices = self._config['devices']
        except KeyError:
            self._report_error('Config has no "devices" section')
            return

        if not isinstance(devices, list):
            self._report_error('"devices" section is not a list')
            return

        device_specs = Idf.DEVICE_DEFINITIONS

        for device in devices:
            # uid
            try:
                uid = device['uid']
            except KeyError:
                self._report_error('Device has no UID')
                continue

            if not isinstance(uid, basestring):
                self._report_error('Device UID is not a string')
                continue

            # name
            try:
                name = device['name']
            except KeyError:
                self._report_error('Device "{0}" has no name'.format(uid))
                continue

            if not isinstance(name, basestring):
                self._report_error('Name of device "{0}" is not a string'.format(uid))
                continue
            elif len(name) == 0:
                self._report_error('Device "{0}" has empty name'.format(uid))
                continue
            elif name not in device_specs:
                self._report_error('Device "{0}" has unknwon name: {1}'.format(uid, name))
                continue

            device_spec = device_specs[name]

            # host
            try:
                host = device['host']
            except KeyError:
                self._report_error('Device "{0}" has no host'.format(uid))
            else:
                if not isinstance(host, basestring):
                    self._report_error('Host of device "{0}" is not a string'.format(uid))
                elif len(host) == 0:
                    self._report_error('Host of device "{0}" is empty'.format(uid))
                elif host not in self._config['hosts']:
                    self._report_error('Host of device "{0}" is unknown: {1}'.format(uid, host))

            # values
            try:
                values = device['values']
            except KeyError:
                self._report_error('Device "{0}" has no values'.format(uid))
            else:
                if not isinstance(values, dict):
                    self._report_error('"values" of device "{0}" is not a dict'.format(uid))
                elif len(values) == 0:
                    self._report_error('"values" of device "{0}" is empty'.format(uid))
                else:
                    for value_spec in device_spec['values']:
                        try:
                            value = values[value_spec['name']]
                        except KeyError:
                            self._report_error('Value "{0}" of device "{1}" is missing'.format(value_spec['name'], uid))
                            continue

                        # interval
                        try:
                            interval = value['interval']
                        except KeyError:
                            self._report_error('Value "{0}" of device "{1}" has no interval'.format(value_spec['name'], uid))
                        else:
                            if not isinstance(interval, int):
                                self._report_error('Interval of value "{0}" of device "{1}" is not an int'.format(value_spec['name'], uid))
                            elif interval < 0:
                                self._report_error('Interval of value "{0}" of device "{1}" is ouf-of-range'.format(value_spec['name'], uid))

                        # subvalues
                        if value_spec['subvalues'] != None:
                            try:
                                subvalues = value['subvalues']
                            except KeyError:
                                self._report_error('Value "{0}" of device "{1}" has no subvalues'.format(value_spec['name'], uid))
                            else:
                                if not isinstance(subvalues, dict):
                                    self._report_error('Subvalues of value "{0}" of device "{1}" is not a dict'.format(value_spec['name'], uid))
                                else:
                                    for subvalue_spec_name in value_spec['subvalues']:
                                        try:
                                            subvalue_value = subvalues[subvalue_spec_name]
                                        except:
                                            self._report_error('Subvalue "{0}" of value "{1}" of device "{2}" is missing'
                                                               .format(subvalue_spec_name, value_spec['name'], uid))
                                            continue

                                        if not isinstance(subvalue_value, bool):
                                            self._report_error('Subvalue "{0}" of value "{1}" of device "{2}" is not a bool'
                                                               .format(subvalue_spec_name, value_spec['name'], uid))

            # options
            if device_spec['options'] != None:
                try:
                    options = device['options']
                except KeyError:
                    self._report_error('Device "{0}" has no options'.format(uid))
                else:
                    if not isinstance(options, dict):
                        self._report_error('"options" of device "{0}" is not a dict'.format(uid))
                    elif len(options) == 0:
                        self._report_error('"options" of device "{0}" is empty'.format(uid))
                    else:
                        for option_spec in device_spec['options']:
                            try:
                                option = options[option_spec['name']]
                            except KeyError:
                                self._report_error('Option "{0}" of device "{1}" is missing'.format(option_spec['name'], uid))
                                continue

                            # value
                            try:
                                value = option['value']
                            except KeyError:
                                self._report_error('Option "{0}" of device "{1}" has no interval'.format(option_spec['name'], uid))
                            else:
                                valid = False

                                if option_spec['type'] == 'choice':
                                    if not isinstance(value, basestring):
                                        self._report_error('Value of option "{0}" of device "{1}" is not a string'
                                                           .format(option_spec['name'], uid))
                                        continue

                                    for option_value_spec in option_spec['values']:
                                        if option_value_spec[0] == value:
                                            valid = True
                                            break
                                elif option_spec['type'] == 'int':
                                    if not isinstance(value, int):
                                        self._report_error('Value of option "{0}" of device "{1}" is not an int'
                                                           .format(option_spec['name'], uid))
                                        continue

                                    valid = value >= option_spec['minimum'] and value <= option_spec['maximum']
                                elif option_spec['type'] == 'float':
                                    if not isinstance(value, float):
                                        self._report_error('Value of option "{0}" of device "{1}" is not a float'
                                                           .format(option_spec['name'], uid))
                                        continue

                                    valid = value >= option_spec['minimum'] and value <= option_spec['maximum']

                                if not valid:
                                    self._report_error('Value of option "{0}" of device "{1}" is invalid: {2}'
                                                       .format(option_spec['name'], uid, value))

        #if interval > 0:
        #    self._log_space_counter.add_lines_per_second(interval * logged_values)


""""
/*---------------------------------------------------------------------------
                                LogSpaceCounter
 ---------------------------------------------------------------------------*/
"""


class LogSpaceCounter(object):
    """
    This class provides functions to count the average lines per second
    which will be written into the log file
    """

    def __init__(self, file_count, file_size):
        """
        file_count -- the amount of logfiles
        file_size -- the size of each file
        """
        self.file_count = file_count
        self.file_size = file_size

        self.lines_per_second = 0.0

    def add_lines_per_second(self, lines):
        self.lines_per_second += lines

    def calculate_time(self):
        """
        This function calculates the time where the logger can
        save data without overwriting old ones.

        18k lines -> 1MB
        """
        if self.lines_per_second <= 0 or self.file_size == 0:
            return 0, 0, 0, 0

        max_available_space = (self.file_count + 1) * ((self.file_size / 1024.0) / 1024.0)
        seconds_for_one_MB = 18000.0 / self.lines_per_second

        sec = seconds_for_one_MB * max_available_space * 1.0

        days = int(sec / 86400.0)
        sec -= 86400.0 * days

        hrs = int(sec / 3600.0)
        sec -= 3600.0 * hrs

        mins = int(sec / 60.0)
        sec -= 60.0 * mins

        return days, hrs, mins, int(sec)
