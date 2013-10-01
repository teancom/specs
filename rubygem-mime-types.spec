# Generated from mime-types-1.17.2.gem by gem2rpm -*- rpm-spec -*-
%global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname mime-types
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global rubyabi 1.8
%global ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"] ')

Summary: This library allows for the identification of a file's likely MIME content type
Name: rubygem-%{gemname}
Version: 1.17.2
Release: 1%{?_dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://mime-types.rubyforge.org/
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
This library allows for the identification of a file's likely MIME content
type. This is release 1.17.2. The identification of MIME content type is based
on a file's filename extensions.
MIME::Types for Ruby originally based on and synchronized with MIME::Types for
Perl by Mark Overmeer, copyright 2001 - 2009. As of version 1.15, the data
format for the MIME::Type list has changed and the synchronization will no
longer happen.
Homepage::  http://mime-types.rubyforge.org/
GitHub::    http://github.com/halostatue/mime-types/
Copyright:: 2002 - 2011, Austin Ziegler
Based in part on prior work copyright Mark Overmeer
:include: License.rdoc


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
rm -rf %{_tmppath}/%{gemname}-%{version}

%files -f %{_tmppath}/%{gemname}-%{version}-filelist
%defattr(-, root, root, -)


%changelog
* Sat Feb 04 2012 David Bishop - 1.17.2-1
- Initial package
