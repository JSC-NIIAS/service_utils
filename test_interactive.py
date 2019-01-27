from service_utils import Service_utils
import logging
import signal


def kill_handler(frame, signal):
    print('kill without -9 doesn\'t works here')


service_utils = Service_utils(
    keys_required={
        '-c': Service_utils.Actions.read_configuration,
        '-p': Service_utils.Actions.write_pid_in_file
    },
    keys_optional={
    },
    config_sections={
    },
    signal_handlers={
        signal.SIGINT: 22,
        signal.SIGTERM: kill_handler
        },
    description='interactive example of service utils')

print('service_utils initialized')
print('configuration:\n{}'.format(service_utils.get_configuration()))
print('args:\n{}'.format(service_utils.get_args()))

greeting = 'write msg'
try:
    greeting = service_utils.get_configuration()['user']['greeting']
except Exception:
    print('Something thorw an exception in configuration reading.')

while True:
    logging.debug(input(greeting + ' : '))
