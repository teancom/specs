%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Process
%global channel pear.symfony-project.com

Name:           php-symfony-Process
Version:        2.3.6
Release:        1%{?_dist}
Summary:        The Symfony Process Component

Group:          Development/Libraries
License:        MIT
URL:            http://components.symfony-project.org/Process/
Source0:        http://pear.symfony-project.com/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-channel(%{channel})

#Requires(post): php-channel(%{channel})
#Requires(postun): php-channel(%{channel})
#Requires:       php-channel(%{channel})
Requires:       php-common >= 5.2.4

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}

%description
The Symfony Process Component.

Symfony Process is a PHP library that parses Process strings and converts them to
PHP arrays. It can also converts PHP arrays to Process strings. 


%prep
%setup -q -c
# package.xml is v2
mv package.xml %{pear_name}-%{version}/%{name}.xml
cd %{pear_name}-%{version}


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf $RPM_BUILD_ROOT docdir
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Move documentation
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
%{pear_phpdir}/Symfony/Component
%{pear_xmldir}/%{name}.xml

%changelog
* Wed Oct 16 2013 David Bishop <david@gnuconsulting.com>
- Initial build
