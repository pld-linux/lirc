%define		_kernel_ver %(grep UTS_RELEASE %{_kernelsrcdir}/include/linux/version.h 2>/dev/null | cut -d'"' -f2)
%define		smpstr	%{?_with_smp:smp}%{!?_with_smp:up}
%define		smp	%{?_with_smp:1}%{!?_with_smp:0}
# needed because of release macro expansion
%define		_release	1

Summary:	Linux Infrared Remote Control daemons
Summary(pl):	Serwery do zdalnej kontroli Linuxa za pomoc± podczerwieni
Name:		lirc
Version:	0.6.4 
Release:	%{_release}
Source0:	http://download.sourceforge.net/LIRC/%{name}-%{version}.tar.bz2
Source1:	http://www.lirc.org/remotes.tar.gz
Source2:	%{name}.sysconfig
Source3:	%{name}d.init
Source4:	%{name}md.init
Patch0:		%{name}-opt.patch
Patch1:		%{name}-spinlock.patch
Patch2:		%{name}-tmp.patch
Patch3:		%{name}-devfs.patch
License:	GPL
URL:		http://www.lirc.org/
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	kernel-source
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	XFree86-devel
BuildRequires:	egcs
Prereq:		chkconfig
Conflicts:	%{name}-libs < 0.6.3-3
# didn't use /tmp/.lircd

%define		_x11bindir	%{_prefix}/X11R6/bin

%description
LIRC is a package that allows you to decode and send infra-red signals
of many (but not all) commonly used remote controls.

%description -l pl
LIRC to program pozwalaj±cy na dekodowanie nadchodz±cych oraz
wysy≥anie sygna≥Ûw w podczerwieni za pomoc± wielu (ale nie wszystkich)
popularnych urz±dzeÒ do zdalnej kontroli

%package modules-dev
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu≥y j±dra dla zdalnej obs≥ugi Linuxa za pomoc± podczerwieni
Group:		Base/Kernel
Group(de):	Grunds‰tzlich/Kern
Group(pl):	Podstawowe/J±dro
Release:	%{_release}@%{_kernel_ver}%{smpstr}
Prereq:		modutils >= 2.4.6-4
Requires:	dev >= 2.8.0-3
Conflicts:	kernel < %{_kernel_ver}, kernel > %{_kernel_ver}
Conflicts:	kernel-%{?_with_smp:up}%{!?_with_smp:smp}
Requires:	%{name} = %{version}
Obsoletes:	lirc-modules

%description modules-dev
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_dev module.

%description modules-dev -l pl
Ten pakiet zawiera modu≥y j±dra niezbÍdne do obs≥ugi niektÛrych
pilotÛw na podczerwieÒ (w tym tych dostarczanych z kartami TV).

Modu≥ lirc_dev.

%package modules-gpio
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu≥y j±dra dla zdalnej obs≥ugi Linuxa za pomoc± podczerwieni
Group:		Base/Kernel
Group(de):	Grunds‰tzlich/Kern
Group(pl):	Podstawowe/J±dro
Release:	%{_release}@%{_kernel_ver}%{smpstr}
Prereq:		modutils >= 2.4.6-4
Requires:	dev >= 2.8.0-3
Conflicts:	kernel < %{_kernel_ver}, kernel > %{_kernel_ver}
Conflicts:	kernel-%{?_with_smp:up}%{!?_with_smp:smp}
Requires:	%{name} = %{version}
Obsoletes:	lirc-modules

%description modules-gpio
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_gpio module.

%description modules-gpio -l pl
Ten pakiet zawiera modu≥y j±dra niezbÍdne do obs≥ugi niektÛrych
pilotÛw na podczerwieÒ (w tym tych dostarczanych z kartami TV).

Modu≥ lirc_gpio.

%package modules-i2c
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu≥y j±dra dla zdalnej obs≥ugi Linuxa za pomoc± podczerwieni
Group:		Base/Kernel
Group(de):	Grunds‰tzlich/Kern
Group(pl):	Podstawowe/J±dro
Release:	%{_release}@%{_kernel_ver}%{smpstr}
Prereq:		modutils >= 2.4.6-4
Requires:	dev >= 2.8.0-3
Conflicts:	kernel < %{_kernel_ver}, kernel > %{_kernel_ver}
Conflicts:	kernel-%{?_with_smp:up}%{!?_with_smp:smp}
Requires:	%{name} = %{version}
Obsoletes:	lirc-modules

