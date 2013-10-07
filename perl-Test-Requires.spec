%define modulename Test-Requires

Name: perl-%{modulename}
Version: 0.07
Release: 1%{?_dist}
Summary:... is what CPAN says, anyways. 
License: distributable
Group: Development/Libraries
URL: http://search.cpan.org/search?mode=module&query=Test-Requires
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: perl >= 0:5.00503
#Requires:      perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Source0: %{modulename}-%{version}.tar.gz
BuildArch: noarch

%description
%{summary}.

%prep
%setup -q -n %{modulename}-%{version} 

%build
grep -rsl '^#!.*perl' . |
grep -v '.bak$' |xargs --no-run-if-empty \
%__perl -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)'
%{__perl} Build.PL
%{__perl} Build

%clean
rm -rf $RPM_BUILD_ROOT
%install

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%{__perl} Build install destdir=%{buildroot}

cmd=/usr/share/spec-helper/compress_files
[ -x $cmd ] || cmd=/usr/lib/rpm/brp-compress
[ -x $cmd ] && $cmd

find $RPM_BUILD_ROOT \( -name perllocal.pod -o -name .packlist \) -exec rm -v {} \;

find $RPM_BUILD_ROOT/usr -type f -print | \
        sed "s@^$RPM_BUILD_ROOT@@g" | \
        grep -v perllocal.pod | \
        grep -v "\.packlist" > %{modulename}-%{version}-filelist
if [ "$(cat %{modulename}-%{version}-filelist)X" = "X" ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit -1
fi

%files -f %{modulename}-%{version}-filelist
%defattr(-,root,root)

%changelog
* Mon Jan 21 2013 David Bishop <david@gnuconsulting.com> 0.06-1
- Initial build. 
