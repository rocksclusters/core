Summary: foundation-libxml2
Name: foundation-libxml2
Version: 2.6.23
Release: 0
License: University of California
Vendor: Rocks Clusters
Group: System Environment/Base
Source: foundation-libxml2-2.6.23.tar.gz
Buildroot: /export/home/repositories/rocks/src/roll/core/src/foundation-libxml2/foundation-libxml2.buildroot




%description
foundation-libxml2
%prep
%setup
%build
printf "\n\n\n### build ###\n\n\n"
BUILDROOT=/export/home/repositories/rocks/src/roll/core/src/foundation-libxml2/foundation-libxml2.buildroot make -f /export/home/repositories/rocks/src/roll/core/src/foundation-libxml2/foundation-libxml2.spec.mk build
%install
printf "\n\n\n### install ###\n\n\n"
BUILDROOT=/export/home/repositories/rocks/src/roll/core/src/foundation-libxml2/foundation-libxml2.buildroot make -f /export/home/repositories/rocks/src/roll/core/src/foundation-libxml2/foundation-libxml2.spec.mk install
%files 
/

