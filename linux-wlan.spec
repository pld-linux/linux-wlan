Summary:	PCMCIA wireless microwave network card services
Summary(pl):	Obs³uga mikrofalowych kart sieciowych PCMCIA
Name:		linux-wlan
Version:	0.3.4
Release:	1
License:	MPL (Mozilla Public License)
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Source0:	http://www.linux-wlan.com/linux-wlan/%{name}-%{version}.tar.gz
Patch0:		%{name}.pld.patch
URL:		http://www.linux-wlan.com/
Requires:	pcmcia-cs
ExcludeArch:	sparc sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The pcmcia-cs package adds microwave wirelless PCMCIA networks cards
handling support for your PLD-Linux system.

%description -l pl
Pakiet pcmcia-cs zawiera programy wspieraj±ce obs³ugê mikrofalowych
kart sieciowych PCMCIA w Twoim PLD-Linuxie.

%prep
%setup -q
%patch0 -p0

%build

%{__make} all 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/sbin
install -d $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia
install -d $RPM_BUILD_ROOT%{_mandir}/man8
install wlanctl/wlanctl $RPM_BUILD_ROOT/sbin
install wlandump/wlandump $RPM_BUILD_ROOT/sbin
install scripts/wla* $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia
install man/*.8 $RPM_BUILD_ROOT%{_mandir}/man8
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/wlan.config /$RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/wlan.conf

gzip -9nf SUPPORTED.CARDS CHANGES COPYING README \
	FAQ.isa README.debug README.isa README.linuxppc \
	README.wep TODO THANKS 

%clean
rm -rf $RPM_BUILD_ROOT

%post
NAME=pcmcia; DESC="pcmcia cardbus daemon"; %chkconfig_add

%preun
NAME=pcmcia; %chkconfig_del

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) /sbin/*

%attr(755,root,root) %{_sysconfdir}/pcmcia/wlan
%attr(644,root,root) %{_sysconfdir}/pcmcia/wlan.conf
%attr(600,root,root) %config %verify(not size mtime md5) %{_sysconfdir}/pcmcia/wlan.opts
%attr(600,root,root) %config %verify(not size mtime md5) %{_sysconfdir}/pcmcia/wlan.network.opts
%{_mandir}/man8/*
