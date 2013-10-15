%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %(php-config --version 2>/dev/null || echo 0)

%define module_version 2.2.7

Name:		php-pecl-memcache
Summary:	PHP extension for interfacing with memcached via libmemcached library
Version:	%{php_apiver}_%{module_version}
Release:	1%{?_dist}
License:	PHP License
Group:		Development/Languages
URL:		http://pecl.php.net/package/memcache
Source:		http://pecl.php.net/get/memcache-%{module_version}.tgz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:	php-pecl(memcache) = %{version}
Requires:	php-api = %{php_apiver}
BuildRequires:	php-devel

%description
Memcached is a caching daemon designed especially for dynamic web applications to decrease database load by
storing objects in memory.

This extension allows you to work with memcached through handy OO and procedural interfaces.

%prep
%setup -c -q

%build
cd memcache-%{module_version}
phpize
%configure "CC=gcc44" "CXX=g++44"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
cd memcache-%{module_version}
%{__make} install INSTALL_ROOT=%{buildroot}

install -m 755 -d %{buildroot}/etc/php.d/
cat << ! > %{buildroot}/etc/php.d/memcache.ini
; Enable memcache extension module
extension=memcache.so
!

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{php_extdir}/memcache.so
%{_sysconfdir}/php.d/memcache.ini

%changelog
* Mon Oct 14 2013 David Bishop <david@gnuconsulting.com>
- initial build
