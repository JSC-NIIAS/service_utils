from service_utils import Service_utils
import logging
import signal


def kill_handler(frame, signal):
    print('kill without -9 doesn\'t works here')


service = Service_utils(
    keys_required={
        '-p': Service_utils.Actions.write_pid_in_file
    },
    keys_optional={
        '-c': Service_utils.Actions.read_configuration,
    },
    signal_handlers={
        signal.SIGINT: 22,
        signal.SIGTERM: kill_handler
        },
    description='interactive example of service utils')

print('service start')
print('configuration:\n{}'.format(service.get_configuration()))
print('args:\n{}'.format(service.get_args()))

greeting = 'write msg'
try:
    greeting = service.get_configuration()['user']['greeting']
except Exception:
    print('Something thorw an exception in configuration reading.')

print(service.get_configuration())
print(service.get_args())

while True:
    logging.debug(input(greeting + ' : '))
