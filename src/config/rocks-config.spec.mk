# This file is called from the generated spec file.
# It can also be used to debug rpm building.
# 	make -f rocks-config.spec.mk build|install

ifndef __RULES_MK
build:
	make ROOT=/export/home/repositories/rocks/src/roll/core/src/config/rocks-config.buildroot build

install:
	make ROOT=/export/home/repositories/rocks/src/roll/core/src/config/rocks-config.buildroot install
endif
