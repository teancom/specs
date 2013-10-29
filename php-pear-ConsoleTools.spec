%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}

%global pear_name   ConsoleTools
%global channel     components.ez.no

Name:           php-pear-ConsoleTools
Version:        1.6.1
Release:        1%{?_dist}
Summary:        A set of classes to do different actions with the console

Group:          Development/Libraries
License:        BSD
URL:            http://ezcomponents.org/
Source0:        http://components.ez.no/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
#BuildRequires:  php-channel(%{channel})
Requires:       php-common >= 5.2.1
Requires:       php-pear(%{channel}/Base) >= 1.8
Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}


%description
The ConsoleTools component provides several useful tools to build applications
that run on a computer console (sometimes also called shell or command line).


%prep
%setup -q -c
[ -f package2.xml ] || %{__mv} package.xml package2.xml
%{__mv} package2.xml %{pear_name}-%{version}/%{name}.xml
cd %{pear_name}-%{version}


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__rm} -rf %{buildroot} docdir
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Move documentation
%{__mv} %{buildroot}%{pear_docdir}/%{pear_name}/docs ./docdir
%{__rm} -rf %{buildroot}%{pear_docdir}

# Clean up unnecessary files
%{__rm} -rf %{buildroot}%{pear_phpdir}/.??*

# Install XML package description
%{__mkdir} -p %{buildroot}%{pear_xmldir}
%{__install} -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%clean
%{__rm} -rf %{buildroot}


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
%doc %{pear_name}-%{version}/docdir/*
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/data/%{pear_name}
%{pear_phpdir}/ezc/%{pear_name}
%{pear_phpdir}/ezc/autoload/console_autoload.php


%changelog
* Wed Oct 16 2013 David Bishop <david@gnuconsulting.com>
- Initial build
