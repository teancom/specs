%define modulename Parse-CPAN-Meta

Name: perl-%{modulename}
Version: 1.4409
Release: 1%{?_dist}
Summary:Parse META.yml and META.json CPAN metadata files 
License: distributable
Group: Development/Libraries
URL: http://search.cpan.org/search?mode=module&query=Parse-CPAN-Meta
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: perl >= 0:5.00503
BuildRequires: perl-CPAN-Meta-YAML >= 0.008 
BuildRequires: perl-JSON-PP >= 2.27200 
Epoch: 1
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
* Fri Feb 10 2012 David Bishop <david@gnuconsulting.com> 1.4402-1
- Initial build. 
