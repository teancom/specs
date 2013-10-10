%define modulename JSON

Name: perl-%{modulename}
Version: 2.59
Release: 1%{?_dist}
Summary: JSON (JavaScript Object Notation) encoder/decoder
License: distributable
Group: Development/Libraries
URL: http://search.cpan.org/search?mode=module&query=JSON
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: perl >= 0:5.00503
BuildRequires: perl(Test::More)
Source0: %{modulename}-%{version}.tar.gz
BuildArch: noarch
AutoReq: no

%description
This module converts Perl data structures to JSON and vice versa using either JSON::XS or JSON::PP.

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
* Mon Oct 07 2013 David Bishop <david@gnuconsulting.com> 2.59-1
- Initial build. 
