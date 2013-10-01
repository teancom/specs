# Generated from activesupport-3.2.0.gem by gem2rpm -*- rpm-spec -*-
%global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname activesupport
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global rubyabi 1.8
%global ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"] ')

Summary: A toolkit of support libraries and Ruby core extensions extracted from the Rails framework
Name: rubygem-%{gemname}
Version: 3.2.0
Release: 1%{?_dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://www.rubyonrails.org
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem

Requires: ruby(abi) = %{rubyabi}
Requires: rubygems >= 0
Requires: ruby >= 1.8.7

Requires: rubygem(i18n) => 0.6

Requires: rubygem(i18n) < 1

Requires: rubygem(multi_json) => 1.0

Requires: rubygem(multi_json) < 2
BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
BuildRequires: rubygems >= 0
BuildRequires: ruby >= 1.8.7
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
A toolkit of support libraries and Ruby core extensions extracted from the
Rails framework. Rich support for multibyte strings, internationalization,
time zones, and testing.


%prep
rm -rf %{buildroot}
rm -rf ./%{name}

%build
mkdir -p ./%{name}/%{gemdir}
export CONFIGURE_ARGS="--with-cflags='%{optflags}' --libdir=%{_libdir}"
gem install --local --install-dir ./%{name}/%{gemdir} -V \
            --force --rdoc %{SOURCE0}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
cp -a ./%{name}/%{gemdir}/* %{buildroot}%{gemdir}

cd %{buildroot}
find ./usr -type f -print | \
        sed "s@^\.@@g" > %{_tmppath}/%{gemname}-%{version}-filelist

if [ "$(cat %{_tmppath}/%{gemname}-%{version}-filelist)X" = "X" ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit -1
fi


%clean
rm -rf %{buildroot}
rm -f %{_tmppath}/%{gemname}-%{version}-filelist

%files -f %{_tmppath}/%{gemname}-%{version}-filelist
%defattr(-, root, root, -)


%changelog
* Sun Jan 22 2012 David Bishop - 3.2.0-1
- Initial package
