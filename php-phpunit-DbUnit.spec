%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name DbUnit
%global channel pear.phpunit.de

Name:           php-phpunit-DbUnit
Version:        1.1.2
Release:        1%{?_dist}
Summary:        DbUnit port for PHP/PHPUnit

Group:          Development/Libraries
License:        BSD
URL:            http://pear.phpunit.de
Source0:        http://pear.phpunit.de/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.9.1
BuildRequires:  php-channel(%{channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-common >= 5.2.7
Requires:       php-pear(%{channel}/PHPUnit) >= 3.6.12
Requires:       php-pear(pear.symfony-project.com/Yaml) >= 2.3.5

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}


%description
DbUnit port for PHP/PHPUnit

%prep
%setup -q -c
# Create a "localized" php.ini to avoid build warning
cp /etc/php.ini .
echo "date.timezone=UTC" >>php.ini

cd %{pear_name}-%{version}
# package.xml is V2
mv ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf $RPM_BUILD_ROOT docdir
cd %{pear_name}-%{version}
PHPRC=../php.ini %{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Move documentation
mkdir -p docdir
mv $RPM_BUILD_ROOT%{pear_docdir}/%{pear_name} ../docdir


# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc docdir/*
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/PHPUnit/Extensions/Database
#%doc %{pear_phpdir}/doc
%{_bindir}/dbunit


%changelog
* Wed Oct 16 2013 David Bishop <david@gnuconsulting.com>
- Initial build
