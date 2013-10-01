%global git_hash 79492aa

Name:       coffeescript
Version:    1.3.3
Release:    1%{?dist}
Summary:    A programming language that transcompiles to JavaScript
License:    MIT
URL:        http://jashkenas.github.com/coffee-script/
# download from http://github.com/jashkenas/coffee-script/tarball/%%{version}
Source0:    jashkenas-coffee-script-%{version}-0-g%{git_hash}.tar.gz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch


# support systemwide installation
# courtesy of Debian:  http://packages.debian.org/source/sid/coffeescript
Patch2:     %{name}-support-system-wide-install.patch

BuildRequires:  nodejs
Requires:       nodejs

%description
CoffeeScript is a little language that compiles into JavaScript. Underneath all
of those embarrassing braces and semicolons, JavaScript has always had a
gorgeous object model at its heart. CoffeeScript is an attempt to expose the
good parts of JavaScript in a simple way.

The golden rule of CoffeeScript is: "It's just JavaScript". The code compiles
one-to-one into the equivalent JS, and there is no interpretation at runtime.
You can use any existing JavaScript library seamlessly (and vice-versa). The
compiled output is readable and pretty-printed, passes through JavaScript Lint
without warnings, will work in every JavaScript implementation, and tends to run
as fast or faster than the equivalent handwritten JavaScript.

%prep
%setup -q -n jashkenas-coffee-script-%{git_hash}
%patch2 -p1

%build
./bin/cake build

%install
rm -rf %{buildroot}
./bin/cake  --prefix %{_prefix}         \
            --destdir %{buildroot}      \
            --nodedir %{_libdir}/../lib/nodejs \
            install

# don't need README and LICENSE in libdir
cd %{buildroot}%{_libdir}/../lib/coffee-script
rm README LICENSE

# library files shouldn't be executable
find lib/ -type f -exec chmod -x "{}" \;
find src/ -type f -exec chmod -x "{}" \;  

#%check
#./bin/cake test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_libdir}/../lib/coffee-script
%{_libdir}/../lib/nodejs/coffee-script
%{_bindir}/coffee
%{_bindir}/cake
%doc documentation/docs/*

%changelog
* Thu Jun 14 2012 David Bishop <david@gnuconsulting.com> - 1.3.3-1
- New upstream version

* Sat Aug 20 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.2-1
- initial package
