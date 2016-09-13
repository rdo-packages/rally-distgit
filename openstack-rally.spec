%global project rally
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

Name:             openstack-%{project}
Version:          XXX
Release:          XXX
Summary:          Benchmarking System for OpenStack

License:          ASL 2.0
URL:              http://wiki.openstack.org/wiki/Rally
Source0:          http://tarballs.openstack.org/rally/rally-master.tar.gz

BuildArch:        noarch

BuildRequires:    python2-devel
BuildRequires:    python-pbr
BuildRequires:    python-setuptools

Requires:         python-alembic
Requires:         python-babel
Requires:         python-boto
Requires:         python-decorator
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
Requires:         python-prettytable
Requires:         PyYAML
Requires:         python-designateclient
Requires:         python-glanceclient >= 1.8.0
Requires:         python-keystoneclient
Requires:         python-manilaclient
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
Requires:         python-subunit
Requires:         python-sqlalchemy
Requires:         python-six >= 1.9.0
Requires:         python-keystoneauth1

%description
Rally is a benchmarking tool capable of performing specific,
complex and reproducible test cases on real deployment scenarios.

%if 0%{?with_doc}
%package doc
Summary:    Documentation for OpenStack Rally

Requires:       %{name} = %{version}-%{release}

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-decorator
BuildRequires:  python-jsonschema
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-utils
BuildRequires:  python-prettytable
BuildRequires:  python-oslo-log
BuildRequires:  python-keystoneclient
BuildRequires:  PyYAML
BuildRequires:  python-oslo-db
BuildRequires:  python-paramiko
BuildRequires:  python-novaclient
BuildRequires:  python-glanceclient
BuildRequires:  python-neutronclient
BuildRequires:  python-novaclient
BuildRequires:  python-saharaclient
BuildRequires:  python-subunit
BuildRequires:  python-boto

%description doc
Rally is a benchmarking tool capable of performing specific,
complex and reproducible test cases on real deployment scenarios.

This package contains documentation files for Rally.
%endif

%prep
%setup -q -n %{project}-%{upstream_version}

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
mkdir -p %{buildroot}/%{_sysconfdir}/bash_completion.d
mv %{buildroot}/usr/etc/bash_completion.d/rally.bash_completion %{buildroot}/%{_sysconfdir}/bash_completion.d

install -d -m 755 %{buildroot}%{_sysconfdir}/%{project}
install -p -D -m 640 etc/%{project}/%{project}.conf.sample %{buildroot}%{_sysconfdir}/%{project}/%{project}.conf

# remove unnecessary files
rm -fr %{buildroot}%{python2_sitelib}/%{project}/deployment

# for Documentation
%if 0%{?with_doc}
%{__python2} setup.py build_sphinx
%endif

%files
%license LICENSE
%{python2_sitelib}/%{project}
%{python2_sitelib}/%{project}*.egg-info
%config(noreplace) %{_sysconfdir}/%{project}/%{project}.conf
%{_bindir}/%{project}
%{_bindir}/%{project}-manage
%{_sysconfdir}/bash_completion.d/rally.bash_completion

%if 0%{?with_doc}
%files doc
%doc LICENSE doc/build/html
%endif

%changelog
