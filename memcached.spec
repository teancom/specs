# Upstream: Brad Fitzpatrick <brad$danga,com>

Summary: Distributed memory object caching system
Name: memcached
Version: 1.4.15
Release: 1%{?_dist}
License: BSD
Group: System Environment/Daemons
URL: http://www.danga.com/memcached/

Source0: http://www.danga.com/memcached/dist/memcached-%{version}.tar.gz
Source1: memcached.sysv
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: libevent-devel
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service

%package devel
Summary: memcached header files
Group: Development/Libraries
Requires: memcached = %{version}-%{release}

%description
memcached is a high-performance, distributed memory object caching system,
generic in nature, but intended for use in speeding up dynamic web
applications by alleviating database load.

%description devel
Provies header files for memcached binary protocol.

%prep
%setup -q

%{__cat} <<EOF >memcached.sysconfig
PORT="11211"
USER="nobody"
MAXCONN="1024"
CACHESIZE="64"
OPTIONS="-L -U 11211"
EOF

%build
%configure \
	--program-prefix="%{?_program_prefix}"
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%{__install} -Dp -m0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/memcached
%{__install} -Dp -m0644 memcached.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/memcached
mkdir -p %{buildroot}/var/run/memcached

%post
/sbin/chkconfig --add memcached

%preun
if [ $1 -eq 0 ]; then
	/sbin/service memcached stop &> /dev/null || :
	/sbin/chkconfig --del memcached
fi

%postun
/sbin/service memcached condrestart &>/dev/null || :

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING doc/*.txt NEWS 
%doc %{_mandir}/man1/memcached.1*
%config(noreplace) %{_sysconfdir}/sysconfig/memcached
%config %{_initrddir}/memcached
%{_bindir}/memcached
%attr(0755,nobody,root) /var/run/memcached

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/memcached/protocol_binary.h


%changelog
* Mon Oct 14 2013 David Bishop <david@gnuconsulting.com> - 1.4.15-1
- initial build

* Tue May 29 2007 Matthias Saou <http://freshrpms.net/> 1.2.2-1 - 5457/thias
- Update to 1.2.2.
- Enable new threads feature.

* Sun Mar 25 2007 Dag Wieers <dag@wieers.com> - 1.2.1-4
- Rebuild against libevent-1.1a on EL5.

* Wed Mar 07 2007 Dag Wieers <dag@wieers.com> - 1.2.1-3
- Rebuild against libevent-1.3b.

* Tue Feb 20 2007 Dag Wieers <dag@wieers.com> - 1.2.1-2
- Rebuild against libevent-1.3a.

* Mon Feb 19 2007 Dag Wieers <dag@wieers.com> - 1.2.1-1
- Updated to release 1.2.1.

* Wed Nov 01 2006 Dag Wieers <dag@wieers.com> - 1.1.13-1
- Updated to release 1.1.13.

* Sat Aug 19 2006 Dag Wieers <dag@wieers.com> - 1.1.12-3
- Rebuild against libevent-1.1b.

* Mon Apr 03 2006 Dag Wieers <dag@wieers.com> - 1.1.12-2
- Rebuild against libevent-1.1a.

* Wed Jan 11 2006 Matthias Saou <http://freshrpms.net/> 1.1.12-1
- Update to 1.1.12.
- Remove no longer needed segfault patch.
- Add Requires(foo):...
- Remove INSTALL from %%doc.
- Don't have the init script be tagged as config, the config part is all in
  the sysconfig file.
- make install now works again.
- Fix non working reload in the init script.

* Mon Mar 07 2005 Dag Wieers <dag@wieers.com> - 1.1.11-1
- Cosmetic changes.

* Thu Feb 24 2005 Rob Starkey <falcon@rasterburn.com> - 1.1.11-1
- Initial package.
