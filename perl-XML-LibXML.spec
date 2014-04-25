%{!?perl_vendorarch: %define perl_vendorarch %(eval "`perl -V:installvendorarch`"; echo $installvendorarch)}

Summary: XML-LibXML Perl module
Name: perl-XML-LibXML
Version: 2.0115
Release: 1%{?_dist}
License: GPL or Artistic
Group: Development/Libraries
URL: http://search.cpan.org/dist/XML-LibXML/
Epoch: 1
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: perl >= 2:5.8.0
Requires: %(perl -MConfig -le 'if (defined $Config{useithreads}) { print "perl(:WITH_ITHREADS)" } else { print "perl(:WITHOUT_ITHREADS)" }')
Requires: %(perl -MConfig -le 'if (defined $Config{usethreads}) { print "perl(:WITH_THREADS)" } else { print "perl(:WITHOUT_THREADS)" }')
Requires: %(perl -MConfig -le 'if (defined $Config{uselargefiles}) { print "perl(:WITH_LARGEFILES)" } else { print "perl(:WITHOUT_LARGEFILES)" }')
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Source0: XML-LibXML-%{version}.tar.gz
BuildRequires: perl(XML::SAX) perl(XML::NamespaceSupport)
BuildRequires: libxml2-devel >= 2.7.3
Requires: perl(XML::SAX) perl(XML::NamespaceSupport)
Obsoletes: perl(XML::LibXML::XPathContext) <= 1.61
Obsoletes: perl-XML-LibXML-Common

%description
%{summary}.

%prep
%setup -q -n XML-LibXML-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" SKIP_SAX_INSTALL=1 perl Makefile.PL INSTALLDIRS=vendor
# the date was different on different architecture (multilib problem), so I set the date with -d
make OPTIMIZE="$RPM_OPT_FLAGS" POD2MAN_EXE="\$(PERLRUN) \"-MExtUtils::Command::MM\" -e pod2man \"--\" -d 2004-03-21"

%install
rm -rf $RPM_BUILD_ROOT
make install \
  PERL_INSTALL_ROOT=$RPM_BUILD_ROOT \
  INSTALLARCHLIB=$RPM_BUILD_ROOT%{perl_archlib}
find $RPM_BUILD_ROOT -type f -a \( -name perllocal.pod -o -name .packlist \
  -o \( -name '*.bs' -a -empty \) \) -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- perl-XML-SAX
for p in XML::LibXML::SAX::Parser XML::LibXML::SAX ; do
  perl -MXML::SAX -e "XML::SAX->add_parser(q($p))->save_parsers()" || :
done

%preun
if [ $1 -eq 0 ] ; then
  for p in XML::LibXML::SAX::Parser XML::LibXML::SAX ; do
    perl -MXML::SAX -e "XML::SAX->remove_parser(q($p))->save_parsers()" \
      2>/dev/null || :
  done
fi

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%attr(0755, root, root) %dir %{perl_vendorarch}/XML
%attr(0755, root, root) %dir %{perl_vendorarch}/XML/LibXML
%attr(0755, root, root) %dir %{perl_vendorarch}/XML/LibXML/SAX
%attr(0755, root, root) %dir %{perl_vendorarch}/auto/XML
%attr(0755, root, root) %dir %{perl_vendorarch}/auto/XML/LibXML
%{perl_vendorarch}/auto/XML
%{perl_vendorarch}/XML
%{_mandir}/man3/*.3*

%changelog
* Mon Jan 21 2013 David Bishop <david@gnuconsulting.com> 2.0014-1
- Initial Maefsco build
