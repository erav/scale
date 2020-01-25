import digitalocean

host_tag = 'ovirt-host'


droplets = digitalocean.Manager().get_all_droplets()
#droplets = digitalocean.Manager().get_all_droplets(tag_name=host_tag)

for droplet in droplets:
    droplet.destroy()
