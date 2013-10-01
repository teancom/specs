# Generated from bluepill-0.0.52.gem by gem2rpm -*- rpm-spec -*-
%global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname bluepill
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global rubyabi 1.8
%global ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"] ')

Summary: A process monitor written in Ruby with stability and minimalism in mind
Name: rubygem-%{gemname}
Version: 0.0.52
Release: 1%{?_dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://github.com/arya/bluepill
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem

Requires: ruby(abi) = %{rubyabi}
Requires: rubygems >= 0
Requires: ruby >= 0

Requires: rubygem(daemons) => 1.1.0

Requires: rubygem(daemons) < 1.2

Requires: rubygem(state_machine) => 1.1.0

Requires: rubygem(state_machine) < 1.2

Requires: rubygem(activesupport) >= 3.0.0

Requires: rubygem(i18n) >= 0.5.0
BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
BuildRequires: rubygems >= 0
BuildRequires: ruby >= 0
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Bluepill keeps your daemons up while taking up as little resources as
possible. After all you probably want the resources of your server to be used
by whatever daemons you are running rather than the thing that's supposed to
make sure they are brought back up, should they die or misbehave.


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
mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{gemdir}/bin
find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

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
* Sun Jan 22 2012 David Bishop - 0.0.52-1
- Initial package
