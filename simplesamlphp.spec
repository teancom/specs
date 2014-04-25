Name: simplesamlphp
Version:	1.11.0
Release:	2%{?_dist}
Summary:	SAML, but simple

License:	F/OSS
URL:		http://simplesamlphp.org/
Source0:	simplesamlphp-%{version}.tar.gz
Patch0:     xmlsec.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Prefix:     /var
BuildArch:  noarch

Requires:	php

%description
SimpleSAMLphp is an award-winning application written in native PHP that deals with authentication. The project is led by UNINETT, has a large user base, a helpful user community and a large set of external contributors.

%prep
%setup -q -n simplesamlphp-%{version}
%patch0 -p0

%build

%install
rm -rf %{buildroot}
mkdir -p -m 755 $RPM_BUILD_ROOT%{prefix}/simplesaml
cp -pr * $RPM_BUILD_ROOT%{prefix}/simplesaml

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{prefix}/simplesaml/

%changelog
* Thu Apr 24 2014 David Bishop <dbishop@robertmaefs.com> 1.11.0-2
- Patch to make it work with riteaide

* Mon Mar 3 2014 David Bishop <dbishop@robertmaefs.com> 1.11.0-1
- initial build for Argyl
