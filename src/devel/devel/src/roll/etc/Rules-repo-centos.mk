
## Create a localrepo at the top level roll directory. Create a local yum.conf
## file
## When complete:
##           yum -c yum.conf [.. yum commands .. ] 
## Will allow use of  yum AND system repository definitions.

## make createlocalrepo 
## does all the work

LOCALPATH=$(CURDIR)
# Some protections for local path system wide
ifeq ($(LOCALPATH),)
	LOCALPATH=/tmp
endif
ifeq ($(strip $(LOCALPATH)),"/etc")
	LOCALPATH=/tmp
endif

YUM.CONF=yum.conf
YUM.REPOS.D=yum.repos.d
SYSTEMPATH=/etc
REPONAME=localrepo
LOCALREPO.CONF=$(LOCALPATH)/$(YUM.REPOS.D)/$(REPONAME).conf
LOCALYUM.CONF=$(LOCALPATH)/$(YUM.CONF)
LOCALCACHE=$(LOCALPATH)/cache


.PHONY: copyrepos copyconf localrepo localcache createlocalrepo

## Setup the local repos directory
$(LOCALPATH)/$(YUM.REPOS.D):
	[ -d $(LOCALPATH)/$(YUM.REPOS.D) ] ||  mkdir $(LOCALPATH)/$(YUM.REPOS.D)

copyrepos: $(LOCALPATH)/$(YUM.REPOS.D)
	/bin/find $(SYSTEMPATH)/$(YUM.REPOS.D) -name '*repo' -exec /bin/cp {} $(LOCALPATH)/$(YUM.REPOS.D) \; -print

$(LOCALREPO.CONF): copyrepos 
	echo "[$(ROLLNAME)-roll]" > $(LOCALREPO.CONF)
	echo "name=$(ROLLNAME)-roll" >> $(LOCALREPO.CONF)
	echo "baseurl=file://$(CURDIR)/$(REPONAME)" >> $(LOCALREPO.CONF)
	echo "enabled=1" >> $(LOCALREPO.CONF)
	echo "gpgcheck=0" >> $(LOCALREPO.CONF)
	echo "protected=1" >> $(LOCALREPO.CONF)

localcache:
	[ -d $(LOCALCACHE) ] || /bin/mkdir $(LOCALCACHE)
localrepo: $(LOCALREPO.CONF) 
	[ -d $(LOCALPATH)/$(REPONAME) ] || /bin/mkdir -p $(LOCALPATH)/$(REPONAME)/RPMS
	find RPMS -name '*rpm' -exec /bin/cp {} $(LOCALPATH)/$(REPONAME)/RPMS \; -print 
	( cd $(LOCALPATH)/$(REPONAME); createrepo $(LOCALPATH)/$(REPONAME))

copyconf:
	/bin/cp $(SYSTEMPATH)/$(YUM.CONF) $(LOCALPATH)/$(YUM.CONF)
	echo "cachedir=$(LOCALCACHE)" >> $(LOCALPATH)/$(YUM.CONF)
	echo "reposdir=$(LOCALPATH)/$(YUM.REPOS.D)" >> $(LOCALPATH)/$(YUM.CONF)

createlocalrepo: copyconf localrepo localcache

Rules-repo-centos.mk:: $(wildcard $(ROLLSROOT)/etc/Rules-repo-centos.mk)
	cp $^ $@


clean::
	/bin/rm -rf $(LOCALPATH)/$(YUM.REPOS.D)
	/bin/rm -rf $(LOCALPATH)/$(REPONAME)
	/bin/rm -rf $(LOCALCACHE)
	/bin/rm -f $(LOCALPATH)/$(YUM.CONF)
