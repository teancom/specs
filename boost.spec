Summary: The Boost C++ Libraries
Name: boost
Version: 1.39.0
Release: 1%{?_dist}
Source0: %{name}-%{version}.tar.bz2
License: Boost Software License
Group: System Environment/Libraries
BuildRoot: %{_builddir}/%{name}-%{version}-root
URL: http://www.boost.org/
Prereq: /sbin/ldconfig
BuildRequires: libstdc++-devel python
Obsoletes: boost <= 1.38.9
Obsoletes: boost-devel <= 1.38.9
Obsoletes: boost-doc <= 1.38.9

%description
Boost provides free peer-reviewed portable C++ source libraries. The
emphasis is on libraries which work well with the C++ Standard
Library. One goal is to establish "existing practice" and provide
reference implementations so that the Boost libraries are suitable for
eventual standardization. (Some of the libraries have already been
proposed for inclusion in the C++ Standards Committee's upcoming C++
Standard Library Technical Report.)

%package devel
Summary: The Boost C++ Headers
Group: System Environment/Libraries
Requires: boost = %{version}-%{release}

%description devel
Headers for the Boost C++ libraries

%prep
%setup -q -n boost_1_39_0
%build
./bootstrap.sh --prefix=$RPM_BUILD_ROOT
./bjam
%install
rm -rf $RPM_BUILD_ROOT
make install
mkdir -p $RPM_BUILD_ROOT/usr
mv $RPM_BUILD_ROOT/lib $RPM_BUILD_ROOT/usr
mv $RPM_BUILD_ROOT/include/boost-1_39/boost $RPM_BUILD_ROOT/include/
rmdir $RPM_BUILD_ROOT/include/boost-1_39
mv $RPM_BUILD_ROOT/include $RPM_BUILD_ROOT/usr
%clean
rm -rf $RPM_BUILD_ROOT
%files
%defattr(-,root,root)
%{_libdir}/*.so.%{version}

%files devel
%defattr(-, root, root)
%{_includedir}/boost
%{_libdir}/*.a
%{_libdir}/*.so
