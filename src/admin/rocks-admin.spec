Summary: rocks-admin
Name: rocks-admin
Version: 6.3
Release: 0
License: University of California
Vendor: Rocks Clusters
Group: System Environment/Base
Source: rocks-admin-6.3.tar.gz
Buildroot: /export/home/repositories/rocks/src/roll/core/src/admin/rocks-admin.buildroot




%description
rocks-admin
%prep
%setup
%build
printf "\n\n\n### build ###\n\n\n"
BUILDROOT=/export/home/repositories/rocks/src/roll/core/src/admin/rocks-admin.buildroot make -f /export/home/repositories/rocks/src/roll/core/src/admin/rocks-admin.spec.mk build
%install
printf "\n\n\n### install ###\n\n\n"
BUILDROOT=/export/home/repositories/rocks/src/roll/core/src/admin/rocks-admin.buildroot make -f /export/home/repositories/rocks/src/roll/core/src/admin/rocks-admin.spec.mk install
%files 
/

