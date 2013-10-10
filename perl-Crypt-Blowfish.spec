%define modulename Crypt-Blowfish

Name: perl-%{modulename}
Version: 2.14
Release: 1%{?_dist}
Summary: Crypt::CBC compliant Blowfish encryption module
License: distributable
Group: Development/Libraries
URL: http://search.cpan.org/search?mode=module&query=Crypt-Blowfish
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: perl >= 0:5.00503, perl(Test::Manifest)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Source0: %{modulename}-%{version}.tar.gz

%description
This module implements the Blowfish cipher.

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
* Mon Oct 07 2013 David Bishop <david@gnuconsulting.com> 2.14-1
- Initial build
