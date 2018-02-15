ifeq ($(strip $(VERSION.MAJOR)), 5)
SSLMK = ssl.mk
else
SSLMK =
endif
ifeq ($(strip $(VERSION.MAJOR)), 7)
GOBJECT = gobject-introspection.mk
else
GOBJECT =
endif
include $(GOBOJECT) pygobject.mk pygtk.mk M2Crypto.mk $(SSLMK) numpy.mk pycairo.mk

