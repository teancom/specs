Name: liquibase
Version: 2.0.5
Release: 1%{?_dist}
Summary: Liquibase is Liquid!
License: distributable
Group: Development/Libraries
URL: http://liquibase.org
BuildRoot: %{_tmppath}/%{name}-root
Source0: liquibase.sh-%{version}
Source1: liquibase-%{version}.jar
Source2: mysql-connector-java-5.1.22-bin.jar
Requires: java >= 1.6.0
BuildArch: noarch

%description
%{summary}.

%prep

%build

%clean
rm -rf $RPM_BUILD_ROOT

%install

rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/lib/java/liquibase/lib $RPM_BUILD_ROOT/usr/bin
cp %{SOURCE0} $RPM_BUILD_ROOT/usr/bin/liquibase
cp %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT/usr/lib/java/liquibase/lib


%files
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/liquibase
/usr/lib/java/*

%changelog
* Thu Oct 04 2012 David Bishop <david@gnuconsulting.com> 2.0.5-1
- Initial build for maefsco
