#
#   - Moose -
#   This spec file was automatically generated by cpan2rpm [ver: 2.029]
#   The following arguments were used:
#       --debug --no-upgrade-chk --no-sign --no-depchk Moose
#   For more information on cpan2rpm please visit: http://perl.arix.com/
#

%define pkgname Moose
%define filelist %{pkgname}-%{version}-filelist
%define NVR %{pkgname}-%{version}-%{release}
%define maketest 0

name:      perl-Moose
summary:   Moose - A postmodern object system for Perl 5
version:   2.1204
release:   1
vendor:    Moose is maintained by the Moose Cabal, along with the help of many contributors. See L<Moose/CABAL> and L<Moose/CONTRIBUTORS> for details.
packager:  Arix International <cpan2rpm@arix.com>
license:   Artistic
group:     Applications/CPAN
url:       http://www.cpan.org
buildroot: %{_tmppath}/%{name}-%{version}-%(id -u -n)
buildarch: x86_64
prefix:    %(echo %{_prefix})
source:    http://search.cpan.org//CPAN/authors/id/D/DO/DOY/Moose-%{version}.tar.gz
Provides:  perl(Moose::Error::Util) perl(Moose::Conflicts) perl(inc::MyInline)
BuildRequires: perl-Carp >= 1.22
BuildRequires: perl-Class-Load >= 0.09 
BuildRequires: perl-Class-Load-XS >= 0.01
BuildRequires: perl-Data-OptList >= 0.107
BuildRequires: perl-Dist-CheckConflicts >= 0.02
BuildRequires: perl-Eval-Closure >= 0.04
BuildRequires: perl-Package-DeprecationManager >= 0.11
BuildRequires: perl-Package-Stash >= 0.32
BuildRequires: perl-Package-Stash-XS >= 0.24
BuildRequires: perl-Devel-StackTrace >= 1.30 
BuildRequires: perl-Module-Runtime >= 0.014 
Requires: perl-Devel-StackTrace >= 1.30 
Requires: perl-Module-Runtime >= 0.014 
Requires: perl-Archive-Tar
Requires: perl-CPAN-Meta-Requirements
Requires: perl-Class-Load >= 0.07
Requires: perl-Class-MOP
Requires: perl-Data-OptList
Requires: perl-Devel-GlobalDestruction
Requires: perl-Eval-Closure
Requires: perl-File-Find-Rule
Requires: perl-File-Slurp
Requires: perl-PathTools
Requires: perl-File-Temp
Requires: perl-IPC-System-Simple
Requires: perl-libwww-perl
Requires: perl-List-MoreUtils
Requires: perl-Scalar-List-Utils
Requires: perl-MRO-Compat
Requires: perl-Package-Stash
Requires: perl-Params-Util
Requires: perl-Path-Class
Requires: perl-Sub-Exporter >= 0.980
Requires: perl-Sub-Name
Requires: perl-Test-Inline
Requires: perl-Try-Tiny
Requires: perl-Carp >= 1.32
Requires: perl-Package-DeprecationManager >= 0.07
Requires: perl-Class-C3
AutoReq: no

%description
None.

#
# This package was generated automatically with the cpan2rpm
# utility.  To get this software or for more information
# please visit: http://perl.arix.com/
#

%prep
%setup -q -n %{pkgname}-%{version} 
chmod -R u+w %{_builddir}/%{pkgname}-%{version}

%build
grep -rsl '^#!.*perl' . |
grep -v '.bak$' |xargs --no-run-if-empty \
%__perl -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)'
CFLAGS="$RPM_OPT_FLAGS"
%{__perl} Makefile.PL `%{__perl} -MExtUtils::MakeMaker -e ' print qq|PREFIX=%{buildroot}%{_prefix}| if \$ExtUtils::MakeMaker::VERSION =~ /5\.9[1-6]|6\.0[0-5]/ '`
%{__make} 
%if %maketest
%{__make} test
%endif

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%{makeinstall} `%{__perl} -MExtUtils::MakeMaker -e ' print \$ExtUtils::MakeMaker::VERSION <= 6.05 ? qq|PREFIX=%{buildroot}%{_prefix}| : qq|DESTDIR=%{buildroot}| '`

cmd=/usr/share/spec-helper/compress_files
[ -x $cmd ] || cmd=/usr/lib/rpm/brp-compress
[ -x $cmd ] && $cmd

# SuSE Linux
if [ -e /etc/SuSE-release -o -e /etc/UnitedLinux-release ]
then
    %{__mkdir_p} %{buildroot}/var/adm/perl-modules
    %{__cat} `find %{buildroot} -name "perllocal.pod"`  \
        | %{__sed} -e s+%{buildroot}++g                 \
        > %{buildroot}/var/adm/perl-modules/%{name}
fi

# remove special files
find %{buildroot} -name "perllocal.pod" \
    -o -name ".packlist"                \
    -o -name "*.bs"                     \
    |xargs -i rm -f {}

# no empty directories
find %{buildroot}%{_prefix}             \
    -type d -depth                      \
    -exec rmdir {} \; 2>/dev/null

%{__perl} -MFile::Find -le '
    find({ wanted => \&wanted, no_chdir => 1}, "%{buildroot}");
    print "%doc  Changes.Class-MOP bin inc author Changes benchmarks TODO xs doc LICENSE";
    for my $x (sort @dirs, @files) {
        push @ret, $x unless indirs($x);
        }
    print join "\n", sort @ret;

    sub wanted {
        return if /auto$/;

        local $_ = $File::Find::name;
        my $f = $_; s|^\Q%{buildroot}\E||;
        return unless length;
        return $files[@files] = $_ if -f $f;

        $d = $_;
        /\Q$d\E/ && return for reverse sort @INC;
        $d =~ /\Q$_\E/ && return
            for qw|/etc %_prefix/man %_prefix/bin %_prefix/share|;

        $dirs[@dirs] = $_;
        }

    sub indirs {
        my $x = shift;
        $x =~ /^\Q$_\E\// && $x ne $_ && return 1 for @dirs;
        }
    ' > %filelist

[ -z %filelist ] && {
    echo "ERROR: empty %files listing"
    exit -1
    }

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -f %filelist
%defattr(-,root,root)
%exclude %{_mandir}/*

%changelog
* Wed Nov 23 2011 ec2-user@ip-10-86-133-163
- Initial build.
