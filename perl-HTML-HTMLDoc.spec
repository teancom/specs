#
#   - HTML::HTMLDoc -
#   This spec file was automatically generated by cpan2rpm [ver: 2.029]
#   The following arguments were used:
#       --debug --no-upgrade-chk --no-sign HTML::HTMLDoc
#   For more information on cpan2rpm please visit: http://perl.arix.com/
#

%define pkgname HTML-HTMLDoc
%define filelist %{pkgname}-%{version}-filelist
%define NVR %{pkgname}-%{version}-%{release}
%define maketest 1

name:      perl-HTML-HTMLDoc
summary:   HTML-HTMLDoc - Perl interface to the htmldoc program for producing PDF-Files from HTML-Content
version:   0.11_01
release:   1
vendor:    Michael Frankl <mfrankl@seibert-media.net>
packager:  Arix International <cpan2rpm@arix.com>
license:   Artistic
group:     Applications/CPAN
url:       http://www.cpan.org
buildroot: %{_tmppath}/%{name}-%{version}-%(id -u -n)
buildarch: noarch
prefix:    %(echo %{_prefix})
source:    http://search.cpan.org//CPAN/authors/id/M/MF/MFRANKL/HTML-HTMLDoc-0.11_01.tar.gz

%description
This Module provides an OO-interface to the htmldoc programm. To install this module you
have to install the htmldoc program first. You can get it from http://www.htmldoc.org .

You can use it to produce PDF or PS files from a HTML-document. Currently many but not all
parameters of HTMLDoc are supported.

You need to have HTMLDoc installed before installing this module.

All the pdf-Methods return true for success or false for failure. You can test if errors
occurred by calling the error-method.

Normaly this module uses IPC::Open3 for communacation with the HTMLDOC process. However,
in mod_perl-environments there appear problems with this module because the standard-output can not
be captured. For this problem this module provides a fix doing the communication in file-mode.

For this you can specify the parameter mode in the constructor:
my $htmldoc = new HTMLDoc('mode'=>'file', 'tmpdir'=>'/tmp');

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
    print "%doc  TODO Changes testdata README";
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

%changelog
* Wed May 9 2012 ec2-user@ip-10-86-133-163
- Initial build.