#!/bin/sh
# This script properly re-adds the frontend's ssh host keys after 
# a restore roll has been executed.
CIPHERS=("rsa" "dsa" "ecdsa" "ed25519")
HOST=$(hostname -s)
echo "Removing host keys from Rocks DB and re-adding local..."
for x in ${CIPHERS[*]}; do
	/opt/rocks/bin/rocks remove host sec_attr $HOST ssh_host_${x}_key
	/opt/rocks/bin/rocks remove host sec_attr $HOST ssh_host_${x}_key.pub
   	/opt/rocks/bin/rocks add host sec_attr $HOST attr=ssh_host_${x}_key crypted=true value=/etc/ssh/ssh_host_${x}_key
   	/opt/rocks/bin/rocks add host sec_attr $HOST attr=ssh_host_${x}_key.pub crypted=true value=/etc/ssh/ssh_host_${x}_key.pub
done
echo "Synching configuration and forcing make in /var/411"
/opt/rocks/bin/rocks sync config
/usr/bin/make -C /var/411 force
