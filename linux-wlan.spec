Summary:	PCMCIA wireless microwave network card services
Summary(pl):	Obs³uga mikrofalowych kart sieciowych PCMCIA
Name:		linux-wlan
Version:	0.3.4
Release:	4
License:	MPL (Mozilla Public License)
Group:		Applications/System
Source0:	http://www.linux-wlan.com/linux-wlan/%{name}-%{version}.tar.gz
Patch0:		%{name}.pld.patch
URL:		http://www.linux-wlan.com/
Prereq:		pcmcia-cs
ExcludeArch:	sparc sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
The pcmcia-cs package adds microwave wirelless PCMCIA networks cards
handling support for your PLD-Linux system.

%description -l pl
Pakiet pcmcia-cs zawiera programy wspieraj±ce obs³ugê mikrofalowych
kart sieciowych PCMCIA w Twoim PLD-Linuksie.

%prep
%setup -q
%patch0 -p0

%build
%{__make} all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,%{_sysconfdir}/pcmcia}

install wlanctl/wlanctl $RPM_BUILD_ROOT/sbin
install wlandump/wlandump $RPM_BUILD_ROOT/sbin
install scripts/wla* $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia
install man/*.8 $RPM_BUILD_ROOT%{_mandir}/man8

mv -f $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/wlan.config /$RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/wlan.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/pcmcia ]; then
	/etc/rc.d/init.d/pcmcia restart 2> /dev/null
else
	echo "Run \"/rc.d/init.d/pcmcia start\" to start pcmcia cardbus daemon."
fi

%postun
if [ "$1" = "0" ]; then
	if [ -f /var/state/run/pcmcia ]; then
		/etc/rc.d/init.d/pcmcia restart 2> /dev/null
	fi
fi

%files
%defattr(644,root,root,755)
%doc SUPPORTED.CARDS CHANGES COPYING README FAQ.isa README.debug README.isa
%doc README.linuxppc README.wep TODO THANKS
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_sysconfdir}/pcmcia/wlan
%attr(644,root,root) %{_sysconfdir}/pcmcia/wlan.conf
%attr(600,root,root) %config %verify(not size mtime md5) %{_sysconfdir}/pcmcia/wlan.opts
%attr(600,root,root) %config %verify(not size mtime md5) %{_sysconfdir}/pcmcia/wlan.network.opts
%{_mandir}/man8/*
