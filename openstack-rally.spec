%global project rally

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:             openstack-%{project}
Version:          0.3.3
Release:          1%{?dist}
Summary:          Benchmarking tool for OpenStack

License:          ASL 2.0
URL:              http://wiki.openstack.org/wiki/Rally
Source0:          http://tarballs.openstack.org/rally/rally-%{version}%{?milestone}.tar.gz

BuildArch:        noarch
BuildRequires:    python2-devel
BuildRequires:    python-jsonschema
BuildRequires:    python-pbr
BuildRequires:    python-setuptools
BuildRequires:    python-oslo-config >= 2.4.0
BuildRequires:    python-oslo-db >= 2.6.0
BuildRequires:    python-oslo-log >= 1.8.0
BuildRequires:    python-paramiko
BuildRequires:    python-glanceclient >= 1.8.0
BuildRequires:    python-neutronclient >= 2.6.0
BuildRequires:    python-novaclient >= 2.29.0
BuildRequires:    python-saharaclient >= 0.10.0
BuildRequires:    python-subunit
BuildRequires:    python-sphinx

Requires:         python-babel
Requires:         python-boto
Requires:         python-decorator
Requires:         python-fixtures
Requires:         python-iso8601
Requires:         python-jinja2
Requires:         python-jsonschema
Requires:         python-netaddr
Requires:         python-oslo-config >= 2.4.0
Requires:         python-oslo-db >= 2.6.0
Requires:         python-oslo-i18n >= 1.5.0
Requires:         python-oslo-log >= 1.8.0
Requires:         python-oslo-serialization >= 1.4.0
Requires:         python-oslo-utils >= 1.4.0
Requires:         python-paramiko
Requires:         python-pecan
Requires:         python-prettytable
Requires:         PyYAML
Requires:         python-psycopg2
Requires:         python-designateclient
Requires:         python-glanceclient >= 1.8.0
Requires:         python-keystoneclient
Requires:         python-manila >= 1.3.0
Requires:         python-novaclient >= 2.29.0
Requires:         python-neutronclient >= 2.6.0
Requires:         python-cinderclient
Requires:         python-heatclient
Requires:         python-ceilometerclient
Requires:         python-ironicclient
Requires:         python-saharaclient >= 0.10.0
Requires:         python-swiftclient >= 2.2.0
Requires:         python-troveclient
Requires:         python-zaqarclient
Requires:         python-requests >= 2.5.2
Requires:         python-simplejson
Requires:         python-subunit
Requires:         python-sqlalchemy
Requires:         python-sphinx
Requires:         python-six >= 1.9.0
Requires:         python-wsme

%description
Rally is a benchmarking tool capable of performing specific,
complex and reproducible test cases on real deployment scenarios.

%prep
%setup -q -n %{project}-%{upstream_version}

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt

%build
PYTHONPATH=. oslo-config-generator --config-file=etc/rally/rally-config-generator.conf
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
mkdir -p %{buildroot}/%{_sysconfdir}/bash_completion.d
mv %{buildroot}/usr/etc/bash_completion.d/rally.bash_completion %{buildroot}/%{_sysconfdir}/bash_completion.d

install -d -m 755 %{buildroot}%{_sysconfdir}/%{project}
install -p -D -m 640 etc/%{project}/%{project}.conf.sample %{buildroot}%{_sysconfdir}/%{project}/%{project}.conf
chmod a+x %{buildroot}%{python2_sitelib}/%{project}/deployment/engines/devstack/install.sh
chmod a+x %{buildroot}%{python2_sitelib}/%{project}/deployment/engines/lxc/start.sh
chmod a+x %{buildroot}%{python2_sitelib}/%{project}/deployment/serverprovider/providers/lxc/lxc-install.sh
chmod a+x %{buildroot}%{python2_sitelib}/%{project}/deployment/serverprovider/providers/lxc/configure_container.sh

%files
%license LICENSE
%{python2_sitelib}/%{project}
%{python2_sitelib}/%{project}*.egg-info
%{_sysconfdir}/%{project}
%{_bindir}/%{project}
%{_bindir}/%{project}-manage
%{_sysconfdir}/bash_completion.d/rally.bash_completion

%changelog
* Thu Mar 31 2016 RDO <rdo-list@redhat.com> 0.3.3-1
- RC1 Rebuild for Mitaka RC1 0.3.3
