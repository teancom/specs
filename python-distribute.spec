%global modulename distribute
%global pyver 2.6
%global python_unmangled_version 26
%global installed_objects /tmp/INSTALLED_OBJECTS
%define _unpackaged_files_terminate_build 0

Summary: Easily download, build, install, upgrade, and uninstall Python packages
Version: 0.6.49
Release: 1%{?_dist}
Source0: %{modulename}-%{version}.tar.gz
License: PSF or ZPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
Url: http://pypi.python.org/pypi/distribute
%if 0%{?python_unmangled_version}
Name: python%{python_unmangled_version}-%{modulename}
Requires: python%{python_unmangled_version}-devel
Obsoletes: python%{python_unmangled_version}-setuptools
Obsoletes: python-setuptools
Provides: python-setuptools
Provides: python%{python_unmangled_version}-setuptools
%else
Name: python-%{modulename}
Requires: python-devel
Obsoletes: python-setuptools
Provides: python-setuptools
%endif

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
	--root=$RPM_BUILD_ROOT \
	--record=%{installed_objects} \
	--single-version-externally-managed \
	--install-lib=%{python_libdir}
%else
python setup.py install \
	--root=$RPM_BUILD_ROOT \
	--record=%{installed_objects} \
	--single-version-externally-managed \
	--install-lib=%{python_libdir}
%endif

/bin/sed -i -e 's/^/"/g' %{installed_objects}
/bin/sed -i -e 's/$/"/g' %{installed_objects}
#/bin/mv /tmp/python-distribute.objects %{installed_objects}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{installed_objects}
%defattr(-,root,root)

%changelog
* Sat Nov 30 2013 David Bishop <david@gnuconsulting.com> - 0.6.49-1
- Initial Argyl build
