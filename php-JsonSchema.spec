%global github_owner   justinrainbow
%global github_name    json-schema
%global github_version 1.3.3
%global github_commit  56fe099669ff3ec3be859ec02e3da965a720184d

%global php_min_ver    5.3.0

%global lib_name       JsonSchema

Name:          php-%{lib_name}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       PHP implementation of JSON schema

Group:         Development/Libraries
License:       BSD
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch: noarch
# For tests
BuildRequires: php-common >= %{php_min_ver}
BuildRequires: php-pear(pear.phpunit.de/DbUnit)
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
BuildRequires: php-pear(pear.phpunit.de/PHPUnit_Story)
# For tests: phpcompatinfo
BuildRequires: php-curl
BuildRequires: php-filter
BuildRequires: php-pecl-jsonc
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-spl

Requires:      php-common >= %{php_min_ver}
# phpcompatinfo
Requires:      php-curl
Requires:      php-filter
Requires:      php-pecl-jsonc
Requires:      php-mbstring
Requires:      php-pcre
Requires:      php-spl

%description
A PHP implementation for validating JSON structures against a given schema.

See http://json-schema.org for more details.


%prep
%setup -q -n %{github_name}-%{github_commit}

# Clean up unnecessary files
find . -type f -name '.git*' -delete

# Create autoloader for tests
( cat <<'AUTOLOAD'
<?php
spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', $class).'.php';
    require_once $src;
});
AUTOLOAD
) > autoload.php


%build
# Empty build section, nothing to build


%install
mkdir -p -m 755 %{buildroot}%{_datadir}/php
cp -rp src/%{lib_name} %{buildroot}%{_datadir}/php/


%check
# Remove empty tests
rm -f tests/JsonSchema/Tests/Drafts/Draft3Test.php \
      tests/JsonSchema/Tests/Drafts/Draft4Test.php

%{_bindir}/phpunit \
    -d include_path="./src:./tests:.:%{pear_phpdir}" \
    -d date.timezone="UTC" \
    --bootstrap=./autoload.php \
    .


%files
%doc LICENSE README.md composer.json
%{_datadir}/php/%{lib_name}


%changelog
* Sun Aug 11 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.3.3-1
- Updated to 1.3.3

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 05 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.3.2-1
- Updated to 1.3.2
- Added php-pear(pear.phpunit.de/DbUnit), php-pear(pear.phpunit.de/PHPUnit_Selenium),
  and php-pear(pear.phpunit.de/PHPUnit_Story) build requires
- Removed php-ctype require
- Added php-mbstring require

* Thu Mar 21 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.3.1-1
- Updated to upstream version 1.3.1

* Sun Feb 24 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.3.0-1
- Updated to upstream version 1.3.0

* Mon Feb 04 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.2.4-1
- Updated to upstream version 1.2.4
- Updates per new Fedora packaging guidelines for Git repos

* Sun Dec 09 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.2.2-2
- Fixed failing Mock/Koji builds
- Removed "docs" directory from %%doc

* Sat Dec 08 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.2.2-1
- Updated to upstream version 1.2.2
- Added php-ctype require
- Added PSR-0 autoloader for tests
- Added %%check

* Tue Nov 27 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.2.1-1
- Initial package
