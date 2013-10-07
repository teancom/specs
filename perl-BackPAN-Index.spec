%define modulename BackPAN-Index

Name: perl-%{modulename}
Version: 0.42
Release: 1%{?_dist}
Summary:... is what CPAN says, anyways. 
License: distributable
Group: Development/Libraries
URL: http://search.cpan.org/search?mode=module&query=BackPAN-Index
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: perl >= 0:5.00503
BuildRequires: perl-autodie
BuildRequires: perl-CPAN-DistnameInfo
BuildRequires: perl-Mouse
#Requires:      perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Source0: %{modulename}-%{version}.tar.gz
BuildArch: noarch

%description
%{summary}.

%prep
%setup -q -n %{modulename}-%{version} 

%build
CFLAGS="$RPM_OPT_FLAGS" perl Build.PL installdirs=vendor destdir=$RPM_BUILD_ROOT
perl ./Build

%check
perl ./Build test

%clean
rm -rf $RPM_BUILD_ROOT
%install

rm -rf $RPM_BUILD_ROOT
perl ./Build install DESTDIR=$RPM_BUILD_ROOT

[ -x /usr/lib/rpm/brp-compress ] && /usr/lib/rpm/brp-compress

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
* Tue Oct 01 2013 David Bishop <david@gnuconsulting.com> 0.42-1
- Initial build. 
