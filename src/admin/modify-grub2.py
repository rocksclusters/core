#!/usr/bin/env python
## This reads /etc/sysconfig/grub file, searches for the
## a keyword and either appends or replaces values for that particular
## keyword
import sys
import os
import getopt
params = { 'grubfile':"/etc/sysconfig/grub",
	    'keyword':"GRUB_CMDLINE_LINUX",
	    'mode':"append" }

def parseArgs(params,argv):
	opts,args = getopt.getopt(argv[1:],"f:k:m:",["file=","keyword=","mode="])
	for o,a in opts:
		if o in ["-f","--file="]:
			params['grubfile'] = a
		elif o in ["-k","--keyword="]:
			params['keyword'] = a
		elif o in ["-m","--mode="]:
			params['mode'] = a
	return args

def grub_append(line,keyword,args):
	if keyword in line:
		rhs=line.split("=",1)[-1]
		if rhs.startswith('"'):
			rhs=rhs[1:]
		if rhs.endswith('"'):
			rhs=rhs[:-1]

		comps=rhs.split()
		for x in args:
			if x not in comps:
				comps.append(x)
		return '%s="' % keyword + " ".join(comps) + '"'
	else:
		return line
	

def grub_delete(line,keyword,args):
	if keyword in line:
		rhs=line.split("=",1)[-1]
		if rhs.startswith('"'):
			rhs=rhs[1:]
		if rhs.endswith('"'):
			rhs=rhs[:-1]

		comps=rhs.split()
		for x in args:
			if x in comps:
				comps.remove(x)
		return '%s="' % keyword + " ".join(comps) + '"'
	else:
		return line
	

def grub_replace(line,keyword,args):
	if keyword in line:
		rhs=line.split("=",1)[-1]
		return '%s="' % keyword + " ".join(args) + '"'
	else:
		return line
	

### Main Program
args = parseArgs(params,sys.argv)

# if there is nothing to do, leave the file alone
if len(args) == 0:
	sys.exit(0)
try:
	f = open(params['grubfile'],"r")
except:
	sys.stderr.write('cannot open file %s\n' % params['grubfile'])
	sys.exit(-1)
output=[]
for line in f.readlines():
	cmd = "grub_%s(line.strip(),params['keyword'],args)" % params['mode']
	output.append(eval(cmd))
f.close()
try: 
	f = open(params['grubfile'],"w")
except:
	sys.stderr.write('cannot open file %s for writing\n' % params['grubfile'])
	sys.exit(-1)

# write the modified output
for o in output:
	f.write("%s\n" % o)
f.close()	
