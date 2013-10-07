%define modulename Params-Validate

Name: perl-%{modulename}
Version: 1.08
Release: 1%{?_dist}
Summary: Validate method/function parameters
License: distributable
Group: Development/Libraries
URL: http://search.cpan.org/search?mode=module&query=Params-Validate
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: perl >= 0:5.00503, perl(Scalar::Util)
BuildRequires: perl(Test::More)
BuildRequires: perl-Attribute-Handlers >= 0.79
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Source0: %{modulename}-%{version}.tar.gz

%description
The Params::Validate module allows you to validate method or function call parameters to an arbitrary level of specificity. At the simplest level, it is capable of validating the required parameters were given and that no unspecified additional parameters were passed in.

It is also capable of determining that a parameter is of a specific type, that it is an object of a certain class hierarchy, that it possesses certain methods, or applying validation callbacks to arguments.

%prep
%setup -q -n %{modulename}-%{version} 

%build
CFLAGS="$RPM_OPT_FLAGS" perl Build.PL installdirs=vendor destdir=$RPM_BUILD_ROOT
perl ./Build

%check
perl ./Build test

%clean
rm -rf $RPM_BUILD_ROOT
%install

rm -rf $RPM_BUILD_ROOT
perl ./Build install DESTDIR=$RPM_BUILD_ROOT

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
* Mon Jan 21 2013 David Bishop <david@gnuconsulting.com> 1.07-1
- Initial build. 
