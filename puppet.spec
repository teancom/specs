# Augeas and SELinux requirements may be disabled at build time by passing
# --without augeas and/or --without selinux to rpmbuild or mock

%{!?ruby_sitelibdir: %global ruby_sitelibdir %(ruby -rrbconfig -e 'puts Config::CONFIG["sitelibdir"]')}
%global confdir conf/redhat

Name:           puppet
Version:        2.7.10
#Release:        0.1rc1%{?dist}
Release:        1%{?dist}
Summary:        A network tool for managing many disparate systems
License:        ASL 2.0
URL:            http://puppetlabs.com
Source0:        http://puppetlabs.com/downloads/%{name}/%{name}-%{version}.tar.gz
#Source0:        http://puppetlabs.com/downloads/%{name}/%{name}-%{version}rc1.tar.gz
Source1:        http://puppetlabs.com/downloads/%{name}/%{name}-%{version}.tar.gz.asc
#Source1:        http://puppetlabs.com/downloads/%{name}/%{name}-%{version}rc1.tar.gz.asc

Group:          System Environment/Base

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  facter >= 1.5
BuildRequires:  ruby >= 1.8.1

%if 0%{?fedora} || 0%{?rhel} >= 5
BuildArch:      noarch
Requires:       ruby(abi) = 1.8
Requires:       ruby-shadow
%endif

# Pull in ruby selinux bindings where available
%if 0%{?fedora} || 0%{?rhel} >= 6
%{!?_without_selinux:Requires: ruby(selinux), libselinux-utils}
%else
%if 0%{?rhel} && 0%{?rhel} == 5
%{!?_without_selinux:Requires: libselinux-ruby, libselinux-utils}
%endif
%endif

Requires:       facter >= 1.5
Requires:       ruby >= 1.8.1
%{!?_without_augeas:Requires: ruby-augeas}

Requires(pre):  shadow-utils
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(postun): initscripts

%description
Puppet lets you centrally manage every important aspect of your system using a
cross-platform specification language that manages all the separate elements
normally aggregated in different files, like users, cron jobs, and hosts,
along with obviously discrete elements like packages, services, and files.

%package server
Group:          System Environment/Base
Summary:        Server for the puppet system management tool
Requires:       puppet = %{version}-%{release}
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(postun): initscripts

%description server
Provides the central puppet server daemon which provides manifests to clients.
The server can also function as a certificate authority and file server.

%prep
%setup -q -n %{name}-%{version}
patch -s -p1 < conf/redhat/rundir-perms.patch


%build
# Fix some rpmlint complaints
for f in mac_dscl.pp mac_dscl_revert.pp \
         mac_pkgdmg.pp ; do
  sed -i -e'1d' examples/$f
  chmod a-x examples/$f
done
for f in external/nagios.rb network/http_server/mongrel.rb relationship.rb; do
  sed -i -e '1d' lib/puppet/$f
done
chmod +x ext/puppetstoredconfigclean.rb

find examples/ -type f -empty | xargs rm
find examples/ -type f | xargs chmod a-x

# puppet-queue.conf is more of an example, used for stompserver
mv conf/puppet-queue.conf examples/etc/puppet/

%install
rm -rf %{buildroot}
ruby install.rb --destdir=%{buildroot} --quick --no-rdoc

install -d -m0755 %{buildroot}%{_sysconfdir}/puppet/manifests
install -d -m0755 %{buildroot}%{_datadir}/%{name}/modules
install -d -m0755 %{buildroot}%{_localstatedir}/lib/puppet
install -d -m0755 %{buildroot}%{_localstatedir}/run/puppet
install -d -m0750 %{buildroot}%{_localstatedir}/log/puppet
install -Dp -m0644 %{confdir}/client.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/puppet
install -Dp -m0755 %{confdir}/client.init %{buildroot}%{_initrddir}/puppet
install -Dp -m0644 %{confdir}/server.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/puppetmaster
install -Dp -m0755 %{confdir}/server.init %{buildroot}%{_initrddir}/puppetmaster
install -Dp -m0644 %{confdir}/fileserver.conf %{buildroot}%{_sysconfdir}/puppet/fileserver.conf
install -Dp -m0644 %{confdir}/puppet.conf %{buildroot}%{_sysconfdir}/puppet/puppet.conf
install -Dp -m0644 %{confdir}/logrotate %{buildroot}%{_sysconfdir}/logrotate.d/puppet

