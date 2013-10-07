%define modulename SQL-Abstract

Name: perl-%{modulename}
Version: 1.74
Release: 1%{?_dist}
Summary:Generate SQL from Perl data structures... is what CPAN says, anyways. 
License: distributable
Group: Development/Libraries
URL: http://search.cpan.org/search?mode=module&query=SQL-Abstract
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: perl >= 0:5.00503
#Requires:      perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires: perl-Class-Accessor-Grouped  >= 0.10005
BuildRequires: perl-Getopt-Long-Descriptive >= 0.091
BuildRequires: perl-Hash-Merge            >=   0.12
Source0: %{modulename}-%{version}.tar.gz
BuildArch: noarch

%description
%{summary}.

%prep
%setup -q -n %{modulename}-%{version} 

%build
CFLAGS="$RPM_OPT_FLAGS" perl Makefile.PL INSTALLDIRS=vendor
make

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT
%install

rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

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
* Tue Oct 01 2013 David Bishop <david@gnuconsulting.com> 1.74-1
- Initial build. 
