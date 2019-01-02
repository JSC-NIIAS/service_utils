# service requirements
import os
import logging
import json
import argparse
import signal
import sys
import configparser
import re


class Service_utils:
    class __Service_utils:
        def __init__(
                self,
                configuration_key,
                configuration_required=False,
                configuration_default_path=None,
                description=''):

            # initialize shell arguments parser
            parser = argparse.ArgumentParser(
                description=description)
            parser.add_argument(
                configuration_key,
                metavar='path_to_configuration_file',
                required=configuration_required,
                help='Path to configuration file.')
            args = parser.parse_args()
            args = dict(args._get_kwargs())

            configuration_key = re.sub('^-+', '', configuration_key)
            configuration_key = re.sub('-', '_', configuration_key)
            configuration_path = configuration_default_path

            if configuration_required is False:
                if args[configuration_key] is None:
                    print('''
                        configuration_path is not exist and it\'s\
                        not required''')
                    print('''
                        configuration_path is set as default''')
                else:
                    configuration_path = args[configuration_key]
                    print('config is not required but it exist')
            else:
                if args[configuration_key] is None:
                    print('config is required but it doesn\'t exist')
                    raise BaseException
                else:
                    configuration_path = args[configuration_key]

            print('configuration_path:', configuration_path)
            configuration = configparser.ConfigParser()
            configuration.read(configuration_path)

            if list(configuration.keys()) == ['DEFAULT']:
                print('Bad config.')
                raise BaseException
            else:
                print('Good config.')

    instance = None

    def __init__(self, *args, **kwargs):
        if Service_utils.instance is None:
            instance = Service_utils.__Service_utils(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.instance, name)

if False:


    # variables
    # signal vars
    handle_sigint_as_terminate = True
    sigint_exit_code = 0

    # shell args
    description = 'Description of service. It will be used in argparse.'
    default_symbol = '%'

    # configuration args
    config_key = '-c'
    default_config = None
    default_config_path = None

    # pid args
    pid_key = '-p'
    pid_out_file = None

    # logging
    support_logging = True

    # interrupt handler for closing application by user ctrl-C signal
    if handle_sigint_as_terminate:
        signal.signal(
            signal.SIGINT, lambda signal, frame: sys.exit(sigint_exit_code))

    # arguments parsing
    parser = argparse.ArgumentParser(
        description=description)

    if config_key is not None and type(config_key) == str:
        required = default_config is not None
        print(required)
        print(config_key)
        parser.add_argument(
            config_key,
            metavar='path_to_configuration_file',
            required=required,
            help='Path to configuration file.')

    if pid_key is not None and type(pid_key) == str:
        required = pid_out_file is not None
        parser.add_argument(
            pid_key,
            metavar='pid_file_name',
            required=required,
            help='Path to file which will contain pid of the process.')

    # start actions
    # read arguments
    args = parser.parse_args()

    # create pid file for closing application outside

    if pid_out_file is not None:
        folders = pid_out_file.split('/')[:-1] 
        pid_file_folder = '/'.join(folders)

        if not os.path.exists(pid_file_folder):
            os.makedirs(pid_out_file)

    if args.p == default_symbol or args.p is None:
        args.p = pid_out_file

    if args.p is not None:
        if args.p[-4:] != '.pid':
            args.p = args.p + '.pid'

        with open(args.p, 'w') as pid_out_file:
            pid_out_file.write('{}'.format(os.getpid()))

    # config reading

    def get_config():
        data = configparser.ConfigParser()
        if args.c == default_symbol or args.c is None:
            if default_config is not None:
                data = default_config
            if default_config_path is not None:
                data.read(default_config_path)
        else:
            data.read(parser.parse_args().c)

        return data

    data = get_config()

    # logging initializing
    try:
        logout = data['logout']['logout']
        debug_mode = data['logout']['debug'] == 'true'
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
        pass