# We need something for these ghosted files, otherwise rpmbuild
# will complain loudly. They won't be included in the binary packages
touch %{buildroot}%{_sysconfdir}/puppet/puppetmasterd.conf
touch %{buildroot}%{_sysconfdir}/puppet/puppetca.conf
touch %{buildroot}%{_sysconfdir}/puppet/puppetd.conf

# Install the ext/ directory to %%{_datadir}/%%{name}
install -d %{buildroot}%{_datadir}/%{name}
cp -a ext/ %{buildroot}%{_datadir}/%{name}
# emacs and vim bits are installed elsewhere
rm -rf %{buildroot}%{_datadir}/%{name}/ext/{emacs,vim}

# Install emacs mode files
emacsdir=%{buildroot}%{_datadir}/emacs/site-lisp
install -Dp -m0644 ext/emacs/puppet-mode.el $emacsdir/puppet-mode.el
install -Dp -m0644 ext/emacs/puppet-mode-init.el \
    $emacsdir/site-start.d/puppet-mode-init.el

# Install vim syntax files
vimdir=%{buildroot}%{_datadir}/vim/vimfiles
install -Dp -m0644 ext/vim/ftdetect/puppet.vim $vimdir/ftdetect/puppet.vim
install -Dp -m0644 ext/vim/syntax/puppet.vim $vimdir/syntax/puppet.vim

%if 0%{?fedora} >= 15
# Setup tmpfiles.d config
mkdir -p %{buildroot}%{_sysconfdir}/tmpfiles.d
echo "D /var/run/%{name} 0755 %{name} %{name} -" > \
    %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf
%endif

