import os
import sys
import time

import digitalocean

manager = digitalocean.Manager()
all_ssh_keys = manager.get_all_sshkeys()

host_tag = 'ovirt-host'

# digitalocean.Droplet.create_multiple seems to work only up to 10 dropletes
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

for i in range(0, 9):
    droplet_name= 'ovirt-43-host-{:02d}'.format(i)
    print('creating ' + droplet_name)
    droplet = digitalocean.Droplet(name=droplet_name,
                                   region='fra1',
                                   image='centos-7-x64',
                                   size_slug='s-1vcpu-2gb',
                                   ipv6=True,
                                   private_networking=True,
                                   monitoring=True,
                                   ssh_keys=all_ssh_keys,
                                   tags=[host_tag]
                                   )
    droplet.create()

droplets = manager.get_all_droplets(tag_name=host_tag)

for droplet in droplets:
    while not droplet.ip_address:
        time.sleep(1)
        droplet.load()
    print(droplet.name, ' ', droplet.ip_address, ' ', type(droplet.ip_address))

    for action in droplet.get_actions():
        while action.status != 'completed':
            time.sleep(1)
            action.load()

print('creating hosts done')
