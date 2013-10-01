%define modulename XML-SAX
%define perl_version %(eval "`%{__perl} -V:version`"; echo $version)

Name: perl-%{modulename}
Version: 0.99
Release: 1%{?_dist}
Summary: Easy API to maintain XML
License: distributable
Group: Development/Libraries
URL: http://search.cpan.org/search?mode=module&query=XML-SAX
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: perl >= 0:5.00503
BuildRequires: perl-XML-NamespaceSupport 
BuildRequires: perl-XML-SAX-Base
Source0: %{modulename}-%{version}.tar.gz
AutoReq: no
BuildArch: noarch

%define buildroot_include_path %{BUILDROOT}/usr/share/perl5/vendor_perl

%description
The XML::SAX module provides a simple XML parsing module.

%prep
%setup -q -n %{modulename}-%{version} 

%build
echo "n" | CFLAGS="$RPM_OPT_FLAGS" perl Makefile.PL INSTALLDIRS=vendor
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

%post
if [ ! -a "/usr/lib/perl5/vendor_perl/%{perl_version}/XML/SAX/ParserDetails.ini" ]; then
perl -I %{buildroot_include_path} -MXML::SAX -e "XML::SAX->add_parser(q(XML::SAX::PurePerl))->save_parsers()"
fi

%changelog
* Mon Jan 21 2013 David Bishop <david@gnuconsulting.com> 0.99-1
- Initial Maefsco build
