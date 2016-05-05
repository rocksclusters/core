Summary: foundation-python-extras
Name: foundation-python-extras
Version: 6.3
Release: 2
License: University of California
Vendor: Rocks Clusters
Group: System Environment/Base
Source: foundation-python-extras-6.3.tar.gz
Buildroot: /export/home/repositories/rocks/src/roll/core/src/foundation-python-extras/foundation-python-extras.buildroot




%description
foundation-python-extras
%prep
%setup
%build
printf "\n\n\n### build ###\n\n\n"
BUILDROOT=/export/home/repositories/rocks/src/roll/core/src/foundation-python-extras/foundation-python-extras.buildroot make -f /export/home/repositories/rocks/src/roll/core/src/foundation-python-extras/foundation-python-extras.spec.mk build
%install
printf "\n\n\n### install ###\n\n\n"
BUILDROOT=/export/home/repositories/rocks/src/roll/core/src/foundation-python-extras/foundation-python-extras.buildroot make -f /export/home/repositories/rocks/src/roll/core/src/foundation-python-extras/foundation-python-extras.spec.mk install
%files 
/

