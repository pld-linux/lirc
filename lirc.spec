Summary:	Linux Infrared Remote Control
Summary(pl):	Zdalna kontrola Linuxa za pomoc± podczerwieni
Name:		lirc
Version:	0.6.3
Release:	1
License:	GPL
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
URL:		http://www.lirc.org/
Source0:	http://www.lirc.org/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Patch0:		%{name}-userbuild.patch
Patch1:		%{name}-opt.patch
Patch2:		%{name}-spinlock.patch
Patch3:		%{name}-foo.patch
# BuildRequires:	kernel-sources
BuildRequires:	XFree86-devel
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	egcs
Prereq:		/sbin/depmod
Prereq:		/sbin/chkconfig
Prereq:		/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_x11bindir	%{_prefix}/X11R6/bin

%description
LIRC is a package that allows you to decode and send infra-red signals
of many (but not all) commonly used remote controls.

Former versions focussed on home-brew hardware connected to the serial
or parallel port. Descriptions how to build this hardware can be found
on the LIRC homepage.

%description -l pl
LIRC to program pozwalaj±cy na dekodowanie nadchodz±cych oraz
wysy³anie sygna³ów w podczerwieni za pomoc± wielu (ale nie wszystkich)
popularnych urz±dzeñ do zdalnej kontroli.

Wersja ta skupia siê na odbiornikach oraz nadajnichach domowej roboty
pod³±czanych do portu szeregowego lub równoleg³ego. Opisy jak zbudowaæ
odpowiednie odbiorniki i nadajniki znajduj± siê na stronie domowej
LIRC.

%package X11
Summary:	Linux Infrared Remote Control - X11 Utils
Summary(pl):	Zdalna kontrola Linuxa za pomoc± podczerwieni - X11
Group:		X11/Applications
Group(de):	Applikationen/System
Group(fr):	Development/Librairies
Group(pl):	Aplikacje/System

%description X11
Linux Infrared Remote Control - X11 Utils.

%description X11 -l pl
Zdalna kontrola Linuxa za pomoc± podczerwieni - Narzêdzia dla X11.

%package kernel
Summary:	Kernel modules with LIRC support
Summary(pl):	Modu³y kernela dodaj±ce wsparcie dla LIRC
Group:		Applications/System
Group(de):	Applikationen/System
Group(fr):	Development/Librairies
Group(pl):	Aplikacje/System

%description kernel
Kernel modules with LIRC support.

%description kernel -l pl
Modu³y kernela ze wsparciem dla LIRC.

%package devel
Summary:	Header files requied to develop licq plugins
Summary(pl):	Pliki nag³ówkowe konieczne przy tworzeniu programów z obs³ug± LIRC
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
Header files required to develop programs with LIRC support.

%description devel -l pl
Pliki nag³ówkowe niezbêdne do tworzenia programów ze wsparciem dla
LIRC.

%package static
Summary:	Static LIRC libraries
Summary(pl):	Biblioteki statyczne LIRC
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description static
Static LIRC libraries.

%description static -l pl
Statyczne biblioteki LIRC.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
rm missing
libtoolize --copy --force
aclocal
autoconf
automake -a -c

# <Ugly part of this spec>
mkdir kernel && cd kernel
cp -a %{_prefix}/src/linux/.* .
for file in %{_prefix}/src/linux/*; do
	ln -s $file .
done
rm include scripts
cp -a %{_prefix}/src/linux/include .
cp -a %{_prefix}/src/linux/scripts .
cd ..
# </Ugly>

# ttyS1 by default (COM2)
%configure \
	--with-kerneldir=$(pwd)/kernel \
	--with-x \
	--with-driver=serial \
	--with-major=61 \
	--with-port=0x2f8 \
	--with-irq=3 \
	--without-soft-carrier

%{__make} -C kernel oldconfig
%{__make} HOSTCC=kgcc

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_x11bindir}
install -d $RPM_BUILD_ROOT%{_aclocaldir}
install -d $RPM_BUILD_ROOT%{_var}/log
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install contrib/lircd.conf	$RPM_BUILD_ROOT%{_sysconfdir}
install contrib/lircmd.conf	$RPM_BUILD_ROOT%{_sysconfdir}
install contrib/*.m4		$RPM_BUILD_ROOT%{_aclocaldir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}

%{__make} DESTDIR=$RPM_BUILD_ROOT install

mv $RPM_BUILD_ROOT%{_bindir}/irxevent	$RPM_BUILD_ROOT%{_x11bindir}/irxevent
mv $RPM_BUILD_ROOT%{_bindir}/xmode2	$RPM_BUILD_ROOT%{_x11bindir}/xmode2

:> $RPM_BUILD_ROOT%{_var}/log/lircd

gzip -9nf ANNOUNCE AUTHORS ChangeLog NEWS README TODO doc/irxevent.keys
gzip -9nf remotes/generic/*.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post kernel
/sbin/depmod -a

%preun kernel
/sbin/depmod -a

%post
/sbin/ldconfig
/sbin/chkconfig --add %{name}
touch %{_var}/log/lircd
chmod 640 %{_var}/log/lircd

%postun
/sbin/ldconfig

%preun
if [ "$1" = "0" -a -f %{_var}/lock/subsys/%{name} ]; then
        %{_sysconfdir}/rc.d/init.d/%{name} stop 1>&2
fi
/sbin/chkconfig --del %{name}

%files
%defattr(644,root,root,755)
%doc *.gz doc/*.html doc/html doc/images doc/*.gz remotes/generic
%doc contrib/lircrc
%attr(755,root,root) %{_bindir}/irexec
%attr(755,root,root) %{_bindir}/irpty
%attr(755,root,root) %{_bindir}/irrecord
%attr(755,root,root) %{_bindir}/irw
%attr(755,root,root) %{_bindir}/mode2
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.conf
%attr(640,root,root) %ghost %{_var}/log/* 

%files X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_x11bindir}/irxevent
%attr(755,root,root) %{_x11bindir}/xmode2

%files kernel
%defattr(644,root,root,755)
/lib/modules/*/misc/*.o

%files devel
%defattr(644,root,root,755)
%{_includedir}/lirc
%{_aclocaldir}/*.m4
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
