%{!?version: %define version %(make get-version)}
%{!?rel: %define rel %(make get-release)}
%{!?package_name: %define package_name %(make get-package_name)}
%{!?package_summary: %define package_summary %(make get-summary)}
%{!?package_description: %define package_description %(make get-description)}

%{!?formula_name: %define formula_name %(make get-formula_name)}
%{!?state_name: %define state_name %(make get-state_name)}
%{!?saltenv: %define saltenv %(make get-saltenv)}
%{!?pillar_dir: %define pillar_dir %(make get-pillar_dir)}
%{!?formula_dir: %define formula_dir %(make get-formula_dir)}

Name:      %{package_name}
Version:   %{version}
Release:   %{rel}%{?dist}
Summary:   %{package_summary}
License:   GPL 2.0
URL:	   http://www.qubes-os.org/

Group:     System administration tools
BuildArch: noarch
Requires:  qubes-mgmt-salt
Requires:  qubes-mgmt-salt-all-yamlscript-renderer

%define _builddir %(pwd)

%description
%{package_description}

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
#qubesctl topd.enable %{state_name} saltenv=%{saltenv} -l quiet --out quiet > /dev/null || true
#qubesctl topd.enable %{state_name}.sudo saltenv=%{saltenv} -l quiet --out quiet > /dev/null || true

# Enable Pillar States
#qubesctl topd.enable %{state_name}.dom0 saltenv=%{saltenv} pillar=True -l quiet --out quiet > /dev/null || true
#qubesctl topd.enable %{state_name}.vm saltenv=%{saltenv} pillar=True -l quiet --out quiet > /dev/null || true

# Enable Test States
#qubesctl topd.enable %{state_name} saltenv=test -l quiet --out quiet > /dev/null || true

# Enable Test Pillar States
#qubesctl topd.enable %{state_name} saltenv=test pillar=true -l quiet --out quiet > /dev/null || true
  
%files
%attr(750, root, root) %dir /srv/formulas/all/users-yamlscript-formula
/srv/formulas/all/users-yamlscript-formula/LICENSE
/srv/formulas/all/users-yamlscript-formula/pillar.example
/srv/formulas/all/users-yamlscript-formula/README.rst
/srv/formulas/all/users-yamlscript-formula/users/init.sls
/srv/formulas/all/users-yamlscript-formula/users/sudo.sls


/srv/formulas/test/users-yamlscript-formula/LICENSE
/srv/formulas/test/users-yamlscript-formula/pillar.example
/srv/formulas/test/users-yamlscript-formula/README.rst
/srv/formulas/test/users-yamlscript-formula/users/init.sls
/srv/formulas/test/users-yamlscript-formula/users/tests.bobby
/srv/formulas/test/users-yamlscript-formula/users/tests.docker
/srv/formulas/test/users-yamlscript-formula/users/tests.mel
/srv/formulas/test/users-yamlscript-formula/users/tests.sudo
/srv/formulas/test/users-yamlscript-formula/users/TODO.txt

%attr(750, root, root) %dir /srv/pillar/all/users
%config(noreplace) /srv/pillar/all/users/dom0.sls
%config(noreplace) /srv/pillar/all/users/vm.sls

%changelog
