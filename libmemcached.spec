
Summary: open source C/C++ client library and tools for the memcached server
Name: libmemcached
Version: 1.0.17
Release: 1%{?dist}
License: GPL
Group: Development/Tools
URL: http://libmemcached.org
Source: https://launchpad.net/%{name}/1.0/%{version}/+download/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: memcached mysql-devel

%description
libMemcached is an open source C/C++ client library and tools for the memcached server (http://danga.com/memcached). It has been designed to be light on memory usage, thread safe, and provide full access to server side methods.

%prep
%setup -q

%build
%configure --with-memcached --with-mysql --with-gnu-ld "CC=gcc44" "CXX=g++44" 
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf ${RPM_BUILD_ROOT}

%files 
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*
%{_libdir}/*
%{_includedir}/*
/usr/share/aclocal/ax_libmemcached.m4

%changelog
* Mon Oct 14 2013 David Bishop <david@gnuconsulting.com> - 1.0.17-1
- Initial build
