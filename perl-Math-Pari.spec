# This package includes the pari library source even though that is
# being introduced to Fedora Extras in its own right (#169703). The
# rationale for this is:
# (a)	This package patches the library source code
# (b)	This package integrates very tightly with the library and may
#	break if the library is changed underneath it
# (c)	Functionality is lost if built against an external PARI library
#	(see the INSTALL file in the distribution)

Summary:	Perl interface to PARI
Name:		perl-Math-Pari
Version:	2.01080605
# You'll need to replace pariversion with a hardcoded version number if you're
# testing with a development version of PARI, as this expression evaluates
# the latest version of GP/PARI the perl module was tested with.
#%define pariversion %(echo %{version} | %{__perl} -pi -e 's/(\\d+)\\.(\\d\\d)(\\d\\d).*/sprintf("%d.%d.%d",$1,$2,$3)/e')
%define pariversion 2.1.7
Release:	4%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
Url:		http://search.cpan.org/dist/Math-Pari/
Source0:	http://search.cpan.org/CPAN/authors/id/I/IL/ILYAZ/modules/Math-Pari-%{version}.tar.gz
Source1:	http://pari.math.u-bordeaux.fr/pub/pari/unix/OLD/pari-%{pariversion}.tgz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires:	perl(ExtUtils::MakeMaker)

%description
This package is a Perl interface to the famous library PARI for numerical/
scientific/ number-theoretic calculations. It allows use of most PARI functions
as Perl functions, and (almost) seamless merging of PARI and Perl data.

%prep
%setup -q -n Math-Pari-%{version} -a 1

# Remove redundant provides (there's also a versioned one)
%global provfilt /bin/sh -c "%{__perl_provides} | %{__grep} -Fvx 'perl(Math::Pari)'"
%define __perl_provides %{provfilt}

%build
# machine=linux-none needed to avoid breakage of 64-bit builds
# other flags cribbed from pari.spec (#169703)
export DLCFLAGS=-fPIC
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor \
	OPTIMIZE="%{optflags} -fomit-frame-pointer" \
	machine=none
%{__make} %{?_smp_mflags}

%check
%{__make} test

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install PERL_INSTALL_ROOT=%{buildroot}
/usr/bin/find %{buildroot} -type f -name .packlist -exec %{__rm} -f {} ';'
/usr/bin/find %{buildroot} -type f -name '*.bs' -a -size 0 -exec %{__rm} -f {} ';'
/usr/bin/find %{buildroot} -depth -type d -exec /bin/rmdir {} 2>/dev/null ';'
%{__chmod} -R u+w %{buildroot}/*

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README
%dir %{perl_vendorarch}/Math/
%exclude %doc %{perl_vendorarch}/Math/libPARI.dumb.pod
%doc %{perl_vendorarch}/Math/libPARI.pod
%{perl_vendorarch}/Math/*.pm
%{perl_vendorarch}/auto/Math/
%{_mandir}/man3/Math::Pari.3pm*
%{_mandir}/man3/Math::PariInit.3pm*
%{_mandir}/man3/Math::libPARI.3pm*
%exclude %{_mandir}/man3/Math::libPARI.dumb.3pm*

%changelog
* Mon Aug 13 2007 Paul Howarth <paul@city-fan.org> 2.010709-3
- clarify license as GPL v1 or later, or Artistic (same as perl)

* Wed Apr 18 2007 Paul Howarth <paul@city-fan.org> 2.010709-2
- Buildrequire perl(ExtUtils::MakeMaker)

* Fri Oct 27 2006 Paul Howarth <paul@city-fan.org> 2.010709-1
- Update to 2.010709

* Wed Oct 18 2006 Paul Howarth <paul@city-fan.org> 2.010708-1
- Update to 2.010708
- Fix argument order for find with -depth
- Fix Source1 URL

* Wed Aug 30 2006 Paul Howarth <paul@city-fan.org> 2.010706-2
- FE6 mass rebuild

* Fri Jun  2 2006 Paul Howarth <paul@city-fan.org> 2.010706-1
- Update to 2.010706

* Wed May 31 2006 Paul Howarth <paul@city-fan.org> 2.010705-1
- Update to 2.010705

* Tue Apr 18 2006 Paul Howarth <paul@city-fan.org> 2.010704-2
- Omit dumb docs (#175198)

* Mon Mar 20 2006 Paul Howarth <paul@city-fan.org> 2.010704-1
- Update to 2.010704

* Fri Mar 17 2006 Paul Howarth <paul@city-fan.org> 2.010703-2
- Simplify %%{__perl_requires} filter

* Wed Feb  1 2006 Paul Howarth <paul@city-fan.org> 2.010703-1
- Update to 2.010703
- Make pari version number calculation more robust

* Wed Dec  7 2005 Paul Howarth <paul@city-fan.org> 2.010702-1
- Initial build
