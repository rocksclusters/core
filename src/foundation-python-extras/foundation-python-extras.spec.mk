# This file is called from the generated spec file.
# It can also be used to debug rpm building.
# 	make -f foundation-python-extras.spec.mk build|install

ifndef __RULES_MK
build:
	make ROOT=/export/home/repositories/rocks/src/roll/core/src/foundation-python-extras/foundation-python-extras.buildroot build

install:
	make ROOT=/export/home/repositories/rocks/src/roll/core/src/foundation-python-extras/foundation-python-extras.buildroot install
endif
