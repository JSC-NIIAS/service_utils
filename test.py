from service_utils import Service_utils

service_utils = Service_utils(
    '--config-key',
    configuration_required=True,
    configuration_default_path='path_to_default_config.ini')

greeting = 'write msg'
try:
    greeting = service_utils.get_configuration()['user']['greeting']
except Exception:
    print('Something thorw an exception')

print(greeting)
