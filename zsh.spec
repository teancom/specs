# this file is encoded in UTF-8  -*- coding: utf-8 -*-

Summary: A powerful interactive shell
Name: zsh
Version: 5.0.2
Release: 1%{?_dist}
License: BSD
URL: http://zsh.sunsite.dk/
Group: System Environment/Shells
Source0: ftp://ftp.zsh.org/pub/zsh-%{version}.tar.bz2
Source1: zlogin.rhs
Source2: zlogout.rhs
Source3: zprofile.rhs
Source4: zshrc.rhs
Source5: zshenv.rhs
Source6: dotzshrc
Source7: zshprompt.pl
Requires: libcap fileutils grep /sbin/install-info
Buildroot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: libtermcap-devel libcap-devel texinfo
BuildRequires: texi2html >= 1.82

%{?_without_check: %define _without_check 1}
%{!?_without_check: %define _without_check 0}

%define _bindir /bin

%description
The zsh shell is a command interpreter usable as an interactive login
shell and as a shell script command processor.  Zsh resembles the ksh
shell (the Korn shell), but includes many enhancements.  Zsh supports
command line editing, built-in spelling correction, programmable
command completion, shell functions (with autoloading), a history
mechanism, and more.

%package html
Summary: Zsh shell manual in html format
Group: System Environment/Shells

%description html
The zsh shell is a command interpreter usable as an interactive login
shell and as a shell script command processor.  Zsh resembles the ksh
shell (the Korn shell), but includes many enhancements.  Zsh supports
command line editing, built-in spelling correction, programmable
command completion, shell functions (with autoloading), a history
mechanism, and more.

This package contains the Zsh manual in html format.

%prep

%setup -q

cp -p %SOURCE7 .

%build
export LDFLAGS=""
./configure --enable-etcdir=/etc --sysconfdir=/etc --with-tcsetpgrp --prefix=/usr --bindir=/bin  --libdir=%{_libdir}

make all html
# Run the testsuite
#%if ! %{_without_check}
#( cd Test; mkdir skipped; mv Y03arguments.ztst skipped)
#  ZTST_verbose=0 make test
#%endif

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT install.info \
	fndir=%{_datadir}/zsh/%{version}/functions \
	sitefndir=%{_datadir}/zsh/site-functions

rm -f ${RPM_BUILD_ROOT}%{_bindir}/zsh-%{version}
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# for cruft from Patch4
rm -f ${RPM_BUILD_ROOT}%{_datadir}/zsh/%{version}/functions/_path_files.path_files

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}
for i in zshrc zlogin zlogout zshenv zprofile; do
	install -m 644 $RPM_SOURCE_DIR/${i}.rhs ${RPM_BUILD_ROOT}%{_sysconfdir}/$i
done

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/skel
install -m 644 %{SOURCE6} ${RPM_BUILD_ROOT}%{_sysconfdir}/skel/.zshrc

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/shells ] ; then
    echo "%{_bindir}/zsh" > %{_sysconfdir}/shells
else
    grep -q "^%{_bindir}/zsh$" %{_sysconfdir}/shells || echo "%{_bindir}/zsh" >> %{_sysconfdir}/shells
fi

/sbin/install-info %{_infodir}/zsh.info.gz %{_infodir}/dir \
	--entry="* zsh: (zsh).			An enhanced bourne shell."

%preun
if [ "$1" = 0 ] ; then
    /sbin/install-info --delete %{_infodir}/zsh.info.gz %{_infodir}/dir \
	--entry="* zsh: (zsh).			An enhanced bourne shell."
fi

%postun
if [ "$1" = 0 ] ; then
    if [ -f %{_sysconfdir}/shells ] ; then
    	TmpFile=`%{_bindir}/mktemp /tmp/.zshrpmXXXXXX`
    	grep -v '^%{_bindir}/zsh$' %{_sysconfdir}/shells > $TmpFile
    	cp -f $TmpFile %{_sysconfdir}/shells
    	rm -f $TmpFile
    	chmod 644 %{_sysconfdir}/shells
    fi
fi

