%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %(php-config --version 2>/dev/null || echo 0)

%define module_version 3.1.13
%define _unpackaged_files_terminate_build 0


Name:		php-pecl-apc
Summary:	Alternative PHP Cache
Version:	%{php_apiver}_%{module_version}
Release:	1%{?_dist}
License:	PHP License
Group:		Development/Languages
URL:		http://pecl.php.net/package/APC
Source:		http://pecl.php.net/get/APC-%{module_version}.tgz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:	php-pecl(apc) = %{version}
Requires:	php-api = %{php_apiver}
Requires:	php >= 5.2.6
BuildRequires:	php-devel

%description
APC is a free, open, and robust framework for caching and optimizing PHP intermediate code.

%prep
%setup -c -q

cd APC-%{module_version}

%build
cd APC-%{module_version}
phpize
%configure --enable-apc --enable-apc-mmap --with-apxs=/usr/sbin/apxs --with-php-config=/usr/bin/php-config --enable-apc-spinlocks
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
cd APC-%{module_version}
%{__make} install INSTALL_ROOT=%{buildroot}

install -m 755 -d %{buildroot}/etc/php.d/
cat << ! > %{buildroot}/etc/php.d/apc.ini
; Enable apc extension module
extension=apc.so
!

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{php_extdir}/apc.so
%{_sysconfdir}/php.d/apc.ini

%changelog
* Mon Oct 14 2013 David Bishop <david@gnuconsulting.com> 
- initial build
