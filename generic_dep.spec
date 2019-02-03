%define _topdir     %(echo $PWD)
%define distro      %(echo ${distro}${dver})
%define arch        %(echo $arch)
%define oname       %(echo $oname)
%define fullver     %(echo $gendep_ver)
%define pkgver      %(echo $gendep_ver | cut -d'.' -f1,2)
%define version     %(echo $gendep_ver | cut -d'.' -f3)
%define d_pkgver    %(echo %pkgver | tr '.' '_')
%define release     %(echo $BUILD_NUMBER)

%define name        gendep_%{d_pkgver}
%define _tmppath    %_topdir/tmp
%define buildroot   %{_topdir}/%{name}-root
%define _build_name_fmt %%{ARCH}/%%{NAME}-%{version}-%{release}.%{distro}.%%{ARCH}.rpm

BuildRoot:      %{buildroot}
Name:           %{name}
Release:        %{release}
Version:        %{version}
Summary:        Generic App
AutoReqProv:    no
Provides:       %{name}-%{version}-%{release}

Group:          Mygroup
License:        My License
URL:            http://localhost.com/
Source:         %{name}

%description
Generic dependency

%prep
cp -ra %{_topdir}/SOURCES/gendep %{_topdir}/SOURCES/%{name}
cp -ra %{_topdir}/SOURCES/%{name} %{_topdir}/BUILD/%{name}
cd %{_topdir}/BUILD/%{name}
[ `/usr/bin/id -u` = '0' ] && /bin/chown -Rhf root .
[ `/usr/bin/id -u` = '0' ] && /bin/chgrp -Rhf root .
/bin/chmod -Rf a+rX,u+w,g-w,o-w .

%build
cd %{name}
./configure --prefix=/opt/local/pkgs/%{name}
make

%install
cd %{_topdir}/BUILD/%{name}
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/opt/local/pkgs/%{name}

%post

%changelog
