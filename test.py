from service_utils import Service_utils

service_utils = Service_utils(
    keys_required={
        '-c': Service_utils.Actions.read_configuration,
        '-p': Service_utils.Actions.write_pid_in_file
    },
    keys_optional={
    },
    config_sections={
    },
    description='interactive example of service utils')

greeting = 'write msg'
try:
    greeting = service_utils.get_configuration()['user']['greeting']
except Exception:
    print('Something thorw an exception')

print(greeting)
