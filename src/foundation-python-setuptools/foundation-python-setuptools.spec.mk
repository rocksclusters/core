# This file is called from the generated spec file.
# It can also be used to debug rpm building.
# 	make -f foundation-python-setuptools.spec.mk build|install

ifndef __RULES_MK
build:
	make ROOT=/export/home/repositories/rocks/src/roll/core/src/foundation-python-setuptools/foundation-python-setuptools.buildroot build

install:
	make ROOT=/export/home/repositories/rocks/src/roll/core/src/foundation-python-setuptools/foundation-python-setuptools.buildroot install
endif
