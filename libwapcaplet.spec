#
# Conditional build:
%bcond_without	static_libs	# don't build static library

Summary:	String internment library
Name:		libwapcaplet
Version:	0.2.1
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://download.netsurf-browser.org/libs/releases/%{name}-%{version}-src.tar.gz
# Source0-md5:	c39048f10e99aab81a15022c500931d8
#Patch0:		lib.patch
URL:		http://www.netsurf-browser.org/projects/libwapcaplet/
BuildRequires:	netsurf-buildsystem >= 1.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibWapcaplet is a string internment library, written in C. It provides
reference counted string interment and rapid string comparison
functionality. It was developed as part of the NetSurf project and is
available for use by other software under the MIT licence.

%package devel
Summary:	libwapcaplet library headers
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libwapcaplet
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is the libraries, include files and other resources you can use
to incorporate libwapcaplet into applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe pozwalające na używanie biblioteki libwapcaplet w
swoich programach.

%package static
Summary:	libwapcaplet static libraries
Summary(pl.UTF-8):	Statyczne biblioteki libwapcaplet
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This is package with static libwapcaplet libraries.

%description static -l pl.UTF-8
Statyczna biblioteka libwapcaplet.

%prep
%setup -q
#%%patch0 -p1

%build
export CC="%{__cc}"
export CFLAGS="%{rpmcflags}"
export LDFLAGS="%{rpmldflags}"

%{__make} Q= \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-shared

%if %{with static_libs}
%{__make}  Q= \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-static
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install Q= \
	lib=%{_lib} \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-shared \
	DESTDIR=$RPM_BUILD_ROOT \

%if %{with static_libs}
%{__make} install Q= \
	lib=%{_lib} \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-static \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwapcaplet.so.*.*.*
%ghost %{_libdir}/libwapcaplet.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libwapcaplet.so
%{_includedir}/libwapcaplet
%{_pkgconfigdir}/libwapcaplet.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libwapcaplet.a
%endif

