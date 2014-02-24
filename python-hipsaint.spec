%global modulename hipsaint
%global pyver 2.6
%global python_unmangled_version 26
%global installed_objects /tmp/INSTALLED_OBJECTS
%define _unpackaged_files_terminate_build 0

Summary: Nagios Alerts to Hipchat Room
Version: 0.4.2
Release: 1%{?_dist}
Source0: %{modulename}-%{version}.tar.gz
License: PSF or ZPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
%if 0%{?python_unmangled_version}
Name: python%{python_unmangled_version}-%{modulename}
#Requires: python%{python_unmangled_version}-devel python%{python_unmangled_version}-distribute
Requires: python%{python_unmangled_version}-requests
#BuildRequires: python%{python_unmangled_version}-distribute
%else
Name: python-%{modulename}
Requires: python-devel python-distribute
Requires: python-requests
BuildRequires: python-distribute
%endif
Url: https://github.com/hannseman/hipsaint

# IF we're 64 bit, our hood is lib64
%ifarch x86_64
%global python_libdir /usr/lib64/python%{pyver}/site-packages
%else
%global python_libdir /usr/lib/python/site-packages
%endif

%description
%{summary}

%prep
%setup -n %{modulename}-%{version}

%build
%if 0%{?python_unmangled_version}
python%{pyver} setup.py build
%else
python setup.py build
%endif

%install
%if 0%{?python_unmangled_version}
python%{pyver} setup.py install \
	--single-version-externally-managed \
	--root=$RPM_BUILD_ROOT \
	--record=%{installed_objects} \
	--install-lib=%{python_libdir}
%else
python setup.py install \
	--single-version-externally-managed \
	--root=$RPM_BUILD_ROOT \
	--record=%{installed_objects} \
	--install-lib=%{python_libdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{installed_objects}
%defattr(-,root,root)

%changelog
* Sat Nov 30 2013 David Bishop <david@gnuconsulting.com>  - 0.4.2-1
- Initial Argyl build
