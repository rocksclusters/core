NAME	= foundation-python-extras
RELEASE = 2
RPM.EXTRAS="%define _python_bytecompile_errors_terminate_build 0"

ifeq ($(strip $(VERSION.MAJOR)), 7)
EXTRAFILES = "\\n/opt/rocks/include/gobject*\\n/opt/rocks/share/man/man1/*\\n/opt/rocks/lib/[a-oq-zA-Z]*"
else
EXTRAFILES = 
endif

RPM.FILES = "/opt/rocks/share/[a-ln-zA-Z]*\\n/opt/rocks/bin/*\\n/opt/rocks/include/pycairo*\\n/opt/rocks/include/pyg*\\n/opt/rocks/include/python2.[67]/*\\n/opt/rocks/lib/pkgconfig/*\\n/opt/rocks/lib/pyg*\\n/opt/rocks/lib/python2.[67]/site-packages/*"

RPM.FILES += $(EXTRAFILES)
