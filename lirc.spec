# TODO
# - regenerate plugindocs index when installing plugin with plugindocs
# - separate lirc-remotes.spec, update remotes configs from lirc-remotes project
#   (http://lirc-remotes.sourceforge.net/ incl. remotes-table.html)
#
# Conditional build:
%bcond_without	portaudio	# Portaudio based audio driver
%bcond_without	static_libs	# static libraries
%bcond_without	x		# without X11-based utilitied

Summary:	Linux Infrared Remote Control daemons
Summary(pl.UTF-8):	Demony do zdalnego sterowania Linuksem za pomocą podczerwieni
Name:		lirc
Version:	0.10.1
Release:	2
License:	GPL v2+
Group:		Daemons
Source0:	http://downloads.sourceforge.net/lirc/%{name}-%{version}.tar.bz2
# Source0-md5:	86c3f8e4efaba10571addb8313d1e040
Source1:	http://lirc.sourceforge.net/remotes.tar.bz2
# Source1-md5:	238d1773d3c405acc02813674f5a55f8
Source2:	%{name}d.sysconfig
Source3:	%{name}d.init
Source4:	%{name}md.init
Source5:	%{name}.tmpfiles
Patch0:		%{name}-tmp.patch
Patch1:		%{name}-remotes.patch
Patch2:		%{name}-link.patch
URL:		http://www.lirc.org/
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	libftdi1-devel >= 1.0
BuildRequires:	libtool >= 2:2
BuildRequires:	libusb-compat-devel >= 0.1.0
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
%{?with_portaudio:BuildRequires:	portaudio-devel >= 19}
BuildRequires:	python3 >= 1:3.5
BuildRequires:	python3-PyYAML
BuildRequires:	rpmbuild(macros) >= 1.701
BuildRequires:	rpm-pythonprov
BuildRequires:	systemd-devel
BuildRequires:	udev-devel
%{?with_x:BuildRequires:	xorg-lib-libX11-devel}
Requires(post,preun):	/sbin/chkconfig
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libftdi1 >= 1.0
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# liblirc_driver expects curr_driver to be defined by user
%define		skip_post_check_so	liblirc_driver.so.*

%description
LIRC is a package that allows you to decode and send infra-red signals
of many (but not all) commonly used remote controls.

%description -l pl.UTF-8
LIRC to program pozwalający na dekodowanie nadchodzących oraz
wysyłanie sygnałów w podczerwieni za pomocą wielu (ale nie wszystkich)
popularnych urządzeń do zdalnego sterowania.

%package remotes
Summary:	Lirc remotes database
Summary(pl.UTF-8):	Baza pilotów obsługiwanych przez lirc
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description remotes
This package contains configuration files for many remotes supported
by lirc.

%description remotes -l pl.UTF-8
Ten pakiet zawiera pliki konfiguracyjne dla wielu pilotów
obsługiwanych przez lirc.

%package X11
Summary:	Linux Infrared Remote Control - X11 utilities
Summary(pl.UTF-8):	Zdalne sterowanie Linuksem za pomocą podczerwieni - narzędzia X11
Group:		X11/Applications
Requires:	%{name}-libs = %{version}-%{release}

%description X11
Linux Infrared Remote Control - X11 utilities.

%description X11 -l pl.UTF-8
Zdalne sterowanie Linuksem za pomocą podczerwieni - narzędzia X11.

%package libs
Summary:	LIRC libraries
Summary(pl.UTF-8):	Biblioteki LIRC
Group:		Libraries
Obsoletes:	lirc-svga
# didn't use /tmp/.lircd
Conflicts:	lirc < 0.6.3-3

%description libs
This package provides the libraries necessary to run lirc client
programs.

%description libs -l pl.UTF-8
Ten pakiet zawiera biblioteki niezbędne do działania klientów LIRC.

%package devel
Summary:	Header files for LIRC development
Summary(pl.UTF-8):	Pliki nagłówkowe do tworzenia programów z obsługą LIRC
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package provides the files necessary to develop LIRC-based
programs.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki niezbędne do tworzenia programów opartych na
LIRC.

%package static
Summary:	Static library for LIRC development
Summary(pl.UTF-8):	Biblioteka statyczna LIRC
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
The files necessary for development of statically-linked lirc-based
programs.

%description static -l pl.UTF-8
Pliki potrzebne do tworzenia łączonych statycznie programów opartych
na LIRC.

