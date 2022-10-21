from collections.abc import MutableMapping
from datetime import datetime
from influxdb_client import InfluxDBClient, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import json
import subprocess
import toml


def change_case(str):
    return ''.join(['_'+i.lower() if i.isupper()
                    else i for i in str]).lstrip('_')


def format_data(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = change_case(parent_key + sep + k if parent_key else k)
        if isinstance(v, MutableMapping):
            items.extend(format_data(v, new_key, sep=sep).items())
        else:
            if type(v) == bool:
                items.append((new_key, 'true' if v else 'false'))
            else:
                items.append((new_key, v))
    return dict(items)


result = json.loads(subprocess.run([
    'speedtest',
    '--accept-gdpr',
    '--accept-license',
    '--format',
    'json'
], stdout=subprocess.PIPE).stdout.decode('utf-8'))

data = format_data(result)

tag_keys = [
    'interface_external_ip',
    'interface_internal_ip',
    'interface_is_vpn',
    'interface_mac_addr',
    'interface_name',
    'isp',
    'result_persisted',
    'server_country',
    'server_host',
    'server_id',
    'server_ip',
    'server_location',
    'server_name',
    'server_port',
    'type'
]

timestamp = data.pop('timestamp')

tags = dict(sorted({tag: data[tag]
            for tag in data if tag in tag_keys}.items()))

fields = dict(sorted({field: data[field]
              for field in data if field not in tag_keys}.items()))

for key, value in tags.items():
    if type(value) == str:
        tags[key] = value.replace(' ', '\\ ')

for key, value in fields.items():
    if type(value) == str:
        fields[key] = '"{}"'.format(value)
    if type(value) == int and value >= 0:
        fields[key] = '{}u'.format(value)

lp = (
    'speed_test,' +
    ','.join('{}={}'.format(key, value) for key, value in tags.items()) +
    ' ' +
    ','.join('{}={}'.format(key, value) for key, value in fields.items()) +
    ' ' +
    str(int(datetime.fromisoformat(timestamp.replace('Z', '+00:00')).timestamp()))
)

print(lp)

influxdb_config = toml.load('/root/.influxdbv2/configs')

client = InfluxDBClient(
    url=influxdb_config['default']['url'],
    token=influxdb_config['default']['token'],
    org=influxdb_config['default']['org']
)

write_api = client.write_api(write_options=SYNCHRONOUS)

write_api.write(
    'speed_tests',
    influxdb_config['default']['org'],
    lp.encode(),
    WritePrecision.S
)
