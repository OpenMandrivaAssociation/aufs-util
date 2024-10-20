%define date 20160216
%define debug_package %{nil}

%define major 2
%define libpkg %mklibname au %{major}

Name: aufs-util
Version: 4.0
Release: 0.%{date}.1
# git clone git://git.code.sf.net/p/aufs/aufs-util
# cd aufs-util
# git archive -o ~/abf/aufs-util/aufs-util-%{version}-%{date}.tar --prefix aufs-util-%{version}-%{date}/ origin/aufs4.x-rcN
Source0: aufs-util-%{version}-%{date}.tar.xz
Source100: %{name}.rpmlintrc
Summary: Tools for working with the AUFS filesystem
URL: https://aufs.sf.net/
License: GPL
Group: System/Base
Requires: %{libpkg} = %{EVRD}

%description
Tools for working with the AUFS filesystem

%package -n %{libpkg}
Summary: The AUFS library
Group: System/Libraries

%description -n %{libpkg}
The AUFS library

%prep
%setup -qn %{name}-%{version}-%{date}
# We don't need to link the tools statically, we have the right lib...
sed -i -e 's,-static,,;s,-o root -g root,,' Makefile
# But it should be available before /usr is needed...
sed -i -e 's,/usr/lib,/%{_lib},g' libau/Makefile
# We don't want a version check, the build machine may not be running the target kernel
sed -i -e 's,all: ver_test,all:,' Makefile

%build
%make CC="%{__cc}" CFLAGS="%{optflags}" LDFLAGS="%{optflags}"

%install
%makeinstall_std

%files
%config %{_sysconfdir}/default/aufs
%{_bindir}/*
/sbin/*
%{_mandir}/*/*

%files -n %{libpkg}
/%{_lib}/libau.so.%{major}*
/%{_lib}/libau.so
