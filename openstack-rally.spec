%global project rally
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global with_kubernetes 1

%global common_desc \
Rally is a benchmarking tool capable of performing specific, \
complex and reproducible test cases on real deployment scenarios.

%if 0%{?fedora} >= 24
%global with_python3 1
%endif

Name:             openstack-%{project}
Version:          XXX
Release:          XXX
Summary:          Benchmarking System for OpenStack

License:          ASL 2.0
URL:              https://rally.readthedocs.io
Source0:          https://tarballs.openstack.org/rally/rally-%{upstream_version}.tar.gz

BuildArch:        noarch

BuildRequires:    git
BuildRequires:    openstack-macros

%if 0%{?with_python3}
Requires:       python3-rally = %{version}-%{release}
%else
Requires:       python2-rally = %{version}-%{release}
%endif

%description
%{common_desc}

%package -n    python2-%{project}
Summary:       Rally Python library

%{?python_provide:%python_provide python2-%{project}}
BuildRequires:    python2-devel
BuildRequires:    python2-pbr
BuildRequires:    python2-setuptools
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
Requires:         python2-osprofiler
Requires:         python2-pbr
Requires:         python2-manilaclient

%description -n python2-%{project}
%{common_desc}

This package contains the rally python library.

# Python3 package
%if 0%{?with_python3}
%package -n    python3-%{project}
Summary:       Rally Python library

%{?python_provide:%python_provide python3-%{project}}

BuildRequires:    python3-devel
BuildRequires:    python3-pbr
BuildRequires:    python3-setuptools
BuildRequires:    python3-oslo-config >= 2:4.0.0
BuildRequires:    python3-oslo-log >= 3.22.0
BuildRequires:    python3-oslo-db >= 4.15.0
BuildRequires:    python3-jsonschema
BuildRequires:    python3-novaclient >= 2.29.0
BuildRequires:    python3-keystoneclient
BuildRequires:    python3-neutronclient >= 5.1.0
BuildRequires:    python3-glanceclient >= 2.3.0
BuildRequires:    python3-saharaclient >= 0.18.0
BuildRequires:    python3-paramiko
BuildRequires:    python3-os-faults
BuildRequires:    python3-subunit
BuildRequires:    python3-osprofiler
BuildRequires:    python2-decorator

Requires:         python3-alembic >= 0.8.7
Requires:         python3-boto
Requires:         python3-decorator
Requires:         python3-PyYAML
Requires:         python3-jinja2
Requires:         python3-jsonschema
Requires:         python3-netaddr
Requires:         python3-oslo-config >= 2:4.0.0
Requires:         python3-oslo-db >= 4.15.0
Requires:         python3-oslo-i18n >= 2.1.0
Requires:         python3-oslo-log >= 3.22.0
Requires:         python3-paramiko
Requires:         python3-prettytable
Requires:         python3-gnocchiclient >= 2.7.0
Requires:         python3-keystoneauth1 >= 3.1.0
Requires:         python3-mistralclient >= 2.0.0
Requires:         python3-glanceclient >= 1:2.5.0
Requires:         python3-keystoneclient
Requires:         python3-novaclient >= 1:6.0.0
Requires:         python3-neutronclient >= 5.1.0
Requires:         python3-cinderclient
Requires:         python3-heatclient
Requires:         python3-ceilometerclient
Requires:         python3-ironicclient
Requires:         python3-saharaclient >= 1.1.0
Requires:         python3-swiftclient >= 3.2.0
Requires:         python3-zaqarclient
Requires:         python3-requests >= 2.10.0
Requires:         python3-subunit
Requires:         python3-sqlalchemy
Requires:         python3-six >= 1.9.0
Requires:         python3-os-faults
Requires:         python3-osprofiler
Requires:         python3-pbr
Requires:         python3-manilaclient

%description -n python3-%{project}
%{common_desc}

This package contains tests for the Rally python library.
%endif

%if 0%{?with_doc}
%package doc
Summary:    Documentation for OpenStack Rally

Requires:       %{name} = %{version}-%{release}

BuildRequires:  python2-sphinx
BuildRequires:  python2-oslo-sphinx
BuildRequires:  python2-prettytable
BuildRequires:  PyYAML
BuildRequires:  python2-subunit
BuildRequires:  python2-boto

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
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# for Documentation
%if 0%{?with_doc}
%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

mkdir -p %{buildroot}/%{_sysconfdir}/bash_completion.d
mv %{buildroot}/usr/etc/bash_completion.d/rally.bash_completion %{buildroot}/%{_sysconfdir}/bash_completion.d

# Generate Rally config
install -d -m 755 %{buildroot}%{_sysconfdir}/%{project}/
PYTHONPATH=. oslo-config-generator --config-file etc/rally/rally-config-generator.conf \
                      --output-file %{buildroot}%{_sysconfdir}/%{project}/rally.conf

# fix config permission
chmod 644 %{buildroot}%{_sysconfdir}/%{project}/rally.conf

# Include Samples as it contains rally plugins and deployment configs
mkdir -p %{buildroot}%{_datarootdir}/%{name}
cp -pr samples %{buildroot}%{_datarootdir}/%{name}

%files
%license LICENSE
%config(noreplace) %{_sysconfdir}/%{project}/%{project}.conf
%{_bindir}/%{project}
%{_bindir}/%{project}-manage
%{_sysconfdir}/bash_completion.d/rally.bash_completion
%{_datarootdir}/%{name}/samples


%files -n python2-%{project}
%license LICENSE
%{python2_sitelib}/%{project}
%{python2_sitelib}/%{project}*.egg-info

%if 0%{?with_python3}
%files -n python3-%{project}
%license LICENSE
%{python3_sitelib}/%{project}
%{python3_sitelib}/%{project}*.egg-info
%endif

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
