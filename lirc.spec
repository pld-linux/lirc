#
# Conditional build:
# _without_dist_kernel	- without sources of distribution kernel
# _without_modules	- build only library+programs, no kernel modules
# _without_x		- without XFree support	
#
%define		_kernel24	%(echo %{_kernel_ver} | grep -q '2\.[012]\.' ; echo $?)
# needed because of release macro expansion

Summary:	Linux Infrared Remote Control daemons
Summary(pl):	Serwery do zdalnej kontroli Linuksa za pomoc� podczerwieni
Name:		lirc
Version:	0.6.6
%define _rel	1
Release:	%{_rel}
License:	GPL
Group:		Daemons
Source0:	http://dl.sourceforge.net/lirc/%{name}-%{version}.tar.bz2
# Source0-md5: 6e7b5ba2fd479961d067730e16df7c54
Source1:	http://lirc.sourceforge.net/remotes.tar.bz2
# Source1-md5: ab33d57db1fc5782c209d90be8c6962e
Source2:	%{name}d.sysconfig
Source3:	%{name}d.init
Source4:	%{name}md.init
Patch0:		%{name}-opt.patch
Patch1:		%{name}-tmp.patch
Patch2:		%{name}-devfs.patch
Patch3:		%{name}-no-svgalib.patch
Patch4:		%{name}-alpha.patch
Patch5:		%{name}-makpc.patch
Patch6:		%{name}-udp.patch
URL:		http://www.lirc.org/
%{!?_without_x:BuildRequires:	XFree86-devel}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
%{!?_without_dist_kernel:BuildRequires:	kernel-headers}
%{!?_without_dist_kernel:%{!?_without_modules:BuildRequires:	kernel-source}}
BuildRequires:	%{kgcc_package}
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	%{name}-libs < 0.6.3-3

%description
LIRC is a package that allows you to decode and send infra-red signals
of many (but not all) commonly used remote controls.

%description -l pl
LIRC to program pozwalaj�cy na dekodowanie nadchodz�cych oraz
wysy�anie sygna��w w podczerwieni za pomoc� wielu (ale nie wszystkich)
popularnych urz�dze� do zdalnej kontroli

%package -n kernel-char-lirc-dev
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu�y j�dra dla zdalnej obs�ugi Linuksa za pomoc� podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_up}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-dev

%description -n kernel-char-lirc-dev
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_dev module.

%description -n kernel-char-lirc-dev -l pl
Ten pakiet zawiera modu�y j�dra niezb�dne do obs�ugi niekt�rych
pilot�w na podczerwie� (w tym tych dostarczanych z kartami TV).

Modu� lirc_dev.

%package -n kernel-char-lirc-gpio
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu�y j�dra dla zdalnej obs�ugi Linuksa za pomoc� podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_up}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}
Requires:	kernel-char-lirc-dev = %{version}
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-gpio

%description -n kernel-char-lirc-gpio
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_gpio module.

%description -n kernel-char-lirc-gpio -l pl
Ten pakiet zawiera modu�y j�dra niezb�dne do obs�ugi niekt�rych
pilot�w na podczerwie� (w tym tych dostarczanych z kartami TV).

Modu� lirc_gpio.

%package -n kernel-char-lirc-i2c
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu�y j�dra dla zdalnej obs�ugi Linuksa za pomoc� podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_up}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}
Requires:	kernel-char-lirc-dev = %{version}
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-i2c

%description -n kernel-char-lirc-i2c
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_i2c module.

%description -n kernel-char-lirc-i2c -l pl
Ten pakiet zawiera modu�y j�dra niezb�dne do obs�ugi niekt�rych
pilot�w na podczerwie� (w tym tych dostarczanych z kartami TV).

Modu� lirc_i2c

%package -n kernel-char-lirc-serial
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu�y j�dra dla zdalnej obs�ugi Linuksa za pomoc� podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_up}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-serial

%description -n kernel-char-lirc-serial
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_serial module for devices connected to serial port.

%description -n kernel-char-lirc-serial -l pl
Ten pakiet zawiera modu�y j�dra niezb�dne do obs�ugi niekt�rych
pilot�w na podczerwie� (w tym tych dostarczanych z kartami TV).

Modu� lirc_serial dla urz�dze� pod��czanych do serial portu.

%package -n kernel-char-lirc-parallel
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu�y j�dra dla zdalnej obs�ugi Linuksa za pomoc� podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_up}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-parallel

%description -n kernel-char-lirc-parallel
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc-parallel module for devices connected to parallel port.

%description -n kernel-char-lirc-parallel -l pl
Ten pakiet zawiera modu�y j�dra niezb�dne do obs�ugi niekt�rych
pilot�w na podczerwie� (w tym tych dostarczanych z kartami TV).

