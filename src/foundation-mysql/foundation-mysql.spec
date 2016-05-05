Summary: foundation-mysql
Name: foundation-mysql
Version: 5.6.26
Release: 1
License: University of California
Vendor: Rocks Clusters
Group: System Environment/Base
Source: foundation-mysql-5.6.26.tar.gz
Buildroot: /export/home/repositories/rocks/src/roll/core/src/foundation-mysql/foundation-mysql.buildroot



%define __perl_provides %{_builddir}/%{name}-%{version}/filter-perl-prov.sh
%define __perl_requires %{_builddir}/%{name}-%{version}/filter-perl-req.sh
%description
foundation-mysql
%prep
%setup
%build
printf "\n\n\n### build ###\n\n\n"
BUILDROOT=/export/home/repositories/rocks/src/roll/core/src/foundation-mysql/foundation-mysql.buildroot make -f /export/home/repositories/rocks/src/roll/core/src/foundation-mysql/foundation-mysql.spec.mk build
%install
printf "\n\n\n### install ###\n\n\n"
BUILDROOT=/export/home/repositories/rocks/src/roll/core/src/foundation-mysql/foundation-mysql.buildroot make -f /export/home/repositories/rocks/src/roll/core/src/foundation-mysql/foundation-mysql.spec.mk install
%files 
/
%config /opt/rocks/mysql/my.cnf
%post 
# when updating this package, make sure that the databases (if they exist) are 
# owned by rocksdb
/bin/grep -q rocksdb /etc/passwd
if [ $? -eq 0 ]; then
	chown -R rocksdb /var/opt/rocks/mysql
fi
