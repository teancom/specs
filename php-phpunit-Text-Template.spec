%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Text_Template
%global channel pear.phpunit.de

Name:           php-phpunit-Text-Template
Version:        1.1.4
Release:        1%{?_dist}
Summary:        Simple template engine

Group:          Development/Libraries
License:        BSD
URL:            http://pear.phpunit.de/
Source0:        http://pear.phpunit.de/get/%{pear_name}-%{version}.tgz
Source1:        http://github.com/sebastianbergmann/php-text-template/raw/master/README.markdown

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.8.1
BuildRequires:  php-channel(%{channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-channel(%{channel})
Requires:       php-common >= 5.1.4

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}

%description
Simple template engine.

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
%{pear_phpdir}/Text
%doc %{pear_phpdir}/doc/Text_Template/ChangeLog.markdown
%doc %{pear_phpdir}/doc/Text_Template/LICENSE
%doc %{pear_phpdir}/doc/Text_Template/README.markdown

%changelog
* Wed Oct 16 2013 David Bishop <david@gnuconsulting.com>
- Initial build
