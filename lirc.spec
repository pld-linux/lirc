# TODO
# - fix build --without kernel
# - restore lirc_parallel driver
# - try to make it use builder_kernel_modules and install_kernel_modules; I couldn't make it
# - investigate Patch8: vserver; non-vserver enabled kernels don't have the find_task_by_real_pid function (like kernel-desktop)
#
# Conditional build:
%bcond_without	dist_kernel	# without sources of distribution kernel
%bcond_without	kernel		# don't build kernel modules, only library+programs
%bcond_without	userspace	# build only packages with kernel modules
%bcond_without	svga		# without svgalib-based utility
%bcond_without	x		# without X11-based utilitied

%if %{without kernel}
%undefine	with_dist_kernel
%endif

#
# main package
#
# lirc_parallel is not thread safe, so not on this list
%define		drivers		"lirc_it87 lirc_serial lirc_atiusb lirc_mceusb lirc_sir lirc_bt829 lirc_i2c lirc_mceusb2 lirc_streamzap lirc_cmdir lirc_igorplugusb lirc_dev lirc_imon lirc_sasem lirc_gpio"
%define		no_install_post_strip 1
Summary:	Linux Infrared Remote Control daemons
Summary(pl.UTF-8):	Serwery do zdalnego sterowania Linuksem za pomocą podczerwieni
Name:		lirc
Version:	0.8.2
%define	_rel	1
Release:	%{_rel}
License:	GPL
Group:		Daemons
Source0:	http://dl.sourceforge.net/lirc/%{name}-%{version}.tar.bz2
# Source0-md5:	83e7060a6693b81075c178d7e3b215af
Source1:	http://lirc.sourceforge.net/remotes.tar.bz2
# Source1-md5:	373ebacae6d9abff25e804bee172d142
Source2:	%{name}d.sysconfig
Source3:	%{name}d.init
Source4:	%{name}md.init
Patch0:		%{name}-opt.patch
Patch1:		%{name}-tmp.patch
Patch2:		%{name}-bttv-headers.patch
Patch3:		%{name}-no-svgalib.patch
Patch4:		%{name}-alpha.patch
Patch5:		%{name}-i2c-2.8.x.patch
Patch6:		%{name}-sparc.patch
Patch7:		%{name}-remotes.patch
Patch8:		%{name}-vserver.patch
Patch9:		%{name}-kernelcc.patch
URL:		http://www.lirc.org/
#%{?with_x:BuildRequires:	xorg-lib-libX11-devel}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
%if %{with kernel}
BuildRequires:	kernel%{_alt_kernel}-module-build
BuildRequires:	kernel%{_alt_kernel}-source
%endif
%{?with_kernel:BuildRequires:	%{kgcc_package}}
BuildRequires:	rpmbuild(macros) >= 1.379
%{?with_svga:BuildRequires:	svgalib-devel}
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Requires:	%{name} = %{version}-%{_rel}

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

%package svga
Summary:	Linux Infrared Remote Control - svgalib utilities
Summary(pl.UTF-8):	Zdalne sterowanie Linuksem za pomocą podczerwieni - narzędzia svgalib
Group:		Applications
Requires:	%{name}-libs = %{version}-%{release}

%description svga
Linux Infrared Remote Control - svgalib-based utilities.

%description svga -l pl.UTF-8
Zdalne sterowanie Linuksem za pomocą podczerwieni - narzędzia oparte
na svgalibie.

%package libs
Summary:	LIRC libraries
Summary(pl.UTF-8):	Biblioteki LIRC
Group:		Libraries
Conflicts:	lirc < 0.6.3-3
# didn't use /tmp/.lircd

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

%package -n kernel%{_alt_kernel}-char-lirc-atiusb
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl.UTF-8):	Moduły jądra dla zdalnej obsługi Linuksa za pomocą podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Conflicts:	dev < 2.8.0-3

%description -n kernel%{_alt_kernel}-char-lirc-atiusb
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_atiusb module.

%description -n kernel%{_alt_kernel}-char-lirc-atiusb -l pl.UTF-8
Ten pakiet zawiera moduły jądra niezbędne do obsługi niektórych
pilotów na podczerwień (w tym tych dostarczanych z kartami TV).

Moduł lirc_atiusb.

%package -n kernel%{_alt_kernel}-char-lirc-bt829
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl.UTF-8):	Moduły jądra dla zdalnej obsługi Linuksa za pomocą podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Conflicts:	dev < 2.8.0-3

%description -n kernel%{_alt_kernel}-char-lirc-bt829
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_bt829 module.

%description -n kernel%{_alt_kernel}-char-lirc-bt829 -l pl.UTF-8
Ten pakiet zawiera moduły jądra niezbędne do obsługi niektórych
pilotów na podczerwień (w tym tych dostarczanych z kartami TV).

Moduł lirc_bt829.