Modu� lirc_parallel dla urz�dze� pod��czanych do portu r�wnoleg�ego.

%package -n kernel-char-lirc-sir
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu�y j�dra dla zdalnej obs�ugi Linuksa za pomoc� podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_up}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-sir

%description -n kernel-char-lirc-sir
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_sir module.

%description -n kernel-char-lirc-sir -l pl
Ten pakiet zawiera modu�y j�dra niezb�dne do obs�ugi niekt�rych
pilot�w na podczerwie� (w tym tych dostarczanych z kartami TV).

Modu� lirc_sir.

%package -n kernel-smp-char-lirc-dev
Summary:	SMP kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu�y j�dra SMP dla zdalnej obs�ugi Linuksa za pomoc� podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-dev

%description -n kernel-smp-char-lirc-dev
This package contains the SMP kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_dev module.

%description -n kernel-smp-char-lirc-dev -l pl
Ten pakiet zawiera modu�y j�dra SMP niezb�dne do obs�ugi niekt�rych
pilot�w na podczerwie� (w tym tych dostarczanych z kartami TV).

Modu� lirc_dev.

%package -n kernel-smp-char-lirc-gpio
Summary:	SMP kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu�y j�dra dla zdalnej obs�ugi Linuksa za pomoc� podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}
Requires:	kernel-smp-char-lirc-dev = %{version}
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-gpio

%description -n kernel-smp-char-lirc-gpio
This package contains the SMP kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_gpio module.

%description -n kernel-smp-char-lirc-gpio -l pl
Ten pakiet zawiera modu�y j�dra SMP niezb�dne do obs�ugi niekt�rych
pilot�w na podczerwie� (w tym tych dostarczanych z kartami TV).

Modu� lirc_gpio.

%package -n kernel-smp-char-lirc-i2c
Summary:	SMP kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu�y j�dra SMP dla zdalnej obs�ugi Linuksa za pomoc� podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}
Requires:	kernel-smp-char-lirc-dev = %{version}
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-i2c

%description -n kernel-smp-char-lirc-i2c
This package contains the SMP kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_i2c module.

%description -n kernel-smp-char-lirc-i2c -l pl
Ten pakiet zawiera modu�y j�dra SMP niezb�dne do obs�ugi niekt�rych
pilot�w na podczerwie� (w tym tych dostarczanych z kartami TV).

Modu� lirc_i2c

%package -n kernel-smp-char-lirc-serial
Summary:	SMP kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu�y j�dra SMP dla zdalnej obs�ugi Linuksa za pomoc� podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-serial

%description -n kernel-smp-char-lirc-serial
This package contains the SMP kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_serial module for devices connected to serial port.

%description -n kernel-smp-char-lirc-serial -l pl
Ten pakiet zawiera modu�y j�dra SMP niezb�dne do obs�ugi niekt�rych
pilot�w na podczerwie� (w tym tych dostarczanych z kartami TV).

Modu� lirc_serial dla urz�dze� pod��czanych do serial portu.

%package -n kernel-smp-char-lirc-parallel
Summary:	SMP kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu�y j�dra SMP dla zdalnej obs�ugi Linuksa za pomoc� podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-parallel

%description -n kernel-smp-char-lirc-parallel
This package contains the SMP kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc-parallel module for devices connected to parallel port.

%description -n kernel-char-lirc-parallel -l pl
Ten pakiet zawiera modu�y j�dra SMP niezb�dne do obs�ugi niekt�rych
pilot�w na podczerwie� (w tym tych dostarczanych z kartami TV).

Modu� lirc_parallel dla urz�dze� pod��czanych do portu r�wnoleg�ego.

%package -n kernel-smp-char-lirc-sir
Summary:	SMP kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu�y j�dra dla zdalnej obs�ugi Linuksa za pomoc� podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-sir

%description -n kernel-smp-char-lirc-sir
This package contains the SMP kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_sir module.

%description -n kernel-smp-char-lirc-sir -l pl
Ten pakiet zawiera modu�y j�dra SMP niezb�dne do obs�ugi niekt�rych
pilot�w na podczerwie� (w tym tych dostarczanych z kartami TV).

Modu� lirc_sir.

%package X11
Summary:	Linux Infrared Remote Control - X11 utilities
Summary(pl):	Zdalna kontrola Linuksa za pomoc� podczerwieni - narz�dzia X11
Group:		X11/Applications

%description X11
Linux Infrared Remote Control - X11 utilities.

%description X11 -l pl
Zdalna kontrola Linuksa za pomoc� podczerwieni - narz�dzia X11.

%package libs
Summary:	LIRC libraries
Summary(pl):	Biblioteki LIRC
Group:		Libraries
Conflicts:	%{name} < 0.6.3-3
# didn't use /tmp/.lircd

