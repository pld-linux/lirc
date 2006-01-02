# TODO
# - are jpegs in docs (remotes) a good idea?
#
# Conditional build:
%bcond_without	dist_kernel	# without sources of distribution kernel
%bcond_without	kernel		# don't build kernel modules, only library+programs
%bcond_without	smp		# don't build SMP module
%bcond_without	userspace	# build only packages with kernel modules
%bcond_without	svga		# without svgalib-based utility
%bcond_without	x		# without X11-based utilitied
#
%define		_kernelsrcdir	/usr/src/linux
#%define		drivers		"lirc_gpio lirc_it87 lirc_serial lirc_atiusb lirc_mceusb lirc_sir lirc_bt829 lirc_i2c lirc_mceusb2 lirc_streamzap lirc_cmdir lirc_igorplugusb lirc_parallel lirc_dev lirc_imon lirc_sasem"
%define		drivers		"lirc_it87 lirc_serial lirc_atiusb lirc_mceusb lirc_sir lirc_bt829 lirc_i2c lirc_mceusb2 lirc_streamzap lirc_cmdir lirc_igorplugusb lirc_dev lirc_imon lirc_sasem lirc_parallel lirc_gpio"
Summary:	Linux Infrared Remote Control daemons
Summary(pl):	Serwery do zdalnego sterowania Linuksem za pomoc± podczerwieni
Name:		lirc
Version:	0.8.0
%define	_rel	0.1
%define	_pre	pre3
Release:	%{_rel}
License:	GPL
Group:		Daemons
Source0:	http://lirc.sourceforge.net/software/snapshots/%{name}-%{version}%{_pre}.tar.bz2
# Source0-md5:	c20cf756b0b5cad96437bc25e81b166a
Source1:	http://lirc.sourceforge.net/remotes.tar.bz2
# Source1-md5:	d769f13b0d659170746f221d4a773c81
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
URL:		http://www.lirc.org/
%{?with_x:BuildRequires:	XFree86-devel}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
%if %{with dist_kernel} && %{with kernel}
BuildRequires:	kernel-headers
#BuildRequires:	kernel24-i2c-devel >= 2.8.0
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
popularnych urz±dzeñ do zdalnego sterowania.

%package X11
Summary:	Linux Infrared Remote Control - X11 utilities
Summary(pl):	Zdalne sterowanie Linuksem za pomoc± podczerwieni - narzêdzia X11
Group:		X11/Applications
Requires:	%{name}-libs = %{version}-%{release}

%description X11
Linux Infrared Remote Control - X11 utilities.

%description X11 -l pl
Zdalne sterowanie Linuksem za pomoc± podczerwieni - narzêdzia X11.

%package svga
Summary:	Linux Infrared Remote Control - svgalib utilities
Summary(pl):	Zdalne sterowanie Linuksem za pomoc± podczerwieni - narzêdzia svgalib
Group:		Applications
Requires:	%{name}-libs = %{version}-%{release}

%description svga
Linux Infrared Remote Control - svgalib-based utilities.

%description svga -l pl
Zdalne sterowanie Linuksem za pomoc± podczerwieni - narzêdzia oparte
na svgalibie.

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

%package -n kernel-char-lirc-atiusb
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	kernel-char-lirc-dev = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
Conflicts:	dev < 2.8.0-3

%description -n kernel-char-lirc-atiusb
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_atiusb module.

%description -n kernel-char-lirc-atiusb -l pl
Ten pakiet zawiera modu³y j±dra niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_atiusb.

%package -n kernel-char-lirc-bt829
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	kernel-char-lirc-dev = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
Conflicts:	dev < 2.8.0-3

%description -n kernel-char-lirc-bt829
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_bt829 module.

%description -n kernel-char-lirc-bt829 -l pl
Ten pakiet zawiera modu³y j±dra niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_bt829.

%package -n kernel-char-lirc-cmdir
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	kernel-char-lirc-dev = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
Conflicts:	dev < 2.8.0-3

%description -n kernel-char-lirc-cmdir
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_cmdir module.

%description -n kernel-char-lirc-cmdir -l pl
Ten pakiet zawiera modu³y j±dra niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_cmdir.

