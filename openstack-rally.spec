# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
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
URL:              https://rally.readthedocs.io
Source0:          https://tarballs.openstack.org/rally/rally-%{upstream_version}.tar.gz

BuildArch:        noarch

BuildRequires:    git
BuildRequires:    openstack-macros

Requires:       python%{pyver}-rally = %{version}-%{release}

%description
%{common_desc}

%package -n    python%{pyver}-%{project}
Summary:       Rally Python library

%{?python_provide:%python_provide python%{pyver}-%{project}}
%if %{pyver} == 3
Obsoletes: python2-%{project} < %{version}-%{release}
%endif
BuildRequires:    python%{pyver}-devel
BuildRequires:    python%{pyver}-pbr
BuildRequires:    python%{pyver}-setuptools
# BuildRequires for oslo-config-generators
BuildRequires:    python%{pyver}-oslo-config >= 2:4.0.0
BuildRequires:    python%{pyver}-oslo-log >= 3.22.0
BuildRequires:    python%{pyver}-oslo-db >= 4.15.0
BuildRequires:    python%{pyver}-jsonschema
BuildRequires:    python%{pyver}-novaclient >= 2.29.0
BuildRequires:    python%{pyver}-keystoneclient
BuildRequires:    python%{pyver}-neutronclient >= 5.1.0
BuildRequires:    python%{pyver}-glanceclient >= 2.3.0
BuildRequires:    python%{pyver}-saharaclient >= 0.18.0
BuildRequires:    python%{pyver}-paramiko
BuildRequires:    python%{pyver}-os-faults
BuildRequires:    python%{pyver}-subunit
BuildRequires:    python%{pyver}-osprofiler

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:    python-decorator
%else
BuildRequires:    python%{pyver}-decorator
%endif

Requires:         python%{pyver}-alembic >= 0.8.7
Requires:         python%{pyver}-boto
Requires:         python%{pyver}-jinja2
Requires:         python%{pyver}-jsonschema
Requires:         python%{pyver}-netaddr
Requires:         python%{pyver}-oslo-config >= 2:4.0.0
Requires:         python%{pyver}-oslo-db >= 4.15.0
Requires:         python%{pyver}-oslo-i18n >= 2.1.0
Requires:         python%{pyver}-oslo-log >= 3.22.0
Requires:         python%{pyver}-paramiko
Requires:         python%{pyver}-prettytable
Requires:         python%{pyver}-gnocchiclient >= 2.7.0
Requires:         python%{pyver}-keystoneauth1 >= 3.1.0
Requires:         python%{pyver}-mistralclient >= 2.0.0
Requires:         python%{pyver}-glanceclient >= 1:2.5.0
Requires:         python%{pyver}-keystoneclient
Requires:         python%{pyver}-novaclient >= 1:6.0.0
Requires:         python%{pyver}-neutronclient >= 5.1.0
Requires:         python%{pyver}-cinderclient
Requires:         python%{pyver}-heatclient
Requires:         python%{pyver}-ceilometerclient
Requires:         python%{pyver}-ironicclient
Requires:         python%{pyver}-saharaclient >= 1.1.0
Requires:         python%{pyver}-swiftclient >= 3.2.0
Requires:         python%{pyver}-zaqarclient
Requires:         python%{pyver}-requests >= 2.10.0
Requires:         python%{pyver}-subunit
Requires:         python%{pyver}-sqlalchemy
Requires:         python%{pyver}-six >= 1.9.0
Requires:         python%{pyver}-os-faults
Requires:         python%{pyver}-osprofiler
Requires:         python%{pyver}-pbr
Requires:         python%{pyver}-manilaclient

# Handle python2 exception
%if %{pyver} == 2
Requires:         python-decorator
Requires:         PyYAML
%else
Requires:         python%{pyver}-decorator
Requires:         python%{pyver}-PyYAML
%endif

%description -n python%{pyver}-%{project}
%{common_desc}

This package contains the rally python library.

%if 0%{?with_doc}
%package doc
Summary:    Documentation for OpenStack Rally

Requires:       %{name} = %{version}-%{release}

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-oslo-sphinx
BuildRequires:  python%{pyver}-prettytable
BuildRequires:  PyYAML
BuildRequires:  python%{pyver}-subunit
BuildRequires:  python%{pyver}-boto

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
%{pyver_build}

# for Documentation
%if 0%{?with_doc}
%{pyver_bin} setup.py build_sphinx
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

mkdir -p %{buildroot}/%{_sysconfdir}/bash_completion.d
mv %{buildroot}/usr/etc/bash_completion.d/rally.bash_completion %{buildroot}/%{_sysconfdir}/bash_completion.d

# Generate Rally config
install -d -m 755 %{buildroot}%{_sysconfdir}/%{project}/
PYTHONPATH=. oslo-config-generator-%{pyver} --config-file etc/rally/rally-config-generator.conf \
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


%files -n python%{pyver}-%{project}
%license LICENSE
%{pyver_sitelib}/%{project}
%{pyver_sitelib}/%{project}*.egg-info

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
