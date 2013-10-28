%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %(php-config --version 2>/dev/null || echo 0)

%define module_version 1.3.2
%define _unpackaged_files_terminate_build 0


Name:		php-pecl-jsonc
Summary:	JavaScript Object Notation
Version:	%{module_version}
Release:	1%{?_dist}
License:	PHP License
Group:		Development/Languages
URL:		http://pecl.php.net/package/jsonc
Source:		http://pecl.php.net/get/jsonc-%{module_version}.tgz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:	php-pecl(jsonc) = %{version}
Requires:	php >= 5.5.5
BuildRequires:	php-devel

%package devel
Summary: JavaScript Object Notation Development
Group: Development/Libraries
Requires: php-pecl-jsonc = %{version}

%description
JavaScript Object Notation

%description devel
JavaScript Object Notation devel package

%prep
%setup -c -q

cd jsonc-%{module_version}

%build
cd jsonc-%{module_version}
phpize
%configure --with-apxs=/usr/sbin/apxs --with-php-config=/usr/bin/php-config 
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
cd jsonc-%{module_version}
%{__make} install INSTALL_ROOT=%{buildroot}

install -m 755 -d %{buildroot}/etc/php.d/
cat << ! > %{buildroot}/etc/php.d/json.ini
; Enable jsonc extension module
extension=json.so
!

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{php_extdir}/json.so
%{_sysconfdir}/php.d/json.ini

%files devel
%defattr(-, root, root, -)
%{_includedir}/php/ext/json/php_json.h

%changelog
* Fri Oct 25 2013 David Bishop <david@gnuconsulting.com> 
- initial build
