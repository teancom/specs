%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}

Name:           php-channel-phpunit
Version:        1.0
Release:        3%{?_dist}
Summary:        Adds phpunit channel to PEAR

Group:          Development/Languages
License:        BSD
URL:            http://pear.phpunit.de
Source0:        http://pear.phpunit.de/channel.xml
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.8.1-1
Requires:       php >= 5.1.4 php-pear(PEAR)
Provides:       php-channel(pear.phpunit.de) = %{version}

%description
This package adds the phpunit channel which allows PEAR packages
from this channel to be installed.


%prep
%setup -q -c -T


%build
# Empty build section, nothing to build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{SOURCE0} $RPM_BUILD_ROOT%{pear_xmldir}/pear.phpunit.de.xml


%clean
rm -rf $RPM_BUILD_ROOT


%post
if [ $1 -eq  1 ] ; then
   %{__pear} channel-add %{pear_xmldir}/pear.phpunit.de.xml > /dev/null || :
else
   %{__pear} channel-update %{pear_xmldir}/pear.phpunit.de.xml > /dev/null ||:
fi


%postun
if [ $1 -eq 0 ] ; then
   %{__pear} channel-delete pear.phpunit.de > /dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_xmldir}/*


%changelog
* Wed Oct 16 2013 David Bishop <david@gnuconsulting.com>
- Initial build
