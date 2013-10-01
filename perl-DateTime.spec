%define modulename DateTime

Name: perl-%{modulename}  
Version: 0.78
Release: 1%{?_dist}
Summary: A date and time object
License: distributable
Group: Development/Libraries
URL: http://search.cpan.org/search?mode=module&query=DateTime
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: perl >= 0:5.00503
BuildRequires: perl-Class-Singleton
BuildRequires: perl-DateTime-TimeZone >= 0.59
BuildRequires: perl-DateTime-Locale >= 0.41
BuildRequires: perl-Math-Round
BuildRequires: perl-Class-ISA >= 0.36
BuildRequires: perl-Module-Build >= 0.3601
BuildRequires: perl-version >= 0.87
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
AutoReq: no
Requires: perl(Math::Round)
Requires: perl(Class::Singleton) perl(DateTime::TimeZone)
Requires: perl-DateTime-Locale >= 0.41
Requires: perl-Class-ISA >= 0.36
Source0: %{modulename}-%{version}.tar.gz

%description
DateTime is a class for the representation of date/time combinations, and is part of the Perl DateTime project. For details on this project please see http://datetime.perl.org/. The DateTime site has a FAQ which may help answer many "how do I do X?" questions. The FAQ is at http://datetime.perl.org/faq.html.

It represents the Gregorian calendar, extended backwards in time before its creation (in 1582). This is sometimes known as the "proleptic Gregorian calendar". In this calendar, the first day of the calendar (the epoch), is the first day of year 1, which corresponds to the date which was (incorrectly) believed to be the birth of Jesus Christ.

The calendar represented does have a year 0, and in that way differs from how dates are often written using "BCE/CE" or "BC/AD".

For infinite datetimes, please see the DateTime::Infinite module.

%prep
%setup -q -n %{modulename}-%{version} 

%build
CFLAGS="$RPM_OPT_FLAGS" perl Build.PL installdirs=vendor
perl ./Build 

%check
perl ./Build test

%clean
rm -rf $RPM_BUILD_ROOT
%install

rm -rf $RPM_BUILD_ROOT
perl ./Build install destdir=$RPM_BUILD_ROOT

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
* Mon Jan 21 2013 David Bishop <david@gnuconsulting.com> 0.78-1
- Initial Maefsco build