%files
%defattr(-, root, root, 0755)
%doc CHANGELOG LICENSE README.md examples
%{_bindir}/pi
%{_bindir}/puppet
%{_bindir}/ralsh
%{_bindir}/filebucket
%{_bindir}/puppetdoc
%{_sbindir}/puppetca
%{_sbindir}/puppetd
%{ruby_sitelibdir}/*
%{_initrddir}/puppet
%dir %{_sysconfdir}/puppet
%if 0%{?fedora} >= 15
%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/puppet
%config(noreplace) %{_sysconfdir}/puppet/puppet.conf
%config(noreplace) %{_sysconfdir}/puppet/auth.conf
%ghost %config(noreplace,missingok) %{_sysconfdir}/puppet/puppetca.conf
%ghost %config(noreplace,missingok) %{_sysconfdir}/puppet/puppetd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/puppet
# We don't want to require emacs or vim, so we need to own these dirs
%{_datadir}/emacs
%{_datadir}/vim
%{_datadir}/%{name}
# These need to be owned by puppet so the server can
# write to them
%attr(-, puppet, puppet) %{_localstatedir}/run/puppet
%attr(-, puppet, puppet) %{_localstatedir}/log/puppet
%attr(-, puppet, puppet) %{_localstatedir}/lib/puppet
%{_mandir}/man5/puppet.conf.5.gz
%{_mandir}/man8/pi.8.gz
%{_mandir}/man8/puppet.8.gz
%{_mandir}/man8/puppetca.8.gz
%{_mandir}/man8/puppetd.8.gz
%{_mandir}/man8/ralsh.8.gz
%{_mandir}/man8/puppetdoc.8.gz
%{_mandir}/man8/puppet-agent.8.gz
%{_mandir}/man8/puppet-apply.8.gz
%{_mandir}/man8/puppet-catalog.8.gz
%{_mandir}/man8/puppet-describe.8.gz
%{_mandir}/man8/puppet-cert.8.gz
%{_mandir}/man8/puppet-certificate.8.gz
%{_mandir}/man8/puppet-certificate_request.8.gz
%{_mandir}/man8/puppet-certificate_revocation_list.8.gz
%{_mandir}/man8/puppet-config.8.gz
%{_mandir}/man8/puppet-device.8.gz
%{_mandir}/man8/puppet-doc.8.gz
%{_mandir}/man8/puppet-facts.8.gz
%{_mandir}/man8/puppet-file.8.gz
%{_mandir}/man8/puppet-filebucket.8.gz
%{_mandir}/man8/puppet-help.8.gz
%{_mandir}/man8/puppet-inspect.8.gz
%{_mandir}/man8/puppet-key.8.gz
%{_mandir}/man8/puppet-kick.8.gz
%{_mandir}/man8/puppet-man.8.gz
%{_mandir}/man8/puppet-node.8.gz
%{_mandir}/man8/puppet-parser.8.gz
%{_mandir}/man8/puppet-plugin.8.gz
%{_mandir}/man8/puppet-queue.8.gz
%{_mandir}/man8/puppet-report.8.gz
%{_mandir}/man8/puppet-resource.8.gz
%{_mandir}/man8/puppet-resource_type.8.gz
%{_mandir}/man8/puppet-secret_agent.8.gz
%{_mandir}/man8/puppet-status.8.gz

%files server
%defattr(-, root, root, 0755)
%{_sbindir}/puppetmasterd
%{_sbindir}/puppetrun
%{_sbindir}/puppetqd
%{_initrddir}/puppetmaster
%config(noreplace) %{_sysconfdir}/puppet/fileserver.conf
%dir %{_sysconfdir}/puppet/manifests
%config(noreplace) %{_sysconfdir}/sysconfig/puppetmaster
%ghost %config(noreplace,missingok) %{_sysconfdir}/puppet/puppetmasterd.conf
%{_mandir}/man8/filebucket.8.gz
%{_mandir}/man8/puppetmasterd.8.gz
%{_mandir}/man8/puppetrun.8.gz
%{_mandir}/man8/puppetqd.8.gz
%{_mandir}/man8/puppet-master.8.gz

# Fixed uid/gid were assigned in bz 472073 (Fedora), 471918 (RHEL-5),
# and 471919 (RHEL-4)
%pre
getent group puppet &>/dev/null || groupadd -r puppet -g 52 &>/dev/null
getent passwd puppet &>/dev/null || \
useradd -r -u 52 -g puppet -d %{_localstatedir}/lib/puppet -s /sbin/nologin \
    -c "Puppet" puppet &>/dev/null
# ensure that old setups have the right puppet home dir
if [ $1 -gt 1 ] ; then
  usermod -d %{_localstatedir}/lib/puppet puppet &>/dev/null
fi
exit 0

%post
/sbin/chkconfig --add puppet || :
if [ "$1" -ge 1 ]; then
  # The pidfile changed from 0.25.x to 2.6.x, handle upgrades without leaving
  # the old process running.
  oldpid="%{_localstatedir}/run/puppet/puppetd.pid"
  newpid="%{_localstatedir}/run/puppet/agent.pid"
  if [ -s "$oldpid" -a ! -s "$newpid" ]; then
    (kill $(< "$oldpid") && rm -f "$oldpid" && \
      /sbin/service puppet start) >/dev/null 2>&1 || :
  fi
fi

%post server
/sbin/chkconfig --add puppetmaster || :
if [ "$1" -ge 1 ]; then
  # The pidfile changed from 0.25.x to 2.6.x, handle upgrades without leaving
  # the old process running.
  oldpid="%{_localstatedir}/run/puppet/puppetmasterd.pid"
  newpid="%{_localstatedir}/run/puppet/master.pid"
  if [ -s "$oldpid" -a ! -s "$newpid" ]; then
    (kill $(< "$oldpid") && rm -f "$oldpid" && \
      /sbin/service puppetmaster start) >/dev/null 2>&1 || :
  fi
fi

%preun
if [ "$1" = 0 ] ; then
  /sbin/service puppet stop >/dev/null 2>&1
  /sbin/chkconfig --del puppet || :
fi

%preun server
if [ "$1" = 0 ] ; then
  /sbin/service puppetmaster stop >/dev/null 2>&1
  /sbin/chkconfig --del puppetmaster || :
fi

%postun
if [ "$1" -ge 1 ]; then
  /sbin/service puppet condrestart >/dev/null 2>&1 || :
fi

%postun server
if [ "$1" -ge 1 ]; then
  /sbin/service puppetmaster condrestart >/dev/null 2>&1 || :
fi

%clean
rm -rf %{buildroot}

%changelog
* Wed Jan 25 2012 Michael Stahnke <stahnma@puppetlabs.com> - 2.7.10-1
- Update for 2.7.10
