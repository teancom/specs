%define modulename Chart-Clicker

Name: perl-%{modulename}
Version: 2.86
Release: 1%{?_dist}
Summary:... is what CPAN says, anyways. 
License: distributable
Group: Development/Libraries
URL: http://search.cpan.org/search?mode=module&query=Chart-Clicker
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: perl >= 0:5.00503
#Requires:      perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Warning: prerequisite Color::Scheme 0 not found.
Warning: prerequisite Geometry::Primitive::Arc 0 not found.
Warning: prerequisite Geometry::Primitive::Circle 0 not found.
Warning: prerequisite Geometry::Primitive::Point 0 not found.
Warning: prerequisite Graphics::Color::RGB 0 not found.
Warning: prerequisite Graphics::Primitive::Border 0 not found.
Warning: prerequisite Graphics::Primitive::Brush 0 not found.
Warning: prerequisite Graphics::Primitive::Canvas 0 not found.
Warning: prerequisite Graphics::Primitive::Component 0 not found.
Warning: prerequisite Graphics::Primitive::Container 0 not found.
Warning: prerequisite Graphics::Primitive::Driver::Cairo 0 not found.
Warning: prerequisite Graphics::Primitive::Font 0 not found.
Warning: prerequisite Graphics::Primitive::Insets 0 not found.
Warning: prerequisite Graphics::Primitive::Operation::Fill 0 not found.
Warning: prerequisite Graphics::Primitive::Operation::Stroke 0 not found.
Warning: prerequisite Graphics::Primitive::Oriented 0 not found.
Warning: prerequisite Graphics::Primitive::Paint::Gradient::Linear 0 not found.
Warning: prerequisite Graphics::Primitive::Paint::Gradient::Radial 0 not found.
Warning: prerequisite Graphics::Primitive::Paint::Solid 0 not found.
Warning: prerequisite Graphics::Primitive::Path 0 not found.
Warning: prerequisite Graphics::Primitive::TextBox 0 not found.
Warning: prerequisite Layout::Manager::Absolute 0 not found.
Warning: prerequisite Layout::Manager::Axis 0 not found.
Warning: prerequisite Layout::Manager::Compass 0 not found.
Warning: prerequisite Layout::Manager::Flow 0 not found.
Warning: prerequisite Layout::Manager::Grid 0 not found.
Warning: prerequisite Layout::Manager::Single 0 not found.
Source0: %{modulename}-%{version}.tar.gz
BuildArch: noarch

%description
%{summary}.

%prep
%setup -q -n %{modulename}-%{version} 

%build
CFLAGS="$RPM_OPT_FLAGS" perl Makefile.PL INSTALLDIRS=vendor
make

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT
%install

rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

[ -x /usr/lib/rpm/brp-compress ] && /usr/lib/rpm/brp-compress

find $RPM_BUILD_ROOT \( -name perllocal.pod -o -name .packlist \) -exec rm -v {} \;

find $RPM_BUILD_ROOT/usr -type f -print | \
        sed "s@^$RPM_BUILD_ROOT@@g" | \
        grep -v perllocal.pod | \
        grep -v "\.packlist" > %{modulename}-%{version}-filelist
if [ "$(cat %{modulename}-%{version}-filelist)X" = "X" ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit -1
fi

%files -f %{modulename}-%{version}-filelist
%defattr(-,root,root)

%changelog
* Sat Sep 14 2013 David Bishop <david@gnuconsulting.com> 2.86-1
- Initial build. 
