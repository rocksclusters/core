#!/usr/bin/env python
import sys
import subprocess
import os.path

isoname=sys.argv[1]
cmd = ['isoinfo','-l','-R','-i', isoname]
p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
p.wait
lines = p.stdout.readlines()
ignore = ['.','..','TRANS.TBL','.discinfo']

files = []
curdir = None
for l in lines:
	if l.startswith("Directory"):
		curdir =  l.split()[-1] 

	else:
		try:
			file = l.split()[-1]
			mode = l.split()[0]
			if not mode.startswith('d') and curdir is not None and file not in ignore:
				files.append(os.path.join(curdir,file))
		except:
			pass
			
for f in files:
	print f
