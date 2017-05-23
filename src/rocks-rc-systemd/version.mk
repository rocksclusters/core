NAME		= rocks-rc-systemd
RELEASE		= 0
PKGROOT		= /etc/systemd/system
RPM.FILES	= "$(PKGROOT)/*"
RPM.REQUIRES	= rocks-config
RPM.SCRIPTLETS.FILE = scriptlets
