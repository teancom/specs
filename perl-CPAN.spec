%define modulename CPAN

Name: perl-%{modulename}
Version: 1.9800
Release: 1%{?_dist}
Summary:CPANiliscous 
License: distributable
Group: Development/Libraries
URL: http://search.cpan.org/search?mode=module&query=CPAN
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: perl >= 0:5.00503
BuildRequires: perl(Module::Signature) perl(YAML) perl(Archive::Zip) perl(YAML::XS) perl(Text::Glob) perl(Term::ReadKey)
BuildRequires: perl(File::HomeDir) perl(Compress::Bzip2) perl(YAML::Syck) perl(LWP::UserAgent)
BuildRequires: perl-HTTP-Tiny >= 0.005 
Autoreq: no
Requires: perl-HTTP-Tiny >= 0.005 
Requires: perl-Module-Signature perl-Archive-Zip perl-YAML-LibYAML perl-Text-Glob perl-TermReadKey perl-File-HomeDir perl-YAML-Syck
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
mkdir -p $RPM_BUILD_ROOT/usr/local/bin
mv $RPM_BUILD_ROOT/usr/bin/cpan $RPM_BUILD_ROOT/usr/local/bin/cpan

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
%exclude /usr/share/man/*/*

%changelog
* Sun Jan 22 2012 David Bishop <david@gnuconsulting.com> 1.9800-1
- Initial build. 