%package -n kernel%{_alt_kernel}-char-lirc-cmdir
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl.UTF-8):	Moduły jądra dla zdalnej obsługi Linuksa za pomocą podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Conflicts:	dev < 2.8.0-3

%description -n kernel%{_alt_kernel}-char-lirc-cmdir
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_cmdir module.

%description -n kernel%{_alt_kernel}-char-lirc-cmdir -l pl.UTF-8
Ten pakiet zawiera moduły jądra niezbędne do obsługi niektórych
pilotów na podczerwień (w tym tych dostarczanych z kartami TV).

Moduł lirc_cmdir.

%package -n kernel%{_alt_kernel}-char-lirc-dev
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl.UTF-8):	Moduły jądra dla zdalnej obsługi Linuksa za pomocą podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-dev
Conflicts:	dev < 2.8.0-3

%description -n kernel%{_alt_kernel}-char-lirc-dev
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_dev module.

%description -n kernel%{_alt_kernel}-char-lirc-dev -l pl.UTF-8
Ten pakiet zawiera moduły jądra niezbędne do obsługi niektórych
pilotów na podczerwień (w tym tych dostarczanych z kartami TV).

Moduł lirc_dev.

%package -n kernel%{_alt_kernel}-char-lirc-gpio
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl.UTF-8):	Moduły jądra dla zdalnej obsługi Linuksa za pomocą podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-gpio
Conflicts:	dev < 2.8.0-3

%description -n kernel%{_alt_kernel}-char-lirc-gpio
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_gpio module.

%description -n kernel%{_alt_kernel}-char-lirc-gpio -l pl.UTF-8
Ten pakiet zawiera moduły jądra niezbędne do obsługi niektórych
pilotów na podczerwień (w tym tych dostarczanych z kartami TV).

Moduł lirc_gpio.

%package -n kernel%{_alt_kernel}-char-lirc-i2c
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl.UTF-8):	Moduły jądra dla zdalnej obsługi Linuksa za pomocą podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-i2c
Conflicts:	dev < 2.8.0-3

%description -n kernel%{_alt_kernel}-char-lirc-i2c
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_i2c module.

%description -n kernel%{_alt_kernel}-char-lirc-i2c -l pl.UTF-8
Ten pakiet zawiera moduły jądra niezbędne do obsługi niektórych
pilotów na podczerwień (w tym tych dostarczanych z kartami TV).

Moduł lirc_i2c.

%package -n kernel%{_alt_kernel}-char-lirc-igorplugusb
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl.UTF-8):	Moduły jądra dla zdalnej obsługi Linuksa za pomocą podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-igorplugusb
Conflicts:	dev < 2.8.0-3

%description -n kernel%{_alt_kernel}-char-lirc-igorplugusb
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_igorplugusb module.

%description -n kernel%{_alt_kernel}-char-lirc-igorplugusb -l pl.UTF-8
Ten pakiet zawiera moduły jądra niezbędne do obsługi niektórych
pilotów na podczerwień (w tym tych dostarczanych z kartami TV).

Moduł lirc_igorplugusb.

%package -n kernel%{_alt_kernel}-char-lirc-imon
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl.UTF-8):	Moduły jądra dla zdalnej obsługi Linuksa za pomocą podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-imon
Conflicts:	dev < 2.8.0-3

%description -n kernel%{_alt_kernel}-char-lirc-imon
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_imon module.

%description -n kernel%{_alt_kernel}-char-lirc-imon -l pl.UTF-8
Ten pakiet zawiera moduły jądra niezbędne do obsługi niektórych
pilotów na podczerwień (w tym tych dostarczanych z kartami TV).

Moduł lirc_imon.

%package -n kernel%{_alt_kernel}-char-lirc-it87
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl.UTF-8):	Moduły jądra dla zdalnej obsługi Linuksa za pomocą podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Conflicts:	dev < 2.8.0-3

%description -n kernel%{_alt_kernel}-char-lirc-it87
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_it87 module.

%description -n kernel%{_alt_kernel}-char-lirc-it87 -l pl.UTF-8
Ten pakiet zawiera moduły jądra niezbędne do obsługi niektórych
pilotów na podczerwień (w tym tych dostarczanych z kartami TV).

Moduł lirc_it87.

%package -n kernel%{_alt_kernel}-char-lirc-mceusb
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl.UTF-8):	Moduły jądra dla zdalnej obsługi Linuksa za pomocą podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Conflicts:	dev < 2.8.0-3

%description -n kernel%{_alt_kernel}-char-lirc-mceusb
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_mceusb module.

%description -n kernel%{_alt_kernel}-char-lirc-mceusb -l pl.UTF-8
Ten pakiet zawiera moduły jądra niezbędne do obsługi niektórych
pilotów na podczerwień (w tym tych dostarczanych z kartami TV).

