Summary: rocks-config
Name: rocks-config
Version: 6.3
Release: 1
License: University of California
Vendor: Rocks Clusters
Group: System Environment/Base
Source: rocks-config-6.3.tar.gz
Buildroot: /export/home/repositories/rocks/src/roll/core/src/config/rocks-config.buildroot




%description
rocks-config
%prep
%setup
%build
printf "\n\n\n### build ###\n\n\n"
BUILDROOT=/export/home/repositories/rocks/src/roll/core/src/config/rocks-config.buildroot make -f /export/home/repositories/rocks/src/roll/core/src/config/rocks-config.spec.mk build
%install
printf "\n\n\n### install ###\n\n\n"
BUILDROOT=/export/home/repositories/rocks/src/roll/core/src/config/rocks-config.buildroot make -f /export/home/repositories/rocks/src/roll/core/src/config/rocks-config.spec.mk install
%files 
/

