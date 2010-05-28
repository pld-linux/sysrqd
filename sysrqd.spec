Summary:	Linux SysRq over network daemon
Name:		sysrqd
Version:	13
Release:	1
License:	GPL v2+
Group:		Applications/Networking
Source0:	http://julien.danjou.info/sysrqd/%{name}-%{version}.tar.xz
# Source0-md5:	0d7b17acc32679aba16d19f140e04f39
Source1:	%{name}.init
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
sysrqd is a small daemon intended to manage Linux SysRq over network.
Its philosophy is to be very responsive under heavy load and try to be
somehow reliable. Authentication is made by clear password.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/sysrqd

:> $RPM_BUILD_ROOT%{_sysconfdir}/sysrqd.secret
echo 0.0.0.0 > $RPM_BUILD_ROOT%{_sysconfdir}/sysrqd.bind

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add sysrqd
%service sysrqd restart "sysrqd daemon"

%preun
if [ "$1" = "0" ]; then
	%service sysrqd stop
	/sbin/chkconfig --del sysrqd
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog INSTALL README
%attr(755,root,root) %{_sbindir}/sysrqd
%attr(754,root,root) /etc/rc.d/init.d/sysrqd
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sysrqd.*