%description modules-i2c
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_i2c module.

%description modules-i2c -l pl
Ten pakiet zawiera modu≥y j±dra niezbÍdne do obs≥ugi niektÛrych
pilotÛw na podczerwieÒ (w tym tych dostarczanych z kartami TV).

Modu≥ lirc_i2c

%package modules-serial
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu≥y j±dra dla zdalnej obs≥ugi Linuxa za pomoc± podczerwieni
Group:		Base/Kernel
Group(de):	Grunds‰tzlich/Kern
Group(pl):	Podstawowe/J±dro
Release:	%{_release}@%{_kernel_ver}%{smpstr}
Prereq:		modutils >= 2.4.6-4
Requires:	dev >= 2.8.0-3
Conflicts:	kernel < %{_kernel_ver}, kernel > %{_kernel_ver}
Conflicts:	kernel-%{?_with_smp:up}%{!?_with_smp:smp}
Requires:	%{name} = %{version}
Obsoletes:	lirc-modules

%description modules-serial
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_serial module for devices connected to serial port.

%description modules-serial -l pl
Ten pakiet zawiera modu≥y j±dra niezbÍdne do obs≥ugi niektÛrych
pilotÛw na podczerwieÒ (w tym tych dostarczanych z kartami TV).

Modu≥ lirc_serial dla urz±dzeÒ pod≥±czanych do serial portu.

%package modules-parallel
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu≥y j±dra dla zdalnej obs≥ugi Linuxa za pomoc± podczerwieni
Group:		Base/Kernel
Group(de):	Grunds‰tzlich/Kern
Group(pl):	Podstawowe/J±dro
Release:	%{_release}@%{_kernel_ver}%{smpstr}
Prereq:		modutils >= 2.4.6-4
Requires:	dev >= 2.8.0-3
Conflicts:	kernel < %{_kernel_ver}, kernel > %{_kernel_ver}
Conflicts:	kernel-%{?_with_smp:up}%{!?_with_smp:smp}
Requires:	%{name} = %{version}
Obsoletes:	lirc-modules

%description modules-parallel
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc-parallel module for devices connected to parallel port.

%description modules-parallel -l pl
Ten pakiet zawiera modu≥y j±dra niezbÍdne do obs≥ugi niektÛrych
pilotÛw na podczerwieÒ (w tym tych dostarczanych z kartami TV).

Modu≥ lirc_parallel  dla urz±dzeÒ pod≥±czanych do portu rÛwnoleg≥ego.

%package modules-sir
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu≥y j±dra dla zdalnej obs≥ugi Linuxa za pomoc± podczerwieni
Group:		Base/Kernel
Group(de):	Grunds‰tzlich/Kern
Group(pl):	Podstawowe/J±dro
Release:	%{_release}@%{_kernel_ver}%{smpstr}
Prereq:		modutils >= 2.4.6-4
Requires:	dev >= 2.8.0-3
Conflicts:	kernel < %{_kernel_ver}, kernel > %{_kernel_ver}
Conflicts:	kernel-%{?_with_smp:up}%{!?_with_smp:smp}
Requires:	%{name} = %{version}
Obsoletes:	lirc-modules

%description modules-sir
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_sir module.

%description modules-sir -l pl
Ten pakiet zawiera modu≥y j±dra niezbÍdne do obs≥ugi niektÛrych
pilotÛw na podczerwieÒ (w tym tych dostarczanych z kartami TV).

Modu≥ lirc_sir.

%package X11
Summary:	Linux Infrared Remote Control - X11 utilities
Summary(pl):	Zdalna kontrola Linuxa za pomoc± podczerwieni - narzÍdzia X11
Group:		X11/Applications
Group(de):	X11/Applikationen
Group(pl):	X11/Aplikacje

%description X11
Linux Infrared Remote Control - X11 utilities.

%description X11 -l pl
Zdalna kontrola Linuxa za pomoc± podczerwieni - narzÍdzia X11.

