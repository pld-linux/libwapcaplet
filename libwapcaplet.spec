#
# Conditional build:
%bcond_without	static_libs	# don't build static library

Summary:	String internment library
Summary(pl.UTF-8):	Biblioteka do więzienia łańcuchów znaków
Name:		libwapcaplet
Version:	0.3.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://download.netsurf-browser.org/libs/releases/%{name}-%{version}-src.tar.gz
# Source0-md5:	aa39f3b2c0066d385797d06be6cae49a
URL:		http://www.netsurf-browser.org/projects/libwapcaplet/
BuildRequires:	netsurf-buildsystem >= 1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibWapcaplet is a string internment library, written in C. It provides
reference counted string internment and rapid string comparison
functionality. It was developed as part of the NetSurf project and is
available for use by other software under the MIT licence.

%description -l pl.UTF-8
LibWapcaplet to napisana w C biblioteka do więzienia łańcuchów znaków.
Umożliwia więzienie łańcuchów ze zliczaniem odwołań oraz ekspresowe
porównywanie. Biblioteka powstała jako część projektu NetSurf i może
być używana w innych programach na licencji MIT.

%package devel
Summary:	libwapcaplet library headers
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libwapcaplet
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the include files and other resources you can
use to incorporate libwapcaplet into applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe pozwalające na używanie biblioteki libwapcaplet w
swoich programach.

%package static
Summary:	libwapcaplet static library
Summary(pl.UTF-8):	Statyczna biblioteka libwapcaplet
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This is package with static libwapcaplet library.

%description static -l pl.UTF-8
Statyczna biblioteka libwapcaplet.

%prep
%setup -q

%build
export CC="%{__cc}"
export CFLAGS="%{rpmcflags} %{rpmcppflags}"
export LDFLAGS="%{rpmldflags}"
export AR="%{__ar}"

%{__make} \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-shared

%if %{with static_libs}
%{__make} \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-static
%endif

%install
rm -rf $RPM_BUILD_ROOT

export CC="%{__cc}"
export CFLAGS="%{rpmcflags} %{rpmcppflags}"
export LDFLAGS="%{rpmldflags}"
export AR="%{__ar}"

%{__make} install \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-shared \
	DESTDIR=$RPM_BUILD_ROOT \

%if %{with static_libs}
%{__make} install \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-static \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README
%attr(755,root,root) %{_libdir}/libwapcaplet.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwapcaplet.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwapcaplet.so
%{_includedir}/libwapcaplet
%{_pkgconfigdir}/libwapcaplet.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libwapcaplet.a
%endif
