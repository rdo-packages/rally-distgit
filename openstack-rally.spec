%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/rally/rally-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:        noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:    git-core
BuildRequires:    openstack-macros

Requires:       python3-rally = %{version}-%{release}

%description
%{common_desc}

%package -n    python3-%{project}
Summary:       Rally Python library

%{?python_provide:%python_provide python3-%{project}}
Obsoletes: python2-%{project} < %{version}-%{release}
BuildRequires:    python3-devel
BuildRequires:    python3-pbr
BuildRequires:    python3-setuptools
# BuildRequires for oslo-config-generators
BuildRequires:    python3-fixtures
BuildRequires:    python3-oslo-config >= 2:4.0.0
BuildRequires:    python3-oslo-log >= 3.22.0
BuildRequires:    python3-oslo-db >= 4.15.0
BuildRequires:    python3-jsonschema
BuildRequires:    python3-paramiko
BuildRequires:    python3-subunit

Requires:         python3-alembic >= 1.3.1
Requires:         python3-jinja2
Requires:         python3-jsonschema
Requires:         python3-oslo-config >= 2:4.0.0
Requires:         python3-oslo-db >= 4.15.0
Requires:         python3-oslo-log >= 4.4.0
Requires:         python3-paramiko
Requires:         python3-prettytable
Requires:         python3-requests >= 2.25.0
Requires:         python3-subunit
Requires:         python3-sqlalchemy
Requires:         python3-pbr
Requires:         python3-pyOpenSSL
Requires:         python3-markupsafe
Requires:         python3-yaml

%description -n python3-%{project}
%{common_desc}

This package contains the rally python library.

%if 0%{?with_doc}
%package doc
Summary:    Documentation for OpenStack Rally

Requires:       %{name} = %{version}-%{release}

BuildRequires:  python3-sphinx
BuildRequires:  python3-oslo-sphinx
BuildRequires:  python3-prettytable
BuildRequires:  python3-subunit

BuildRequires:  python3-yaml

%description doc
%{common_desc}

This package contains documentation files for Rally.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -S git -n %{project}-%{upstream_version}

%py_req_cleanup

# Fix permissions
chmod 644 `find samples/tasks/scenarios -type f -regex ".*\.\(yaml\|json\)" -print`

%build
%{py3_build}

# for Documentation
%if 0%{?with_doc}
export PYTHONPATH=.
sphinx-build -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

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
%{_sysconfdir}/bash_completion.d/rally.bash_completion
%{_datarootdir}/%{name}/samples


%files -n python3-%{project}
%license LICENSE
%{python3_sitelib}/%{project}
%{python3_sitelib}/%{project}*.egg-info

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
