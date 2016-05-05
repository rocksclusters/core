Summary: foundation-python-xml
Name: foundation-python-xml
Version: 0.8.4
Release: 0
License: University of California
Vendor: Rocks Clusters
Group: System Environment/Base
Source: foundation-python-xml-0.8.4.tar.gz
Buildroot: /export/home/repositories/rocks/src/roll/core/src/foundation-python-xml/foundation-python-xml.buildroot




%description
foundation-python-xml
%prep
%setup
%build
printf "\n\n\n### build ###\n\n\n"
BUILDROOT=/export/home/repositories/rocks/src/roll/core/src/foundation-python-xml/foundation-python-xml.buildroot make -f /export/home/repositories/rocks/src/roll/core/src/foundation-python-xml/foundation-python-xml.spec.mk build
%install
printf "\n\n\n### install ###\n\n\n"
BUILDROOT=/export/home/repositories/rocks/src/roll/core/src/foundation-python-xml/foundation-python-xml.buildroot make -f /export/home/repositories/rocks/src/roll/core/src/foundation-python-xml/foundation-python-xml.spec.mk install
%files 
/

