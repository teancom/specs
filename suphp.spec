%define		pname suphp
%define		pversion 0.7.1
%define 	bversion 101
%define		rpmrelease maefsco

%define 	debug_package %{nil}

# INSTRUCTIONS!!! <--------------------- READ THEM!!!
#
# You can rebuild  this  package safely using Command 
# Line Overrides. For example, if you want to rebuild
# this package for RedHat just type:
# $ rpm --rebuild --with redhat package.src.rpm
# $ rpm -ba --with redhat package.spec
#
# mdk = GNU/Linux Mandrake
# rht = Linux Red-Hat
# sus = Suse Linux
# fdr = Fedora Linux
# cos = CentOS
# whb = White Box Linux
# rhe = Red Hat Enterprise
# unk = Unknown
#

%define 	build_rht_90   0
%define		build_cos_3x   0
%define		build_fdr_10   0
%define		build_fdr_20   0
%define		build_fdr_30   0
%define		build_fdr_40   0
%define		build_whb_3x   0
%define		build_rhe_2x   0
%define		build_rhe_3x   0
%define		build_rhe_4x   0

%define		build_unk      1

# Command Line Overrides
%{?_with_rht90:   	%{expand: %%define build_rht_90   1}}
%{?_with_cos3x: 	%{expand: %%define build_cos_3x   1}}
%{?_with_fdr10: 	%{expand: %%define build_fdr_10   1}}
%{?_with_fdr20: 	%{expand: %%define build_fdr_20   1}}
%{?_with_fdr30: 	%{expand: %%define build_fdr_30   1}}
%{?_with_fdr40: 	%{expand: %%define build_fdr_40   1}}
%{?_with_whb3x: 	%{expand: %%define build_whb_3x   1}}
%{?_with_rhe2x: 	%{expand: %%define build_rhe_2x   1}}
%{?_with_rhe3x: 	%{expand: %%define build_rhe_3x   1}}
%{?_with_rhe4x: 	%{expand: %%define build_rhe_4x   1}}

%{?_with_unk: 		%{expand: %%define build_unk      1}}

# Distro Statements
%if %{build_rht_90}
%define		oscode rht90
%define 	ostype RedHat 9
BuildRequires:	httpd-devel
Requires: 	httpd
%define		ccflags %{optflags}
%define		ldflags %{optflags}
%define		build_unk 0
%endif

%if %{build_cos_3x}
%define		oscode cos3x
%define 	ostype CentOS 3.x
BuildRequires:	apr
BuildRequires:	apr-util
Requires: 	httpd
%define		ccflags %{optflags}
%define		ldflags %{optflags}
%define		build_unk 0
%endif

%if %{build_fdr_10}
%define		oscode fdr10
%define 	ostype Fedora Core 1
BuildRequires:	httpd-devel
Requires: 	httpd
%define		ccflags %{optflags}
%define		ldflags %{optflags}
%define		build_unk 0
%endif

%if %{build_fdr_20}
%define		oscode fdr20
%define 	ostype Fedora Core 2
BuildRequires:	httpd-devel
Requires: 	httpd
%define		ccflags %{optflags}
%define		ldflags %{optflags}
%define		build_unk 0
%endif

%if %{build_fdr_30}
%define		oscode fdr30
%define 	ostype Fedora Core 3
BuildRequires:	httpd-devel
Requires: 	httpd
%define		ccflags %{optflags}
%define		ldflags %{optflags}
%define		build_unk 0
%endif

%if %{build_fdr_40}
%define		oscode fdr40
%define 	ostype Fedora Core 4
BuildRequires:	apr
BuildRequires:	apr-util
Requires: 	httpd
%define		ccflags %{optflags}
%define		ldflags %{optflags}
%define		build_unk 0
%endif

%if %{build_whb_3x}
%define		oscode whb3x
%define 	ostype White Box 3.x
BuildRequires:	apr
BuildRequires:	apr-util
Requires: 	httpd
%define		ccflags %{optflags}
%define		ldflags %{optflags}
%define		build_unk 0
%endif

%if %{build_rhe_2x}
%define		oscode rhe2x
%define 	ostype RedHat Enterprise 2.x
BuildRequires:	apr
BuildRequires:	apr-util
Requires: 	httpd
%define		ccflags %{optflags}
%define		ldflags %{optflags}
%define		build_unk 0
%endif

%if %{build_rhe_3x}
%define		oscode rhe3x
%define 	ostype RedHat Enterprise 3.x
BuildRequires:	apr
BuildRequires:	apr-util
Requires: 	httpd
%define		ccflags %{optflags}
%define		ldflags %{optflags}
%define		build_unk 0
%endif

%if %{build_rhe_4x}
%define		oscode rhe4x
%define 	ostype RedHat Enterprise 4.x
BuildRequires:	apr
BuildRequires:	apr-util
Requires: 	httpd
%define		ccflags %{optflags}
%define		ldflags %{optflags}
%define		build_unk 0
%endif

%define	release %{bversion}.%{oscode}.%{rpmrelease}

##
# THIS MUST BE LAST
##

%if %{build_unk}
%define		oscode unk
%define 	ostype Unknown Distribution
%define		release %{bversion}.%{rpmrelease}
%define		ccflags %{optflags}
%define		ldflags %{optflags}
%endif

############### RPM ################################

Summary:	suPHP -  suexec for PHP
Name:		%{pname}
Version:	%{pversion}
Release: 	%{release}
License:	GPL

Group:		System Environment/Daemons
Source0:	%{name}-%{version}.tar.gz
URL:		http://www.suphp.org

#Distribution:	InterWorx-HAL
#Vendor:         NEXCESS.NET L.L.C
Packager:	Chris Wells <clwells@nexcess.net>

