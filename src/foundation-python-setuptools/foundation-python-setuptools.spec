Summary: foundation-python-setuptools
Name: foundation-python-setuptools
Version: 0.6.10
Release: 0
License: University of California
Vendor: Rocks Clusters
Group: System Environment/Base
Source: foundation-python-setuptools-0.6.10.tar.gz
Buildroot: /export/home/repositories/rocks/src/roll/core/src/foundation-python-setuptools/foundation-python-setuptools.buildroot




%description
foundation-python-setuptools
%prep
%setup
%build
printf "\n\n\n### build ###\n\n\n"
BUILDROOT=/export/home/repositories/rocks/src/roll/core/src/foundation-python-setuptools/foundation-python-setuptools.buildroot make -f /export/home/repositories/rocks/src/roll/core/src/foundation-python-setuptools/foundation-python-setuptools.spec.mk build
%install
printf "\n\n\n### install ###\n\n\n"
BUILDROOT=/export/home/repositories/rocks/src/roll/core/src/foundation-python-setuptools/foundation-python-setuptools.buildroot make -f /export/home/repositories/rocks/src/roll/core/src/foundation-python-setuptools/foundation-python-setuptools.spec.mk install
%files 
/

