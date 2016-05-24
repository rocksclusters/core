#!/bin/bash
# Hacky bootstrap if given the core roll iso
# Creates in local directory
ISO=$1
CURDIR=$(pwd)
mount -o loop $ISO /mnt
find /mnt -name 'rocks-devel*rpm' -exec yum -y install {} \;
. /etc/profile.d/rocks-devel.sh

mkdir $CURDIR/RPMS
find /mnt -name '*rpm' -print -exec cp -p {} $CURDIR/RPMS \; 
umount /mnt

## Install all RPMS defined in this roll iso
cp /opt/rocks/share/devel/src/roll/template/Makefile . 
cat /opt/rocks/share/devel/src/roll/template/version.mk | sed -e 's/@template@/core/' > version.mk
make createlocalrepo
yum -c yum.conf --disablerepo='*' --enablerepo=core-roll list available | grep core-roll | awk '{print $1}' | awk -F. '{print $1}' | grep -v 'roll.*kickstart' | less | xargs yum -y -c yum.conf install

# Get the nodes/graphs files from the roll itself
rpm --relocate=/export/profile=`pwd` -ivh RPMS/roll-core-kickstart-6.3-2.noarch.rpm 
. /etc/profile.d/rocks-binaries.sh

# Now bootstrap the database
tmpfile=$(/bin/mktemp)
/bin/cat nodes/database.xml nodes/database-schema.xml nodes/database-sec.xml | /opt/rocks/bin/rocks report post attrs="{'hostname':'', 'HttpRoot':'/var/www/html','os':'linux'}"  > $tmpfile
if [ $? != 0 ]; then echo "FAILURE to create script for bootstrapping the Database"; exit -1; fi
/bin/sh $tmpfile
# /bin/rm $tmpfile
MYNAME=`hostname -s`
/opt/rocks/bin/rocks add distribution rocks-dist
/opt/rocks/bin/rocks add appliance bootstrap node=server
/opt/rocks/bin/rocks add host $MYNAME rack=0 rank=0 membership=bootstrap
/opt/rocks/bin/rocks add network private 127.0.0.1 netmask=255.255.255.255
MAC=`/sbin/ifconfig -a | grep -i HWADDR | head -1 | /bin/awk '{print $NF}'`
/opt/rocks/bin/rocks add host interface $MYNAME lo subnet=private ip=127.0.0.1 mac=$MAC
/opt/rocks/bin/rocks add attr os `./_os` 


#3. Add appliance types so that we can build the other Rolls
/opt/rocks/bin/rocks add attr Kickstart_PrivateKickstartBasedir install
/opt/rocks/bin/rocks add appliance compute graph=default node=compute membership=Compute public=yes
/opt/rocks/bin/rocks add attr rocks_version `/opt/rocks/bin/rocks report version`
/opt/rocks/bin/rocks add attr rocks_version_major `/opt/rocks/bin/rocks report version major=1`

#4 create a repo entry for rocks-dist distribution
REPONAME=/etc/yum.repos.d/rocks-local.repo
if [ ! -f $REPONAME ]; then
cat > $REPONAME << EOF
[Rocks-`/opt/rocks/bin/rocks report version`]
name=Rocks
baseurl=file:///export/rocks/install/rocks-dist/`uname -i`
enabled = 1
EOF
fi

#5 Add the core roll and enable it
/opt/rocks/bin/rocks add roll $1
ROLL=`echo $1 | cut -d 1 -f 1`
/opt/rocks/bin/rocks/enable roll $ROLL

. /etc/profile.d/rocks-binaries.sh

#6 Some additional attributes. These are needed for the KVM roll,e.g.,
/opt/rocks/bin/rocks add attr Kickstart_PublicHostname $MYNAME 
/opt/rocks/bin/rocks add attr Kickstart_PrivateGateway 127.0.0.1 
/opt/rocks/bin/rocks add attr Kickstart_PrivateDNSServers 127.0.0.1 
/opt/rocks/bin/rocks add attr Kickstart_PrivateNetMask 255.255.255.0 
/opt/rocks/bin/rocks add attr Kickstart_PrivateKickstartHost 127.0.0.1 

#7 Install packages from the core roll
PKGS=`/opt/rocks/bin/rocks list host profile localhost | /bin/awk '/%packages/,/%end/' | /usr/bin/head -n -1 | /usr/bin/tail -n +2` 
/usr/bin/yum -y --nogpgcheck install $PKGS
