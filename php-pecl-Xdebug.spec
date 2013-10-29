%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %(php-config --version 2>/dev/null || echo 0)

%define module_version 2.2.3

Name:		php-pecl-Xdebug
Summary:	Provides functions for function traces and profiling
Version:	%{php_apiver}_%{module_version}
Release:	1%{?dist}
License:	PHP License
Group:		Development/Languages
URL:		http://pecl.php.net/package/Xdebug
Source:		http://pecl.php.net/get/xdebug-%{module_version}.tgz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:	php-pecl(Xdebug) = %{version}
Requires:	php-api = %{php_apiver}
BuildRequires:	php-devel
Obsoletes:	php-pecl-xdebug <= 2.0.3

%description
The Xdebug extension helps you debugging your script by providing a lot of
valuable debug information.

%prep
%setup -c -q

%build
cd xdebug-%{module_version}
phpize
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
cd xdebug-%{module_version}
%{__make} install INSTALL_ROOT=%{buildroot}

install -m 755 -d %{buildroot}/etc/php.d/
cat << ! > %{buildroot}/etc/php.d/xdebug.ini
; Enable xdebug extension module
[Zend]
zend_extension = %{php_extdir}/xdebug.so
xdebug.remote_enable = 1
xdebug.remote_port = 9000
xdebug.remote_host = localhost
!

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{php_extdir}/xdebug.so
%{_sysconfdir}/php.d/xdebug.ini

%changelog
* Wed Oct 16 2013 David Bishop <david@gnuconsulting.com>
- Initial build
