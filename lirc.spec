#
# Conditional build:
%bcond_without	dist_kernel	# without sources of distribution kernel
%bcond_without	kernel		# don't build kernel modules, only library+programs
%bcond_without	userspace	# build only packages with kernel modules
%bcond_without	svga		# without svgalib-based utility
%bcond_without	x		# without X11-based utilitied
#
%define		_kernel24	%(echo %{_kernel_ver} | grep -qv '2\.4\.' ; echo $?)
Summary:	Linux Infrared Remote Control daemons
Summary(pl):	Serwery do zdalnej kontroli Linuksa za pomoc± podczerwieni
Name:		lirc
Version:	0.6.6
%define _rel	8
Release:	%{_rel}
License:	GPL
Group:		Daemons
Source0:	http://dl.sourceforge.net/lirc/%{name}-%{version}.tar.bz2
# Source0-md5:	6e7b5ba2fd479961d067730e16df7c54
Source1:	http://lirc.sourceforge.net/remotes.tar.bz2
# Source1-md5:	367be71922338f75c27c461880302f54
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
Patch7:		http://delvare.free.fr/i2c/other/%{name}-0.6.6-i2c-2.8.0.patch
Patch8:		%{name}-sparc.patch
Patch9:		%{name}-am18.patch
URL:		http://www.lirc.org/
%{?with_x:BuildRequires:	XFree86-devel}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
%if %{with dist_kernel} && %{with kernel}
BuildRequires:	kernel-headers
BuildRequires:	kernel-i2c-devel >= 2.8.0
BuildRequires:	kernel-source
%endif
%{?with_kernel:BuildRequires:	%{kgcc_package}}
BuildRequires:	rpmbuild(macros) >= 1.118
%{?with_svga:BuildRequires:	svgalib-devel}
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LIRC is a package that allows you to decode and send infra-red signals
of many (but not all) commonly used remote controls.

%description -l pl
LIRC to program pozwalaj±cy na dekodowanie nadchodz±cych oraz
wysy³anie sygna³ów w podczerwieni za pomoc± wielu (ale nie wszystkich)
popularnych urz±dzeñ do zdalnej kontroli

%package X11
Summary:	Linux Infrared Remote Control - X11 utilities
Summary(pl):	Zdalna kontrola Linuksa za pomoc± podczerwieni - narzêdzia X11
Group:		X11/Applications
Requires:	%{name}-libs = %{version}-%{release}

%description X11
Linux Infrared Remote Control - X11 utilities.

%description X11 -l pl
Zdalna kontrola Linuksa za pomoc± podczerwieni - narzêdzia X11.

%package svga
Summary:	Linux Infrared Remote Control - svgalib utilities
Summary(pl):	Zdalna kontrola Linuksa za pomoc± podczerwieni - narzêdzia svgalib
Group:		Applications
Requires:	%{name}-libs = %{version}-%{release}

%description svga
Linux Infrared Remote Control - svgalib-based utilities.

%description svga -l pl
Zdalna kontrola Linuksa za pomoc± podczerwieni - narzêdzia oparte na
svgalibie.

%package libs
Summary:	LIRC libraries
Summary(pl):	Biblioteki LIRC
Group:		Libraries
Conflicts:	lirc < 0.6.3-3
# didn't use /tmp/.lircd

%description libs
This package provides the libraries necessary to run lirc client
programs.

%description libs -l pl
Ten pakiet zawiera biblioteki niezbêdne do dzia³ania klientów LIRC.

%package devel
Summary:	Header files for LIRC development
Summary(pl):	Pliki nag³ówkowe do tworzenia programów z obs³ug± LIRC
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package provides the files necessary to develop LIRC-based
programs.

%description devel -l pl
Ten pakiet zawiera pliki niezbêdne do tworzenia programów opartych na
LIRC.

%package static
Summary:	Static library for LIRC development
Summary(pl):	Biblioteka statyczna LIRC
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
The files necessary for development of statically-linked lirc-based
programs.

%description static -l pl
Pliki potrzebne do tworzenia ³±czonych statycznie programów opartych
na LIRC.

%package -n kernel-char-lirc-dev
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{release}
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-dev

%description -n kernel-char-lirc-dev
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_dev module.

%description -n kernel-char-lirc-dev -l pl
Ten pakiet zawiera modu³y j±dra niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_dev.

%package -n kernel-char-lirc-gpio
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{release}
Requires:	kernel-char-lirc-dev = %{version}-%{release}
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-gpio

%description -n kernel-char-lirc-gpio
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_gpio module.

%description -n kernel-char-lirc-gpio -l pl
Ten pakiet zawiera modu³y j±dra niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_gpio.

%package -n kernel-char-lirc-i2c
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{release}
Requires:	kernel-char-lirc-dev = %{version}-%{release}
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-i2c

%description -n kernel-char-lirc-i2c
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_i2c module.

%description -n kernel-char-lirc-i2c -l pl
Ten pakiet zawiera modu³y j±dra niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_i2c

