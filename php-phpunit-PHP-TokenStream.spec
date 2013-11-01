%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name     PHP_TokenStream
%global channel       pear.phpunit.de

Name:           php-phpunit-PHP-TokenStream
Version:        1.1.4
Release:        1%{?_dist}
Summary:        Wrapper around PHP tokenizer extension

Group:          Development/Libraries
License:        BSD
URL:            http://github.com/sebastianbergmann/php-token-stream
Source0:        http://pear.phpunit.de/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.9.1
BuildRequires:  php-channel(%{channel})
Requires:       php-channel(%{channel})
Requires:       php-common >= 5.2.7
Requires:       php-tokenizer
Requires:       php-pear(components.ez.no/ConsoleTools) >= 1.6 
Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}


%description
Wrapper around PHP tokenizer extension.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
%{__mv} package2.xml %{pear_name}-%{version}/%{name}.xml

cd %{pear_name}-%{version}

# Create a "localized" php.ini to avoid build warning
cp /etc/php.ini .
echo "date.timezone=UTC" >>php.ini

%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__rm} -rf $RPM_BUILD_ROOT docdir
PHPRC=./php.ini %{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
%{__rm} -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
%{__mkdir} -p $RPM_BUILD_ROOT%{pear_xmldir}
%{__install} -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
%{__rm} -rf $RPM_BUILD_ROOT


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
%{pear_phpdir}/PHP
#%{_bindir}/phptok
%doc %{pear_phpdir}/doc

%changelog
* Wed Oct 16 2013 David Bishop <david@gnuconsulting.com>
- Initial build