%package libs
Summary:	LIRC libraries
Summary(pl):	Biblioteki LIRC
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Group(pt_BR):	Bibliotecas
Group(ru):	‚…¬Ã…œ‘≈À…
Group(uk):	‚¶¬Ã¶œ‘≈À…
Conflicts:	%{name} < 0.6.3-3
# didn't use /tmp/.lircd

%description libs
This package provides the libraries necessary to run lirc client
programs.

%description libs -l pl
Ten pakiet zawiera biblioteki niezbÍdne do dzia≥ania klientÛw LIRC.

%package devel
Summary:	Header and library files for LIRC development
Summary(pl):	Pliki nag≥Ûwkowe i biblioteki dla tworzenia programÛw z obs≥ug± LIRC
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Ú¡⁄“¡¬œ‘À¡/‚…¬Ã…œ‘≈À…
Group(uk):	Úœ⁄“œ¬À¡/‚¶¬Ã¶œ‘≈À…
Requires:	%{name}-libs = %{version}

%description devel
This package provides the files necessary to develop LIRC-based
programs.

%description devel -l pl
Ten pakiet zawiera pliki niezbÍdne do tworzenia programÛw opartych na
LIRC.

%package static
Summary:	Static library for LIRC development
Summary(pl):	Biblioteka statyczna LIRC
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Ú¡⁄“¡¬œ‘À¡/‚…¬Ã…œ‘≈À…
Group(uk):	Úœ⁄“œ¬À¡/‚¶¬Ã¶œ‘≈À…
Requires:	%{name}-devel = %{version}

%description static
The files necessary for development of statically-linked lirc-based
programs.

%description static -l pl
Pliki potrzebne do tworzenia ≥±czonych statycznie programÛw opartych
na LIRC.

%package remotes
Summary:	LIRC configuration files for many popular remotes
Summary(pl):	Pliki konfiguracyjne LIRC'a dla wielu popularnych pilotÛw
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
Requires:	%{name}

%description remotes
This package contains LIRC configuraion files for more than 400 
popular remotes.

%description remotes -l pl
Pakiet ten zawiera pliki konfiguracyjne LIRC'a dla ponad 400 
popularnych pilotÛw.

%prep
%setup -q -a 1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
echo '#' > drivers/Makefile.am
rm -f missing
libtoolize --copy --force
aclocal
automake -a -c
autoconf

%configure \
	--with-driver=any \
	--with-kerneldir=%{_kernelsrcdir} \
	--with-x \
	--with-port=0x2f8 \
	--with-irq=3 \
	--without-soft-carrier
%{__make}

%if %{smp}
SMP="-D__KERNEL_SMP=1"
%endif
cd drivers
for drv in lirc_*; do
	kgcc %{rpmcflags} -D__KERNEL__ -DMODULE -DHAVE_CONFIG_H $SMP \
	-DIRCTL_DEV_MAJOR=61 -I.. -I%{_kernelsrcdir}/include \
	-fno-strict-aliasing -fno-common \
	-c -o $drv/$drv.o $drv/$drv.c || true
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT/dev
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{rc.d/init.d,sysconfig}
install -d $RPM_BUILD_ROOT%{_datadir}/lircmd
install -d $RPM_BUILD_ROOT%{_datadir}/lircd
install -d $RPM_BUILD_ROOT%{_x11bindir}
install -d $RPM_BUILD_ROOT%{_aclocaldir}
install -d $RPM_BUILD_ROOT%{_localstatedir}/log
%{__make} install DESTDIR=$RPM_BUILD_ROOT \
	sysconfdir=$RPM_BUILD_ROOT%{_sysconfdir}

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
cp drivers/*/*.o $RPM_BUILD_ROOT/lib/modules/*/misc

