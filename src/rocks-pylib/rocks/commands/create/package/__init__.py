# $Id: __init__.py,v 1.9 2012/11/27 00:48:11 phil Exp $
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
# $Log: __init__.py,v $
# Revision 1.9  2012/11/27 00:48:11  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.8  2012/05/06 05:48:22  phil
# Copyright Storm for Mamba
#
# Revision 1.7  2011/07/23 02:30:27  phil
# Viper Copyright
#
# Revision 1.6  2011/01/24 17:54:44  mjk
# Disable RPM computing the provides list
#
# Revision 1.5  2010/09/07 23:52:52  bruno
# star power for gb
#
# Revision 1.4  2009/05/01 19:06:56  mjk
# chimi con queso
#
# Revision 1.3  2008/10/18 00:55:48  mjk
# copyright 5.1
#
# Revision 1.2  2008/08/20 23:22:46  mjk
# docstring
#
# Revision 1.1  2008/08/20 22:15:16  mjk
# works / needs docstring
#

import os
import tempfile
import shutil
import rocks.commands

		
class Command(rocks.commands.create.command):
	"""
	Create a RedHat or Solaris package from a given directory.  The
	package will install files in either the same location as the given
	directory, or a combination of the directory basename and the
	provided prefix.

	<arg type='string' name='directory'>
	The source directory of the files used to create the OS-specific
	package.
	</arg>

	<param type='string' name='prefix'>
	The prefix pathname prepended to the base name of the source
	directory.
	</param>

	<param type='string' name='version'>
	Version number of the created package (default is '1.0')
	</param>

	<param type='string' name='release'>
	Release number of the created package (default is '1')
	</param>

	<param type='string' name='append-version-mk'>
	Append the named file to the automatically created version.mk file.
	This can be used to override any directives. Often used to define
	the specific files that the package includes with RPM.FILES = directive
	(Default is None)
	</param>

	<example cmd='create package /opt/stream stream'>
	Create a package named stream in the current directory using the
	contents of the /opt/stream directory.  The resulting package will
	install its files at /opt/stream.
	</example>

	<example cmd='create package /opt/stream localstream prefix=/usr/local'>
	Create a package named localstream in the current directory using the
	contents of the /opt/stream directory.  The resulting package will
	install its files at /usr/local/stream.
	</example>
	
	"""

	def run(self, params, args):

		(args, name) = self.fillPositionalArgs(('name', ))

		if len(args) != 1:
			self.abort('must supply directory name')
			
		if not name:
			self.abort('must supply package name')

		dir = args[0]
			
		(version, release, prefix, append_version_mk) = self.fillParams(
			[('version', '1.0'),
			('release', '1'),
			('prefix', None),
			('append-version-mk', None)
			])
		
		rocksRoot = os.environ['ROCKSROOT']

		if not prefix:
			prefix = os.path.split(dir)[0]
		
		tmp = tempfile.mktemp()
		os.makedirs(tmp)
		shutil.copy(os.path.join(rocksRoot,'etc', 'create-package.mk'),
			    os.path.join(tmp, 'Makefile'))
		cwd = os.getcwd()
		os.chdir(tmp)


		nofiles = open(os.path.join(tmp, 'rocks.empty'),'w')
		nofiles.write('')
		nofiles.close()
		file = open(os.path.join(tmp, 'version.mk'), 'w')
		file.write('NAME=%s\n' % name)
		file.write('VERSION=%s\n' % version)
		file.write('RELEASE=%s\n' % release)
		file.write('PREFIX=%s\n' % prefix)
		file.write('SOURCE_DIRECTORY=%s\n' % dir)
		file.write('DEST_DIRECTORY=%s\n' % cwd)
		file.write('RPM.EXTRAS=AutoReqProv: no\n')

		if append_version_mk is not None:
			try:
				f = open(append_version_mk,'r')
				for line in f.readlines():
					file.write(line)
			except:
				print "Error: Could not open/read %s" % append_version_mk
		else:
			files=[]
			for root,subdir,fs in os.walk(dir):
				for ff in fs:
					files.append(os.path.join(root,ff))
			if len(files) > 0:
				file.write('RPM.FILES=%s\n' % "\\n".join(files))
			else:
				file.write('RPM.FILESLIST=rocks.empty\n')
		file.close()

		for line in os.popen('make dir2pkg').readlines():
			self.addText(line)

		# shutil.rmtree(tmp)