BuildRoot:	%{_tmppath}/%{name}-%{version}-root

Source1:	mod_suphp.conf
Source2:	suphp.conf

%description
suPHP is a tool for executing PHP scripts with the permissions 
of their owners. It consists of an Apache module (mod_suphp) 
and a setuid root binary (suphp) that is called by the Apache 
module to change the uid of the process executing the PHP 
interpreter.

%prep

[ -n %{buildroot} ] && rm -rf %{buildroot}

[ -d %{_builddir}/%{name}-%{pversion} ] && rm -rf %{_builddir}/%{name}-%{pversion}

%setup -q -n %{name}-%{pversion}

# Try detecting newest gcc (some distributions have got more then one compiler)
# and write it on a temp file 

[ -f %{_tmppath}/%{name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc

if   [ -x /usr/bin/gcc-3.2.3 ]; then
	echo "/usr/bin/gcc-3.2.3" > %{_tmppath}/%{name}-%{pversion}-gcc
elif   [ -x /usr/bin/gcc-3.2.2 ]; then
	echo "/usr/bin/gcc-3.2.2" > %{_tmppath}/%{name}-%{pversion}-gcc
elif   [ -x /usr/bin/gcc-3.2.1 ]; then
	echo "/usr/bin/gcc-3.2.1" > %{_tmppath}/%{name}-%{pversion}-gcc
elif [ -x /usr/bin/gcc-3.2 ]; then
        echo "/usr/bin/gcc-3.2" > %{_tmppath}/%{name}-%{pversion}-gcc
elif [ -x /usr/bin/gcc-3.1.1 ]; then
        echo "/usr/bin/gcc-3.1.1" > %{_tmppath}/%{name}-%{pversion}-gcc
else
	echo "gcc" > %{_tmppath}/%{name}-%{pversion}-gcc
fi

# Display compilation flags and OS with colors ;)

[ -f %{_tmppath}/%{name}-%{pversion}-show_flags ] && rm -f %{_tmppath}/%{name}-%{pversion}-show_flags
cat <<EOF >>%{_tmppath}/%{name}-%{pversion}-show_flags
#!/bin/sh

RPM="RPM RELEASE: \033[40m\033[001;033m%{release}"
OS="OS TYPE IS : \033[40m\033[001;033m%{ostype}"
GCC="GCC IS     : \033[40m\033[001;033m`cat %{_tmppath}/%{name}-%{pversion}-gcc`"
CCF="CCFLAGS    : \033[40m\033[001;033m%{ccflags}"
LDF="LDFLAGS    : \033[40m\033[001;033m%{ldflags}"

echo
echo
echo -e "\033[40m\033[001;031m\$RPM\033[0m"
echo -e "\033[40m\033[001;031m\$OS\033[0m"
echo -e "\033[40m\033[001;031m\$GCC\033[0m"
echo -e "\033[40m\033[001;031m\$CCF\033[0m"
echo -e "\033[40m\033[001;031m\$LDF\033[0m"
echo
echo

sleep 3

EOF

# Take care to execute and then to delete
chmod u+x %{_tmppath}/%{name}-%{pversion}-show_flags
%{_tmppath}/%{name}-%{pversion}-show_flags
[ -f %{_tmppath}/%{name}-%{pversion}-show_flags ] && rm -f %{_tmppath}/%{name}-%{pversion}-show_flags

# We have gcc written in a temp file
export CC="`cat %{_tmppath}/%{name}-%{pversion}-gcc` %{ccflags}"

# Delete gcc temp file
[ -f %{_tmppath}/%{name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc

%build

[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}

# Delete gcc temp file
[ -f %{_tmppath}/%{name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc

export CFLAGS="$RPM_OPT_FLAGS -fomit-frame-pointer -fPIC -I`apr-config --includedir`"
export CPPFLAGS="$CFLAGS"

./configure                               \
	--prefix=%{_prefix}               \
	--bindir=%{_bindir}               \
	--mandir=%{_mandir}               \
	--localstatedir=%{_localstatedir} \
	--libdir=%{_libdir}               \
	--datadir=%{_datadir}             \
	--includedir=%{_includedir}       \
	--sysconfdir=%{_sysconfdir}       \
        --with-setid-mode=paranoid        \
	--with-min-uid=100                \
	--with-min-gid=100                \
	--with-apache-user=apache         \
	--with-logfile=%{_localstatedir}/log/httpd/suphp.log

%{__make} %{?_smp_mflags}

%install

## make the "install" dir
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_libdir}/httpd/modules
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d

install -m0755 src/apache2/.libs/mod_suphp.so \
	%{buildroot}%{_libdir}/httpd/modules
install -m4755 src/suphp \
	%{buildroot}%{_sbindir}
install -m0644 %{SOURCE1} \
	%{buildroot}%{_sysconfdir}/httpd/conf.d/suphp.conf
install -m0644 %{SOURCE2} \
	%{buildroot}%{_sysconfdir}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
[ -d %{_builddir}/%{name}-%{pversion} ] && rm -rf %{_builddir}/%{name}-%{pversion}

%pre

%postun

[ -d %{_localstatedir}/%{name} ] && 
	rm -rf %{_localstatedir}/%{name} || :

%post

%files
%defattr(-,root,root)

%attr(0755,root,root) %{_libdir}/httpd/modules/mod_suphp.so
%attr(0644,root,root) %{_sysconfdir}/httpd/conf.d/suphp.conf
%attr(0644,root,root) %{_sysconfdir}/suphp.conf
%attr(4755,root,root) %{_sbindir}/suphp

%changelog
* Thu Jun 23 2005 Chris Wells <clwells@nexcess.net>
- Initial packaging as part of InterWorx-HAL OS