%package -n kernel-char-lirc-serial
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{release}
%{?with_dist_kernel:Requires:	setserial}
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-serial

%description -n kernel-char-lirc-serial
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_serial module for devices connected to serial port.

%description -n kernel-char-lirc-serial -l pl
Ten pakiet zawiera modu³y j±dra niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_serial dla urz±dzeñ pod³±czanych do serial portu.

%package -n kernel-char-lirc-parallel
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{release}
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-parallel

%description -n kernel-char-lirc-parallel
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc-parallel module for devices connected to parallel port.

%description -n kernel-char-lirc-parallel -l pl
Ten pakiet zawiera modu³y j±dra niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_parallel dla urz±dzeñ pod³±czanych do portu równoleg³ego.

%package -n kernel-char-lirc-sir
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{release}
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-sir

%description -n kernel-char-lirc-sir
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_sir module.

%description -n kernel-char-lirc-sir -l pl
Ten pakiet zawiera modu³y j±dra niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_sir.

%package -n kernel-smp-char-lirc-dev
Summary:	SMP kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra SMP dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{release}
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-dev

%description -n kernel-smp-char-lirc-dev
This package contains the SMP kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_dev module.

%description -n kernel-smp-char-lirc-dev -l pl
Ten pakiet zawiera modu³y j±dra SMP niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_dev.

%package -n kernel-smp-char-lirc-gpio
Summary:	SMP kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{release}
Requires:	kernel-smp-char-lirc-dev = %{version}-%{release}
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-gpio

%description -n kernel-smp-char-lirc-gpio
This package contains the SMP kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_gpio module.

%description -n kernel-smp-char-lirc-gpio -l pl
Ten pakiet zawiera modu³y j±dra SMP niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_gpio.

%package -n kernel-smp-char-lirc-i2c
Summary:	SMP kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra SMP dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{release}
Requires:	kernel-smp-char-lirc-dev = %{version}-%{release}
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-i2c

%description -n kernel-smp-char-lirc-i2c
This package contains the SMP kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_i2c module.

%description -n kernel-smp-char-lirc-i2c -l pl
Ten pakiet zawiera modu³y j±dra SMP niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_i2c

%package -n kernel-smp-char-lirc-serial
Summary:	SMP kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra SMP dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{release}
%{?with_dist_kernel:Requires:	setserial}
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-serial

%description -n kernel-smp-char-lirc-serial
This package contains the SMP kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_serial module for devices connected to serial port.

%description -n kernel-smp-char-lirc-serial -l pl
Ten pakiet zawiera modu³y j±dra SMP niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_serial dla urz±dzeñ pod³±czanych do serial portu.

%package -n kernel-smp-char-lirc-parallel
Summary:	SMP kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra SMP dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{release}
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-parallel

%description -n kernel-smp-char-lirc-parallel
This package contains the SMP kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc-parallel module for devices connected to parallel port.

%description -n kernel-char-lirc-parallel -l pl
Ten pakiet zawiera modu³y j±dra SMP niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_parallel dla urz±dzeñ pod³±czanych do portu równoleg³ego.

%package -n kernel-smp-char-lirc-sir
Summary:	SMP kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
PreReq:		modutils >= 2.4.6-4
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{release}
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-sir

%description -n kernel-smp-char-lirc-sir
This package contains the SMP kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_sir module.

%description -n kernel-smp-char-lirc-sir -l pl
Ten pakiet zawiera modu³y j±dra SMP niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_sir.

%prep
%setup -q -a 1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%if %{without svga}
%patch3 -p1
%endif
%patch4 -p1
%patch5 -p1
%patch6 -p1
%if %{with kernel}
if grep -qs 'I2C_VERSION.*"2\.8\.' %{_kernelsrcdir}/include/linux/i2c.h ; then
%patch7 -p1
fi
%endif
%patch8 -p1
%patch9 -p1

%build
echo '#' > drivers/Makefile.am
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoheader}
%{__autoconf}

%configure \
	--with-driver=any \
	--with-kerneldir=%{_kernelsrcdir} \
	%{?with_x:--with-x} \
	--with-port=0x2f8 \
	--with-irq=3 \
	--without-soft-carrier
%{__make}

%if %{with kernel}
cd drivers

