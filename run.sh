source auth.sh
engine=2a03:b0c0:3:d0::dd7:9001
ssh root@$engine yum install -y https://resources.ovirt.org/pub/yum-repo/ovirt-release43.rpm
ssh root@$engine yum install -y ovirt-engine

OVESETUP_ENGINE_CONFIG/fqdn=str:$OVIRT_FQDN

ssh root@$engine -T "cat > /root/answerfile.txt" <<EOF
[environment:default]
OVESETUP_CONFIG/fqdn=str:$OVIRT_FQDN
OVESETUP_CONFIG/adminPassword=str:$OVIRT_PASSWORD
EOF

ssh root@$engine engine-setup --accept-defaults --offline --config-append=/root/answerfile.txt
ansible-playbook add_networks.yml

