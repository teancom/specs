%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%define channel components.ez.no

Name:           php-channel-ezc
Version:        1
Release:        1%{?_dist}
Summary:        Adds eZ Components channel to PEAR

Group:          Development/Libraries
License:        BSD
URL:            http://ezcomponents.org/
Source0:        http://components.ez.no/channel.xml
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  php-pear(PEAR)
Requires:       php-pear(PEAR)
Requires(post): %{__pear}
Requires(postun): %{__pear}

#Provides:       php-channel(ezc)
Provides:       php-channel(%{channel})


%description
This package adds the eZ Components channel which allows PEAR packages
from this channel to be installed.


%prep
%setup -qcT


%build
# Empty build section, nothing to build


%install
rm -rf %{buildroot}
install -d %{buildroot}%{pear_xmldir}
install -p -m 644 %{SOURCE0} %{buildroot}%{pear_xmldir}/%{name}.xml


%clean
rm -rf %{buildroot}


%post
if [ $1 -eq  1 ] ; then
    %{__pear} channel-add %{pear_xmldir}/%{name}.xml > /dev/null || :
else
    %{__pear} channel-update %{pear_xmldir}/%{name}.xml > /dev/null ||:
fi


%postun
if [ $1 -eq 0 ] ; then
    %{__pear} channel-delete %{channel} > /dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_xmldir}/%{name}.xml


%changelog
* Wed Oct 16 2013 David Bishop <david@gnuconsulting.com>
- Initial build
