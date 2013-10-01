# Generated from builder-3.0.0.gem by gem2rpm -*- rpm-spec -*-
%global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname builder
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global rubyabi 1.8
%global ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"] ')

Summary: Builders for MarkUp
Name: rubygem-%{gemname}
Version: 3.0.0
Release: 1%{?_dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://onestepback.org
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem

Requires: ruby(abi) = %{rubyabi}
Requires: rubygems >= 0
Requires: ruby >= 0
BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
BuildRequires: rubygems >= 0
BuildRequires: ruby >= 0
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Builder provides a number of builder objects that make creating structured
data
simple to do.  Currently the following builder objects are supported:
* XML Markup
* XML Events

%package -n ruby-%{gemname}
Summary: Builders for MarkUp
Group: Development/Languages
Requires: rubygem(%{gemname}) = %{version}
%description -n ruby-%{gemname}
Builder provides a number of builder objects that make creating structured
data
simple to do.  Currently the following builder objects are supported:
* XML Markup
* XML Events

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

mkdir -p %{buildroot}%{ruby_sitelib}
ln -s %{gemdir}/gems/%{gemname}-%{version}/lib/blankslate.rb %{buildroot}%{ruby_sitelib}
ln -s %{gemdir}/gems/%{gemname}-%{version}/lib/builder.rb %{buildroot}%{ruby_sitelib}

%clean
rm -rf %{buildroot}
rm -f %{_tmppath}/%{gemname}-%{version}-filelist

%files -f %{_tmppath}/%{gemname}-%{version}-filelist
%defattr(-, root, root, -)

%files -n ruby-%{gemname}
%defattr(-, root, root, -)
%{ruby_sitelib}/*

%changelog
* Sat Feb 04 2012 David Bishop - 3.0.0-1
- Initial package
