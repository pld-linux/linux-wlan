Summary:	PCMCIA wireless microwave network card services
Summary(pl.UTF-8):   Obsługa mikrofalowych kart sieciowych PCMCIA
Name:		linux-wlan
Version:	0.3.4
Release:	5
License:	MPL
Group:		Applications/System
Source0:	http://www.linux-wlan.com/linux-wlan/%{name}-%{version}.tar.gz
# Source0-md5:	47fb22cb5ca497eaa6bc51eed2056929
Patch0:		%{name}.pld.patch
URL:		http://www.linux-wlan.com/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	pcmcia-cs
ExcludeArch:	sparc sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
The pcmcia-cs package adds microwave wirelless PCMCIA networks cards
handling support for your PLD-Linux system.

%description -l pl.UTF-8
Pakiet pcmcia-cs zawiera programy wspierające obsługę mikrofalowych
kart sieciowych PCMCIA w Twoim PLD-Linuksie.

%prep
%setup -q
%patch0 -p0

%build
%{__make} all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,%{_sysconfdir}/pcmcia}

install wlanctl/wlanctl $RPM_BUILD_ROOT%{_sbindir}
install wlandump/wlandump $RPM_BUILD_ROOT%{_sbindir}
install scripts/wla* $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia
install man/*.8 $RPM_BUILD_ROOT%{_mandir}/man8

mv -f $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/wlan.config /$RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/wlan.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service pcmcia restart "pcmcia cardbus daemon"

%postun
if [ "$1" = "0" ]; then
	%service pcmcia restart
fi

%files
%defattr(644,root,root,755)
%doc SUPPORTED.CARDS CHANGES COPYING README FAQ.isa README.debug README.isa
%doc README.linuxppc README.wep TODO THANKS
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_sysconfdir}/pcmcia/wlan
%{_sysconfdir}/pcmcia/wlan.conf
%attr(600,root,root) %config %verify(not md5 mtime size) %{_sysconfdir}/pcmcia/wlan.opts
%attr(600,root,root) %config %verify(not md5 mtime size) %{_sysconfdir}/pcmcia/wlan.network.opts
%{_mandir}/man8/*
