Summary:	Utilities for Cyclades-Z and Cyclom-Y asynchronous multiport boards
Summary(pl):	Narzêdzia dla asynchronicznych kart wieloportowych Cyclades-Z i Cyclom-Y
Name:		cyc_async
Version:	6.6.1
Release:	1
License:	GPL
Group:		Applications/Networking
# "stable": ftp://ftp.cyclades.com/pub/cyclades/async/linux/%{name}-659.tgz
Source0:	ftp://ftp.cyclades.com/pub/cyclades/async/linux/beta/%{name}-%{version}.tgz
Patch0:		%{name}-system-libpci.patch
Patch1:		%{name}-cyzfirm-path.patch
URL:		http://www.cyclades.com/
BuildRequires:	pciutils-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Utilities for Cyclades-Z and Cyclom-Y asynchronous multiport boards.

%description -l pl
Narzêdzia dla asynchronicznych kart wieloportowych Cyclades-Z i
Cyclom-Y.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
cd common
# avoid using precompiled versions
rm -f pciutils.h cyclades-z/{lib,pciutils.h}
%{__make} clean
%{__make} clean -C cyclades-z
%{__make} clean -C cyclom-y

%{__make} \
	CC="%{__cc}" \
	OPT="%{rpmcflags} %{!?debug:-fomit-frame-pointer} -I/usr/include/pci"

%{__make} -C cyclades-z \
	CC="%{__cc}" \
	OPT="%{rpmcflags} %{!?debug:-fomit-frame-pointer} -I/usr/include/pci"

%{__make} -C cyclom-y \
	CC="%{__cc}" \
	OPT="%{rpmcflags} %{!?debug:-fomit-frame-pointer} -I/usr/include/pci"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_datadir}/cyc_async}

cd common
install cylines cyclades-z/{cyzload,cyzutil} cyclom-y/cyyutil \
	$RPM_BUILD_ROOT%{_sbindir}
install cyclades-z/cyzfirm.bin $RPM_BUILD_ROOT%{_datadir}/cyc_async

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_sbindir}/*
%{_datadir}/%{name}
