Summary:	Linux Infrared Remote Control
Summary(pl):	Zdalna kontrola Linuxa za pomoc± podczerwieni
Name:		lirc
Version:	0.6.3 
Release:	2@%{_kernel_ver}
Source0:	http://download.sourceforge.net/LIRC/%{name}-%{version}.tar.gz
Source1:	%{name}-mksocket.c
Source2:	%{name}.sysconfig
Source3:	%{name}d.init
Source4:	%{name}md.init
Patch0:		%{name}-userbuild.patch
Patch1:		%{name}-opt.patch
Patch2:		%{name}-anydriver.patch
Patch3:		%{name}-foo.patch
Patch4:		%{name}-spinlock.patch
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
%conflicts_kernel_ver

%define		_x11bindir	%{_prefix}/X11R6/bin

%description
LIRC is a package that allows you to decode and send infra-red signals
of many (but not all) commonly used remote controls.

%description -l pl
LIRC to program pozwalaj±cy na dekodowanie nadchodz±cych oraz
wysy³anie sygna³ów w podczerwieni za pomoc± wielu (ale nie wszystkich)
popularnych urz±dzeñ do zdalnej kontroli

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
cp %{SOURCE1} mksocket.c
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
rm -f missing
libtoolize --copy --force
aclocal
automake -a -c
autoconf

# <Ugly part of this spec>
mkdir kernel && cd kernel
ln -s %{_prefix}/src/linux/* .
rm include scripts
cp -a %{_prefix}/src/linux/{.[^.]*,include,scripts} .
cd ..
# </Ugly>

%configure \
	--with-driver=any \
	--with-kerneldir=$(pwd)/kernel \
	--with-x \
	--with-port=0x2f8 \
	--with-irq=3 \
	--without-soft-carrier
#./config.status
%{__make} -C kernel oldconfig </dev/null
%{__make} HOSTCC=kgcc
gcc mksocket.c -o mksocket

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
mknod $RPM_BUILD_ROOT/dev/lircm p
./mksocket $RPM_BUILD_ROOT/dev/lircd
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
/sbin/depmod -a
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
echo "If you are using a kernel-module-based driver, don't forget to add an"
echo "'alias lirc <your_driver>' line to your /etc/modules.conf. See"
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

%postun
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/*
%config %{_sysconfdir}/sysconfig/*
%config %{_sysconfdir}/*.conf
/lib/modules/*/*/*
%attr(660,root,root) /dev/lircm
%ghost %attr(660,root,root) /dev/lircd
%ghost %attr(600,root,root) %{_localstatedir}/log/lircd
%{_datadir}/lircmd
%doc *.gz remotes/remotes contrib/*.gz
%doc doc/*.gz doc/doc.html doc/html doc/images

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
