Summary: 	Crypto and SSL toolkit for Python
Name: 		python-m2crypto
Version: 	0.21.1
Release: 	1
Source0:	http://pypi.python.org/packages/source/M/M2Crypto/M2Crypto-%{version}.tar.gz
License:	MIT
Group: 		Development/Python
BuildRoot: 	%{_tmppath}/%{name}-buildroot
Url: 		http://chandlerproject.org/Projects/MeTooCrypto
BuildRequires:	swig
BuildRequires:	openssl-devel

%description
M2Crypto is a crypto and SSL toolkit for Python featuring the following:

    * RSA, DSA, DH, HMACs, message digests, symmetric ciphers (including AES).
    * SSL functionality to implement clients and servers.
    * HTTPS extensions to Python's httplib, urllib, and xmlrpclib.
    * Unforgeable HMAC'ing AuthCookies for web session management.
    * FTP/TLS client and server.
    * S/MIME.
    * ZServerSSL: A HTTPS server for Zope.
    * ZSmime: An S/MIME messenger for Zope.

%prep
%setup -q -n M2Crypto-%version
for i in SWIG/_ec.i SWIG/_evp.i; do
	sed -i -e "s/openssl\/opensslconf/%{multiarch_platform}\/openssl\/opensslconf/" "$i"
done

%build
env CFLAGS="$RPM_OPT_FLAGS" python setup.py build
# test requires some files ( such as a certificat, so disabled for now )
#PYTHONPATH="./build/lib.linux-i686-2.4/M2Crypto/:." python tests/alltests.py
%install
python setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{py_platsitedir}/M2Crypto
%{py_platsitedir}/*.egg-info
%doc CHANGES README INSTALL LICENCE


%changelog
* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 0.20.2-4mdv2011.0
+ Revision: 667946
- mass rebuild

* Wed Apr 07 2010 Funda Wang <fwang@mandriva.org> 0.20.2-3mdv2011.0
+ Revision: 532467
- fix build with openssl 1.0 (patch from archlinux)

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 0.20.2-2mdv2010.1
+ Revision: 511632
- rebuilt against openssl-0.9.8m

* Sat Nov 21 2009 Funda Wang <fwang@mandriva.org> 0.20.2-1mdv2010.1
+ Revision: 468012
- New version 0.20.2

* Wed Jul 23 2008 Thierry Vignaud <tv@mandriva.org> 0.17-3mdv2009.0
+ Revision: 242420
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sun May 27 2007 Pascal Terjan <pterjan@mandriva.org> 0.17-1mdv2008.0
+ Revision: 31668
- use python macro
- ship .egg-info
- 0.17


* Wed Nov 30 2005 Lenny Cartier <lenny@mandriva.com> 0.13-4mdk
- reupload and clean spec

* Tue Mar 01 2005 Michael Scherer <misc@mandrake.org> 0.13-3mdk
- Rebuild for new python
- fix compilation ( patch 0 )

* Sun May 30 2004 Pascal Terjan <pterjan@mandrake.org> 0.13-2mdk
- FIx DIRM

* Mon Apr 19 2004 Pascal Terjan <pterjan@mandrake.org> 0.13-1mdk
- First Mandrake package


