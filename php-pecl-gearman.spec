%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %(php-config --version 2>/dev/null || echo 0)

%define module_version 1.1.2

Name:       php-pecl-gearman
Summary:    PHP wrapper to libgearman
Version:    %{php_version}_%{module_version}
Release:    1%{?_dist}
License:    PHP License
Group:      Development/Languages
URL:        http://pecl.php.net/package/gearman
Source:     http://pecl.php.net/get/gearman-%{module_version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:   php-pecl(gearman) = %{version}
Requires:   php-api = %{php_apiver}
BuildRequires:  php-devel >= 5.2
BuildRequires:  gearmand-devel

%description
PHP wrapper to libgearman

%prep
%setup -c -q

%build
cd gearman-%{module_version}
phpize
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
cd gearman-%{module_version}
%{__make} install INSTALL_ROOT=%{buildroot}

install -m 755 -d %{buildroot}/etc/php.d/
cat << ! > %{buildroot}/etc/php.d/gearman.ini
; Enable gearman extension module
extension=gearman.so
!

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{php_extdir}/gearman.so
%{_sysconfdir}/php.d/gearman.ini

%changelog
* Thu Oct 11 2013 David Bishop <david@gnuconsulting.com> 1.1.2-1
- Initial build
