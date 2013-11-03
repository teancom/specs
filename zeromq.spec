Name:          zeromq
Version:       3.2.4
Release:       1%{?dist}
Summary:       The ZeroMQ messaging library
Group:         Applications/Internet
License:       LGPLv3+
URL:           http://www.zeromq.org/
Source:        http://download.zeromq.org/%{name}-%{version}.tar.gz
Prefix:        %{_prefix}
Buildroot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gcc, make, gcc-c++, libstdc++-devel
Requires:      libstdc++

BuildRequires: libuuid-devel
Requires:      libuuid

# Build pgm only on supported archs
%ifarch pentium3 pentium4 athlon i386 i486 i586 i686 x86_64
BuildRequires: python, perl
%endif

%description
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialised messaging middleware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.

This package contains the ZeroMQ shared library.

%package devel
Summary:  Development files and static library for the ZeroMQ library
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}, pkgconfig

%description devel
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialised messaging middleware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.

This package contains ZeroMQ related development libraries and header files.

%prep
%setup -q

%build
%ifarch pentium3 pentium4 athlon i386 i486 i586 i686 x86_64
  %configure --with-pgm --with-pic --with-gnu-ld
%else
  %configure
%endif

%{__make} %{?_smp_mflags}

%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

# Install the package to build area
%{__make} check
%makeinstall

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)

# docs in the main package
%doc AUTHORS ChangeLog COPYING COPYING.LESSER NEWS README

# libraries
%{_libdir}/libzmq.so.3
%{_libdir}/libzmq.so.3.0.0

%{_mandir}/man7/zmq.7.gz

%files devel
%defattr(-,root,root,-)
%{_includedir}/zmq.h
%{_includedir}/zmq_utils.h

%{_libdir}/libzmq.la
%{_libdir}/libzmq.a
%{_libdir}/pkgconfig/libzmq.pc
%{_libdir}/libzmq.so

%{_mandir}/man3/*
%{_mandir}/man7/*

%changelog
* Mon Nov 26 2012 Justin Cook <jhcook@gmail.com> 3.2.2
- Update packaged files

* Fri Apr 8 2011 Mikko Koppanen <mikko@kuut.io> 3.0.0-1
- Update dependencies and packaged files

* Sat Apr 10 2010 Mikko Koppanen <mkoppanen@php.net> 2.0.7-1
- Initial packaging
