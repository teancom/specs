%define modulename DateTime-TimeZone

Name: perl-%{modulename}
Version: 1.56
Release: 1%{?_dist}
Summary:... is what CPAN says, anyways. 
License: distributable
Group: Development/Libraries
URL: http://search.cpan.org/search?mode=module&query=DateTime-TimeZone
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: perl >= 0:5.00503
BuildRequires: perl-Class-Load
BuildRequires: perl-Params-Validate >= 0.72
BuildRequires: perl-Test-Simple >= 0.88
BuildRequires: perl-Test-Output
BuildRequires: perl-parent
BuildRequires: perl-Class-Singleton
BuildRequires: perl-Params-Validate
BuildRequires: perl-PathTools
AutoReq: no
Requires: perl-Class-Singleton perl-Params-Validate
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
* Mon Jan 21 2013 David Bishop <david@gnuconsulting.com> 1.56-1
- Initial Maefsco build. 