%package -n kernel-char-lirc-dev
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	modutils >= 2.4.6-4
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
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	kernel-char-lirc-dev = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
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
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	kernel-char-lirc-dev = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
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

%package -n kernel-char-lirc-igorplugusb
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	kernel-char-lirc-dev = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-igorplugusb

%description -n kernel-char-lirc-igorplugusb
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_igorplugusb module.

%description -n kernel-char-lirc-igorplugusb -l pl
Ten pakiet zawiera modu³y j±dra niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_igorplugusb

%package -n kernel-char-lirc-imon
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	kernel-char-lirc-dev = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-imon

%description -n kernel-char-lirc-imon
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_imon module.

%description -n kernel-char-lirc-imon -l pl
Ten pakiet zawiera modu³y j±dra niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_imon

%package -n kernel-char-lirc-it87
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	kernel-char-lirc-dev = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
Conflicts:	dev < 2.8.0-3

%description -n kernel-char-lirc-it87
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_it87 module.

%description -n kernel-char-lirc-it87 -l pl
Ten pakiet zawiera modu³y j±dra niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_it87.

%package -n kernel-char-lirc-mceusb
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	kernel-char-lirc-dev = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
Conflicts:	dev < 2.8.0-3

%description -n kernel-char-lirc-mceusb
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_mceusb module.

%description -n kernel-char-lirc-mceusb -l pl
Ten pakiet zawiera modu³y j±dra niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_mceusb.

%package -n kernel-char-lirc-sasem
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	kernel-char-lirc-dev = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
Conflicts:	dev < 2.8.0-3

%description -n kernel-char-lirc-sasem
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_sasem module.

%description -n kernel-char-lirc-sasem -l pl
Ten pakiet zawiera modu³y j±dra niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_sasem.

%package -n kernel-char-lirc-serial
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	kernel-char-lirc-dev = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
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

%package -n kernel-char-lirc-streamzap
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	kernel-char-lirc-dev = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-streamzap

%description -n kernel-char-lirc-streamzap
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_streamzap module.

%description -n kernel-char-lirc-streamzap -l pl
Ten pakiet zawiera modu³y j±dra niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_streamzap.

%package -n kernel-char-lirc-parallel
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	modutils >= 2.4.6-4
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
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	modutils >= 2.4.6-4
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

%package -n kernel-smp-char-lirc-atiusb
Summary:	SMP kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra SMP dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	kernel-smp-char-lirc-dev = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
Conflicts:	dev < 2.8.0-3

%description -n kernel-smp-char-lirc-atiusb
This package contains the SMP kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_atiusb module.

%description -n kernel-smp-char-lirc-atiusb -l pl
Ten pakiet zawiera modu³y j±dra SMP niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_atiusb.

%package -n kernel-smp-char-lirc-bt829
Summary:	SMP kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra SMP dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	kernel-smp-char-lirc-dev = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
Conflicts:	dev < 2.8.0-3

%description -n kernel-smp-char-lirc-bt829
This package contains the SMP kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_bt829 module.

%description -n kernel-smp-char-lirc-bt829 -l pl
Ten pakiet zawiera modu³y j±dra SMP niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_bt829.

%package -n kernel-smp-char-lirc-cmdir
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	kernel-smp-char-lirc-dev = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
Conflicts:	dev < 2.8.0-3

%description -n kernel-smp-char-lirc-cmdir
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_cmdir module.

%description -n kernel-smp-char-lirc-cmdir -l pl
Ten pakiet zawiera modu³y j±dra niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_cmdir.

%package -n kernel-smp-char-lirc-dev
Summary:	SMP kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra SMP dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
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
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	kernel-smp-char-lirc-dev = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
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
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	kernel-smp-char-lirc-dev = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
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

Modu³ lirc_i2c.

%package -n kernel-smp-char-lirc-igorplugusb
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	kernel-spm-char-lirc-dev = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-igorplugusb

%description -n kernel-smp-char-lirc-igorplugusb
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_igorplugusb module.

%description -n kernel-smp-char-lirc-igorplugusb -l pl
Ten pakiet zawiera modu³y j±dra niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_igorplugusb

