%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name PHPUnit_Selenium
%global channel pear.phpunit.de

Name:           php-phpunit-PHPUnit-Selenium
Version:        1.3.2
Release:        1%{?_dist}
Summary:        Selenium RC integration for PHPUnit

Group:          Development/Libraries
License:        BSD
URL:            http://pear.phpunit.de/
Source0:        http://pear.phpunit.de/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.9.1
BuildRequires:  php-channel(%{channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(%{channel}/PHPUnit) >= 3.7.27
Requires:       php-common >= 5.2.7

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}


%description
Selenium RC integration for PHPUnit


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
cd %{pear_name}-%{version}
rm -rf $RPM_BUILD_ROOT docdir
PHPRC=../php.ini %{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

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
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/PHPUnit/Extensions/
%doc %{pear_phpdir}/doc


%changelog
* Wed Oct 16 2013 David Bishop <david@gnuconsulting.com>
- Initial build
