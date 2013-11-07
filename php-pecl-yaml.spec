%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %(php-config --version 2>/dev/null || echo 0)

%define module_version 1.1.0
%define _unpackaged_files_terminate_build 0


Name:		php-pecl-yaml
Summary:	YAML YAML YAML
Version:	%{php_apiver}_%{module_version}
Release:	1%{?_dist}
License:	PHP License
Group:		Development/Languages
URL:		http://pecl.php.net/package/yaml
Source:		http://pecl.php.net/get/yaml-%{module_version}.tgz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:	php-pecl(yaml) = %{version}
Requires:	php >= 5.2.6
BuildRequires:	php-devel libyaml-devel

%description
yaml is a yaml, yaml.

%prep
%setup -c -q

cd yaml-%{module_version}

%build
cd yaml-%{module_version}
phpize
%configure --enable-yaml --with-apxs=/usr/sbin/apxs --with-php-config=/usr/bin/php-config 
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
cd yaml-%{module_version}
%{__make} install INSTALL_ROOT=%{buildroot}

install -m 755 -d %{buildroot}/etc/php.d/
cat << ! > %{buildroot}/etc/php.d/yaml.ini
; Enable yaml extension module
extension=yaml.so
!

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{php_extdir}/yaml.so
%{_sysconfdir}/php.d/yaml.ini

%changelog
* Wed Nov 06 2013 David Bishop <david@gnuconsulting.com> 
- initial build
