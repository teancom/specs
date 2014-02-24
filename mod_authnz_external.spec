Name: mod_authnz_external
Version: 3.2.6
Release: 1%{?_dist}
Source0: https://mod-auth-external.googlecode.com/files/mod_authnz_external-%{version}.tar.gz
Summary: Apache mod_authnz_external
License: distributable
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: httpd-devel >= 2.2
BuildRequires: httpd-devel < 2.3
Requires: httpd >= 2.2
Requires: httpd < 2.3

%description
%{summary}.

%prep
%setup -q

%build
apxs -c mod_authnz_external.c

%check

%clean
rm -rf $RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/httpd/modules
apxs -i -S LIBEXECDIR=$RPM_BUILD_ROOT%{_libdir}/httpd/modules mod_authnz_external.la

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
cat >$RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/0-mod_authnz_external.conf <<EOF
LoadModule authnz_external_module modules/mod_authnz_external.so
EOF
chmod 0644 $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/*

%files
%defattr(-,root,root)
%{_libdir}/httpd/modules/*
%{_sysconfdir}/httpd/conf.d/*

%changelog
* Sun Dec 15 2013 David Bishop <david@gnuconsulting.com> 3.2.6-1
- Initial Argyl build.
