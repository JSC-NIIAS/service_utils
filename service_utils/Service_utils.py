# service requirements
import os
import logging
import argparse
import signal
import psutil
import atexit
import time
import sys
import configparser
import re

from .Singleton import Singleton


class Service_utils(metaclass=Singleton):
    def __init__(
            self,
            keys_required={},
            keys_optional={},
            description=''):

        # initialize shell arguments parser
        self.__parser = argparse.ArgumentParser(
            description=description)
        self.__keys_required = keys_required
        self.__keys_optional = keys_optional
        self.__description = description

        # set default values for service variables
        self.__configuration = None
        self.__args = None

    def start(self):
        # append required keys
        for key, action in self.__keys_required.items():
            self.__parser.add_argument(
                key,
                required=True)

        # append optional keys
        for key, action in self.__keys_optional.items():
            self.__parser.add_argument(
                key,
                required=False)

        self.__args = self.__parser.parse_args()
        self.__args = dict(self.__args._get_kwargs())

#        # parse args and do actions
#        for key, action in keys_required.items():
#            if isinstance(action, Service_utils.Actions):
#                key = self.__modify_key(key)
#                if action == Service_utils.Actions.read_configuration:
#                    self.__create_configuration(
#                        self.__args[key], True)
#                elif action == Service_utils.Actions.write_pid_in_file:
#                    self.__configure_pid(
#                        self.__args[key])
#            elif isinstance(action, type(lambda x: x)):
#                pass
#            else:
#                pass

    def __modify_key(self, key):
        key = re.sub('^-+', '', key)
        key = re.sub('-', '_', key)

        return key
            
#    def __create_configuration(self, configuration_path, required):
#        print('configuration_path:', configuration_path)
#        configuration = configparser.ConfigParser()
#        configuration.read(configuration_path)

    def get_configuration(self):
        return self.__configuration

    def get_args(self):
        return self.__args

#    def __configure_pid(self, pid_file_path, suffix=''):
##            try:
##                self.__configuration['pid']
##            except KeyError:
##                return
##
##            pid_file_path = self.__configuration['pid']['pid_file_path']
#        if pid_file_path is None:
#            print('pid file path is None')
#            return
#
#        folders = pid_file_path.split('/')[:-1]
#        pid_file_folder = '/'.join(folders)
#
#        if not os.path.exists(pid_file_folder) and pid_file_folder != '':
#            os.makedirs(pid_file_folder)
#            print('{} directory made'.format(pid_file_folder))
#
#        if len(suffix) != 0:
#            if len(pid_file_path) < len(suffix):
#                pid_file_path = pid_file_path + '.pid'
#            elif pid_file_path[-4:] != '.pid':
#                pid_file_path = pid_file_path + '.pid'
#
#        self.__write_pid(pid_file_path)
#
#    def __write_pid(self, pid_file_path):
#        with open(pid_file_path, 'w') as pid_out_file:
#            pid_out_file.write('{}'.format(os.getpid()))
#
#    def __configure_logging(self):
#        # logging initializing
#        try:
#            logout = self.__configuration['logging']['logout']
#            debug_mode = self.__configuration['logging']['debug'] == 'true'
#            logging_level = logging.DEBUG if debug_mode else logging.INFO
#
#            if logout == 'stdout' or logout == '':
#                logging.basicConfig(
#                    format='\
#                        \r%(asctime)s %(levelname)s: %(message)s',
#                    datefmt='%Y/%m/%d %H:%M:%S',
#                    level=logging_level)
#            else:
#                logging.basicConfig(
#                    filename=logout, filemode='w',
#                    format='%(asctime)s %(levelname)s: %(message)s',
#                    datefmt='%Y/%m/%d %H:%M:%S',
#                    level=logging_level)
#        except BaseException:
#            print('logging in not configured')
#            pass
#
#    def create_exit_snapshot(self):
#        # global vars
#        start_time = time.time()
#
#        # snapshot function
#        def snapshot(exit_msg, file_prefix):
#            nonlocal start_time
#            with open(file_prefix + str(int(time.time())) + '.txt', 'w') as out:
#                out.write(exit_msg)
#                end_time = time.time()
#                out.write(
#                    'CPU percent: {}\n'.format(
#                        psutil.cpu_percent(percpu=True)))
#                out.write(
#                    'Virtual memory: {}\n'.format(
#                        psutil.virtual_memory()))
#                out.write(
#                    'Virtual memory used by this process: {}%\n'.format(
#                        psutil.Process().memory_percent()))
#                out.write(
#                    'Swap memory: {}\n'.format(
#                        psutil.swap_memory()))
#                out.write(
#                    'Temperature: {}\n'.format(
#                        psutil.sensors_temperatures()))
#                out.write(
#                    'Start time: {}\n'.format(
#                        start_time))
#                out.write(
#                    'End time: {}\n'.format(
#                        end_time))
#                out.write(
#                    'Up time: {} seconds\n'.format(
#                        end_time-start_time))
#
#        def handler_partial(
#                msg='Signal handler called with signal',
#                file_prefix='./',
#                default_handler=signal.SIG_DFL):
#            ''
#            def handler(signum, frame):
#                snapshot(msg, file_prefix)
#                signal.signal(signum, default_handler)
#                os.kill(os.getpid(), signum)
#
#            return handler
#
#        atexit.register(
#            snapshot, 'Exit from service logic', './snapshots/')
#
#        for sig in list(signal.Signals):
#            try:
#                sig_handler = signal.getsignal(sig)
#                signal.signal(
#                    sig,
#                    handler_partial(
#                        'Service get signal {}\n'.format(sig.name),
#                        './snapshots',
#                        sig_handler))
#            except OSError:
#                print('couldn\'t handle {} signal\n'.format(sig.name))
#
#
#    def __set_signal_handlers(self):
#        if self.__signal_handlers is None:
#            return
#
#        # TODO the right methods for solve this problem using config
#        # check if it lambda(handler), string(config arg) or
#        # int(exit code)_
#        for sig, action in self.__signal_handlers.items():
#            assert isinstance(sig, type(signal.SIGINT))
#
#            if isinstance(action, int):
#                exit_code = action
#                signal.signal(
#                    sig,
#                    lambda signal, frame: sys.exit(exit_code))
#            # TODO improve types
#            elif isinstance(action, type(lambda x: x)):
#                signal.signal(
#                    sig,
#                    lambda *args, **kwargs: action(*args, **kwargs))
#            # TODO change exception types and messages
#            else:
#                raise BaseException('type of signal handler is unknown')
