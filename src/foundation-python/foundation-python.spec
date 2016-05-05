Summary: foundation-python
Name: foundation-python
Version: 2.6.7
Release: 0
License: University of California
Vendor: Rocks Clusters
Group: System Environment/Base
Source: foundation-python-2.6.7.tar.gz
Buildroot: /export/home/repositories/rocks/src/roll/core/src/foundation-python/foundation-python.buildroot




%description
foundation-python
%prep
%setup
%build
printf "\n\n\n### build ###\n\n\n"
BUILDROOT=/export/home/repositories/rocks/src/roll/core/src/foundation-python/foundation-python.buildroot make -f /export/home/repositories/rocks/src/roll/core/src/foundation-python/foundation-python.spec.mk build
%install
printf "\n\n\n### install ###\n\n\n"
BUILDROOT=/export/home/repositories/rocks/src/roll/core/src/foundation-python/foundation-python.buildroot make -f /export/home/repositories/rocks/src/roll/core/src/foundation-python/foundation-python.spec.mk install
%files 
/