%if %{_kernel24}
# 2.4 drivers
LIRC_NORMAL="lirc_gpio lirc_i2c lirc_serial lirc_sir"
LIRC_SYMTAB="lirc_dev"
%else
# 2.2 drivers
LIRC_NORMAL="lirc_serial lirc_sir"
LIRC_SYMTAB=""
%endif

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
install -d $RPM_BUILD_ROOT{%{_bindir},%{_aclocaldir},/dev,/var/log} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%if %{with kernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
install drivers/*.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install drivers/*/*.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc
%endif

%if %{with userspace}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	sysconfdir=$RPM_BUILD_ROOT%{_sysconfdir}

cat>$RPM_BUILD_ROOT%{_sysconfdir}/lircd.conf<<END
#
# This is a placeholder for your configuration file.
# See %{_docdir}/%{name}-%{version}/remotes for some examples.
#
END
cp -f $RPM_BUILD_ROOT%{_sysconfdir}/lirc{,m}d.conf
install contrib/*.m4 $RPM_BUILD_ROOT%{_aclocaldir}
:> $RPM_BUILD_ROOT/var/log/lircd

install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/lircd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/lircd
install %{SOURCE4} $RPM_BUILD_ROOT/etc/rc.d/init.d/lircmd
%endif

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
%depmod %{_kernel_ver}

%postun -n kernel-char-lirc-dev
%depmod %{_kernel_ver}

%post	-n kernel-char-lirc-gpio
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_gpio' line"
	echo "to your /etc/modules.conf."
fi

%postun -n kernel-char-lirc-gpio
%depmod %{_kernel_ver}

%post	-n kernel-char-lirc-i2c
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_i2c' line"
	echo "to your /etc/modules.conf."
fi

%postun -n kernel-char-lirc-i2c
%depmod %{_kernel_ver}

%post	-n kernel-char-lirc-serial
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_serial' line"
	echo "to your /etc/modules.conf."
fi

%postun -n kernel-char-lirc-serial
%depmod %{_kernel_ver}

%post	-n kernel-char-lirc-parallel
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_parallel' line"
	echo "to your /etc/modules.conf."
fi

%postun -n kernel-char-lirc-parallel
%depmod %{_kernel_ver}

%post	-n kernel-char-lirc-sir
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_sir' line"
	echo "to your /etc/modules.conf."
fi

%postun -n kernel-char-lirc-sir
%depmod %{_kernel_ver}

%post	-n kernel-smp-char-lirc-dev
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-char-lirc-dev
%depmod %{_kernel_ver}smp

%post	-n kernel-smp-char-lirc-gpio
%depmod %{_kernel_ver}smp
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_gpio' line"
	echo "to your /etc/modules.conf."
fi

%postun -n kernel-smp-char-lirc-gpio
%depmod %{_kernel_ver}smp

%post	-n kernel-smp-char-lirc-i2c
%depmod %{_kernel_ver}smp
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_i2c' line"
	echo "to your /etc/modules.conf."
fi

%postun -n kernel-smp-char-lirc-i2c
%depmod %{_kernel_ver}smp

%post	-n kernel-smp-char-lirc-serial
%depmod %{_kernel_ver}smp
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_serial' line"
	echo "to your /etc/modules.conf."
fi

%postun -n kernel-smp-char-lirc-serial
%depmod %{_kernel_ver}smp

%post -n kernel-smp-char-lirc-parallel
%depmod %{_kernel_ver}smp
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_parallel' line"
	echo "to your /etc/modules.conf."
fi

%postun -n kernel-smp-char-lirc-parallel
%depmod %{_kernel_ver}smp

%post	-n kernel-smp-char-lirc-sir
%depmod %{_kernel_ver}smp
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_sir' line"
	echo "to your /etc/modules.conf."
fi

%postun -n kernel-smp-char-lirc-sir
%depmod %{_kernel_ver}smp

%if %{with userspace}
%files
%defattr(644,root,root,755)
# XXX: are jpegs in docs (remotes) a good idea?
%doc ANNOUNCE AUTHORS NEWS README TODO ChangeLog
%doc contrib/lircrc doc/{html,images,lirc.css} remotes
%attr(755,root,root) %{_bindir}/ir[!x]*
%attr(755,root,root) %{_bindir}/mode2
%attr(755,root,root) %{_bindir}/rc
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/*
%config(noreplace) %{_sysconfdir}/*.conf
%{_mandir}/man1/ir[!x]*
%{_mandir}/man1/[!isx]*
%{_mandir}/man8/*
%ghost %attr(600,root,root) /var/log/lircd

%if %{with x}
%files X11
%defattr(644,root,root,755)
%doc doc/irxevent.keys
%attr(755,root,root) %{_bindir}/irxevent
%attr(755,root,root) %{_bindir}/xmode2
%{_mandir}/man1/irxevent.1*
%{_mandir}/man1/xmode2.1*
%endif

%if %{with svga}
%files svga
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/smode2
%{_mandir}/man1/smode2.1*
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/lirc
%{_aclocaldir}/*.m4

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif

%if %{with kernel}
%if %{_kernel24}
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

%files -n kernel-char-lirc-serial
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_serial*

%files -n kernel-char-lirc-parallel
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_parallel*

%files -n kernel-char-lirc-sir
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_sir*

%if %{_kernel24}
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

%files -n kernel-smp-char-lirc-serial
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/lirc_serial*

# currently not SMP-safe
%if 0
%files -n kernel-smp-char-lirc-parallel
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/lirc_parallel*
%endif

%files -n kernel-smp-char-lirc-sir
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/lirc_sir*
%endif
