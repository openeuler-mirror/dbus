Name:     dbus
Epoch:    1
Version:  1.12.16
Release:  4
Summary:  System Message Bus
License:  AFLv2.1 or GPLv2+
URL:      http://www.freedesktop.org/Software/dbus/
Source0:  https://dbus.freedesktop.org/releases/dbus/%{name}-%{version}.tar.gz
Source1:  00-start-message-bus.sh

Patch9000:  bugfix-let-systemd-restart-dbus-when-the-it-enters-failed.patch

BuildRequires:  systemd-devel expat-devel libselinux-devel audit-libs-devel doxygen xmlto cmake
BuildRequires:  autoconf-archive libtool libX11-devel libcap-ng-devel libxslt

Requires:  systemd libselinux shadow
Requires(pre): shadow

Obsoletes:  %{name}-common %{name}-daemon %{name}-tools %{name}-libs %{name}-x11

Provides:  %{name}-common %{name}-daemon %{name}-tools %{name}-libs %{name}-x11

%description
D-Bus is a message bus system, a simple way for applications to talk to one another.
In addition to interprocess communication, D-Bus helps coordinate process lifecycle;
it makes it simple and reliable to code a "single instance" application or daemon, 
and to launch applications and daemons on demand when their services are needed.

%package devel
Summary: Development files for developers
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release} xml-common

%description devel
This package contains development files for developers.

%package help
Summary: Man pages and other related documents for D-Bus
BuildArch: noarch
Obsoletes: %{name}-doc

%description help
Man pages and other related documents for D-Bus.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%configure \
--disable-static \
--enable-inotify \
--enable-libaudit \
--enable-selinux=yes \
--enable-systemd \
--with-system-socket=%{_localstatedir}/run/dbus/system_bus_socket \
--with-dbus-user=dbus \
--libexecdir=/%{_libexecdir}/dbus-1 \
--enable-user-session \
--docdir=%{_pkgdocdir} \
--enable-doxygen-docs \
--disable-asserts

%make_build V=1

%install
%make_install
install -Dp -m755 %{SOURCE1} %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/00-start-message-bus.sh
install -d $RPM_BUILD_ROOT%{_sysconfdir}/dbus-1/session.d
install -d $RPM_BUILD_ROOT%{_sysconfdir}/dbus-1/system.d
install -d $RPM_BUILD_ROOT%{_datadir}/dbus-1/interfaces
install -d $RPM_BUILD_ROOT%{_localstatedir}/run/dbus
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/dbus

ln -s dbus.service $RPM_BUILD_ROOT%{_unitdir}/messagebus.service

find $RPM_BUILD_ROOT -type f -name "*.la" -delete -print
%check
make check

%pre
# Add the "dbus" user and group
%{_sbindir}/groupadd -r dbus 2>/dev/null || :
%{_sbindir}/useradd -r -c 'D-Bus' -g dbus -s /sbin/nologin -d %{_localstatedir}/run/dbus dbus 2> /dev/null || :


%preun
%systemd_preun dbus.service dbus.socket
%systemd_user_preun dbus.service dbus.socket

%post
%systemd_post dbus.service dbus.socket
%systemd_user_post dbus.service dbus.socket
/sbin/ldconfig

%post devel -p /sbin/ldconfig

%postun
%systemd_postun dbus.service dbus.socket
%systemd_user_postun dbus.service dbus.socket
/sbin/ldconfig

%postun devel -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README
%license COPYING

%dir %{_sysconfdir}/dbus-1
%dir %{_sysconfdir}/dbus-1/session.d
%dir %{_sysconfdir}/dbus-1/system.d
%config %{_sysconfdir}/dbus-1/session.conf
%config %{_sysconfdir}/dbus-1/system.conf
%dir %{_datadir}/dbus-1
%{_datadir}/dbus-1/session.conf
%{_datadir}/dbus-1/system.conf
%{_datadir}/dbus-1/services
%{_datadir}/dbus-1/system-services
%{_datadir}/dbus-1/interfaces
%{_sysusersdir}/dbus.conf

%ghost %dir /run/%{name}
%dir %{_localstatedir}/lib/dbus/
%{_tmpfilesdir}/dbus.conf
%{_unitdir}/dbus.service
%{_unitdir}/dbus.socket
%{_unitdir}/messagebus.service
%{_unitdir}/multi-user.target.wants/dbus.service
%{_unitdir}/sockets.target.wants/dbus.socket
%{_userunitdir}/dbus.service
%{_userunitdir}/dbus.socket
%{_userunitdir}/sockets.target.wants/dbus.socket

%dir %{_libexecdir}/dbus-1
%attr(4750,root,dbus) %{_libexecdir}/dbus-1/dbus-daemon-launch-helper
%{_bindir}/dbus-daemon
%{_bindir}/dbus-cleanup-sockets
%{_bindir}/dbus-run-session
%{_bindir}/dbus-test-tool
%{_bindir}/dbus-send
%{_bindir}/dbus-monitor
%{_bindir}/dbus-update-activation-environment
%{_bindir}/dbus-uuidgen
%{_bindir}/dbus-launch

%{_libdir}/*dbus-1*.so.*
%{_sysconfdir}/X11/xinit/xinitrc.d/00-start-message-bus.sh

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libdbus-1.so
%dir %{_libdir}/dbus-1.0
%{_libdir}/dbus-1.0/include
%{_datadir}/xml/dbus-1
%{_libdir}/cmake/DBus1
%{_libdir}/pkgconfig/dbus-1.pc

%files help
%{_mandir}/man1/dbus-*
%{_pkgdocdir}/*
%exclude %{_pkgdocdir}/AUTHORS
%exclude %{_pkgdocdir}/ChangeLog
%exclude %{_pkgdocdir}/NEWS
%exclude %{_pkgdocdir}/README

%changelog
* Tue Sep 24 2019 openEuler Buildteam <buildteam@openeuler.org> - 1:1.12.16-4
- Add build requires to add runtime requires and add a start-message-bus.sh

* Tue Sep 24 2019 openEuler Buildteam <buildteam@openeuler.org> - 1:1.12.16-3
- Adjust requires 'shadow-utils' to 'shadow'

* Fri Sep 20 2019 openEuler Buildteam <buildteam@openeuler.org> - 1:1.12.16-2
- Modify license 'and' to 'or'

* Thu Aug 29 2019 openEuler Buildteam <buildteam@openeuler.org> - 1:1.12.16-1
- Package init