Moduł lirc_mceusb.

%package -n kernel%{_alt_kernel}-char-lirc-sasem
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl.UTF-8):	Moduły jądra dla zdalnej obsługi Linuksa za pomocą podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Conflicts:	dev < 2.8.0-3

%description -n kernel%{_alt_kernel}-char-lirc-sasem
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_sasem module.

%description -n kernel%{_alt_kernel}-char-lirc-sasem -l pl.UTF-8
Ten pakiet zawiera moduły jądra niezbędne do obsługi niektórych
pilotów na podczerwień (w tym tych dostarczanych z kartami TV).

Moduł lirc_sasem.

%package -n kernel%{_alt_kernel}-char-lirc-serial
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl.UTF-8):	Moduły jądra dla zdalnej obsługi Linuksa za pomocą podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
%{?with_dist_kernel:Requires:	setserial}
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-serial
Conflicts:	dev < 2.8.0-3

%description -n kernel%{_alt_kernel}-char-lirc-serial
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_serial module for devices connected to serial port.

%description -n kernel%{_alt_kernel}-char-lirc-serial -l pl.UTF-8
Ten pakiet zawiera moduły jądra niezbędne do obsługi niektórych
pilotów na podczerwień (w tym tych dostarczanych z kartami TV).

Moduł lirc_serial dla urządzeń podłączanych do portu szeregowego.

%package -n kernel%{_alt_kernel}-char-lirc-streamzap
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl.UTF-8):	Moduły jądra dla zdalnej obsługi Linuksa za pomocą podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-streamzap
Conflicts:	dev < 2.8.0-3

%description -n kernel%{_alt_kernel}-char-lirc-streamzap
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_streamzap module.

%description -n kernel%{_alt_kernel}-char-lirc-streamzap -l pl.UTF-8
Ten pakiet zawiera moduły jądra niezbędne do obsługi niektórych
pilotów na podczerwień (w tym tych dostarczanych z kartami TV).

Moduł lirc_streamzap.

%package -n kernel%{_alt_kernel}-char-lirc-sir
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl.UTF-8):	Moduły jądra dla zdalnej obsługi Linuksa za pomocą podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-sir
Conflicts:	dev < 2.8.0-3

%description -n kernel%{_alt_kernel}-char-lirc-sir
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_sir module.

%description -n kernel%{_alt_kernel}-char-lirc-sir -l pl.UTF-8
Ten pakiet zawiera moduły jądra niezbędne do obsługi niektórych
pilotów na podczerwień (w tym tych dostarczanych z kartami TV).

Moduł lirc_sir.

## XXX: Unused now, as all kernels are smp by default
%package -n kernel%{_alt_kernel}-char-lirc-parallel
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl.UTF-8):	Moduły jądra dla zdalnej obsługi Linuksa za pomocą podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-parallel
Conflicts:	dev < 2.8.0-3

%description -n kernel%{_alt_kernel}-char-lirc-parallel
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc-parallel module for devices connected to parallel port.

%description -n kernel%{_alt_kernel}-char-lirc-parallel -l pl.UTF-8
Ten pakiet zawiera moduły jądra niezbędne do obsługi niektórych
pilotów na podczerwień (w tym tych dostarczanych z kartami TV).

Moduł lirc_parallel dla urządzeń podłączanych do portu równoległego.

%prep
%setup -q -a 1
%patch0 -p1
%patch1 -p1
#%patch2 -p1
%if !%{with svga}
%patch3 -p1
%endif
%patch4 -p1
%if %{with kernel}
if grep -qs 'I2C_VERSION.*"2\.8\.' %{_kernelsrcdir}/include/linux/i2c.h ; then
%patch5 -p0
fi
%endif
%patch6 -p1
%patch7 -p1
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
	ac_cv_header_portaudio_h=no \
%if %{with kernel}
	KERNELCC="%{kgcc}" \
%else
	ac_cv_have_kernel="no_kernel=yes" \
%endif
	--with-kerneldir=%{_kernelsrcdir} \
	%{?with_x:--with-x} \
	--with-port=0x2f8 \
	--with-irq=3 \
	--without-soft-carrier \
	--with-driver=userspace \
	--with-igor

%if %{with userspace}
%{__make}
%endif

%if %{with kernel}
cd drivers

drivers=%{drivers}
rm -rf o
if [ ! -r "%{_kernelsrcdir}/config-dist" ]; then
	exit 1
fi

install -d o/include/{linux,config}
ln -sf %{_kernelsrcdir}/config-dist o/.config
ln -sf %{_kernelsrcdir}/include/linux/autoconf-dist.h o/include/linux/autoconf.h
[ ! -L o/include/asm ] && ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} o/include/asm
ln -sf %{_kernelsrcdir}/Module.symvers-dist o/Module.symvers

