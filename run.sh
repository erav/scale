#!/bin/bash

source auth.sh
engine=$OVIRT_FQDN
ssh root@$engine yum install -y https://resources.ovirt.org/pub/yum-repo/ovirt-release43.rpm
ssh root@$engine yum install -y ovirt-engine

ssh root@$engine -T "cat > /root/answerfile.txt" <<EOF
[environment:default]
OVESETUP_CONFIG/fqdn=str:$OVIRT_FQDN
OVESETUP_CONFIG/adminPassword=str:$OVIRT_PASSWORD
VESETUP_OVN/ovirtProviderOvn=bool:False
OVESETUP_CONFIG/websocketProxyConfig=bool:False
OVESETUP_VMCONSOLE_PROXY_CONFIG/vmconsoleProxyConfig=bool:False
EOF

if [ $(ssh root@engine ps -AF | grep ovirt-engine | wc -l) -eq 1 ]; do
	echo 'setting up engine on $engine'
	ssh root@$engine engine-setup --accept-defaults --offline --config-append=/root/answerfile.txt
	sleep(30)
	echo 'setup engine done'
fi

ansible-playbook add_networks.yml

