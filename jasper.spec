# based on PLD Linux spec git://git.pld-linux.org/packages/.git
Summary:	JasPer - collection of software for coding and manipulation of images
Name:		jasper
Version:	1.900.1
Release:	16
License:	BSD-like
Group:		Libraries
Source0:	http://www.ece.uvic.ca/~mdadams/jasper/software/%{name}-%{version}.zip
# Source0-md5:	a342b2b4495b3e1394e161eb5d85d754
Patch0:		%{name}-jpc_dec.c.patch
Patch1:		%{name}-tepsizes-overflow.patch
Patch2:		%{name}-CVE-2008-3520.patch
Patch3:		%{name}-CVE-2008-3522.patch
URL:		http://www.ece.uvic.ca/~mdadams/jasper/
BuildRequires:	OpenGL-glut-devel >= 3.7
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libjpeg-devel
BuildRequires:	libtool
BuildRequires:	unzip
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JasPer is a collection of software (i.e., a library and application
programs) for the coding and manipulation of images. This software can
handle image data in a variety of formats. One such format supported
by JasPer is the JPEG-2000 code stream format defined in ISO/IEC
15444-1:2000 (but JasPer contains only partial implementation).

%package libs
Summary:	JasPer library
Group:		Libraries

%description libs
JasPer library.

%package devel
Summary:	JasPer - header files
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description devel
Header files needed to compile programs with libjasper.

%package jiv
Summary:	JasPer Image Viewer
Group:		X11/Applications/Graphics
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description jiv
Simple JasPer Image Viewer. Basic pan and zoom functionality is
provided. Components of an image may be viewed individually. Color
components may also be viewed together as a composite image. At
present, the jiv image viewer has only trivial support for color. It
recognizes RGB and YCbCr color spaces, but does not use tone
reproduction curves and the like in order to accurately reproduce
color. For basic testing purposes, however, the color reproduction
should suffice.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# not used
%{__sed} -i -e 's| -lXmu -lXi -lXext -lXt | |' configure.ac

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static \
	--enable-shared
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# nothing interesting
rm -f $RPM_BUILD_ROOT%{_bindir}/tmrdemo

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE NEWS README doc/jasper.pdf doc/jpeg2000.pdf
%attr(755,root,root) %{_bindir}/img*
%attr(755,root,root) %{_bindir}/jasper
%{_mandir}/man1/img*.1*
%{_mandir}/man1/jasper.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libjasper.so.?
%attr(755,root,root) %{_libdir}/libjasper.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjasper.so
%{_libdir}/libjasper.la
%{_includedir}/jasper

%files jiv
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/jiv
%{_mandir}/man1/jiv.1*

