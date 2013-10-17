%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name PHPUnit
%global channel pear.phpunit.de

Name:           php-pear-PHPUnit
Version:        3.7.27
Release:        1%{?_dist}
Summary:        Regression testing framework for unit tests

Group:          Development/Libraries
License:        BSD
URL:            http://www.phpunit.de
Source0:        http://pear.phpunit.de/get/%{pear_name}-%{version}.tgz
Source1:        http://github.com/sebastianbergmann/phpunit/raw/3.4/README.markdown

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.9.1
BuildRequires:  php-channel(%{channel})

Requires:       php-xml >= 5.2.7
Requires:       php-pear(PEAR) >= 1.9.1
Requires:       php-channel(%{channel})
Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(%{channel}/File_Iterator) >= 1.3.1, 
Requires:       php-pear(%{channel}/Text_Template) >= 1.1.1
Requires:       php-pear(%{channel}/PHP_CodeCoverage) >= 1.2.13
Requires:       php-pear(%{channel}/PHP_Timer) >= 1.0.5
Requires:       php-pear(pear.symfony-project.com/Yaml) >= 2.3.5
# PHPUnit Extensions (yes, with circular dependency on PHPUnit)
Requires:       php-pear(%{channel}/PHPUnit_MockObject) >= 1.2.3
Requires:       php-pear(%{channel}/PHPUnit_Selenium) >= 1.3.2
Requires:       php-pear(%{channel}/DbUnit) >= 1.2.3
Requires:       php-pear(%{channel}/PHP_TokenStream) >= 1.2.0

# Optionnal dependencies
Requires:       php-json php-pdo php-soap
Requires:       php-pecl(Xdebug) >= 2.0.5

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}
Obsoletes:      php-pear-PHPUnit < %{version}
Provides:       php-pear-PHPUnit = %{version}-%{release}


%description
PHPUnit is a family of PEAR packages that supports the development of
object-oriented PHP applications using the concepts and methods of Agile
Software Development, Extreme Programming, Test-Driven Development and
Design-by-Contract Development by providing an elegant and robust framework
for the creation, execution and analysis of Unit Tests.


%prep
%setup -qc
cp %{SOURCE1} README.markdown

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

# Install Package
PHPRC=../php.ini %{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Move documentation
mv $RPM_BUILD_ROOT%{pear_docdir}/%{pear_name} ../docdir

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
install -d $RPM_BUILD_ROOT%{pear_xmldir}
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

%triggerpostun -- php-pear-PHPUnit
# re-register extension unregistered during postun of obsoleted php-pear-PHPUnit
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :



%files
%defattr(-,root,root,-)
%doc docdir/* README.markdown
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/%{pear_name}
%{_bindir}/phpunit


%changelog
* Wed Oct 16 2013 David Bishop <david@gnuconsulting.com>
- Initial build