%files
%defattr(-,root,root)
%doc README LICENCE Etc/BUGS Etc/CONTRIBUTORS Etc/FAQ
%attr(644,root,root) %doc Etc/zsh-development-guide Etc/completion-style-guide zshprompt.pl
%attr(755,root,root) %{_bindir}/zsh
%{_mandir}/*/*
%{_infodir}/*
%{_datadir}/zsh
%{_libdir}/zsh
%config(noreplace) %{_sysconfdir}/*

%files html
%defattr(-,root,root)
%doc Doc/*.html

%changelog
* Thu Oct 10 2013 David Bishop <david@gnuconsulting.com> - 5.0.2-1
- New upstream version

* Tue Oct  3 2006 James Antill <jantill@redhat.com> - 4.2.0-4.EL.4.5
- New patch zsh-4.2.0-rlimit.patch (backport from 4.2.6) for 169644

* Tue Jun 21 2005 Colin Walters <walters@redhat.com> - 4.2.0-3.EL.3
- New patch zsh-4.2.0-path_files.patch (Backported from 4.2.1, 155598)
- New patch zsh-4.2.0-texi.patch, fixes some Texinfo syntax errors
- Disable Y03arguments.ztst; it fails even before this patch
- Change cp -p to install to fix mode as 644
- Default mode of doc files to 644

* Mon Jul  5 2004 Jens Petersen <petersen@redhat.com> - 4.2.0-3
- source profile in zprofile rather than .zshrc (Péter Kelemen,
  Magnus Gustavsson, 102187,126539)
- add zsh-4.2.0-jobtable-125452.patch to fix job table bug
  (Henrique Martins, 125452)
- buildrequire tetex for texi2html (Maxim Dzumanenko, 124182)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Apr 10 2004 Jens Petersen <petersen@redhat.com> - 4.2.0-1
- update to 4.2.0 stable release
- zsh-4.0.7-bckgrnd-bld-102042.patch no longer needed
- add compinit and various commented config improvements to .zshrc
  (Eric Hattemer,#114887)
- include zshprompt.pl in doc dir (Eric Hattemer)
- drop setenv function from zshrc

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 13 2004 Jens Petersen <petersen@redhat.com> - 4.0.9-1
- update to 4.0.9 release
- zsh-4.0.7-completion-_files-110852.patch no longer needed
- update zsh-4.0.7-bckgrnd-bld-102042.patch to better one with --with-tcsetpgrp
  configure option by Philippe Troin
- configure --with-tcsetpgrp
- buildrequire texinfo for makeinfo
- fix ownership of html manual (Florian La Roche, #112749)

* Tue Dec  9 2003 Jens Petersen <petersen@redhat.com> - 4.0.7-3
- no longer "stty erase" in /etc/zshrc for screen [Lon Hohberger]

* Thu Nov 27 2003 Jens Petersen <petersen@redhat.com> - 4.0.7-2
- quote %% in file glob'ing completion code (#110852)
  [reported with patch by Keith T. Garner]
- add zsh-4.0.7-bckgrnd-bld-102042.patch from Philippe Troin to allow
  configure to run in the background (#102042) [reported by Michael Redinger]
- above patch requires autoconf to be run
- include html manual in separate -html subpackage
- changed url to master site
- skip completion tests on ppc and ppc64 for now, since they hang

* Fri Jun 20 2003 Jens Petersen <petersen@redhat.com> - 4.0.7-1
- update to 4.0.7 bugfix release

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May  1 2003 Jens Petersen <petersen@redhat.com> - 4.0.6-7
- don't set stty erase in a dumb terminal with tput kbs in /etc/zshrc (#89856)
  [reported by Ben Liblit]
- make default prompt more informative, like bash

* Mon Feb 10 2003 Jens Petersen <petersen@redhat.com> - 4.0.6-5
- skip completion tests on s390 and s390x since they hang

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 25 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix adding zsh to /etc/shells

* Fri Nov 29 2002 Florian La Roche <Florian.LaRoche@redhat.de> 4.0.6-2
- make sure /bin/zsh is owned by root and not bhcompile
- do not package zsh-%{version} into binary rpm

* Thu Nov 28 2002 Jens Petersen <petersen@redhat.com> 4.0.6-1
- define _bindir to be /bin and use it
- use _sysconfdir and _libdir

* Mon Nov 25 2002 Jens Petersen <petersen@redhat.com>
- 4.0.6
- add url
- add --without check build option
- don't autoconf
- make "make test" failure not go ignored
- move sourcing of profile from zshenv to new .zshrc file for now (#65509)
- preserve dates when installing rc files

* Fri Nov 15 2002 Jens Petersen <petersen@redhat.com>
- setup backspace better with tput in zshrc to please screen (#77833)
- encode spec file in utf-8

* Fri Jun 28 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.0.4-8
- Make it work with a serial port (#56353)
- Add $HOME/bin to path for login shells (#67110)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Apr  5 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.0.4-5
- Source /etc/profile from /etc/zshenv instead of /etc/zprofile, 
  to run things the same way bash do (#62788)

* Tue Apr  2 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.0.4-4
- Explicitly specify blank LDFLAGS to avoid autoconf thinking it 
  should strip when linking

* Thu Feb 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.0.4-3
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Oct 26 2001 Trond Eivind Glomsrød <teg@redhat.com> 4.0.4-1
- 4.0.4
- Don't force emacs keybindings, they're the default (#55102)

* Wed Oct 24 2001 Trond Eivind Glomsrød <teg@redhat.com> 4.0.3-1
- 4.0.3

* Mon Jul 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Fix typo in comment in zshrc (#50214)
- Don't set environment variables in  /etc/zshrc (#50308)

* Tue Jun 26 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 4.0.2
- Run the testsuite during build

* Wed Jun 20 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add libtermcap-devel and libcap-devel to buildrequires

* Fri Jun  1 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 4.0.1

* Thu May 17 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 4.0.1pre4
- zsh is now available in bz2 - use it

* Mon Apr  9 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 4.0.1pre3
- remove the dir file from the info directory

* Wed Mar 21 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Remove contents from /etc/zshenv file - no reason to duplicate things
  from /etc/profile, which is sourced from /etc/zprofile (#32478)

* Thu Mar 15 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 4.0.1pre2
- remove some obsolete code in /etc/zprofile

* Tue Feb 27 2001 Preston Brown <pbrown@redhat.com>
- noreplace config files.

* Thu Feb 15 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Handle RLIMIT_LOCKS in 2.4 (#27834 - patch from H.J. Lu)

* Mon Jan 08 2001 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild to fix #23568  (empty signal list)

* Tue Nov 28 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix the post script, so we only have only line for zsh
  and can remove the trigger
- get rid of some instances of "/usr/local/bin/zsh"

* Mon Nov 20 2000 Bill Nottingham <notting@redhat.com>
- fix ia64 build

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jul 02 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Tue Jun 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 3.0.8
- use %%configure and %%makeinstall
- updated URL
- disable old patches
- add better patch for texi source
- use %%{_mandir} and %%{_infodir}
- use %%{_tmppath}

* Tue May 02 2000 Trond Eivind Glomsrød <teg@redhat.com>
- patched to recognize export in .zshrc (bug #11169)

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Fri Mar 03 2000 Cristian Gafton <gafton@redhat.com>
- fix postun script so that we don't remove ourselves on every update
  doh...
- add a trigger to fix old versions of the package

* Mon Jan 31 2000 Cristian Gafton <gafton@redhat.com>
- rebuild to fix dependencies

* Thu Jan 13 2000 Jeff Johnson <jbj@redhat.com>
- update to 3.0.7.
- source /etc/profile so that USER gets set correctly (#5655).

* Fri Sep 24 1999 Michael K. Johnson <johnsonm@redhat.com>
- source /etc/profile.d/*.sh in zprofile

* Tue Sep 07 1999 Cristian Gafton <gafton@redhat.com>
- fix zshenv and zprofile scripts - foxed versions from HJLu.

* Thu Jul 29 1999 Bill Nottingham <notting@redhat.com>
- clean up init files some. (#4055)

* Tue May 18 1999 Jeff Johnson <jbj@redhat.com>
- Make sure that env variable TmpFile is evaluated. (#2898)

* Sun May  9 1999 Jeff Johnson <jbj@redhat.com>
- fix select timeval initialization (#2688).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 10)
- fix the texi source
- patch to detect & link against nsl

* Wed Mar 10 1999 Cristian Gafton <gafton@redhat.com>
- use mktemp to handle temporary files.

* Thu Feb 11 1999 Michael Maher <mike@redhat.com>
- fixed bug #365

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Thu Sep 10 1998 Jeff Johnson <jbj@redhat.com>
- compile for 5.2

* Sat Jun 06 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Sat Jun  6 1998 Jeff Johnson <jbj@redhat.com>
- Eliminate incorrect info page removal.

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat Apr 11 1998 Cristian Gafton <gafton@redhat.com>
- manhattan build
- moved profile.d handling from zshrc to zprofile

* Wed Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- Upgraded to 3.0.5
- Install-info handling

* Thu Jul 31 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Thu Apr 10 1997 Michael Fulbright <msf@redhat.com>
- Upgraded to 3.0.2
- Added 'reasonable' default startup files in /etc
