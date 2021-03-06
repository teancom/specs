# Fedora 17 ships with ruby 1.9, which uses vendorlibdir instead
# of sitelibdir
%if 0%{?fedora} >= 17
%global hiera_libdir   %(ruby -rrbconfig -e 'puts RbConfig::CONFIG["vendorlibdir"]')
%else
%global hiera_libdir   %(ruby -rrbconfig -e 'puts RbConfig::CONFIG["sitelibdir"]')
%endif

%if 0%{?rhel} == 5
%global _sharedstatedir %{_prefix}/lib
%endif

# VERSION is subbed out during rake srpm process
%global realversion 1.3.2
%global rpmversion 1.3.2

Name:           hiera
Version:        %{rpmversion}
Release:        2%{?dist}
Summary:        A simple pluggable Hierarchical Database
Vendor:         %{?_host_vendor}
Group:          System Environment/Base
License:        ASL 2.0
URL:            http://projects.puppetlabs.com/projects/%{name}/
Source0:        http://downloads.puppetlabs.com/%{name}/%{name}-%{realversion}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  ruby >= 1.8.5
Requires:       ruby(abi) >= 1.8
Requires:       ruby >= 1.8.5
Requires:       rubygem-json

%description
A simple pluggable Hierarchical Database.

%prep
%setup -q  -n %{name}-%{realversion}


%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{hiera_libdir}
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT/%{_sharedstatedir}/hiera
cp -pr lib/hiera $RPM_BUILD_ROOT/%{hiera_libdir}
cp -pr lib/hiera.rb $RPM_BUILD_ROOT/%{hiera_libdir}
install -p -m0755 bin/hiera $RPM_BUILD_ROOT/%{_bindir}
install -p -m0644 ext/hiera.yaml $RPM_BUILD_ROOT/%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/hiera
%{hiera_libdir}/hiera.rb
%{hiera_libdir}/hiera
%config(noreplace) %{_sysconfdir}/hiera.yaml
%{_sharedstatedir}/hiera
%doc COPYING README.md


%changelog
* Thu Oct 10 2013 David Bishop <david@gnuconsulting.com> - 1.2.1-1
- New upstream version

* Thu Dec 27 2012 Puppet Labs Release <info@puppetlabs.com> -  1.1.2-1
- Build for 1.1.2

* Mon May 14 2012 Matthaus Litteken <matthaus@puppetlabs.com> - 1.0.0-0.1rc2
- 1.0.0rc2 release

* Mon May 14 2012 Matthaus Litteken <matthaus@puppetlabs.com> - 1.0.0-0.1rc1
- 1.0.0rc1 release

* Thu May 03 2012 Matthaus Litteken <matthaus@puppetlabs.com> - 0.3.0.28-1
- Initial Hiera Packaging. Upstream version 0.3.0.28