%description libs
This package provides the libraries necessary to run lirc client
programs.

%description libs -l pl
Ten pakiet zawiera biblioteki niezb�dne do dzia�ania klient�w LIRC.

%package devel
Summary:	Header and library files for LIRC development
Summary(pl):	Pliki nag��wkowe i biblioteki dla tworzenia program�w z obs�ug� LIRC
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}

%description devel
This package provides the files necessary to develop LIRC-based
programs.

%description devel -l pl
Ten pakiet zawiera pliki niezb�dne do tworzenia program�w opartych na
LIRC.

%package static
Summary:	Static library for LIRC development
Summary(pl):	Biblioteka statyczna LIRC
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
The files necessary for development of statically-linked lirc-based
programs.

%description static -l pl
Pliki potrzebne do tworzenia ��czonych statycznie program�w opartych
na LIRC.

%prep
%setup -q -a 1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
echo '#' > drivers/Makefile.am
rm -f missing
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoconf}

%configure \
	--with-driver=any \
	--with-kerneldir=%{_kernelsrcdir} \
	%{!?_without_x:--with-x }\
	--with-port=0x2f8 \
	--with-irq=3 \
	--without-soft-carrier
%{__make}

%if %{_kernel24}
# 2.4 drivers
LIRC_NORMAL="lirc_gpio lirc_i2c lirc_serial lirc_sir"
LIRC_SYMTAB="lirc_dev"
%else
# 2.2 drivers
LIRC_NORMAL="lirc_serial lirc_sir"
LIRC_SYMTAB=""
%endif

%if 0%{!?_without_modules:1}
cd drivers

# lirc_parallel is not smp safe

# UP

if [ -n "$LIRC_NORMAL" ]; then
  for drv in $LIRC_NORMAL lirc_parallel; do
	%{kgcc} %{rpmcflags} -D__KERNEL__ -DMODULE -DHAVE_CONFIG_H \
	-DIRCTL_DEV_MAJOR=61 -I.. -I%{_kernelsrcdir}/include \
	-fno-strict-aliasing -fno-common \
	-c -o $drv.o $drv/$drv.c
  done
fi

if [ -n "$LIRC_SYMTAB" ]; then
  for drv in $LIRC_SYMTAB; do
	%{kgcc} %{rpmcflags} -D__KERNEL__ -DMODULE -DHAVE_CONFIG_H \
	-DEXPORT_SYMTAB \
	-DIRCTL_DEV_MAJOR=61 -I.. -I%{_kernelsrcdir}/include \
	-fno-strict-aliasing -fno-common \
	-c -o $drv.o $drv/$drv.c
  done
fi

# SMP
if [ -n "$LIRC_NORMAL" ]; then
  for drv in $LIRC_NORMAL; do
	%{kgcc} %{rpmcflags} -D__KERNEL__ -DMODULE -DHAVE_CONFIG_H \
	-D__KERNEL_SMP=1 -DIRCTL_DEV_MAJOR=61 -I.. -I%{_kernelsrcdir}/include \
	-fno-strict-aliasing -fno-common \
	-c -o $drv/$drv.o $drv/$drv.c
  done
fi

if [ -n "$LIRC_SYMTAB" ]; then
  for drv in $LIRC_SYMTAB; do
	%{kgcc} %{rpmcflags} -D__KERNEL__ -DMODULE -DHAVE_CONFIG_H \
	-D__KERNEL_SMP=1 -DEXPORT_SYMTAB \
	-DIRCTL_DEV_MAJOR=61 -I.. -I%{_kernelsrcdir}/include \
	-fno-strict-aliasing -fno-common \
	-c -o $drv/$drv.o $drv/$drv.c
  done
fi
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT/dev
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{rc.d/init.d,sysconfig}
install -d $RPM_BUILD_ROOT%{_aclocaldir}
install -d $RPM_BUILD_ROOT%{_localstatedir}/log
%{__make} install DESTDIR=$RPM_BUILD_ROOT \
	sysconfdir=$RPM_BUILD_ROOT%{_sysconfdir}

%if 0%{!?_without_modules:1}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
cp -f drivers/*.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
cp -f drivers/*/*.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc
%endif

