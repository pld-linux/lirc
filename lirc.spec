%define		_kernel_ver %(grep UTS_RELEASE /usr/src/linux/include/linux/version.h 2>/dev/null | cut -d'"' -f2)
%define		smpstr	%{?_with_smp:smp}%{!?_with_smp:up}
%define		smp	%{?_with_smp:1}%{!?_with_smp:0}

Summary:	Linux Infrared Remote Control daemons
Summary(pl):	Serwery do zdalnej kontroli Linuxa za pomoc± podczerwieni
Name:		lirc
Version:	0.6.3 
Release:	2
Source0:	http://download.sourceforge.net/LIRC/%{name}-%{version}.tar.gz
Source2:	%{name}.sysconfig
Source3:	%{name}d.init
Source4:	%{name}md.init
Patch0:		%{name}-userbuild.patch
Patch1:		%{name}-opt.patch
Patch2:		%{name}-anydriver.patch
Patch3:		%{name}-foo.patch
Patch4:		%{name}-spinlock.patch
Patch5:		%{name}-tmp.patch
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
Prereq:		/sbin/depmod
Prereq:		chkconfig
Requires:	dev >= 2.8.0-3
Requires:	modutils >= 2.4.6-4
Conflicts:	kernel < %{_kernel_ver}, kernel > %{_kernel_ver}
# didn't use /tmp/.lircd
Conflicts:	lirc-libs < 0.6.3-3

%define		_x11bindir	%{_prefix}/X11R6/bin

%description
LIRC is a package that allows you to decode and send infra-red signals
of many (but not all) commonly used remote controls.

%description -l pl
LIRC to program pozwalaj±cy na dekodowanie nadchodz±cych oraz
wysy³anie sygna³ów w podczerwieni za pomoc± wielu (ale nie wszystkich)
popularnych urz±dzeñ do zdalnej kontroli

%package modules-%{smpstr}
Summary:	Kernel modules for Linux Infrared Remote Control
Summary(pl):	Modu³y j±dra dla zdalnej obs³ugi Linuxa za pomoc± podczerwieni
Group:		Base/Kernel
Release:	%{release}@%{_kernel_ver}
Provides:	lirc-modules = %{version}

%description modules-%{smpstr}
This package contains the kernel modules necessary to operate some 
infrared remote control devices (such as the ones bundled with TV cards).

%description modules-%{smpstr} -l pl
Ten pakiet zawiera modu³y j±dra niezbêdne do obs³ugi niektórych pilotów na 
podczerwieñ (w tym tych dostarczanych z kartami TV).

%package X11
Summary:	Linux Infrared Remote Control - X11 utilities
Summary(pl):	Zdalna kontrola Linuxa za pomoc± podczerwieni - narzêdzia X11
Group:		X11/Applications
Group(de):	X11/Applikationen
Group(pl):	X11/Aplikacje

%description X11
Linux Infrared Remote Control - X11 utilities.

%description X11 -l pl
Zdalna kontrola Linuxa za pomoc± podczerwieni - narzêdzia X11.

%package libs
Summary:	LIRC libraries
Summary(pl):	Biblioteki LIRC
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
# didn't use /tmp/.lircd
Conflicts:	lirc < 0.6.3-3

%description libs
This package provides the libraries necessary to run lirc client
programs.

%description libs -l pl
Ten pakiet zawiera biblioteki niezbêdne do dzia³ania klientów LIRC.

%package devel
Summary:	Header and library files for LIRC development
Summary(pl):	Pliki nag³ówkowe i biblioteki dla tworzenia programów z obs³ug± LIRC
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-libs = %{version}

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
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description static
The files necessary for development of statically-linked lirc-based
programs.

%description static -l pl
Pliki potrzebne do tworzenia ³±czonych statycznie programów opartych
na LIRC.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
echo '#' > drivers/Makefile.am
rm -f missing
libtoolize --copy --force
aclocal
automake -a -c
autoconf

%configure \
	--with-driver=any \
	--with-kerneldir=/usr/src/linux \
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
	-DIRCTL_DEV_MAJOR=61 -I.. -I/usr/src/linux/include \
	-fno-strict-aliasing -fno-common \
	-c -o $drv/$drv.o $drv/$drv.c || true
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT/dev
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{rc.d/init.d,sysconfig}
install -d $RPM_BUILD_ROOT%{_datadir}/lircmd
install -d $RPM_BUILD_ROOT%{_x11bindir}
install -d $RPM_BUILD_ROOT%{_aclocaldir}
install -d $RPM_BUILD_ROOT%{_localstatedir}/log
%{__make} install DESTDIR=$RPM_BUILD_ROOT \
	sysconfdir=$RPM_BUILD_ROOT%{_sysconfdir}

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install -m644 drivers/*/*.o $RPM_BUILD_ROOT/lib/modules/*/misc

cat remotes/*/lircd.conf.* > $RPM_BUILD_ROOT%{_sysconfdir}/lircd.conf
cp remotes/*/lircmd.conf.* $RPM_BUILD_ROOT%{_datadir}/lircmd
install contrib/*.m4 $RPM_BUILD_ROOT%{_aclocaldir}
mv $RPM_BUILD_ROOT%{_bindir}/{irxevent,xmode2} $RPM_BUILD_ROOT%{_x11bindir}
:> $RPM_BUILD_ROOT%{_localstatedir}/log/lircd

ln -s %{_localstatedir}/state/lircmd.conf $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/lirc
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/lircd
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/lircmd

gzip -9nf ANNOUNCE AUTHORS DRIVERS NEWS README TODO doc/irxevent.keys
gzip -9nf remotes/generic/*.conf contrib/lircrc
mv remotes/generic remotes/remotes

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
echo "install the lirc-modules-up or lirc-modules-smp package. See"
echo "%{_docdir}/%{name}-%{version}/DRIVERS.gz for details."

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

%post modules-%{smpstr}
/sbin/depmod -a
echo "Don't forget to add an 'alias lirc <your_driver>' line to your 
echo "/etc/modules.conf."

%postun modules-%{smpstr}
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/*
%config %{_sysconfdir}/sysconfig/*
%config %{_sysconfdir}/*.conf
%ghost %attr(600,root,root) %{_localstatedir}/log/lircd
%{_datadir}/lircmd
%doc *.gz remotes/remotes contrib/*.gz
%doc doc/*.gz doc/doc.html doc/html doc/images

%files modules-%{smpstr}
%defattr(644,root,root,755)
/lib/modules/*/*/*

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
