%define modulename Carp

Name: perl-%{modulename}
Version: 1.32
Release: 1%{?_dist}
Summary:Throw exceptions outside current package... is what CPAN says, anyways. 
License: distributable
Group: Development/Libraries
URL: http://search.cpan.org/search?mode=module&query=Carp
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: perl >= 0:5.00503
BuildRequires: perl-parent
#Requires:      perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
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
%exclude %{_mandir}/man3/*

%changelog
* Sat Sep 14 2013 David Bishop <david@gnuconsulting.com> 1.32-1
- Initial build. 
