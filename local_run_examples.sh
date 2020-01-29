
$OVIRT_HOST_IP=

source auth.sh
ansible-playbook -vvv -i $OVIRT_HOST_IP, -u root prepare_host.yml

# check that password has been correctly set by prepare_host.yml
ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no root@$OVIRT_HOST_IP

# run the add_host.yml on the remote engine machine ($OVIRT_FQDN)
source auth.sh
ansible-playbook -vvv -i $OVIRT_FQDN, -u root -e ovirt_host=ovirt-43-host-01 -e ovirt_address=$OVIRT_HOST_IP add_host.yml

