Name: rave		
Version:	0.22
Release:	1%{?_dist}
Summary:	Social! Cloud! Yay!

License:	F/OSS
URL:		http://rave.apache.org/
Source0:	apache-rave-%{version}-bin.tar.gz
Source1:    rave.init
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Prefix:     /opt
BuildArch:  noarch

Requires:	java7 >= 1.7.0

%description
Lots of social nonsense.

%prep
%setup -q -n apache-rave-%{version}

%build

%install
rm -rf %{buildroot}
mkdir -p -m 755 \
$RPM_BUILD_ROOT%{prefix}/rave \
$RPM_BUILD_ROOT%{prefix}/rave/db \
$RPM_BUILD_ROOT%{prefix}/rave/work \
$RPM_BUILD_ROOT/etc/init.d \
$RPM_BUILD_ROOT/var/log/rave
cp -pr * $RPM_BUILD_ROOT%{prefix}/rave
cp -pr %{SOURCE1} $RPM_BUILD_ROOT/etc/init.d/rave

%clean
rm -rf %{buildroot}

%pre
if [ $1 = 1 ]; then
  groupadd -r rave || %{user_group_error};
  useradd -M -r -g rave -d /opt/rave rave || %{user_group_error};
fi

%preun
if [ $1 = 0 ]; then
  /usr/sbin/userdel rave || true;
fi

/sbin/chkconfig --del rave

%post 
if [ $1 = 1 ]; then
    /sbin/chkconfig --add rave
fi

%files
%defattr(-,rave,rave,-)
%{prefix}/rave/webapps
%{prefix}/rave/lib
%{prefix}/rave/logs
%{prefix}/rave/shared
%{prefix}/rave/temp
%{prefix}/rave/common
%{prefix}/rave/bin
%{prefix}/rave/db
%{prefix}/rave/work
/var/log/rave
%doc %{prefix}/rave/CHANGELOG
%doc %{prefix}/rave/LICENSE
%doc %{prefix}/rave/NOTICE
%doc %{prefix}/rave/README
%doc %{prefix}/rave/RUNNING.txt
%config(noreplace) %{prefix}/rave/conf
%attr(0755,root,root) /etc/init.d/rave


%changelog
* Mon Oct 21 2013 David Bishop <dbishop@robertmaefs.com> 0.22-1
- initial build for Argyl