%package -n kernel-smp-char-lirc-imon
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	kernel-smp-char-lirc-dev = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-imon

%description -n kernel-smp-char-lirc-imon
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_imon module.

%description -n kernel-smp-char-lirc-imon -l pl
Ten pakiet zawiera modu³y j±dra niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_imon

%package -n kernel-smp-char-lirc-it87
Summary:	SMP kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra SMP dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	kernel-smp-char-lirc-dev = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
Conflicts:	dev < 2.8.0-3

%description -n kernel-smp-char-lirc-it87
This package contains the SMP kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_it87 module.

%description -n kernel-smp-char-lirc-it87 -l pl
Ten pakiet zawiera modu³y j±dra SMP niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_it87.

%package -n kernel-smp-char-lirc-mceusb
Summary:	SMP kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra SMP dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	kernel-smp-char-lirc-dev = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
Conflicts:	dev < 2.8.0-3

%description -n kernel-smp-char-lirc-mceusb
This package contains the SMP kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_mceusb module.

%description -n kernel-smp-char-lirc-mceusb -l pl
Ten pakiet zawiera modu³y j±dra SMP niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_mceusb.

%package -n kernel-smp-char-lirc-sasem
Summary:	SMP kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra SMP dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	kernel-smp-char-lirc-dev = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
Conflicts:	dev < 2.8.0-3

%description -n kernel-smp-char-lirc-sasem
This package contains the SMP kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_sasem module.

%description -n kernel-smp-char-lirc-sasem -l pl
Ten pakiet zawiera modu³y j±dra SMP niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_sasem.

%package -n kernel-smp-char-lirc-serial
Summary:	SMP kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra SMP dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	kernel-smp-char-lirc-dev = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
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

%package -n kernel-smp-char-lirc-streamzap
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	kernel-smp-char-lirc-dev = %{version}-%{_rel}@%{_kernel_ver_str}
Requires:	modutils >= 2.4.6-4
Conflicts:	dev < 2.8.0-3
Obsoletes:	lirc-modules
Obsoletes:	lirc-modules-streamzap

%description -n kernel-smp-char-lirc-streamzap
This package contains the kernel modules necessary to operate some
infrared remote control devices (such as the ones bundled with TV
cards).

lirc_streamzap module.

%description -n kernel-smp-char-lirc-streamzap -l pl
Ten pakiet zawiera modu³y j±dra niezbêdne do obs³ugi niektórych
pilotów na podczerwieñ (w tym tych dostarczanych z kartami TV).

Modu³ lirc_streamzap.

%package -n kernel-smp-char-lirc-parallel
Summary:	SMP kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra SMP dla zdalnej obs³ugi Linuksa za pomoc± podczerwieni
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	modutils >= 2.4.6-4
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
Requires(post,postun):	/sbin/depmod
Requires:	%{name} = %{version}-%{_rel}
Requires:	modutils >= 2.4.6-4
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

%package	remotes
Summary:	Lirc remotes database
Summary(pl):	Baza pilotów obs³ugiwanych przez lirc
Group:		Documentation
Requires:	%{name} = %{version}-%{_rel}

%description remotes
This package contains configuration files for many remotes supported
by lirc.

%description remotes -l pl
Ten pakiet zawiera pliki konfiguracyjne dla wielu pilotów
obs³ugiwanych przez lirc.

%prep
%setup -q -a 1 -n %{name}-%{version}pre3
%patch0 -p1
%patch1 -p1
#%patch2 -p1
%if %{without svga}
%patch3 -p1
%endif
%patch4 -p1
%if %{with kernel}
if grep -qs 'I2C_VERSION.*"2\.8\.' %{_kernelsrcdir}/include/linux/i2c.h ; then
%patch5 -p0
fi
%endif
%patch6 -p1

%build
echo '#' > drivers/Makefile.am
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoheader}
%{__autoconf}

%configure \
	ac_cv_header_portaudio_h=no \
	--with-kerneldir=%{_kernelsrcdir} \
	%{?with_x:--with-x} \
	--with-port=0x2f8 \
	--with-irq=3 \
	--without-soft-carrier \
	--with-driver=serial
