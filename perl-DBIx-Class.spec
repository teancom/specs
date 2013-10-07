%define modulename DBIx-Class

Name: perl-%{modulename}
Version: 0.08250
Release: 1%{?_dist}
Summary:... is what CPAN says, anyways. 
License: distributable
Group: Development/Libraries
URL: http://search.cpan.org/search?mode=module&query=DBIx-Class
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: perl >= 0:5.00503
#Requires:      perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires: perl-DBD-SQLite >=               1.29
BuildRequires: perl-File-Temp >=              0.22
BuildRequires: perl-Package-Stash          >=  0.36
BuildRequires: perl-Test-Simple             >= 0.98 
BuildRequires: perl-Test-Deep                >= 0.101
BuildRequires: perl-Test-Exception           >= 0.31
BuildRequires: perl-Test-Warn                >= 0.21
BuildRequires: perl-Class-Accessor-Grouped  >= 0.10010
BuildRequires: perl-Class-C3-Componentised  >= 1.0009
BuildRequires: perl-Class-Inspector          >= 1.24
BuildRequires: perl-Config-Any               >= 0.20
BuildRequires: perl-Context-Preserve         >= 0.01
BuildRequires: perl-DBI                       >= 1.63
BuildRequires: perl-Data-Compare             >= 1.22
BuildRequires: perl-Data-Dumper-Concise     >= 2.020
BuildRequires: perl-Data-Page                >= 2.00
BuildRequires: perl-Devel-GlobalDestruction  >= 0.09
BuildRequires: perl-PathTools                >= 3.40
BuildRequires: perl-Hash-Merge               >= 0.12
BuildRequires: perl-Scalar-List-Utils        >= 1.21
BuildRequires: perl-MRO-Compat               >= 0.12
BuildRequires: perl-Module-Find              >= 0.07
BuildRequires: perl-Moo                       >= 1.000006
BuildRequires: perl-Path-Class               >= 0.32 
BuildRequires: perl-SQL-Abstract             >= 1.73
BuildRequires: perl-Scope-Guard              >= 0.03
BuildRequires: perl-Sub-Name                 >= 0.05
BuildRequires: perl-Text-Balanced            >= 2.00
BuildRequires: perl-Try-Tiny                 >= 0.11 
BuildRequires: perl-namespace-clean          >= 0.24
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
* Tue Oct 01 2013 David Bishop <david@gnuconsulting.com> 0.08250-1
- Initial build. 
