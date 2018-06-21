%global project rally
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global with_kubernetes 1

%global common_desc \
Rally is a benchmarking tool capable of performing specific, \
complex and reproducible test cases on real deployment scenarios.

Name:             openstack-%{project}
Version:          XXX
Release:          XXX
Summary:          Benchmarking System for OpenStack

License:          ASL 2.0
URL:              http://wiki.openstack.org/wiki/Rally
Source0:          https://tarballs.openstack.org/rally/rally-%{upstream_version}.tar.gz

BuildArch:        noarch

BuildRequires:    git
BuildRequires:    python2-devel
BuildRequires:    python2-pbr
BuildRequires:    python2-setuptools
BuildRequires:    openstack-macros
# BuildRequires for oslo-config-generators
BuildRequires:    python2-oslo-config >= 2:4.0.0
BuildRequires:    python2-oslo-log >= 3.22.0
BuildRequires:    python2-oslo-db >= 4.15.0
BuildRequires:    python2-jsonschema
BuildRequires:    python2-novaclient >= 2.29.0
BuildRequires:    python2-keystoneclient
BuildRequires:    python2-neutronclient >= 5.1.0
BuildRequires:    python2-glanceclient >= 2.3.0
BuildRequires:    python2-saharaclient >= 0.18.0
BuildRequires:    python2-paramiko
BuildRequires:    python2-os-faults
BuildRequires:    python2-subunit
BuildRequires:    python2-osprofiler

Requires:         python2-alembic >= 0.8.7
Requires:         python2-boto
%if 0%{?fedora} >0
Requires:         python2-decorator
Requires:         python2-pyyaml
BuildRequires:    python2-decorator
%else
Requires:         python-decorator
Requires:         PyYAML
BuildRequires:    python-decorator
%endif
Requires:         python2-jinja2
Requires:         python2-jsonschema
Requires:         python2-netaddr
Requires:         python2-oslo-config >= 2:4.0.0
Requires:         python2-oslo-db >= 4.15.0
Requires:         python2-oslo-i18n >= 2.1.0
Requires:         python2-oslo-log >= 3.22.0
Requires:         python2-oslo-serialization >= 1.10.0
Requires:         python2-oslo-utils >= 3.20.0
Requires:         python2-paramiko
Requires:         python2-prettytable
Requires:         python2-gnocchiclient >= 2.7.0
Requires:         python2-keystoneauth1 >= 3.1.0
Requires:         python2-mistralclient >= 2.0.0
Requires:         python2-glanceclient >= 1:2.5.0
Requires:         python2-keystoneclient
Requires:         python2-novaclient >= 1:6.0.0
Requires:         python2-neutronclient >= 5.1.0
Requires:         python2-cinderclient
Requires:         python2-heatclient
Requires:         python2-ceilometerclient
Requires:         python2-ironicclient
Requires:         python2-saharaclient >= 1.1.0
Requires:         python2-swiftclient >= 3.2.0
Requires:         python2-zaqarclient
Requires:         python2-requests >= 2.10.0
Requires:         python2-subunit
Requires:         python2-sqlalchemy
Requires:         python2-six >= 1.9.0
Requires:         python2-os-faults
%if 0%{?with_kubernetes}
Requires:         python2-kubernetes
%endif
Requires:         python2-osprofiler
Requires:         python2-pbr
Requires:         python2-manilaclient

%description
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:    Documentation for OpenStack Rally

Requires:       %{name} = %{version}-%{release}

BuildRequires:  python2-sphinx
BuildRequires:  python2-oslo-sphinx
BuildRequires:  python2-oslo-utils
BuildRequires:  python2-prettytable
BuildRequires:  PyYAML
BuildRequires:  python2-subunit
BuildRequires:  python2-boto
%if 0%{?with_kubernetes}
BuildRequires:  python2-kubernetes
%endif

%description doc
%{common_desc}

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
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/rally/commit/?id=5dfda156e39693870dcf6c6af89b317a6d57a1d2