%{__make}

%if %{with kernel}
cd drivers

for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	drivers=%{drivers}
	for drv in $drivers; do
		if [ "$drv" == "lirc_parallel" ] && [ "$cfg" == "smp" ]; then
			echo "lirc_parallel is not smp safe"
		else
		cd $drv
		if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
			exit 1
		fi
		#rm -rf include
		install -d include/{linux,config}
		ln -sf %{_kernelsrcdir}/config-$cfg .config
		ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
		[ ! -L include/asm ] && ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
		ln -sf %{_kernelsrcdir}/Module.symvers-$cfg Module.symvers
		%if %{without dist_kernel}
			ln -sf %{_kernelsrcdir}/scripts
		%endif
		touch include/config/MARKER
		%{__make} clean \
			RCS_FIND_IGNORE="-name '*.ko' -o" \
			M=$PWD O=$PWD \
			%{?with_verbose:V=1}
		%{__make} \
			M=$PWD O=$PWD \
			%{?with_verbose:V=1}
		mv $drv{,-$cfg}.ko
		cd ../
		fi
	done
done
cd ../

%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_aclocaldir},/dev,/var/log} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%if %{with kernel}
drivers=%{drivers}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
for drv in $drivers; do
	install drivers/$drv/$drv-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
		$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/$drv.ko
	%if %{with smp} && %{with dist_kernel}
		if [ ! "$drv" == "lirc_parallel" ]; then
			install drivers/$drv/$drv-smp.ko \
				$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/$drv.ko
		fi
	%endif
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

%post	-n kernel-char-lirc-atiusb
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_atiusb' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-char-lirc-atiusb
%depmod %{_kernel_ver}

%post	-n kernel-char-lirc-bt829
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_bt829' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-char-lirc-bt829
%depmod %{_kernel_ver}

%post	-n kernel-char-lirc-cmdir
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_cmdir' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-char-lirc-cmdir
%depmod %{_kernel_ver}

%post	-n kernel-char-lirc-dev
%depmod %{_kernel_ver}

%postun	-n kernel-char-lirc-dev
%depmod %{_kernel_ver}

%post	-n kernel-char-lirc-gpio
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_gpio' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-char-lirc-gpio
%depmod %{_kernel_ver}

%post	-n kernel-char-lirc-i2c
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_i2c' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-char-lirc-i2c
%depmod %{_kernel_ver}

%post	-n kernel-char-lirc-igorplugusb
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_igorplugusb' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-char-lirc-igorplugusb
%depmod %{_kernel_ver}

%post	-n kernel-char-lirc-imon
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_imon' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-char-lirc-imon
%depmod %{_kernel_ver}

%post	-n kernel-char-lirc-it87
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_it87' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-char-lirc-it87
%depmod %{_kernel_ver}

%post	-n kernel-char-lirc-mceusb
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_mceusb' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-char-lirc-mceusb
%depmod %{_kernel_ver}

%post	-n kernel-char-lirc-sasem
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_sasem' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-char-lirc-sasem
%depmod %{_kernel_ver}

%post	-n kernel-char-lirc-serial
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_serial' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-char-lirc-serial
%depmod %{_kernel_ver}

%post	-n kernel-char-lirc-streamzap
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_streamzap' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-char-lirc-streamzap
%depmod %{_kernel_ver}

%post	-n kernel-char-lirc-parallel
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_parallel' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-char-lirc-parallel
%depmod %{_kernel_ver}

%post	-n kernel-char-lirc-sir
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_sir' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-char-lirc-sir
%depmod %{_kernel_ver}

%post	-n kernel-smp-char-lirc-atiusb
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_atiusb' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-smp-char-lirc-atiusb
%depmod %{_kernel_ver}

%post	-n kernel-smp-char-lirc-bt829
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_bt829' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-smp-char-lirc-bt829
%depmod %{_kernel_ver}

%post	-n kernel-smp-char-lirc-cmdir
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_cmdir' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-smp-char-lirc-cmdir
%depmod %{_kernel_ver}

%post	-n kernel-smp-char-lirc-dev
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-char-lirc-dev
%depmod %{_kernel_ver}smp

