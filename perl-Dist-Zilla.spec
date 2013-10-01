%define modulename Dist-Zilla

Name: perl-%{modulename}
Version: 4.300007
Release: 1%{?_dist}
Summary:... is what CPAN says, anyways. 
License: distributable
Group: Development/Libraries
URL: http://search.cpan.org/search?mode=module&query=Dist-Zilla
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: perl >= 0:5.00503
BuildRequires: perl(Perl::PrereqScanner) perl(Test::Deep) perl(MooseX::SetOnce) perl(MooseX::LazyRequire) 
BuildRequires: perl(File::pushd) perl(File::HomeDir) perl(MooseX::Types::Path::Class)
BuildRequires: perl(Data::Section) perl(Log::Dispatchouli) perl(Perl::Version) perl(File::Find::Rule)
BuildRequires: perl(YAML::Tiny) perl(CPAN::Uploader) perl(File::ShareDir::Install) perl(MooseX::Types::Perl)
BuildRequires: perl(DateTime) perl(Pod::Eventual) perl(App::Cmd::Setup) perl(autobox) perl(Software::License)
BuildRequires: perl(Config::MVP::Reader::INI) perl(Moose::Autobox) perl(Hash::Merge::Simple) perl(File::Copy::Recursive)
BuildRequires: perl(File::ShareDir) perl(Sub::Exporter::ForMethods)
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

%changelog
* Thu Feb 09 2012 David Bishop <david@gnuconsulting.com> 4.300007-1
- Initial build. 
