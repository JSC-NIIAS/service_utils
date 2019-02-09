from service_utils import Service_utils
import logging
import signal


def kill_handler(frame, signal):
    print('kill without -9 doesn\'t works here')


service = Service_utils(
    keys_required={
        '-p': None
    },
    keys_optional={
        '-c': None
    },
    description='interactive example of service utils')

service.start()

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
