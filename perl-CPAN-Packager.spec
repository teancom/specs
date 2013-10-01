%define modulename CPAN-Packager

Name: perl-%{modulename}
Version: 0.33
Release: 1%{?_dist}
Summary:Creates packages from modules 
License: distributable
Group: Development/Libraries
URL: http://search.cpan.org/search?mode=module&query=CPAN-Packager
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: perl >= 0:5.00503
BuildRequires: perl(FindBin::libs)
BuildRequires: perl(Hash::Merge)
BuildRequires: perl(List::Compare)
BuildRequires: perl(Module::Depends)
BuildRequires: perl-Getopt-Long-Descriptive >= 0.083
BuildRequires: perl-Kwalify >= 1.20
BuildRequires: perl-Log-Log4perl >= 1.26
BuildRequires: perl-MouseX-Getopt >= 0.33
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
* Sun Jan 22 2012 David Bishop <david@gnuconsulting.com> 0.33-1
- Initial build. 
