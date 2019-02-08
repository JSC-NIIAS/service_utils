# service requirements
import os
import logging
import argparse
import signal
import sys
import configparser
import re
from enum import Enum


class Service_utils:
    ''
    class Actions(Enum):
        '''
            Actions:
                1. read configuration (path_to_config: str)
                2. save pid of application process in file (pidout_file: str)
                3. create logger (path to stdout file: str)
                4. configure exits (-f) #TODO
        '''  #TODO
        read_configuration = 1
        write_pid_in_file = 2
        create_logger = 3
        # handle_signals = 4 
        configure_exits = 5 

    class __Service_utils:
        def __init__(
                self,
                keys_required={},
                keys_optional={},
                signal_handlers=None,
                description=''):

            # initialize shell arguments parser
            self.__parser = argparse.ArgumentParser(
                description=description)
            # save signal handlers
            self.__signal_handlers = signal_handlers

            # set default values for service variables
            self.__configuration = None

            # append required keys
            for key, action in keys_required.items():
                self.__parser.add_argument(
                    key,
                    required=True)

            # append optional keys
            for key, action in keys_optional.items():
                self.__parser.add_argument(
                    key,
                    required=False)

            self.__args = self.__parser.parse_args()
            self.__args = dict(self.__args._get_kwargs())

            # parse args and do actions
            for key, action in keys_required.items():
                if isinstance(action, Service_utils.Actions):
                    key = self.__modify_key(key)
                    if action == Service_utils.Actions.read_configuration:
                        self.__create_configuration(
                            self.__args[key], True)
                    elif action == Service_utils.Actions.write_pid_in_file:
                        self.__configure_pid(
                            self.__args[key])
                elif isinstance(action, type(lambda x: x)):
                    pass
                else:
                    pass

            self.__set_signal_handlers()

        def __modify_key(self, key):
            key = re.sub('^-+', '', key)
            key = re.sub('-', '_', key)

            return key
                
        def __create_configuration(self, configuration_path, required):
            print('configuration_path:', configuration_path)
            configuration = configparser.ConfigParser()
            configuration.read(configuration_path)

            # TODO
            # if list(configuration.keys()) == ['DEFAULT']:
            #     raise BaseException('Bad config.')

            self.__configuration = configuration
#            self.__configure_logging()

        def get_configuration(self):
            return self.__configuration

        def get_args(self):
            return self.__args

        def __configure_pid(self, pid_file_path, suffix=''):
#            try:
#                self.__configuration['pid']
#            except KeyError:
#                return
#
#            pid_file_path = self.__configuration['pid']['pid_file_path']
            if pid_file_path is None:
                print('pid file path is None')
                return

            folders = pid_file_path.split('/')[:-1]
            pid_file_folder = '/'.join(folders)

            if not os.path.exists(pid_file_folder) and pid_file_folder != '':
                os.makedirs(pid_file_folder)
                print('{} directory made'.format(pid_file_folder))

            if len(suffix) != 0:
                if len(pid_file_path) < len(suffix):
                    pid_file_path = pid_file_path + '.pid'
                elif pid_file_path[-4:] != '.pid':
                    pid_file_path = pid_file_path + '.pid'

            self.__write_pid(pid_file_path)

        def __write_pid(self, pid_file_path):
            with open(pid_file_path, 'w') as pid_out_file:
                pid_out_file.write('{}'.format(os.getpid()))

        def __configure_logging(self):
            # logging initializing
            try:
                logout = self.__configuration['logging']['logout']
                debug_mode = self.__configuration['logging']['debug'] == 'true'
                logging_level = logging.DEBUG if debug_mode else logging.INFO

                if logout == 'stdout' or logout == '':
                    logging.basicConfig(
                        format='\
                            \r%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S',
                        level=logging_level)
                else:
                    logging.basicConfig(
                        filename=logout, filemode='w',
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S',
                        level=logging_level)
            except BaseException:
                print('logging in not configured')
                pass

        def __set_signal_handlers(self):
            if self.__signal_handlers is None:
                return

            # TODO the right methods for solve this problem using config
            # check if it lambda(handler), string(config arg) or
            # int(exit code)_
            for sig, action in self.__signal_handlers.items():
                assert isinstance(sig, type(signal.SIGINT))

                if isinstance(action, int):
                    exit_code = action
                    signal.signal(
                        sig,
                        lambda signal, frame: sys.exit(exit_code))
                # TODO improve types
                elif isinstance(action, type(lambda x: x)):
                    signal.signal(
                        sig,
                        lambda *args, **kwargs: action(*args, **kwargs))
                # TODO change exception types and messages
                else:
                    raise BaseException('type of signal handler is unknown')

    instance = None

    # singletone methods
    def __init__(self, *args, **kwargs):
        if Service_utils.instance is None:
            Service_utils.instance = Service_utils.__Service_utils(
                *args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def get_configuration(self):
        if Service_utils.instance.get_configuration() is None:
            return None
        return dict([
            (i, dict(j.items()))
            for i, j in Service_utils.instance.get_configuration().items()])

    def get_args(self):
        return Service_utils.instance.get_args()
