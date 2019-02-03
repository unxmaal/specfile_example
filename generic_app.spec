%define _topdir     %(echo $PWD)
%define distro      %(echo ${distro}${dver})
%define arch        %(echo $arch)
%define oname       %(echo $oname)
%define _tmppath    %_topdir/tmp
%define fullver     %(echo $genapp_name)
%define pkgver      %(echo $genapp_name | cut -d'.' -f1,2)
%define version     %(echo $genapp_name | cut -d'.' -f3)
%define d_pkgver    %(echo %pkgver | tr '.' '_')
%define release     %(echo $BUILD_NUMBER)

%define name        genapp_%{d_pkgver}
%define _tmppath    %_topdir/tmp
%define buildroot   %{_topdir}/%{name}-root
%define _build_name_fmt %%{ARCH}/%%{NAME}-%{version}-%{release}.%{distro}.%%{ARCH}.rpm

%define gendep_name         %(echo $apr_name)

%define gendep_ver          %(echo $apr_ver)


BuildRoot:      %{buildroot}
Name:           %{name}
Release:        %{release}
Version:        %{version}
Summary:        Generic App
AutoReqProv:    no
Requires:       %{gendep_name}-%{gendep_ver}
Provides:       %{name}-%{version}-%{release}


Group:          Mygroup
License:        My License
URL:            http://localhost.com/
Source:         %{name}

%description
Generic app

%prep
cp -ra %{_topdir}/SOURCES/genapp %{_topdir}/SOURCES/%{name}
cp -ra %{_topdir}/SOURCES/%{name} %{_topdir}/BUILD/%{name}
cd %{_topdir}/BUILD/%{name}
[ `/usr/bin/id -u` = '0' ] && /bin/chown -Rhf root .
[ `/usr/bin/id -u` = '0' ] && /bin/chgrp -Rhf root .
/bin/chmod -Rf a+rX,u+w,g-w,o-w .

%build

# global
export CFLAGS="-fPIC -O3 -pipe"

# gendepp
export CPPFLAGS="${CPPFLAGS} -I/opt/local/pkgs/%{gendep_name}/include"
export LDFLAGS="${LDFLAGS} -L/opt/local/pkgs/%{gendep_name}/lib -Wl,--rpath -Wl,/opt/local/pkgs/%{gendep_name}/lib"
export LIBS="${LIBS} -L/opt/local/pkgs/%{gendep_name}/lib"

cd %{_topdir}/BUILD/%{name}
./buildconf --with-genapp=%{_topdir}/SOURCES/%{name}/srclib/%{genappsrc}
./configure --prefix=/opt/local/pkgs/%{name} \
                            --enable-some-stuff=all \
                            --enable-other-bits=yes

make

%install
cd %{_topdir}/BUILD/%{name}
make install DESTDIR=$RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/opt/local/pkgs/%{name}

%post

%changelog
