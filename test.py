from service_utils import Service_utils

service_utils = Service_utils(
    '--config-key',
    configuration_required=True,
    configuration_default_path={'a':3})

while True:
    print(input('write msg:'))
