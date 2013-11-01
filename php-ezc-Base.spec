%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%define pear_name Base
%define channel components.ez.no

Name:           php-ezc-Base
Version:        1.8
Release:        1%{?_dist}
Summary:        Provides the basic infrastructure that all packages rely on

Group:          Development/Libraries
License:        BSD
URL:            http://ezcomponents.org/
Source0:        http://components.ez.no/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  php-pear >= 1:1.4.9-1.2
#BuildRequires:  php-channel(%{channel})
Requires:       php-common >= 5.2.1
Requires:       php-pear(PEAR)
Requires:       php-channel(%{channel})
Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}


%description
The Base package provides the basic infrastructure that all packages rely on.
Therefore every component relies on this package.


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
%dir %{pear_phpdir}/ezc
%dir %{pear_phpdir}/ezc/autoload
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/data/%{pear_name}
%{pear_phpdir}/ezc/%{pear_name}
%{pear_phpdir}/ezc/autoload/base_autoload.php


%changelog
* Thu Dec 24 2009 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.8-1
- upstream 1.8

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.7-1
- upstream 1.7

* Sun Feb 22 2009 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.6.1-2
- Add owner to %%{pear_phpdir}/ezc and %%{pear_phpdir}/ezc/autoload

* Mon Feb 09 2009 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.6.1-1
- upstream 1.6.1

* Thu Feb 03 2009 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.6-1
- Initial packaging
