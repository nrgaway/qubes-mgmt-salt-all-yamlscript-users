%{!?version: %define version %(cat version)}
%{!?rel: %define rel %(cat rel)}
%{!?formula_name: %define formula_name %(cat formula_name)}

Name:      qubes-mgmt-salt-base-yamlscript-users
Version:   %{version}
Release:   %{rel}%{?dist}
Summary:   A YAMLScript formula to add system users and or groups
License:   GPL 2.0
URL:	   http://www.qubes-os.org/

Group:     System administration tools
BuildArch: noarch
Requires:  qubes-mgmt-salt-config
Requires:  qubes-mgmt-salt-base-yamlscript-renderer

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
mkdir -p /srv/pillar/dom0/qubes
mkdir -p /srv/pillar/vm/qubes
ln -sf /srv/formulas/base/users-yamlscript-formula/pillar/qubes/users-dom0.sls /srv/pillar/dom0/qubes/users.sls
ln -sf /srv/formulas/base/users-yamlscript-formula/pillar/qubes/users-vm.sls /srv/pillar/vm/qubes/users.sls

%files
%defattr(-,root,root)
%attr(750, root, root) %dir /srv/formulas/base/%{formula_name}
/srv/formulas/base/%{formula_name}/*

%changelog
