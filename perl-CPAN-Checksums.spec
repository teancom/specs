%define modulename CPAN-Checksums

Name: perl-%{modulename}
Version: 2.08
Release: 1%{?_dist}
Summary:Checksums all the CPANs 
License: distributable
Group: Development/Libraries
URL: http://search.cpan.org/search?mode=module&query=CPAN-Checksums
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: perl >= 0:5.00503
BuildRequires: perl(Module::Signature) perl(Compress::Bzip2) perl(Data::Compare)
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
        grep -v "\.packlist" > ../%{modulename}-%{version}-filelist
if [ "$(cat ../%{modulename}-%{version}-filelist)X" = "X" ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit -1
fi

%files -f ../%{modulename}-%{version}-filelist
%defattr(-,root,root)

%changelog
* Mon Jan 23 2012 David Bishop <david@gnuconsulting.com> 2.08-1
- Initial build. 
