ifeq ($(strip $(VERSION.MAJOR)), 5)
SSLMK = ssl.mk
else
SSLMK =
endif
ifeq ($(strip $(VERSION.MAJOR)), 6)
GOBJECT =
else
GOBJECT = gobject-introspection.mk
endif
# include $(GOBOJECT) pygobject.mk pygtk.mk M2Crypto.mk $(SSLMK) numpy.mk pycairo.mk
include gobject-introspection.mk pygobject.mk pygtk.mk M2Crypto.mk $(SSLMK) numpy.mk pycairo.mk
