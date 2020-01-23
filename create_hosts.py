import time

import digitalocean

manager = digitalocean.Manager()
all_ssh_keys = manager.get_all_sshkeys()

host_tag = 'ovirt-host'

for i in range(0, 49):
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

print('booting ...')
time.sleep(60)

droplets = manager.get_all_droplets(tag_name=host_tag)

for droplet in droplets:
    print('ansible-playbook -i {}, prepare_host.yml &'.format(droplet.ip_address))


for droplet in droplets:
    print(
        'ansible-playbook -e ovirt_host={} -e ovirt_address={} add_host.yml &'.format(
            droplet.name, droplet.ip_address)
    )
