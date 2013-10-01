# $Revision: 1.119 $, $Date: 2012/07/07 18:32:39 $
#
# Conditional build:
%bcond_with	pcre16		# enable 16 bit character support (one test fails)
%bcond_without	static_libs	# don't build static libraries
%bcond_without	tests		# don't perform "make check"

Summary:	Perl-Compatible Regular Expression library
Summary(pl.UTF-8):	Biblioteka perlowych wyrażeń regularnych
Summary(pt_BR.UTF-8):	Biblioteca de expressões regulares versão
Name:		pcre8
Version:	8.32
Release:	1%{?_dist}
License:	BSD (see LICENCE)
Group:		Libraries
Source0:	ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-%{version}.tar.bz2
Patch0:		%{name}-pcreposix-glibc-conflict.patch
URL:		http://www.pcre.org/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	libstdc++-devel
BuildRequires:	readline-devel
BuildRequires:	zlib-devel
Obsoletes:	libpcre0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PCRE stands for the Perl Compatible Regular Expression library. It
contains routines to match text against regular expressions similar to
Perl's. It also contains a POSIX compatibility library.

%package devel
Summary:	Perl-Compatible Regular Expression header files and development documentation
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja do bibliotek pcre
Summary(pt_BR.UTF-8):	Arquivos para desenvolvimento com pcre
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	libpcre0-devel

%description devel
Perl-Compatible Regular Expression header files and development
documentation.

%package static
Summary:	Perl-Compatible Regular Expression static libraries
Summary(pl.UTF-8):	Biblioteki statyczne pcre
Summary(pt_BR.UTF-8):	Arquivos para desenvolvimento estático com pcre
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Perl-Compatible Regular Expression library static libraries.

%package cxx
Summary:	C++ wrapper to PCRE library
Summary(pl.UTF-8):	Interfejs C++ do biblioteki PCRE
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description cxx
C++ wrapper to PCRE library.

%package cxx-devel
Summary:	Header file for C++ wrapper to PCRE library
Summary(pl.UTF-8):	Plik nagłówkowy interfejsu C++ do biblioteki PCRE
Group:		Development/Libraries
Requires:	%{name}-cxx = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Requires:	libstdc++-devel

%description cxx-devel
Header file for C++ wrapper to PCRE library.

%package cxx-static
Summary:	Static version of pcrecpp library
Summary(pl.UTF-8):	Statyczna wersja biblioteki pcrecpp
Group:		Development/Libraries
Requires:	%{name}-cxx-devel = %{version}-%{release}

%description cxx-static
Static version of pcrecpp library.

%package -n pcregrep
Summary:	Grep using Perl Compatible Regular Expressions
Summary(pl.UTF-8):	Grep używający perlowych wyrażeń regularnych
Group:		Applications/Text
Obsoletes:	pgrep

%description -n pcregrep
pgrep is a grep workalike which uses perl-style regular expressions
instead of POSIX regular expressions.

%package -n pcretest
Summary:	A program for testing Perl-comaptible regular expressions
Summary(pl.UTF-8):	Program do testowania kompatybilnych z perlem wyrażeń regularnych
Group:		Applications/Text

%description -n pcretest
pcretest is a program which you can use to test regular expression.

%package doc-html
Summary:	Documentation for PCRE in HTML format
Summary(pl.UTF-8):	Dokumentacja dla PCRE w formacie HTML
Group:		Applications/Text

%description doc-html
Documentation for PCRE in HTML format.

%description doc-html -l pl.UTF-8
Dokumentacja dla PCRE w formacie HTML.

%prep
%setup -q -n pcre-%{version}
#%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake} --add-missing
%configure \
	CXXLDFLAGS="%{rpmldflags}" \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--enable-jit \
	%{?with_pcre16:--enable-pcre16} \
	--enable-pcregrep-libz \
	--enable-pcregrep-libbz2 \
	--enable-pcretest-libreadline \
	--enable-unicode-properties \
	--enable-utf8

%{__make}

%if %{with tests}
# tests need big stack
ulimit -s 32768
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/%{_lib},%{_examplesdir}/%{name}-%{version}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_libdir}/libpcre.so.* $RPM_BUILD_ROOT/%{_lib}
mv -f $RPM_BUILD_ROOT%{_libdir}/libpcreposix.so.* $RPM_BUILD_ROOT/%{_lib}
%{?with_pcre16:mv -f $RPM_BUILD_ROOT%{_libdir}/libpcre16.so.* $RPM_BUILD_ROOT/%{_lib}}

ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libpcre.so.*.*.*) $RPM_BUILD_ROOT%{_libdir}/libpcre.so
%{?with_pcre16:ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libpcre16.so.*.*.*) $RPM_BUILD_ROOT%{_libdir}/libpcre16.so}
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libpcreposix.so.*.*.*) $RPM_BUILD_ROOT%{_libdir}/libpcreposix.so

cp -a pcredemo.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

rm -rf $RPM_BUILD_ROOT%{_docdir}/pcre

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post   cxx -p /sbin/ldconfig
%postun cxx -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README NEWS LICENCE ChangeLog
%attr(755,root,root) /%{_lib}/libpcre.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libpcre.so.1
%attr(755,root,root) /%{_lib}/libpcreposix.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libpcreposix.so.0
%if %{with pcre16}
%attr(755,root,root) /%{_lib}/libpcre16.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libpcre16.so.0
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pcre-config
%attr(755,root,root) %{_libdir}/libpcre.so
%{?with_pcre16:%attr(755,root,root) %{_libdir}/libpcre16.so}
%attr(755,root,root) %{_libdir}/libpcreposix.so
%{_libdir}/libpcre.la
%{?with_pcre16:%{_libdir}/libpcre16.la}
%{_libdir}/libpcreposix.la
%{_includedir}/pcre.h
%{_includedir}/pcreposix.h
%{_libdir}/pkgconfig/libpcre.pc
%{?with_pcre16:%{_libdir}/pkgconfig/libpcre16.pc}
%{_libdir}/pkgconfig/libpcreposix.pc
%exclude %{_mandir}/man1/pcre-config.1*
%exclude %{_mandir}/man3/pcre*.3*
%exclude %{_mandir}/man3/pcrecpp.3*
#%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libpcre.a
%{?with_pcre16:%{_libdir}/libpcre16.a}
%{_libdir}/libpcreposix.a
%endif

%files cxx
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpcrecpp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcrecpp.so.0

%files cxx-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpcrecpp.so
%{_libdir}/libpcrecpp.la
%{_includedir}/pcrecpp.h
%{_includedir}/pcre_scanner.h
%{_includedir}/pcre_stringpiece.h
%{_includedir}/pcrecpparg.h
%{_libdir}/pkgconfig/libpcrecpp.pc
%exclude %{_mandir}/man3/pcrecpp.3*

%if %{with static_libs}
%files cxx-static
%defattr(644,root,root,755)
%{_libdir}/libpcrecpp.a
%endif

%files -n pcregrep
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pcregrep
%exclude %{_mandir}/man1/pcregrep.1*

%files -n pcretest
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pcretest
%exclude %{_mandir}/man1/pcretest.1*

%files doc-html
%defattr(644,root,root,755)
%doc doc/html/*

%define date	%(echo `LC_ALL="C" date +"%a %b %d %Y"`)
%changelog
* Fri Mar 01 2013 David Bishop <david@gnuconsulting.com> 8.32-1
Initial build for maefsco
