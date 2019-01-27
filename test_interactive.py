from service_utils import Service_utils
import logging
import signal


def kill_handler(frame, signal):
    print('kill without -9 doesn\'t works here')


service_utils = Service_utils(
    '--config-key',
    configuration_required=True,
    configuration_default_path='path_to_default_config.ini',
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
    print('Something thorw an exception')

while True:
    logging.debug(input(greeting + ' : '))
