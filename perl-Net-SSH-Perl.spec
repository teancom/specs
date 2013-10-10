%define modulename Net-SSH-Perl

Name: perl-%{modulename}
Version: 1.36
Release: 1%{?_dist}
Summary:Perl client interface to SSH 
License: distributable
Group: Development/Libraries
URL: http://search.cpan.org/search?mode=module&query=Net-SSH-Perl
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: perl >= 0:5.00503
BuildRequires: perl(Crypt::DSA) perl(Convert::PEM) perl(Crypt::IDEA) 
BuildRequires: perl(Digest::HMAC_MD5) perl(Crypt::DH) perl(Math::GMP) 
BuildRequires: perl(Crypt::DES) perl(String::CRC32) perl(Math::Pari) 
Requires: perl(Class::ErrorHandler) perl(Math::Pari) >= 2.01080605-3 perl(Math::BigInt::Pari)
Source0: %{modulename}-%{version}.tar.gz
BuildArch: noarch

%description
%{summary}.

%prep
%setup -q -n %{modulename}-%{version} 

%build
echo "2" | CFLAGS="$RPM_OPT_FLAGS" perl Makefile.PL INSTALLDIRS=vendor
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
* Mon Oct 07 2013 David Bishop <david@gnuconsulting.com> 1.36-1
- Initial build. 
