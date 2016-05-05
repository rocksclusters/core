# This file is called from the generated spec file.
# It can also be used to debug rpm building.
# 	make -f rocks-pylib.spec.mk build|install

ifndef __RULES_MK
build:
	make ROOT=/export/home/repositories/rocks/src/roll/core/src/rocks-pylib/rocks-pylib.buildroot build

install:
	make ROOT=/export/home/repositories/rocks/src/roll/core/src/rocks-pylib/rocks-pylib.buildroot install
endif
