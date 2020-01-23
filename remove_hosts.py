import time

import digitalocean

manager = digitalocean.Manager()
all_ssh_keys = manager.get_all_sshkeys()

host_tag = 'ovirt-host'


droplets = manager.get_all_droplets()
# droplets = manager.get_all_droplets(tag_name=host_tag)

for droplet in droplets:
    droplet.destroy()