%package doc
Summary:	Documentation for LIRC
Summary(pl.UTF-8):	Dokumentacja LIRC-a
Group:		Documentation

%description doc
Documentation for LIRC.

%description doc -l pl.UTF-8
Dokumentacja LIRC-a.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}

%configure \
	%{!?with_portaudio:ac_cv_header_portaudio_h=no} \
	am_cv_python_pythondir=%{py3_sitescriptdir} \
	--enable-devinput \
	%{?with_static_libs:--enable-static} \
	--enable-uinput \
	%{?with_x:--with-x}

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},/dev,/var/{log,run/lirc}} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,lirc} \
	$RPM_BUILD_ROOT%{systemdtmpfilesdir}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

:> $RPM_BUILD_ROOT/var/log/lircd

cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/lircd
install -p %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/lircd
install -p %{SOURCE4} $RPM_BUILD_ROOT/etc/rc.d/init.d/lircmd
cp -p %{SOURCE5} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lirc/plugins/*.la \
	$RPM_BUILD_ROOT%{py3_sitedir}/lirc/_client.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lirc/plugins/*.a \
	$RPM_BUILD_ROOT%{py3_sitedir}/lirc/_client.a
%endif

# nothing useful
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/lirc/contrib
# dist packages
%{__rm} $RPM_BUILD_ROOT%{_datadir}/lirc/lirc-%{version}.tar.gz
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/lirc/python-pkg
# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/lirc/lircd.conf.d/README.conf.d
# useless
%{__rm} $RPM_BUILD_ROOT%{_docdir}/lirc/VERSION
# packaged as %doc in -X11 package
%{__rm} $RPM_BUILD_ROOT%{_docdir}/lirc/irxevent.keys

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post
/sbin/chkconfig --add lircd
/sbin/chkconfig --add lircmd
%service lircd restart
%service lircmd restart

%preun
if [ "$1" = "0" ]; then
	%service lircd stop
	%service lircmd stop
	/sbin/chkconfig --del lircd
	/sbin/chkconfig --del lircmd
fi

%triggerpostun -- %{name} < 0.8.6-8
if [ -f %{_sysconfdir}/lircd.conf.rpmsave ]; then
	mv -f %{_sysconfdir}/lircd.conf.rpmsave %{_sysconfdir}/lirc/lircd.conf
fi
if [ -f %{_sysconfdir}/lircmd.conf.rpmsave ]; then
	mv -f %{_sysconfdir}/lircmd.conf.rpmsave %{_sysconfdir}/lirc/lircmd.conf
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README README.conf.d contrib/lircrc
%attr(755,root,root) %{_bindir}/ircat
%attr(755,root,root) %{_bindir}/irexec
%attr(755,root,root) %{_bindir}/irpipe
%attr(755,root,root) %{_bindir}/irpty
%attr(755,root,root) %{_bindir}/irrecord
%attr(755,root,root) %{_bindir}/irsend
%attr(755,root,root) %{_bindir}/irsimreceive
%attr(755,root,root) %{_bindir}/irsimsend
%attr(755,root,root) %{_bindir}/irtestcase
%attr(755,root,root) %{_bindir}/irtext2udp
%attr(755,root,root) %{_bindir}/irw
%attr(755,root,root) %{_bindir}/lirc-config-tool
%attr(755,root,root) %{_bindir}/lirc-init-db
%attr(755,root,root) %{_bindir}/lirc-lsremotes
%attr(755,root,root) %{_bindir}/lirc-make-devinput
%attr(755,root,root) %{_bindir}/lircrcd
%attr(755,root,root) %{_bindir}/mode2
%attr(755,root,root) %{_bindir}/pronto2lirc
%attr(755,root,root) %{_sbindir}/lirc-lsplugins
%attr(755,root,root) %{_sbindir}/lircd
%attr(755,root,root) %{_sbindir}/lircd-setup
%attr(755,root,root) %{_sbindir}/lircd-uinput
%attr(755,root,root) %{_sbindir}/lircmd
%dir %{_libdir}/lirc
%dir %{_libdir}/lirc/plugins
%attr(755,root,root) %{_libdir}/lirc/plugins/accent.so
%attr(755,root,root) %{_libdir}/lirc/plugins/alsa_usb.so
%attr(755,root,root) %{_libdir}/lirc/plugins/atilibusb.so
%attr(755,root,root) %{_libdir}/lirc/plugins/atwf83.so
%{?with_portaudio:%attr(755,root,root) %{_libdir}/lirc/plugins/audio.so}
%attr(755,root,root) %{_libdir}/lirc/plugins/audio_alsa.so
%attr(755,root,root) %{_libdir}/lirc/plugins/awlibusb.so
%attr(755,root,root) %{_libdir}/lirc/plugins/bte.so
%attr(755,root,root) %{_libdir}/lirc/plugins/commandir.so
%attr(755,root,root) %{_libdir}/lirc/plugins/creative.so
%attr(755,root,root) %{_libdir}/lirc/plugins/creative_infracd.so
%attr(755,root,root) %{_libdir}/lirc/plugins/default.so
%attr(755,root,root) %{_libdir}/lirc/plugins/devinput.so
%attr(755,root,root) %{_libdir}/lirc/plugins/dfclibusb.so
%attr(755,root,root) %{_libdir}/lirc/plugins/dsp.so
%attr(755,root,root) %{_libdir}/lirc/plugins/ea65.so
%attr(755,root,root) %{_libdir}/lirc/plugins/file.so
%attr(755,root,root) %{_libdir}/lirc/plugins/ftdi.so
%attr(755,root,root) %{_libdir}/lirc/plugins/girs.so
%attr(755,root,root) %{_libdir}/lirc/plugins/hiddev.so
%attr(755,root,root) %{_libdir}/lirc/plugins/i2cuser.so
%attr(755,root,root) %{_libdir}/lirc/plugins/irlink.so
%attr(755,root,root) %{_libdir}/lirc/plugins/irtoy.so
%attr(755,root,root) %{_libdir}/lirc/plugins/livedrive_midi.so
%attr(755,root,root) %{_libdir}/lirc/plugins/livedrive_seq.so
%attr(755,root,root) %{_libdir}/lirc/plugins/logitech.so
%attr(755,root,root) %{_libdir}/lirc/plugins/mouseremote.so
%attr(755,root,root) %{_libdir}/lirc/plugins/mp3anywhere.so
%attr(755,root,root) %{_libdir}/lirc/plugins/mplay.so
%attr(755,root,root) %{_libdir}/lirc/plugins/pcmak.so
%attr(755,root,root) %{_libdir}/lirc/plugins/pinsys.so
%attr(755,root,root) %{_libdir}/lirc/plugins/pixelview.so
%attr(755,root,root) %{_libdir}/lirc/plugins/silitek.so
%attr(755,root,root) %{_libdir}/lirc/plugins/srm7500libusb.so
%attr(755,root,root) %{_libdir}/lirc/plugins/tira.so
%attr(755,root,root) %{_libdir}/lirc/plugins/udp.so
%attr(755,root,root) %{_libdir}/lirc/plugins/uirt2.so
%attr(755,root,root) %{_libdir}/lirc/plugins/uirt2_raw.so
%attr(755,root,root) %{_libdir}/lirc/plugins/usbx.so
%attr(755,root,root) %{_libdir}/lirc/plugins/zotac.so
%attr(754,root,root) /etc/rc.d/init.d/lircd
%attr(754,root,root) /etc/rc.d/init.d/lircmd
%{systemdunitdir}/irexec.service
%{systemdunitdir}/lircd.service
%{systemdunitdir}/lircd.socket
%{systemdunitdir}/lircd-setup.service
%{systemdunitdir}/lircd-uinput.service
%{systemdunitdir}/lircmd.service
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/lircd
%dir %{_sysconfdir}/lirc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lirc/irexec.lircrc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lirc/lirc_options.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lirc/lircd.conf
%{_sysconfdir}/lirc/lircd.conf.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lirc/lircmd.conf
%dir %{_datadir}/lirc
%{_datadir}/lirc/configs
%{_datadir}/lirc/lirc.hwdb
%dir %{_docdir}/lirc
%dir %{_docdir}/lirc/plugindocs
%{_mandir}/man1/ircat.1*
%{_mandir}/man1/irexec.1*
%{_mandir}/man1/irpipe.1*
%{_mandir}/man1/irpty.1*
%{_mandir}/man1/irrecord.1*
%{_mandir}/man1/irsend.1*
%{_mandir}/man1/irsimreceive.1*
%{_mandir}/man1/irsimsend.1*
%{_mandir}/man1/irtestcase.1*
%{_mandir}/man1/irtext2udp.1*
%{_mandir}/man1/irw.1*
%{_mandir}/man1/lirc-config-tool.1*
%{_mandir}/man1/lirc-lsplugins.1*
%{_mandir}/man1/lirc-lsremotes.1*
%{_mandir}/man1/lirc-make-devinput.1*
%{_mandir}/man1/mode2.1*
%{_mandir}/man1/pronto2lirc.1*
%{_mandir}/man5/lircd.conf.5*
%{_mandir}/man5/lircrc.5*
%{_mandir}/man8/lircd.8*
%{_mandir}/man8/lircd-setup.8*
%{_mandir}/man8/lircd-uinput.8*
%{_mandir}/man8/lircmd.8*
%{_mandir}/man8/lircrcd.8*
%attr(600,root,root) %ghost /var/log/lircd
%dir /var/run/lirc
%{systemdtmpfilesdir}/%{name}.conf

%attr(755,root,root) %{_bindir}/irdb-get
%attr(755,root,root) %{_bindir}/lirc-setup
%{_mandir}/man1/irdb-get.1*
%{_mandir}/man1/lirc-setup.1*

%dir %{py3_sitedir}/lirc
%{py3_sitedir}/lirc/__pycache__
%{py3_sitedir}/lirc/*.py
%attr(755,root,root) %{py3_sitedir}/lirc/_client.so

%dir %{py3_sitedir}/lirc-setup
%{py3_sitedir}/lirc-setup/__pycache__
%{py3_sitedir}/lirc-setup/*.py
%{py3_sitedir}/lirc-setup/configs
%{py3_sitedir}/lirc-setup/lirc-setup
%{py3_sitedir}/lirc-setup/lirc-setup.ui

%files remotes
%defattr(644,root,root,755)
# XXX: are jpegs in docs (remotes) a good idea?
%doc remotes

%if %{with x}
%files X11
%defattr(644,root,root,755)
%doc doc/irxevent.keys
%attr(755,root,root) %{_bindir}/irxevent
%attr(755,root,root) %{_bindir}/xmode2
%{_mandir}/man1/irxevent.1*
%{_mandir}/man1/xmode2.1*
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libirrecord.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libirrecord.so.0
%attr(755,root,root) %{_libdir}/liblirc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblirc.so.0
%attr(755,root,root) %{_libdir}/liblirc_client.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblirc_client.so.0
%attr(755,root,root) %{_libdir}/liblirc_driver.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblirc_driver.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libirrecord.so
%attr(755,root,root) %{_libdir}/liblirc.so
%attr(755,root,root) %{_libdir}/liblirc_client.so
%attr(755,root,root) %{_libdir}/liblirc_driver.so
%{_libdir}/libirrecord.la
%{_libdir}/liblirc.la
%{_libdir}/liblirc_client.la
%{_libdir}/liblirc_driver.la
%{_includedir}/lirc
%{_includedir}/lirc_client.h
%{_includedir}/lirc_driver.h
%{_includedir}/lirc_private.h
%{_pkgconfigdir}/lirc.pc
%{_pkgconfigdir}/lirc-driver.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libirrecord.a
%{_libdir}/liblirc.a
%{_libdir}/liblirc_client.a
%{_libdir}/liblirc_driver.a

%files doc
%defattr(644,root,root,755)
%dir %{_docdir}/lirc
%{_docdir}/lirc/html
%{_docdir}/lirc/images
%{_docdir}/lirc/lirc.org
%dir %{_docdir}/lirc/plugindocs
%{_docdir}/lirc/plugindocs/README
%{_docdir}/lirc/plugindocs/Makefile
%{_docdir}/lirc/plugindocs/lirc.css
%attr(755,root,root) %{_docdir}/lirc/plugindocs/make-ext-driver-toc.sh
%{_docdir}/lirc/plugindocs/*.tmpl
%{_docdir}/lirc/plugindocs/*.xsl
%{_docdir}/lirc/plugindocs/var
# upstream decided to use /var because index can be regenerated after adding more plugins docs
%dir /var/lib/lirc
/var/lib/lirc/images
%dir /var/lib/lirc/plugins
# can be regenerated
%verify(not md5 mtime size) /var/lib/lirc/plugins/index.html
/var/lib/lirc/plugins/lirc.css
