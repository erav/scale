import os
import sys
import digitalocean

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

#droplets = digitalocean.Manager().get_all_droplets()
droplets = digitalocean.Manager().get_all_droplets(tag_name='ovirt-host')

stream = os.popen('source auth.sh')
output = stream.read()
print(output)
for droplet in droplets:
    droplet.destroy()
