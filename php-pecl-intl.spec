%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %(php-config --version 2>/dev/null || echo 0)

%define module_version 2.0.1

Name:		php-pecl-intl
Summary:	Internationalization extension implements ICU library functionality in PHP.
Version:	%{php_version}_%{module_version}
Release:	1%{?_dist}
License:	PHP License
Group:		Development/Languages
URL:		http://pecl.php.net/package/intl
Source:		http://pecl.php.net/get/intl-%{module_version}.tgz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:	php-pecl(intl) = %{version}
BuildRequires:	php-devel >= 5.2
BuildRequires:  libicu-devel

%description
Internationalization extension implements ICU library functionality in PHP.

%prep
%setup -c -q

%build
cd intl-%{module_version}
phpize
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
cd intl-%{module_version}
%{__make} install INSTALL_ROOT=%{buildroot}

install -m 755 -d %{buildroot}/etc/php.d/
cat << ! > %{buildroot}/etc/php.d/intl.ini
; Enable intl extension module
extension=intl.so
!

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{php_extdir}/intl.so
%{_sysconfdir}/php.d/intl.ini

%changelog
* Mon Oct 14 2013 David Bishop <david@gnuconsulting.com> 2.0.1-1
- initial build
