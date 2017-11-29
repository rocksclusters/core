#!/bin/bash
#
# This file should remain OS independent
# Bootstrap0: designed for "pristine" systems (aka no rocks)
# NOTE: This should not be used on ANY Rocks appliance. 
#
# $Id: prepdevel.sh,v 1.5 2012/11/27 00:48:00 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWindwer)
# 		         version 7.0 (Manzanita)
# 
# Copyright (c) 2000 - 2017 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#

. src/devel/devel/src/roll/etc/bootstrap-functions.sh

# 2. Create a fake bootstrap appliance, network, and host in the database
if [ `hostname | grep localhost` ] ; then
	# some built host (aka batlab) uses hostname == localhost
	# this confuses really all rocks command so let's avoid that
	MYNAME=develmachine
else
	MYNAME=`hostname -s`
fi

/opt/rocks/bin/rocks add distribution rocks-dist
/opt/rocks/bin/rocks add appliance bootstrap node=server
/opt/rocks/bin/rocks add host $MYNAME rack=0 rank=0 membership=bootstrap
/opt/rocks/bin/rocks add network private 127.0.0.1 netmask=255.255.255.255
/opt/rocks/bin/rocks add host interface $MYNAME lo subnet=private ip=127.0.0.1
/opt/rocks/bin/rocks add attr os `./_os` 
/opt/rocks/bin/rocks add attr arch `./_arch` 

# 2.5 add the Kickstart_PublicAddress
device=$(/usr/sbin/ip route list 0.0.0.0/0 | /usr/bin/cut -d ' ' -f5)
ipaddr=$(/usr/sbin/ip -4 address show dev eth0 | /usr/bin/grep inet | /usr/bin/awk '{print $2}' | /usr/bin/cut -d/ -f1)
/opt/rocks/bin/rocks add attr Kickstart_PublicAddress $ipaddr
/opt/rocks/bin/rocks add attr distribution rocks-dist 

# 3. Add appliance types so that we can build the OS Roll
/opt/rocks/bin/rocks add attr Kickstart_DistroDir /export/rocks
/opt/rocks/bin/rocks add attr Kickstart_PrivateKickstartBasedir install
/opt/rocks/bin/rocks add appliance compute graph=default node=compute membership=Compute public=yes
/opt/rocks/bin/rocks add attr rocks_version `/opt/rocks/bin/rocks report version`
/opt/rocks/bin/rocks add attr rocks_version_major `/opt/rocks/bin/rocks report version major=1`

# 4. Rest of packages for full build
if [ `./_os` == "linux" ]; then
        install_os_packages bootstrap-packages-core
fi

# 5. Add a rocks distribution to system
/usr/bin/cat nodes/yum-core.xml | /opt/rocks/bin/rocks report post attrs="`/opt/rocks/bin/rocks report host attr localhost pydict=true`" | sh