# this files would also suit good in "remotes" package
cat remotes/*/lircd.conf.* > $RPM_BUILD_ROOT%{_sysconfdir}/lircd.conf

cp remotes/*/lircmd.conf.* $RPM_BUILD_ROOT%{_datadir}/lircmd
install contrib/*.m4 $RPM_BUILD_ROOT%{_aclocaldir}
mv $RPM_BUILD_ROOT%{_bindir}/{irxevent,xmode2} $RPM_BUILD_ROOT%{_x11bindir}
:> $RPM_BUILD_ROOT%{_localstatedir}/log/lircd

ln -s %{_localstatedir}/state/lircmd.conf $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/lirc
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/lircd
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/lircmd

cd remotes
for dir in *; do
    for file in $dir/!(*.conf.*|*.jpg); do
        if [ -f $file ]; then 
	    cp $file generic/$dir-`basename $file`.conf; 
	fi
    done
done 
cd -

install remotes/generic/*.conf $RPM_BUILD_ROOT%{_datadir}/lircd

gzip -9nf ANNOUNCE AUTHORS NEWS README TODO ChangeLog doc/irxevent.keys
gzip -9nf contrib/lircrc

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post
/sbin/chkconfig --add lircd
if [ -f /var/lock/subsys/lircd ]; then
	/etc/rc.d/init.d/lircd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/lircd start\" to start lircd." >&2
fi
/sbin/chkconfig --add lircmd
if [ -f /var/lock/subsys/lircmd ]; then
	/etc/rc.d/init.d/lircmd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/lircmd start\" to start lircmd." >&2
fi
echo "If you are using a kernel-module-based driver, don't forget to"
echo "install the lirc-modules-<your_driver> package."

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/lircd ]; then
		/etc/rc.d/init.d/lircd stop >&2
	fi
	/sbin/chkconfig --del lircd
fi
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/lircmd ]; then
		/etc/rc.d/init.d/lircmd stop >&2
	fi
	/sbin/chkconfig --del lircmd
fi

%post modules-dev
/sbin/depmod -a
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias char-major-61 lirc_dev' line"
	echo "to your /etc/modules.conf."
fi

%postun modules-dev
/sbin/depmod -a

%post modules-gpio
/sbin/depmod -a
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias char-major-61 lirc_gpio' line"
	echo "to your /etc/modules.conf."
fi

%postun modules-gpio
/sbin/depmod -a

%post modules-i2c
/sbin/depmod -a
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias char-major-61 lirc_i2c' line"
	echo "to your /etc/modules.conf."
fi

%postun modules-i2c
/sbin/depmod -a

%post modules-serial
/sbin/depmod -a
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias char-major-61 lirc_serial' line"
	echo "to your /etc/modules.conf."
fi

%postun modules-serial
/sbin/depmod -a

%post modules-parallel
/sbin/depmod -a
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias char-major-61 lirc_parallel' line"
	echo "to your /etc/modules.conf."
fi

%postun modules-parallel
/sbin/depmod -a

%post modules-sir
/sbin/depmod -a
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias char-major-61 lirc_sir' line"
	echo "to your /etc/modules.conf."
fi

%postun modules-sir
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/*
%config(noreplace) %{_sysconfdir}/*.conf
%ghost %attr(600,root,root) %{_localstatedir}/log/lircd
%doc *.gz remotes/remotes contrib/*.gz
%doc doc/*.gz doc/doc.html doc/html doc/images

%files remotes
%{_datadir}/lircmd
%{_datadir}/lircd

%files modules-dev
%defattr(644,root,root,755)
/lib/modules/*/*/lirc_dev*

%files modules-gpio
%defattr(644,root,root,755)
/lib/modules/*/*/lirc_gpio*

%files modules-i2c
%defattr(644,root,root,755)
/lib/modules/*/*/lirc_i2c*

%files modules-serial
%defattr(644,root,root,755)
/lib/modules/*/*/lirc_serial*

%files modules-parallel
%defattr(644,root,root,755)
/lib/modules/*/*/lirc_parallel*

%files modules-sir
%defattr(644,root,root,755)
/lib/modules/*/*/lirc_sir*

%files X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_x11bindir}/*

%files libs
%defattr(644,root,root,755)
%{_libdir}/*.so.*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/lirc
%{_aclocaldir}/*
%attr(755,root,root) %{_libdir}/*.so
%attr(755,root,root) %{_libdir}/*.la

%files static
%defattr(644,root,root,755)
%{_libdir}/*a

%clean
rm -rf $RPM_BUILD_ROOT
