import os
import sys
import time
import re

import digitalocean

regex = re.compile('[2-8]{1}')
droplets = digitalocean.Manager().get_all_droplets(tag_name='ovirt-host')

stream = os.popen('source auth.sh')
output = stream.read()
print(output)

try:
    os.environ['OVIRT_FQDN']
    os.environ['OVIRT_URL']
    os.environ['OVIRT_USERNAME']
    os.environ['OVIRT_PASSWORD']
    os.environ['DIGITALOCEAN_ACCESS_TOKEN']
    os.environ['ANSIBLE_HOST_KEY_CHECKING']
except KeyError:
    print ("Please set environment variables")
    sys.exit(1)

for droplet in droplets:
    if regex.findall(droplet.name):
        while not droplet.ip_address:
            time.sleep(1)
            droplet.load()
        print(droplet.name, ' ', droplet.ip_address)

        for action in droplet.get_actions():
            while action.status != 'completed':
                time.sleep(1)
                action.load()

        stream = os.popen(
            'ansible-playbook -vvv -i $OVIRT_FQDN, -u root -e ovirt_host={} -e ovirt_address={} ansible/add_host.yml'.format(
                droplet.name, droplet.ip_address)
        )
        output = stream.read()
        print(output)
