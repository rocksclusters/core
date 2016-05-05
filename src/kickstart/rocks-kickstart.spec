Summary: rocks-kickstart
Name: rocks-kickstart
Version: 6.3
Release: 0
License: University of California
Vendor: Rocks Clusters
Group: System Environment/Base
Source: rocks-kickstart-6.3.tar.gz
Buildroot: /export/home/repositories/rocks/src/roll/core/src/kickstart/rocks-kickstart.buildroot




%description
rocks-kickstart
%prep
%setup
%build
printf "\n\n\n### build ###\n\n\n"
BUILDROOT=/export/home/repositories/rocks/src/roll/core/src/kickstart/rocks-kickstart.buildroot make -f /export/home/repositories/rocks/src/roll/core/src/kickstart/rocks-kickstart.spec.mk build
%install
printf "\n\n\n### install ###\n\n\n"
BUILDROOT=/export/home/repositories/rocks/src/roll/core/src/kickstart/rocks-kickstart.buildroot make -f /export/home/repositories/rocks/src/roll/core/src/kickstart/rocks-kickstart.spec.mk install
%files 
/