cat>$RPM_BUILD_ROOT%{_sysconfdir}/lircd.conf<<END
#
# This is a placeholder for your configuration file.
# See %{_docdir}/%{name}-%{version}/remotes for some examples.
#
END
cp -f $RPM_BUILD_ROOT%{_sysconfdir}/lirc{,m}d.conf
install contrib/*.m4 $RPM_BUILD_ROOT%{_aclocaldir}
:> $RPM_BUILD_ROOT%{_localstatedir}/log/lircd

install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/lircd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/lircd
install %{SOURCE4} $RPM_BUILD_ROOT/etc/rc.d/init.d/lircmd

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

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
echo "install the kernel-char-lirc-<your_driver> or"
echo "kernel-smp-char-lirc-<your_driver> package."

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

%post	-n kernel-char-lirc-dev
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}

%postun -n kernel-char-lirc-dev
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}

%post	-n kernel-char-lirc-gpio
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_gpio' line"
	echo "to your /etc/modules.conf."
fi

%postun -n kernel-char-lirc-gpio
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}

%post	-n kernel-char-lirc-i2c
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_i2c' line"
	echo "to your /etc/modules.conf."
fi

%postun -n kernel-char-lirc-i2c
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}

%post	-n kernel-char-lirc-serial
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_serial' line"
	echo "to your /etc/modules.conf."
fi

%postun -n kernel-char-lirc-serial
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}

%post	-n kernel-char-lirc-parallel
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_parallel' line"
	echo "to your /etc/modules.conf."
fi

%postun -n kernel-char-lirc-parallel
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}

%post	-n kernel-char-lirc-sir
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_sir' line"
	echo "to your /etc/modules.conf."
fi

%postun -n kernel-char-lirc-sir
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}

%post	-n kernel-smp-char-lirc-dev
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver}smp }%{_kernel_ver}smp

%postun -n kernel-smp-char-lirc-dev
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver}smp }%{_kernel_ver}smp

%post	-n kernel-smp-char-lirc-gpio
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver}smp }%{_kernel_ver}smp
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_gpio' line"
	echo "to your /etc/modules.conf."
fi

%postun -n kernel-smp-char-lirc-gpio
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver}smp }%{_kernel_ver}smp

%post	-n kernel-smp-char-lirc-i2c
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver}smp }%{_kernel_ver}smp
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_i2c' line"
	echo "to your /etc/modules.conf."
fi

%postun -n kernel-smp-char-lirc-i2c
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver}smp }%{_kernel_ver}smp

%post	-n kernel-smp-char-lirc-serial
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver}smp }%{_kernel_ver}smp
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_serial' line"
	echo "to your /etc/modules.conf."
fi

%postun -n kernel-smp-char-lirc-serial
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver}smp }%{_kernel_ver}smp

%post -n kernel-smp-char-lirc-parallel
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver}smp }%{_kernel_ver}smp
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_parallel' line"
	echo "to your /etc/modules.conf."
fi

%postun -n kernel-smp-char-lirc-parallel
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver}smp }%{_kernel_ver}smp

%post	-n kernel-smp-char-lirc-sir
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver}smp }%{_kernel_ver}smp
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_sir' line"
	echo "to your /etc/modules.conf."
fi

%postun -n kernel-smp-char-lirc-sir
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver}smp }%{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc ANNOUNCE AUTHORS NEWS README TODO ChangeLog
%doc contrib/lircrc doc/* remotes
%attr(755,root,root) %{_bindir}/ir[!x]*
%attr(755,root,root) %{_bindir}/mode2
%attr(755,root,root) %{_bindir}/rc
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/*
%config(noreplace) %{_sysconfdir}/*.conf
%{_mandir}/man?/*
%ghost %attr(600,root,root) %{_localstatedir}/log/lircd

%if 0%{!?_without_modules:%{_kernel24}}
%files -n kernel-char-lirc-dev
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_dev*

%files -n kernel-char-lirc-gpio
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_gpio*

%files -n kernel-char-lirc-i2c
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_i2c*
%endif

%if 0%{!?_without_modules:1}
%files -n kernel-char-lirc-serial
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_serial*

%files -n kernel-char-lirc-parallel
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_parallel*

%files -n kernel-char-lirc-sir
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_sir*
%endif

%if 0%{!?_without_modules:%{_kernel24}}
%files -n kernel-smp-char-lirc-dev
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/lirc_dev*

%files -n kernel-smp-char-lirc-gpio
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/lirc_gpio*

%files -n kernel-smp-char-lirc-i2c
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/lirc_i2c*
%endif

%if 0%{!?_without_modules:1}
%files -n kernel-smp-char-lirc-serial
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/lirc_serial*
%endif

# currently not SMP-safe
%if 0
%files -n kernel-smp-char-lirc-parallel
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/lirc_parallel*
%endif

%if 0%{!?_without_modules:1}
%files -n kernel-smp-char-lirc-sir
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/lirc_sir*
%endif

%if %{!?_without_x:1)%{?_without_x:0}
%files X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/irxevent
%attr(755,root,root) %{_bindir}/xmode2
%endif

%files libs
%defattr(644,root,root,755)
%{_libdir}/*.so.*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/lirc
%{_aclocaldir}/*
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
