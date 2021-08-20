%global __cmake_in_source_build 1
%global real_name SVT-VP9

Name:           svt-vp9
Version:        0.3.0
Release:        2%{?dist}
Summary:        Scalable Video Technology for VP9 Encoder
License:        BSD-2-Clause-Patent
URL:            https://github.com/OpenVisualCloud/%{real_name}

Source0:        %{url}/archive/v%{version}/%{real_name}-%{version}.tar.gz
# Build GStreamer plugin from tree directly
Patch0:         %{name}-gst.patch

BuildRequires:  cmake3
BuildRequires:  meson
BuildRequires:  pkgconfig(gstreamer-1.0) >= 1.8
BuildRequires:  pkgconfig(gstreamer-base-1.0) >= 1.8
BuildRequires:  pkgconfig(gstreamer-video-1.0) >= 1.8
BuildRequires:  yasm

%if 0%{?rhel} == 7
BuildRequires:  devtoolset-8-gcc
%else
BuildRequires:  gcc
%endif

ExclusiveArch:  x86_64

%description
The Scalable Video Technology for VP9 Encoder (SVT-VP9 Encoder) is a VP9
compliant encoder library core. The SVT-VP9 Encoder development is a work in
progress targeting performance levels applicable to both VOD and Live
encoding/transcoding video applications.

%package        libs
Summary:        %{name} libraries

%description    libs
Scalable Video Technology for VP9 Encoder (SVT-VP9 Encoder) libraries.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{real_name}.

%package -n     gstreamer1-%{name}
Summary:        GStreamer 1.0 %{real_name} plug-in
Requires:       gstreamer1-plugins-base%{?_isa} >= 1.8

%description -n gstreamer1-%{name}
This package provides an %{real_name} based GStreamer plug-in.

%prep
%autosetup -p1 -n %{real_name}-%{version}

%build
%if 0%{?rhel} == 7
. /opt/rh/devtoolset-8/enable
%endif

# Do not use 'Release' build or it hardcodes compiler settings:
%cmake3 -G Ninja -DCMAKE_BUILD_TYPE='Fedora'
%ninja_build

pushd gstreamer-plugin
export LIBRARY_PATH="$PWD/../Bin/Fedora:$LIBRARY_PATH"
%meson
%meson_build
popd

%install
%ninja_install
pushd gstreamer-plugin
%meson_install
popd

%files
%{_bindir}/SvtVp9EncApp

%files libs
%license LICENSE.md
%doc README.md Docs
%{_libdir}/libSvtVp9Enc.so.1*

%files devel
%{_includedir}/svt-vp9
%{_libdir}/libSvtVp9Enc.so
%{_libdir}/pkgconfig/SvtVp9Enc.pc

%files -n gstreamer1-%{name}
%{_libdir}/gstreamer-1.0/libgstsvtvp9enc.so

%changelog
* Fri Aug 20 2021 Simone Caronni <negativo17@gmail.com> - 0.3.0-2
- Bump version to replace the EPEL package.

* Thu Nov 26 2020 Simone Caronni <negativo17@gmail.com> - 0.3.0-1
- First build, make it build also on CentOS/RHEL 7 with rebased GStreamer.
