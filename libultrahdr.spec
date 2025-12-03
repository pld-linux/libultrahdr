# TODO: actually package java part, then enable bcond by default
#
# Conditional build:
%bcond_with	java	# Java interface (JNI wrapper+Java classes)
#
Summary:	Library for encoding and decoding ultrahdr images
Summary(pl.UTF-8):	Biblioteka do kodowania i dekodowania obrazów ultrahdr
Name:		libultrahdr
Version:	1.4.0
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/google/libultrahdr/releases
Source0:	https://github.com/google/libultrahdr/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ddfbb3e6ff777d62f2d696d644c90a72
Patch0:		%{name}-opt.patch
URL:		https://github.com/google/libultrahdr
BuildRequires:	cmake >= 3.15
%{?with_java:BuildRequires:	jdk}
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libultrahdr is an image compression library that uses gain map
technology to store and distribute HDR images. Conceptually on the
encoding side, the library accepts SDR and HDR rendition of an image
and from these a Gain Map (quotient between the two renditions) is
computed. The library then uses backward compatible means to store the
base image (SDR), gain map image and some associated metadata. Legacy
readers that do not support handling the gain map image and/or
metadata, will display the base image. Readers that support the format
combine the base image with the gain map and render a high dynamic
range image on compatible displays.

%description -l pl.UTF-8
libultrahdr to biblioteka kompresji obrazu, wykorzystująca technikę
mapy wzmocnień do przechowywania i dystrybucji obrazów HDR.
Koncepcyjnie po stronie kodowania biblioteka przyjmuje wersje SDR oraz
HDR obrazu i wylicza z nich mapę wzmocnień (współczynnik między dwoma
wersjami). Następnie wykorzystując wstecznie zgodne metody zapisuje
obraz podstawowy (SDR), obraz mapy wzmocnień oraz trochę powiązanych
metadanych. Starsze czytniki, nie obsługujące obrazu mapy wzmocnień
i/lub metadanych, wyświetlą obraz podstawowy. Czytniki obsługujące
format połączą obraz podstawowy z mapą wzmocnień i na zgodnym ekranie
wyświetlą obraz HDR.

%package devel
Summary:	Header files for libuhdr library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libuhdr
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libjpeg-devel

%description devel
Header files for libuhdr library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libuhdr.

%package static
Summary:	Static libuhdr library
Summary(pl.UTF-8):	Statyczna biblioteka libuhdr
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libuhdr library.

%description static -l pl.UTF-8
Statyczna biblioteka libuhdr.

%prep
%setup -q
%patch -P0 -p1

%build
# .pc file generation expects relative INCLUDEDIR/LIBDIR
%cmake -B build \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	%{?with_java:-DUHDR_BUILD_JAVA=ON}

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc DESCRIPTION README.md
%attr(755,root,root) %{_bindir}/ultrahdr_app
%{_libdir}/libuhdr.so.*.*.*
%ghost %{_libdir}/libuhdr.so.1

%files devel
%defattr(644,root,root,755)
%{_libdir}/libuhdr.so
%{_includedir}/ultrahdr_api.h
%{_pkgconfigdir}/libuhdr.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libuhdr.a
