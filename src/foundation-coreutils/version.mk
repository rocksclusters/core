NAME	= foundation-coreutils
VERSION = 8.9
ifeq ($(strip $(VERSION.MAJOR)), 7)
VERSION = 8.22
endif
RELEASE = 0
