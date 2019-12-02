NAME = rocks-devel
RELEASE = 12 
RPM.FILES="/etc/profile.d/*\\n/opt/rocks/share/devel/*"
RPM.EXTRAS="%define _use_internal_dependency_generator 0\\n%define __find_requires %{_builddir}/%{name}-%{version}/filter-requires.sh"
RPM.REQUIRES="createrepo redhat-lsb"
