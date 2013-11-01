%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}

Name:		php-channel-symfony
Version:	1.3
Release:	1%{?_dist}
Summary:	Adds symfony project channel to PEAR

Group:		Development/Languages
License:	MIT
URL:		http://www.symfony-project.com/
Source0:	http://pear.symfony-project.com/channel.xml
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch
BuildRequires:	php-pear >= 1:1.4.9-1.2
Requires:	php-cli
Requires:	php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:	php-channel(pear.symfony-project.com)

%description
This package adds the symfony channel which allows
PEAR packages from this channel to be installed.


%prep
%setup -q -c -T


%build
# Empty build section, nothing to build


%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT%{pear_xmldir}
%{__install} -pm 644 %{SOURCE0} $RPM_BUILD_ROOT%{pear_xmldir}/pear.symfony-project.com.xml


%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post
if [ $1 -eq  1 ] ; then
	%{__pear} channel-add %{pear_xmldir}/pear.symfony-project.com.xml > /dev/null || :
else
	%{__pear} channel-update %{pear_xmldir}/pear.symfony-project.com.xml > /dev/null ||:
fi


%postun
if [ $1 -eq 0 ] ; then
	%{__pear} channel-delete pear.symfony-project.com > /dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_xmldir}/*


%changelog
* Wed Oct 16 2013 David Bishop <david@gnuconsulting.com>
- Initial build
