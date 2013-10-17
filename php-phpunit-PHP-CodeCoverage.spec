%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name PHP_CodeCoverage
%global channel pear.phpunit.de

Name:           php-phpunit-PHP-CodeCoverage
Version:        1.2.13
Release:        1%{?_dist}
Summary:        PHP code coverage information

Group:          Development/Libraries
License:        BSD
URL:            http://pear.phpunit.de/
Source0:        http://pear.phpunit.de/get/%{pear_name}-%{version}.tgz
Source1:        http://github.com/sebastianbergmann/php-code-coverage/raw/master/README.markdown

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
BuildRequires:  php-channel(%{channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-xml >= 5.2.7
Requires:       php-pecl(Xdebug) >= 2.0.5
Requires:       php-pear(%{channel}/File_Iterator) >= 1.2.2
Requires:       php-pear(%{channel}/PHP_TokenStream) >= 1.0.0
Requires:       php-pear(%{channel}/Text_Template) >= 1.0.0
Requires:       php-pear(components.ez.no/ConsoleTools) >= 1.6

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}

%description
Library that provides collection, processing, and rendering functionality
for PHP code coverage information.


%prep
%setup -q -c
# Create a "localized" php.ini to avoid build warning
cp /etc/php.ini .
echo "date.timezone=UTC" >>php.ini

cp %{SOURCE1} README.markdown

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
%doc README.markdown
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/PHP
%doc %{pear_phpdir}/doc
#%{_bindir}/phpcov


%changelog
* Wed Oct 16 2013 David Bishop <david@gnuconsulting.com>
- Initial build
