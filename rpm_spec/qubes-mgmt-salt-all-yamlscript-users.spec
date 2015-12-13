%{!?version: %define version %(cat version)}

Name:      qubes-mgmt-salt-all-yamlscript-users
Version:   %{version}
Release:   1%{?dist}
Summary:   A YAMLScript formula to add system users and or groups
License:   GPL 2.0
URL:	   http://www.qubes-os.org/

Group:     System administration tools
BuildArch: noarch
Requires:  qubes-mgmt-salt
Requires:  qubes-mgmt-salt-all-yamlscript-renderer

%define _builddir %(pwd)

%description
A YAMLScript formula to add system users and or groups.

%prep
# we operate on the current directory, so no need to unpack anything
# symlink is to generate useful debuginfo packages
rm -f %{name}-%{version}
ln -sf . %{name}-%{version}
%setup -T -D

%build

%install
make install DESTDIR=%{buildroot} LIBDIR=%{_libdir} BINDIR=%{_bindir} SBINDIR=%{_sbindir} SYSCONFDIR=%{_sysconfdir}

%post
# Update Salt Configuration
qubesctl state.sls config -l quiet --out quiet > /dev/null || true
qubesctl saltutil.clear_cache -l quiet --out quiet > /dev/null || true
qubesctl saltutil.sync_all refresh=true -l quiet --out quiet > /dev/null || true

# Enable States
#qubesctl top.enable users saltenv=all -l quiet --out quiet > /dev/null || true
#qubesctl top.enable users.sudo saltenv=all -l quiet --out quiet > /dev/null || true

# Enable Pillar States
#qubesctl top.enable users.dom0 saltenv=all pillar=True -l quiet --out quiet > /dev/null || true
#qubesctl top.enable users.vm saltenv=all pillar=True -l quiet --out quiet > /dev/null || true

# Enable Test States
#qubesctl top.enable users saltenv=test -l quiet --out quiet > /dev/null || true

# Enable Test Pillar States
#qubesctl top.enable users saltenv=test pillar=true -l quiet --out quiet > /dev/null || true

%files
%defattr(-,root,root)
%doc LICENSE README.rst
%attr(750, root, root) %dir /srv/formulas/all/users-yamlscript-formula
/srv/formulas/all/users-yamlscript-formula/LICENSE
/srv/formulas/all/users-yamlscript-formula/pillar.example
/srv/formulas/all/users-yamlscript-formula/README.rst
/srv/formulas/all/users-yamlscript-formula/users/init.sls
/srv/formulas/all/users-yamlscript-formula/users/sudo.sls

/srv/formulas/test/users-yamlscript-formula/LICENSE
/srv/formulas/test/users-yamlscript-formula/pillar.example
/srv/formulas/test/users-yamlscript-formula/README.rst
/srv/formulas/test/users-yamlscript-formula/users/default.sls
/srv/formulas/test/users-yamlscript-formula/users/sudo.sls
/srv/formulas/test/users-yamlscript-formula/users/tests.bobby
/srv/formulas/test/users-yamlscript-formula/users/tests.docker
/srv/formulas/test/users-yamlscript-formula/users/tests.mel
/srv/formulas/test/users-yamlscript-formula/users/tests.sudo
/srv/formulas/test/users-yamlscript-formula/users/TODO.txt

%attr(750, root, root) %dir /srv/pillar/all/users
%config(noreplace) /srv/pillar/all/users/dom0.sls
%config(noreplace) /srv/pillar/all/users/vm.sls

%changelog
