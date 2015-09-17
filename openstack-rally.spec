%global project rally
Name:             openstack-%{project}
Version:          0.0.4
Release:          1%{?dist}
Summary:          Benchmarking tool for OpenStack

License:          ASL 2.0
URL:              http://wiki.openstack.org/wiki/Rally
Source0:          https://pypi.python.org/packages/source/r/rally/%{project}-%{version}.tar.gz

BuildArch:        noarch 
BuildRequires:    python2-devel
BuildRequires:    python-jsonschema
BuildRequires:    python-pbr

Requires:         python-babel
Requires:         python-boto
Requires:         python-decorator
Requires:         python-fixtures
Requires:         python-iso8601
Requires:         python-jinja2
Requires:         python-jsonschema
Requires:         python-netaddr
Requires:         python-oslo-config >= 1.11.0
Requires:         python-oslo-db >= 1.7.0
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
Requires:         python-glanceclient
Requires:         python-keystoneclient
Requires:         python-novaclient
Requires:         python-neutronclient
Requires:         python-cinderclient
Requires:         python-heatclient
Requires:         python-ceilometerclient
Requires:         python-ironicclient
Requires:         python-saharaclient
Requires:         python-troveclient
Requires:         python-zaqarclient
Requires:         python-subunit
Requires:         python-requests >= 2.5.2
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
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
mkdir -p %{buildroot}/%{_sysconfdir}/bash_completion.d
mv %{buildroot}/usr/etc/bash_completion.d/rally.bash_completion %{buildroot}/%{_sysconfdir}/bash_completion.d

chmod a+x %{buildroot}%{python2_sitelib}/%{project}/deploy/engines/devstack/install.sh
chmod a+x %{buildroot}%{python2_sitelib}/%{project}/deploy/engines/lxc/start.sh
chmod a+x %{buildroot}%{python2_sitelib}/%{project}/deploy/serverprovider/providers/lxc/lxc-install.sh
chmod a+x %{buildroot}%{python2_sitelib}/%{project}/deploy/serverprovider/providers/lxc/configure_container.sh

%post
# Configure Rally
RALLY_DB_DIR=%{_sharedstatedir}/{%project}/database
RALLY_CONF_DIR=%{_sysconfdir}/{%project}
mkdir -p ${RALLY_DATABASE_DIR} ${RALLY_CONFIGURATION_DIR}
sed 's|#connection=<None>|connection=sqlite:///'${RALLY_DATABASE_DIR}'/rally.sqlite|' \
${TMP}/etc/rally/rally.conf.sample > ${RALLY_CONFIGURATION_DIR}/rally.conf
rally-manage db recreate
chmod -R go+w ${RALLY_DATABASE_DIR}

%files
%license LICENSE
%{python2_sitelib}/%{project}
%{python2_sitelib}/%{project}*.egg-info

%{_bindir}/%{project}
%{_bindir}/%{project}-manage
%{_sysconfdir}/bash_completion.d/rally.bash_completion

%changelog
* Fri Sep 11 2015 Steve Linabery <slinaber@redhat.com> - 0.0.4-1
- rebase to 0.0.4 release

* Wed May 13 2015 Victoria Martinez de la Cruz <vkmc@fedorapeople.org> - 0.0.1-1
- Initial package.
