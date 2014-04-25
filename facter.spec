%{!?ruby_sitelibdir: %define ruby_sitelibdir %(ruby -rrbconfig -e 'puts Config::CONFIG["sitelibdir"]')}

%define has_ruby_abi 0%{?fedora} || 0%{?rhel} >= 5
%define has_ruby_noarch %has_ruby_abi

Summary: Ruby module for collecting simple facts about a host operating system
Name: facter
Version: 2.0.1
Release: 1%{?_dist}
License: GPLv2+
Group: System Environment/Base
URL: http://reductivelabs.com/projects/facter
Source0: http://reductivelabs.com/downloads/facter/%{name}-%{version}.tar.gz
Patch0: ec2.patch
# http://github.com/reductivelabs/facter/commit/75db918c37a9fef36c829105d1f8a99ff8bcf751
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: ruby >= 1.8.7-6
Requires: which redhat-lsb
%if %has_ruby_abi
Requires: ruby(abi) = 1.8
%endif
BuildRequires: ruby >= 1.8.1
#BuildArch: noarch

%description
Ruby module for collecting simple facts about a host Operating
system. Some of the facts are preconfigured, such as the hostname and the
operating system. Additional facts can be added through simple Ruby scripts

%prep
%setup -q
#%patch0 -p0

%build

%install
rm -rf %{buildroot}
ruby install.rb --destdir=%{buildroot} --quick --no-rdoc

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/facter
%{ruby_sitelibdir}/facter.rb
%{ruby_sitelibdir}/facter
%{_mandir}
%doc LICENSE 


%changelog
* Wed Oct 02 2013 David Bishop <david@gnuconsulting.com> - 1.7.3-2
- New upstream version
- Add patch to make ec2 facts work in a VPC

* Fri Feb 03 2012 David Bishop <david@gnuconsulting.com> - 1.6.5-1
- Initial package for maefsco