%if %{without dist_kernel}
	touch o/include/config/MARKER
	ln -sf %{_kernelsrcdir}/scripts o/
%else
	%{__make} -j1 -C %{_kernelsrcdir} O=$PWD/o prepare scripts
%endif

for drv in $drivers; do
	cd $drv
	if [ "$drv" == "lirc_parallel" ] && grep -q ^CONFIG_SMP o/.config ]; then
		echo "lirc_parallel is not smp safe"
	else
		ln -sf ../o
		%{__make} clean \
			RCS_FIND_IGNORE="-name '*.ko' -o" \
			M=$PWD O=$PWD/o \
			%{?with_verbose:V=1}

		%{__make} \
			M=$PWD O=$PWD/o \
			%{?with_verbose:V=1}
			mv $drv{,-dist}.ko
	fi
	cd ..
done

cd ..

%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_aclocaldir},/dev,/var/log} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%if %{with kernel}
drivers=%{drivers}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
for drv in $drivers; do
	install drivers/$drv/$drv-%{?with_dist_kernel:dist}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/$drv.ko
done
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
echo "install the kernel%{_alt_kernel}-char-lirc-<your_driver> or"
echo "kernel%{_alt_kernel}-smp-char-lirc-<your_driver> package."

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

%post	-n kernel%{_alt_kernel}-char-lirc-atiusb
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_atiusb' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel%{_alt_kernel}-char-lirc-atiusb
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-char-lirc-bt829
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_bt829' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel%{_alt_kernel}-char-lirc-bt829
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-char-lirc-cmdir
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_cmdir' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel%{_alt_kernel}-char-lirc-cmdir
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-char-lirc-dev
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-char-lirc-dev
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-char-lirc-gpio
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_gpio' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel%{_alt_kernel}-char-lirc-gpio
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-char-lirc-i2c
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_i2c' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel%{_alt_kernel}-char-lirc-i2c
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-char-lirc-igorplugusb
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_igorplugusb' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel%{_alt_kernel}-char-lirc-igorplugusb
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-char-lirc-imon
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_imon' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel%{_alt_kernel}-char-lirc-imon
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-char-lirc-it87
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_it87' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel%{_alt_kernel}-char-lirc-it87
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-char-lirc-mceusb
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_mceusb' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel%{_alt_kernel}-char-lirc-mceusb
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-char-lirc-sasem
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_sasem' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel%{_alt_kernel}-char-lirc-sasem
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-char-lirc-serial
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_serial' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel%{_alt_kernel}-char-lirc-serial
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-char-lirc-streamzap
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_streamzap' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel%{_alt_kernel}-char-lirc-streamzap
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-char-lirc-parallel
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_parallel' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel%{_alt_kernel}-char-lirc-parallel
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-char-lirc-sir
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_sir' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel%{_alt_kernel}-char-lirc-sir
%depmod %{_kernel_ver}


%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc ANNOUNCE AUTHORS NEWS README TODO ChangeLog
%doc contrib/lircrc doc/{html,images,lirc.css}
%attr(755,root,root) %{_bindir}/ir[!x]*
%attr(755,root,root) %{_bindir}/mode2
%attr(755,root,root) %{_bindir}/lircrcd
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*
%config(noreplace) %{_sysconfdir}/*.conf
%{_mandir}/man1/ir[!x]*
%{_mandir}/man1/[!isx]*
%{_mandir}/man8/*
%ghost %attr(600,root,root) /var/log/lircd

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
%files -n kernel%{_alt_kernel}-char-lirc-atiusb
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_atiusb*

%files -n kernel%{_alt_kernel}-char-lirc-bt829
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_bt829*

%files -n kernel%{_alt_kernel}-char-lirc-cmdir
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_cmdir*

%files -n kernel%{_alt_kernel}-char-lirc-dev
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_dev*

%files -n kernel%{_alt_kernel}-char-lirc-gpio
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_gpio*

%files -n kernel%{_alt_kernel}-char-lirc-i2c
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_i2c*

%files -n kernel%{_alt_kernel}-char-lirc-igorplugusb
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_igorplugusb*

%files -n kernel%{_alt_kernel}-char-lirc-imon
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_imon*

%files -n kernel%{_alt_kernel}-char-lirc-it87
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_it87*

%files -n kernel%{_alt_kernel}-char-lirc-mceusb
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_mceusb*

%files -n kernel%{_alt_kernel}-char-lirc-sasem
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_sasem*

%files -n kernel%{_alt_kernel}-char-lirc-serial
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_serial*

%files -n kernel%{_alt_kernel}-char-lirc-streamzap
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_streamzap*

%files -n kernel%{_alt_kernel}-char-lirc-sir
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_sir*

# XXX currently not SMP-safe
%if 0
%files -n kernel%{_alt_kernel}-char-lirc-parallel
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_parallel*
%endif
%endif
