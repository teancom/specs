%global vermajor 0.10
%global verminor .21

Name:       nodejs
Version:    %{vermajor}%{?verminor}
Release:    1%{?_dist}
Summary:    Evented I/O for V8 JavaScript
License:    BSD and MIT and ASL 2.0 and GPLv3
Group:      Development/Languages
URL:        http://nodejs.org/
Source0:    http://nodejs.org/dist/node-v%{version}.tar.gz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:   nodejs(engine) = %{version}
Provides:   nodejs(abi) = %{vermajor}
Provides:	node

BuildRequires:  python >= 2.6.6
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel

# V8 sucks at sonames so we're explicit here
Conflicts:      chromium <= 14

%description
Node.js is a server-side JavaScript environment that uses an asynchronous
event-driven model.  Node's goal is to provide an easy way to build scalable
network programs.

%prep
%setup -q -n node-v%{version}

%build
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ;
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ;
FFLAGS="${FFLAGS:-%optflags}" ; export FFLAGS ;

# nodejs-v0.6.8 FTBFS without this
LINKFLAGS="-lz"; export LINKFLAGS ;

python ./configure \
        --prefix=%{_prefix} 

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
/usr/bin/*
/usr/lib/*
/usr/share/*

%changelog
* Sat Nov 02 2013 David Bishop <david@gnuconsulting.com> - 0.10.21-1
- Initial build
