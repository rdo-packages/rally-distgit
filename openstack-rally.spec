%global project rally
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global with_kubernetes 1

Name:             openstack-%{project}
Version:          0.9.1
Release:          1%{?dist}
Summary:          Benchmarking System for OpenStack

License:          ASL 2.0
URL:              http://wiki.openstack.org/wiki/Rally
Source0:          https://tarballs.openstack.org/rally/rally-%{upstream_version}.tar.gz

BuildArch:        noarch

BuildRequires:    git
BuildRequires:    python2-devel
BuildRequires:    python-pbr
BuildRequires:    python-setuptools
BuildRequires:    openstack-macros
# BuildRequires for oslo-config-generators
BuildRequires:    python-oslo-config >= 2:4.0.0
BuildRequires:    python-oslo-log >= 3.22.0
BuildRequires:    python-decorator
BuildRequires:    python-oslo-db >= 4.15.0
BuildRequires:    python-jsonschema
BuildRequires:    python-novaclient >= 2.29.0
BuildRequires:    python-keystoneclient
BuildRequires:    python-neutronclient >= 5.1.0
BuildRequires:    python-glanceclient >= 2.3.0
BuildRequires:    python-saharaclient >= 0.18.0
BuildRequires:    python-paramiko
BuildRequires:    python-os-faults
BuildRequires:    python-subunit
BuildRequires:    python-osprofiler

Requires:         python-alembic >= 0.8.7
Requires:         python-boto
Requires:         python-decorator
Requires:         python-jinja2
Requires:         python-jsonschema
Requires:         python-netaddr
Requires:         python-oslo-config >= 2:4.0.0
Requires:         python-oslo-db >= 4.15.0
Requires:         python-oslo-i18n >= 2.1.0
Requires:         python-oslo-log >= 3.22.0
Requires:         python-oslo-serialization >= 1.10.0
Requires:         python-oslo-utils >= 3.20.0
Requires:         python-paramiko
Requires:         python-prettytable
Requires:         PyYAML
Requires:         python-gnocchiclient >= 2.7.0
Requires:         python-keystoneauth1 >= 3.1.0
Requires:         python-mistralclient >= 2.0.0
Requires:         python-glanceclient >= 1:2.5.0
Requires:         python-keystoneclient
Requires:         python-novaclient >= 1:6.0.0
Requires:         python-neutronclient >= 5.1.0
Requires:         python-cinderclient
Requires:         python-heatclient
Requires:         python-ceilometerclient
Requires:         python-ironicclient
Requires:         python-saharaclient >= 1.1.0
Requires:         python-swiftclient >= 3.2.0
Requires:         python-zaqarclient
Requires:         python-requests >= 2.10.0
Requires:         python-subunit
Requires:         python-sqlalchemy
Requires:         python-six >= 1.9.0
Requires:         python-os-faults
%if 0%{?with_kubernetes}
Requires:         python-kubernetes
%endif
Requires:         python-osprofiler
Requires:         python-pbr
Requires:         python-manilaclient

%description
Rally is a benchmarking tool capable of performing specific,
complex and reproducible test cases on real deployment scenarios.

%if 0%{?with_doc}
%package doc
Summary:    Documentation for OpenStack Rally

Requires:       %{name} = %{version}-%{release}

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-oslo-utils
BuildRequires:  python-prettytable
BuildRequires:  PyYAML
BuildRequires:  python-subunit
BuildRequires:  python-boto
%if 0%{?with_kubernetes}
BuildRequires:  python-kubernetes
%endif

%description doc
Rally is a benchmarking tool capable of performing specific,
complex and reproducible test cases on real deployment scenarios.

This package contains documentation files for Rally.
%endif

%prep
%autosetup -S git -n %{project}-%{upstream_version}

%py_req_cleanup

# Fix permissions
chmod 644 `find samples/tasks/scenarios -type f -regex ".*\.\(yaml\|json\)" -print`

%build
%{__python2} setup.py build

# for Documentation
%if 0%{?with_doc}
%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
mkdir -p %{buildroot}/%{_sysconfdir}/bash_completion.d
mv %{buildroot}/usr/etc/bash_completion.d/rally.bash_completion %{buildroot}/%{_sysconfdir}/bash_completion.d

# Generate Rally config
install -d -m 755 %{buildroot}%{_sysconfdir}/%{project}/
PYTHONPATH=. oslo-config-generator --config-file etc/rally/rally-config-generator.conf \
                      --output-file %{buildroot}%{_sysconfdir}/%{project}/rally.conf

# fix config permission
chmod 644 %{buildroot}%{_sysconfdir}/%{project}/rally.conf

# remove unnecessary files
rm -fr %{buildroot}%{python2_sitelib}/%{project}/deployment/engines/devstack
rm -fr %{buildroot}%{python2_sitelib}/%{project}/deployment/engines/lxc
rm -fr %{buildroot}%{python2_sitelib}/%{project}/deployment/serverprovider/providers/lxc

# Include Samples as it contains rally plugins and deployment configs
mkdir -p %{buildroot}%{_datarootdir}/%{name}
cp -pr samples %{buildroot}%{_datarootdir}/%{name}

%files
%license LICENSE
%{python2_sitelib}/%{project}
%if 0%{?with_kubernetes}
%{python2_sitelib}/%{project}/plugins/openstack/scenarios/magnum
%{python2_sitelib}/%{project}/plugins/openstack/context/magnum
%else
%exclude %{python2_sitelib}/%{project}/plugins/openstack/scenarios/magnum
%exclude %{python2_sitelib}/%{project}/plugins/openstack/context/magnum
%endif
%{python2_sitelib}/%{project}*.egg-info
%config(noreplace) %{_sysconfdir}/%{project}/%{project}.conf
%{_bindir}/%{project}
%{_bindir}/%{project}-manage
%{_sysconfdir}/bash_completion.d/rally.bash_completion
%{_datarootdir}/%{name}/samples

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Fri Aug 25 2017 Alfredo Moralejo <amoralej@redhat.com> 0.9.1-1
- Update to 0.9.1

