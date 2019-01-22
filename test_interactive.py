from service_utils import Service_utils
import logging

service_utils = Service_utils(
    '--config-key',
    configuration_required=True,
    configuration_default_path='path_to_default_config.ini')

greeting = 'write msg'
try:
    greeting = service_utils.get_configuration()['user']['greeting']
except:
    pass

while True:
    logging.debug(input(greeting + ' : '))