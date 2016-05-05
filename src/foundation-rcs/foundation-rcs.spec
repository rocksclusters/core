Summary: foundation-rcs
Name: foundation-rcs
Version: 5.7
Release: 0
License: University of California
Vendor: Rocks Clusters
Group: System Environment/Base
Source: foundation-rcs-5.7.tar.gz
Buildroot: /export/home/repositories/rocks/src/roll/core/src/foundation-rcs/foundation-rcs.buildroot




%description
foundation-rcs
%prep
%setup
%build
printf "\n\n\n### build ###\n\n\n"
BUILDROOT=/export/home/repositories/rocks/src/roll/core/src/foundation-rcs/foundation-rcs.buildroot make -f /export/home/repositories/rocks/src/roll/core/src/foundation-rcs/foundation-rcs.spec.mk build
%install
printf "\n\n\n### install ###\n\n\n"
BUILDROOT=/export/home/repositories/rocks/src/roll/core/src/foundation-rcs/foundation-rcs.buildroot make -f /export/home/repositories/rocks/src/roll/core/src/foundation-rcs/foundation-rcs.spec.mk install
%files 
/

