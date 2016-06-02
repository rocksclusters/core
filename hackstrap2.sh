#!/bin/bash
# Hacky bootstrap if given the core roll iso
# Creates in local directory
ISO=$1
CURDIR=$(pwd)
mount -o loop $ISO /mnt
find /mnt -name 'rocks-devel*rpm' -exec yum -y install {} \;
. /etc/profile.d/rocks-devel.sh

# Now copy the RPMS from the ISO to local RPMS directory
mkdir $CURDIR/RPMS
find /mnt -name '*rpm' -print -exec cp -p {} $CURDIR/RPMS \; 
umount /mnt

## Install all RPMS defined in the corestrap-packages.xml file (which is in
## the roll-core-kickstart rpm
cp /opt/rocks/share/devel/src/roll/template/Makefile . 
cat /opt/rocks/share/devel/src/roll/template/version.mk | sed -e 's/@template@/core/' > version.mk
make createlocalrepo
PKGS=$(mktemp)
rpm2cpio $CURDIR/RPMS/noarch/roll-*-kickstart-*.noarch.rpm | cpio -i --quiet --to-stdout '*/corestrap-packages.xml' | grep "<package>" | cut -d '>' -f 2 | cut -d '<' -f 1 > $PKGS
yum -c yum.conf install `cat $PKGS`
/bin/rm $PKGS

# Get the nodes/graphs files from the roll itself. These  will be put under
# $CURDIR/export/profile
rpm2cpio $CURDIR/RPMS/noarch/roll-*-kickstart-*.noarch.rpm | cpio -id 

# Now bootstrap the database
NODES=export/profile/nodes
tmpfile=$(/bin/mktemp)
/bin/cat $NODES/database.xml $NODES/database-schema.xml $NODES/database-sec.xml | /opt/rocks/bin/rocks report post attrs="{'hostname':'', 'HttpRoot':'/var/www/html','os':'linux'}"  > $tmpfile
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

#4a.  Define the repository directory
if [ "x$2" == "x" ]; then
	DISTRODIR="/export/rocks"
else
	DISTRODIR="$2"
fi
#4 create a repo entry for rocks-dist distribution
REPONAME=/etc/yum.repos.d/rocks-local.repo
if [ ! -f $REPONAME ]; then
cat > $REPONAME << EOF
[Rocks-`/opt/rocks/bin/rocks report version`]
name=Rocks
baseurl=file://$DISTRODIR/install/rocks-dist/`uname -i`
enabled = 1
gpgcheck = 0
EOF
fi

#5 Add the core roll and enable it
/opt/rocks/bin/rocks add roll $1
ROLL=`echo $1 | cut -d - -f 1`
/opt/rocks/bin/rocks enable roll $ROLL

. /etc/profile.d/rocks-binaries.sh

pushd $DISTRODIR/install 
/opt/rocks/bin/rocks create distro
popd

#6 Some additional attributes. These are needed for the KVM roll,e.g.,
/opt/rocks/bin/rocks add attr Kickstart_PublicHostname $MYNAME 
/opt/rocks/bin/rocks add attr Kickstart_PublicAddress 127.0.0.1 
/opt/rocks/bin/rocks add attr Kickstart_PrivateGateway 127.0.0.1 
/opt/rocks/bin/rocks add attr Kickstart_PrivateDNSServers 127.0.0.1 
/opt/rocks/bin/rocks add attr Kickstart_PrivateNetmask 255.255.255.0 
/opt/rocks/bin/rocks add attr Kickstart_PrivateNetwork  127.0.0.0 
/opt/rocks/bin/rocks add attr Kickstart_PrivateKickstartHost 127.0.0.1 
# This will keep rocks sync config from updating system files
/opt/rocks/bin/rocks add attr Config_NoUpdate true


#7 Run the roll 
SCRIPT=$(mktemp)
/opt/rocks/bin/rocks run roll core > $SCRIPT
/sbin/service foundation-mysql stop
sh $SCRIPT
/bin/rm $SCRIPT
