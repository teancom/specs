%global modulename requests
%global pyver 2.6
%global python_unmangled_version 26
%global installed_objects /tmp/INSTALLED_OBJECTS-%{_gpg_name}
%define _unpackaged_files_terminate_build 0

Summary: Requests is an ISC Licensed HTTP library, written in Python, for human beings.
Version: 1.1.0
Release: 1%{?_dist}
Source0: %{modulename}-%{version}.tar.gz
License: ISC
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
%if 0%{?python_unmangled_version}
Name: python%{python_unmangled_version}-%{modulename}
Requires: python%{python_unmangled_version}-devel
%else
Name: python-%{modulename}
Requires: python-devel
%endif
Url: http://pypi.python.org/pypi/Requests

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
* Sat Nov 30 2013 David Bishop <david@gnuconsulting.com> - 1.1.0-1
- Initial Argyl build
