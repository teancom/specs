# Generated from multi_json-1.0.4.gem by gem2rpm -*- rpm-spec -*-
%global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname multi_json
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global rubyabi 1.8
%global ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"] ')

Summary: A gem to provide swappable JSON backends
Name: rubygem-%{gemname}
Version: 1.0.4
Release: 1%{?_dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://github.com/intridea/multi_json
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem

Requires: ruby(abi) = %{rubyabi}
Requires: rubygems >= 1.3.6
Requires: ruby >= 0
BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
BuildRequires: rubygems >= 1.3.6
BuildRequires: ruby >= 0
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
A gem to provide swappable JSON backends utilizing Yajl::Ruby, the JSON gem,
JSON pure, or a vendored version of okjson.


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
* Sun Jan 22 2012 David Bishop - 1.0.4-1
- Initial package
