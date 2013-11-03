Name:		python-zmq
Version:	2.2.0.1
Release:	1%{?dist}
Summary:	Python binding for ZeroMQ messaging library.

Group:		Development/Libraries
License:	GPL
URL:		http://www.zeromq.org/bindings:python
Source0:	https://github.com/zeromq/pyzmq/downloads/pyzmq-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	zeromq-devel
BuildRequires:	python
BuildRequires:	python-devel
Requires:	python
Requires:	zeromq

%description
%{summary}

%prep
%setup -q -n pyzmq-%{version}


%build
python setup.py build


%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root $RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.rst

/usr/lib*/python*/site-packages/pyzmq*
/usr/lib*/python*/site-packages/zmq/

%changelog