%post	-n kernel-smp-char-lirc-gpio
%depmod %{_kernel_ver}smp
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_gpio' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-smp-char-lirc-gpio
%depmod %{_kernel_ver}smp

%post	-n kernel-smp-char-lirc-i2c
%depmod %{_kernel_ver}smp
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_i2c' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-smp-char-lirc-i2c
%depmod %{_kernel_ver}smp

%post	-n kernel-smp-char-lirc-igorplugusb
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_igorplugusb' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-smp-char-lirc-igorplugusb
%depmod %{_kernel_ver}

%post	-n kernel-smp-char-lirc-imon
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_imon' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-smp-char-lirc-imon
%depmod %{_kernel_ver}

%post	-n kernel-smp-char-lirc-it87
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_it87' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-smp-char-lirc-it87
%depmod %{_kernel_ver}

%post	-n kernel-smp-char-lirc-mceusb
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_mceusb' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-smp-char-lirc-mceusb
%depmod %{_kernel_ver}

%post	-n kernel-smp-char-lirc-sasem
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_sasem' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-smp-char-lirc-sasem
%depmod %{_kernel_ver}

%post	-n kernel-smp-char-lirc-serial
%depmod %{_kernel_ver}smp
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_serial' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-smp-char-lirc-serial
%depmod %{_kernel_ver}smp

%post	-n kernel-smp-char-lirc-streamzap
%depmod %{_kernel_ver}
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_streamzap' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-smp-char-lirc-streamzap
%depmod %{_kernel_ver}

%post	-n kernel-smp-char-lirc-parallel
%depmod %{_kernel_ver}smp
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_parallel' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-smp-char-lirc-parallel
%depmod %{_kernel_ver}smp

%post	-n kernel-smp-char-lirc-sir
%depmod %{_kernel_ver}smp
if [ "$1" = "1" ]; then
	echo "Don't forget to add an 'alias lirc lirc_sir' line"
	echo "to your /etc/modules.conf."
fi

%postun	-n kernel-smp-char-lirc-sir
%depmod %{_kernel_ver}smp

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
%files -n kernel-char-lirc-atiusb
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_atiusb*

%files -n kernel-char-lirc-bt829
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_bt829*

%files -n kernel-char-lirc-cmdir
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_cmdir*

%files -n kernel-char-lirc-dev
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_dev*

%files -n kernel-char-lirc-gpio
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_gpio*

%files -n kernel-char-lirc-i2c
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_i2c*

%files -n kernel-char-lirc-igorplugusb
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_igorplugusb*

%files -n kernel-char-lirc-imon
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_imon*

%files -n kernel-char-lirc-it87
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_it87*

%files -n kernel-char-lirc-mceusb
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_mceusb*

%files -n kernel-char-lirc-sasem
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_sasem*

%files -n kernel-char-lirc-serial
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_serial*

%files -n kernel-char-lirc-streamzap
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_streamzap*

%files -n kernel-char-lirc-parallel
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_parallel*

%files -n kernel-char-lirc-sir
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/*/lirc_sir*

%files -n kernel-smp-char-lirc-atiusb
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/lirc_atiusb*

%files -n kernel-smp-char-lirc-bt829
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/lirc_bt829*

%files -n kernel-smp-char-lirc-cmdir
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/lirc_cmdir*

%files -n kernel-smp-char-lirc-dev
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/lirc_dev*

%files -n kernel-smp-char-lirc-gpio
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/lirc_gpio*

%files -n kernel-smp-char-lirc-i2c
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/lirc_i2c*

%files -n kernel-smp-char-lirc-igorplugusb
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/lirc_igorplugusb*

%files -n kernel-smp-char-lirc-imon
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/lirc_imon*

%files -n kernel-smp-char-lirc-it87
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/lirc_it87*

%files -n kernel-smp-char-lirc-mceusb
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/lirc_mceusb*

%files -n kernel-smp-char-lirc-sasem
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/lirc_sasem*

%files -n kernel-smp-char-lirc-serial
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/lirc_serial*

%files -n kernel-smp-char-lirc-streamzap
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/*/lirc_streamzap*

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
