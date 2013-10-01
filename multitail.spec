# vim: set ts=4 sw=4 et:
# Copyright (c) 2004-2010 oc2pus, pbleser
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

Name:           multitail
Summary:        Tail Multiple Files
Version:        5.2.9
Release:        1%{?_dist}
Group:          System/X11/Terminals
License:        GNU General Public License version 2 or later (GPLv2 or later)
URL:            http://www.vanheusden.com/multitail/
Source:         http://www.vanheusden.com/multitail/multitail-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  ncurses-devel make gcc

%description
MultiTail lets you view one or multiple files like the original
tail program.

The difference is that it creates multiple windows on your console
(with ncurses). Merging of 2 or even more logfiles is possible.

It can also use colors while displaying the logfiles (through
regular expressions), for faster recognition of what is important
and what not. It can also filter lines (again with regular
expressions). It has interactive menus for editing given regular
expressions and deleting and adding windows. One can also have
windows with the output of shell scripts and other software. When
viewing the output of external software, MultiTail can mimic the
functionality of tools like 'watch' and such.

%prep
%setup -q

%__sed -i 's/\r//g' manual.html
%__chmod 644 manual.html

%__sed -i 's|/etc/%{name}|%{_datadir}/%{name}|g' "%{name}.conf"

%build
export CFLAGS="%{optflags} -I%{_includedir}/ncurses"
%__make %{?_smp_mflags} DEBUG=""

%install
%__install -dm 755 %{buildroot}%{_sysconfdir}
%__install  -m 644 %{name}.conf \
    %{buildroot}%{_sysconfdir}

%__install -dm 755 %{buildroot}%{_bindir}
%__install -m 755 %{name} \
    %{buildroot}%{_bindir}

%__install -dm 755 %{buildroot}%{_datadir}/%{name}
%__install  -m 755 convert-* \
    %{buildroot}%{_datadir}/%{name}
%__install  -m 755 colors-* \
    %{buildroot}%{_datadir}/%{name}

%__install -dm 755 %{buildroot}%{_mandir}/man1
%__install  -m 644 %{name}.1 \
    %{buildroot}%{_mandir}/man1

%clean
%{?buildroot:%__rm -rf "%{buildroot}"}

