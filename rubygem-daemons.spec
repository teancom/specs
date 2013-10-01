# Generated from daemons-1.1.6.gem by gem2rpm -*- rpm-spec -*-
%global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname daemons
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global rubyabi 1.8
%global ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"] ')

Summary: A toolkit to create and control daemons in different ways
Name: rubygem-%{gemname}
Version: 1.1.6
Release: 1%{?_dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://daemons.rubyforge.org
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
Daemons provides an easy way to wrap existing ruby scripts (for example a
self-written server)  to be run as a daemon and to be controlled by simple
start/stop/restart commands.  You can also call blocks as daemons and control
them from the parent or just daemonize the current process.  Besides this
basic functionality, daemons offers many advanced features like exception 
backtracing and logging (in case your ruby script crashes) and monitoring and
automatic restarting of your processes if they crash.


%prep

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
* Fri Jan 20 2012 David Bishop - 1.1.6-1
- Initial package
