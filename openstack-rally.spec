%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%global project rally
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global with_kubernetes 1

%global common_desc \
Rally is a benchmarking tool capable of performing specific, \
complex and reproducible test cases on real deployment scenarios.

Name:             openstack-%{project}
Version:          XXX
Release:          XXX
Summary:          Benchmarking System for OpenStack

License:          Apache-2.0
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

Obsoletes: python2-%{project} < %{version}-%{release}
BuildRequires:    python3-devel
BuildRequires:    pyproject-rpm-macros

%description -n python3-%{project}
%{common_desc}

This package contains the rally python library.

%if 0%{?with_doc}
%package doc
Summary:    Documentation for OpenStack Rally
Requires:       %{name} = %{version}-%{release}

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


# Fix permissions
chmod 644 `find samples/tasks/scenarios -type f -regex ".*\.\(yaml\|json\)" -print`

sed -i /.*-c.*upper-constraints.txt.*/d tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

# for Documentation
%if 0%{?with_doc}
export PYTHONPATH=.
%tox -e docs
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

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
%{python3_sitelib}/%{project}*.dist-info

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