%files
%defattr(-, root, root)
%doc *.txt Changes manual*.html
%config(noreplace) %{_sysconfdir}/%{name}.conf
%dir %{_datadir}/multitail
%{_datadir}/multitail/*
%{_bindir}/multitail
%{_mandir}/man1/multitail.*

%changelog
* Sun Jan 29 2012 David Bishop <david@gnuconsulting.com> 5.2.9-1
- Remove patches
* Sun Jan  1 2012 pascal.bleser@opensuse.org
- add IPv6 support for sending to a syslog server and receiving syslog events
- update to 5.2.9:
  * fixes a segfault which happened when searching for strings with printf
    escapes in them (e.g., %%n)
* Fri Apr 15 2011 pascal.bleser@opensuse.org
- update to 5.2.8:
  * handle sources that disappear before reading more gracefully
  * no longer segfault when a file is truncated
* Wed Jan 19 2011 pascal.bleser@opensuse.org
- update to 5.2.7:
  * a fix for missing home directories failures
* Thu Feb 18 2010 pascal.bleser@opensuse.org
- update to 5.2.6:
  * fixes a segfault bug in the "scrollback" functionality
* Sun Feb 14 2010 pascal.bleser@opensuse.org
- copied to openSUSE Build Service
* Sun Feb 14 2010 toni@links2linux.de
- Update to multitail-5.2.5
- This version handles ANSI codes in logfiles more gracefully when using the
  "scrollback" functionality. Of course, you still need to add the "-cT ansi"
  switch for that.
* Mon May 19 2008 toni@links2linux.de
- Update to multitail-5.2.2
* Wed Feb 20 2008 toni@links2linux.de
- Update to multitail-5.2.1
* Mon Jul  9 2007 toni@links2linux.de
- Update to multitail-5.2.0
* Fri Jul  6 2007 toni@links2linux.de
- Update to multitail-5.1.2
* Mon Jun 18 2007 toni@links2linux.de
- Update to multitail-5.1.1
* Sat Jun  9 2007 toni@links2linux.de
- Update to multitail-5.1.0
* Fri Jun  1 2007 toni@links2linux.de
- Update to multitail-5.0.4
* Thu May 10 2007 toni@links2linux.de
- Update to multitail-5.0.3
* Wed May  2 2007 toni@links2linux.de
- Update to multitail-5.0.2
* Thu Apr 26 2007 toni@links2linux.de
- Update to multitail-5.0.1
* Fri Apr  6 2007 toni@links2linux.de
- Update to multitail-5.0.0
* Tue Apr  3 2007 toni@links2linux.de
- Update to multitail-4.3.7
* Thu Mar 29 2007 toni@links2linux.de
- Update to multitail-4.3.6
* Mon Mar 26 2007 toni@links2linux.de
- Update to multitail-4.3.5
* Tue Mar 20 2007 toni@links2linux.de
- Update to multitail-4.3.4
* Sun Mar 11 2007 toni@links2linux.de
- Update to multitail-4.3.3
* Wed Mar  7 2007 toni@links2linux.de
- Update to multitail-4.3.2
* Tue Feb 27 2007 toni@links2linux.de
- Update to multitail-4.3.1
* Tue Jan 16 2007 toni@links2linux.de
- Update to multitail-4.3.0
* Mon Sep 18 2006 toni@links2linux.de
- build for packman
* Fri Sep  8 2006 oc2pus@arcor.de 4.2.0-0.oc2pus.1
- Update to multitail-4.2.0
* Fri Aug 18 2006 oc2pus@arcor.de 4.1.2-0.oc2pus.1
- Update to multitail-4.1.2
* Fri Aug  4 2006 oc2pus@arcor.de 4.1.1-0.oc2pus.1
- Update to multitail-4.1.1
* Wed Jul 12 2006 oc2pus@arcor.de 4.1.0-0.oc2pus.1
- Update to multitail-4.1.0
* Wed Jun 14 2006 oc2pus@arcor.de 4.0.6-0.oc2pus.1
- Update to multitail-4.0.6
* Sat Jun 10 2006 oc2pus@arcor.de 4.0.5-0.oc2pus.1
- Update to multitail-4.0.5
* Mon May 22 2006 oc2pus@arcor.de 4.0.4-0.oc2pus.1
- Update to multitail-4.0.4
* Tue Apr 18 2006 oc2pus@arcor.de 4.0.3-0.oc2pus.1
- Update to multitail-4.0.3
* Thu Apr 13 2006 oc2pus@arcor.de 4.0.0-0.oc2pus.1
- Update to multitail-4.0.0
* Tue Apr  4 2006 oc2pus@arcor.de 3.9.15-0.oc2pus.1
- Update to multitail-3.9.15
* Thu Mar 30 2006 oc2pus@arcor.de 3.9.14.2-0.oc2pus.1
- Update to multitail-3.9.14.2
* Tue Mar 28 2006 oc2pus@arcor.de 3.9.14.1-0.oc2pus.1
- Update to multitail-3.9.14.1
* Wed Mar 22 2006 oc2pus@arcor.de 3.9.13-0.oc2pus.1
- Update to multitail-3.9.13
* Wed Mar 15 2006 oc2pus@arcor.de 3.9.12-0.oc2pus.1
- Update to multitail-3.9.12
* Sun Mar 12 2006 oc2pus@arcor.de 3.9.11-0.oc2pus.1
- Update to multitail-3.9.11
* Sun Mar  5 2006 oc2pus@arcor.de 3.9.10-0.oc2pus.1
- Update to multitail-3.9.10
* Tue Feb 28 2006 oc2pus@arcor.de 3.9.9-0.oc2pus.1
- Update to multitail-3.9.9
* Sun Feb 26 2006 oc2pus@arcor.de 3.9.8-0.oc2pus.1
- Update to multitail-3.9.8
* Thu Feb 23 2006 oc2pus@arcor.de 3.9.7-0.oc2pus.1
- Update to multitail-3.9.7
* Mon Feb 20 2006 oc2pus@arcor.de 3.9.6-0.oc2pus.1
- Update to multitail-3.9.6
* Tue Feb 14 2006 oc2pus@arcor.de 3.9.5-0.oc2pus.1
- Update to multitail-3.9.5
* Mon Jan 30 2006 oc2pus@arcor.de 3.9.4-0.oc2pus.1
- Update to multitail-3.9.4
* Sun Jan 29 2006 oc2pus@arcor.de 3.9.3-0.oc2pus.1
- Update to multitail-3.9.3
* Fri Jan 27 2006 oc2pus@arcor.de 3.9.2-0.oc2pus.1
- Update to multitail-3.9.2
* Fri Jan 13 2006 oc2pus@arcor.de 3.8.4-0.oc2pus.1
- Update to multitail-3.8.4
* Wed Jan  4 2006 oc2pus@arcor.de 3.8.3-0.oc2pus.1
- Update to multitail-3.8.3
* Mon Jan  2 2006 oc2pus@arcor.de 3.8.2-0.oc2pus.1
- Update to multitail-3.8.2
* Thu Dec 29 2005 oc2pus@arcor.de 3.8.1-0.oc2pus.1
- Update to multitail-3.8.1
* Wed Dec 28 2005 oc2pus@arcor.de 3.8.0-0.oc2pus.1
- Update to multitail-3.8.0
* Fri Dec 16 2005 oc2pus@arcor.de 3.7.6-0.oc2pus.1
- Update to multitail-3.7.6
* Thu Dec  8 2005 oc2pus@arcor.de 3.7.5-0.oc2pus.1
- Update to multitail-3.7.5
- removed patches
* Sun Nov 27 2005 oc2pus@arcor.de 3.7.4-0.oc2pus.1
- Update to multitail-3.7.4
* Fri Nov 18 2005 oc2pus@arcor.de 3.7.3-0.oc2pus.2
- rebuild SuSE-10
* Sat Oct 29 2005 oc2pus@arcor.de 3.7.3-0.oc2pus.1
- Update to multitail-3.7.3
* Sat Oct 22 2005 oc2pus@arcor.de 3.7.2-0.oc2pus.1
- Update to multitail-3.7.2
* Sun Aug 28 2005 oc2pus@arcor.de 3.6.1-0.oc2pus.1
- Update to multitail-3.6.1
- repacked as tar.bz2
* Thu Jul 14 2005 oc2pus@arcor.de 3.5.7-0.oc2pus.1
- Update to multitail-3.5.7
* Fri Jul  1 2005 oc2pus@arcor.de 3.5.5-0.oc2pus.1
- Update to multitail-3.5.5
* Mon Jun  6 2005 oc2pus@arcor.de 3.5.4-0.oc2pus.1
- Update to multitail-3.5.4
- strip binary
* Thu Mar 17 2005 oc2pus@arcor.de 3.5.2-0.oc2pus.1
- Update to multitail-3.5.2
* Sat Feb 26 2005 oc2pus@arcor.de 3.5.1-0.oc2pus.1
- Update to multitail-3.5.1
* Thu Feb 24 2005 oc2pus@arcor.de 3.4.7-0.oc2pus.1
- Update to multitail-3.4.7
* Tue Feb 22 2005 oc2pus@arcor.de 3.4.6-0.oc2pus.1
- Update to multitail-3.4.6
* Thu Jan 20 2005 oc2pus@arcor.de 3.4.5-0.oc2pus.1
- Update to multitail-3.4.5
* Sun Jan 16 2005 oc2pus@arcor.de 3.4.4-0.oc2pus.1
- Update to multitail-3.4.4
* Sat Dec 25 2004 oc2pus@arcor.de 3.4.3-0.oc2pus.1
- Update to multitail-3.4.3
* Fri Dec 24 2004 oc2pus@arcor.de 3.4.2-0.oc2pus.2
- build for SuSE-9.2
* Sat Nov 27 2004 oc2pus@arcor.de 3.4.2-0.oc2pus.1
- Update to multitail-3.4.2
* Sun Oct 31 2004 oc2pus@arcor.de 3.4.1-0.oc2pus.1
- Update to multitail-3.4.1
* Mon Oct 18 2004 oc2pus@arcor.de 3.4.0-0.oc2pus.1
- Update to multitail-3.4.0
* Sun Oct 17 2004 oc2pus@arcor.de 3.3.8-0.oc2pus.1
- Update to multitail-3.3.8
* Tue Oct  5 2004 oc2pus@arcor.de 3.3.7-0.oc2pus.1
- Update to multitail-3.3.7
- based on SuSE-spec Wed Feb 18 2004 - mmj@suse.de
