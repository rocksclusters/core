#! @PYTHON@
#
# $Id: rocks-console.py,v 1.19 2012/11/27 00:48:08 phil Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
# 
# Copyright (c) 2000 - 2014 The Regents of the University of California.
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
# $Log: rocks-console.py,v $
# Revision 1.19  2012/11/27 00:48:08  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.18  2012/05/06 05:48:17  phil
# Copyright Storm for Mamba
#
# Revision 1.17  2012/04/03 23:30:36  phil
# Should now work on 5 and 6.
#
# Revision 1.16  2011/07/23 02:30:23  phil
# Viper Copyright
#
# Revision 1.15  2010/09/07 23:52:48  bruno
# star power for gb
#
# Revision 1.14  2009/06/18 04:25:00  bruno
# for anoop. he owes me *at least* a couple beers.
#
# Revision 1.13  2009/05/01 19:06:50  mjk
# chimi con queso
#
# Revision 1.12  2008/10/18 00:55:47  mjk
# copyright 5.1
#
# Revision 1.11  2008/03/06 23:41:32  mjk
# copyright storm on
#
# Revision 1.10  2007/06/23 04:03:19  mjk
# mars hill copyright
#
# Revision 1.9  2007/06/14 16:01:43  bruno
# in ananconda 10.1.1.63, when running ekv on the frontend (for a remote
# reinstall), the environment doesn't map 'localhost' to 127.0.0.1 -- so
# let's explicitly tunnel to 127.0.0.1 instead of localhost.
#
# Revision 1.8  2006/09/11 22:47:02  mjk
# monkey face copyright
#
# Revision 1.7  2006/08/10 00:09:25  mjk
# 4.2 copyright
#
# Revision 1.6  2006/08/09 15:41:38  anoop
# Changes to shootnode and rocks-console. These changes were necessary to
# support shooting multiple nodes in one command. The threading in shoot-node
# would cause a lot of problems because multiple threads would try to manipulate
# stderr, and all would fail but one.
#
# Also race conditions are created by the presence of threads, and so sockets need
# to be released only at the last possible moment, to avoid multiple bindings.
#
# Revision 1.5  2006/07/10 22:40:40  anoop
# Silly little bug removed.
#
# Revision 1.4  2006/07/03 22:13:11  anoop
# Rocks console can connect to multiple servers now without barfing
#
# Revision 1.3  2006/06/16 21:09:01  bruno
# make default local port for ekv to be 8000
#
# Revision 1.2  2006/06/15 23:04:51  bruno
# name the vncviewer window to the same name as the node it is connected to
#
# Revision 1.1  2006/06/15 21:28:47  bruno
# new command to get the vnc and ekv consoles on an installing node
#
#
#

import os
import sys
import rocks.app
import socket
import time
import subprocess 
		        
class App(rocks.app.Application):

	def __init__(self, argv):
		rocks.app.Application.__init__(self, argv)	

		self.usage_name = 'Rocks Console'
		self.usage_version = '@VERSION@'

		self.nodename = ''
		self.known_hosts = '/tmp/.known_hosts'
		self.defaultport = 5901
		self.sshport	= 22
		if self.usage_version.split('.')[0] == '6':	
			self.remotedefaultport = 5900
			self.sshport = 2200
		else:
			self.remotedefaultport = self.defaultport 
		self.localport = 0
		self.remoteport = 0
		self.ekv = 0

		porthelp = '(port number of VNC server - default = %d)' \
			% (self.defaultport)


		self.getopt.l.extend([
				'ekv',
				('port=', porthelp)
			])

		return


	def parseArg(self, c):
		rocks.app.Application.parseArg(self, c)

		key, val = c
		if key in ('--port'):
			self.localport = int(val)
		elif key in ('--ekv'):
			self.ekv = 1

		return


	def usageTail(self):
		return ' <nodename (e.g., compute-0-0)>\n'


	def ekvviewer(self):
		cmd = 'telnet localhost %d' % (self.localport)
		os.system(cmd)
		return


	def vncviewer(self):
		cmd = 'vncviewer localhost:%d' \
			% (self.localport - self.defaultport + 1)
		os.system(cmd)

		return

	def createSecureTunnel_linux(self):
		#
		# use a temporary file to store the host key. we do this
		# because a new temporary host key is created in the
		# installer and if we add this temporary host key to
		# /root/.ssh/known_hosts, then the next time the node is
		# installed, the ssh tunnel will get a 'man-in-middle' error
		# and not allow port forwarding.
		#
		self.known_hosts = "%s_%s" % (self.known_hosts,self.nodename)
		if os.path.exists(self.known_hosts):
			os.unlink(self.known_hosts)

		cmd = 'ssh -q -f -o UserKnownHostsFile=%s ' % (self.known_hosts)
		cmd += '-o GlobalKnownHostsFile=%s ' % (self.known_hosts)
		cmd += '-L %d:127.0.0.1:%d ' % (self.localport, self.remoteport)
		cmd += '%s -p %d ' % (self.nodename,self.sshport)
		cmd += '\'/bin/bash -c "sleep 20"\' '
		self.s.close()
		os.system(cmd)


	def createSecureTunnel_sunos(self):
		#
		# use a temporary file to store the host key. we do this
		# because a new temporary host key is created in the
		# installer and if we add this temporary host key to
		# /root/.ssh/known_hosts, then the next time the node is
		# installed, the ssh tunnel will get a 'man-in-middle' error
		# and not allow port forwarding.
		#
		self.known_hosts = "%s_%s" % (self.known_hosts,self.nodename)
		if os.path.exists(self.known_hosts):
			os.unlink(self.known_hosts)

		cmd = 'ssh -q -f -o UserKnownHostsFile=%s ' % (self.known_hosts)
		cmd +='-o XAuthLocation=/tmp/root/.TTauthority '
		cmd += '-L %d:localhost:%d ' % (self.localport, self.remoteport)
		cmd += '%s -p 2200 ' % (self.nodename)
		cmd +="\'/tmp/root/usr/bin/x11vnc -display :0 "	\
			"-quiet -once -nopw -rfbport %d -auth "	\
			"/tmp/root/.TTauthority -localhost -noshm\'" % self.remoteport
		self.s.close()
		print cmd
		os.system(cmd)
		time.sleep(5)
		return



	def createSecureTunnel(self):

		cmd = "rocks report host attr attr=os %s " % self.nodename 
		p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
	
		r,w = (p.stdout, p.stdin)
		w.close()
		osname = r.readline().strip()
		if osname == '':
			osname = 'linux'
		f = getattr(self, "createSecureTunnel_%s" % osname)	
		f()
		return


	def run(self):
		if len(self.args) > 0:
			self.nodename = self.args[0]
		else:
			print '\n\t"nodename" was not specified\n'
			self.usage()
			sys.exit(-1)

		self.nodename = self.args[0]

		if self.ekv == 1:
			if self.localport == 0:
				self.localport = 8000
			self.remoteport = 8000
		else:
			if self.localport == 0:
				self.localport = self.defaultport
			self.remoteport = self.remotedefaultport

		# Check ports to see which one is open. If ports are already bound
		# go to the next one to check. Whatever binds is successfully is used.
		self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		done = 0
		while(done == 0):
		 	try:
				self.s.bind(("localhost",self.localport))
				done = 1
			except socket.error,(errno,string):
			   if(errno == 98):
				done = 0
				self.localport = self.localport + 1
		
		#Connect to the secure tunnel and go...
		self.createSecureTunnel()

		if self.ekv == 1:
			self.ekvviewer()
		else:
			self.vncviewer()

		return


app = App(sys.argv)
app.parseArgs()
app.run()

