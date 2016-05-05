Summary: rocks-pylib
Name: rocks-pylib
Version: 6.3
Release: 3
License: University of California
Vendor: Rocks Clusters
Group: System Environment/Base
Source: rocks-pylib-6.3.tar.gz
Buildroot: /export/home/repositories/rocks/src/roll/core/src/rocks-pylib/rocks-pylib.buildroot

Buildarch: noarch


%description
rocks-pylib
%prep
%setup
%build
printf "\n\n\n### build ###\n\n\n"
BUILDROOT=/export/home/repositories/rocks/src/roll/core/src/rocks-pylib/rocks-pylib.buildroot make -f /export/home/repositories/rocks/src/roll/core/src/rocks-pylib/rocks-pylib.spec.mk build
%install
printf "\n\n\n### install ###\n\n\n"
BUILDROOT=/export/home/repositories/rocks/src/roll/core/src/rocks-pylib/rocks-pylib.buildroot make -f /export/home/repositories/rocks/src/roll/core/src/rocks-pylib/rocks-pylib.spec.mk install
%files 
/

