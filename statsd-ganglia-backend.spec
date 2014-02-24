Name:	statsd-ganglia-backend
Version:	0.2.1
Release:	1%{?dist}
Summary:	Ganglia backend for statsd

Group:		Development
License:	Freeware
URL:		https://github.com/jbuchbinder/statsd-ganglia-backend
Source0:	statsd-ganglia-backend-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires:	statsd

%description
A statsd backend that allows you to push to ganglia


%prep
%setup -q -n statsd-ganglia-backend


%build

%install
rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/usr/share/statsd/node_modules
cp -rp * $RPM_BUILD_ROOT/usr/share/statsd/node_modules


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
/usr/share/statsd/node_modules/*

%changelog
* Thu Nov 07 2013 David Bishop <david@gnuconsulting.com> 0.2.1
- Initial build
