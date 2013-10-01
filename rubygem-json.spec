# Generated from json-1.6.5.gem by gem2rpm -*- rpm-spec -*-
%global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname json
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global rubyabi 1.8
%global ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"] ')

Summary: JSON Implementation for Ruby
Name: rubygem-%{gemname}
Version: 1.6.5
Release: 1%{?_dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://flori.github.com/json
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem

Requires: ruby(abi) = %{rubyabi}
Requires: rubygems >= 0
Requires: ruby >= 0
BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
BuildRequires: rubygems >= 0
BuildRequires: ruby >= 0
Provides: rubygem(%{gemname}) = %{version}

%description
This is a JSON implementation as a Ruby extension in C.


%prep
%setup -q -T -c

%build
mkdir -p ./%{gemdir}
export CONFIGURE_ARGS="--with-cflags='%{optflags}' --libdir=%{_libdir}"
gem install --local --install-dir ./%{gemdir} -V \
            --force --rdoc %{SOURCE0}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
cp -a ./%{gemdir}/* %{buildroot}%{gemdir}

find $RPM_BUILD_ROOT/usr -type f -print | \
        sed "s@^$RPM_BUILD_ROOT@@g" > %{gemname}-%{version}-filelist

if [ "$(cat %{gemname}-%{version}-filelist)X" = "X" ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit -1
fi


%clean
rm -rf %{buildroot}

%files -f %{gemname}-%{version}-filelist
%defattr(-, root, root, -)


%changelog
* Thu Jan 19 2012 David Bishop - 1.6.5-1
- Initial package
