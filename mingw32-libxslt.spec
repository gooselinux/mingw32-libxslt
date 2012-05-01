%global __strip %{_mingw32_strip}
%global __objdump %{_mingw32_objdump}
%global _use_internal_dependency_generator 0
%global __find_requires %{_mingw32_findrequires}
%global __find_provides %{_mingw32_findprovides}
%define __debug_install_post %{_mingw32_debug_install_post}

Name:           mingw32-libxslt
Version:        1.1.26
Release:        2%{?dist}
Summary:        MinGW Windows Library providing the Gnome XSLT engine


License:        MIT
Group:          Development/Libraries
URL:            http://xmlsoft.org/XSLT/
Source0:        ftp://xmlsoft.org/XSLT/libxslt-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

# Fix compilation on MinGW environments
Patch1000:      mingw32-libxslt-dont-use-pthread.patch

BuildRequires:  mingw32-filesystem >= 30
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-dlfcn
BuildRequires:  mingw32-iconv
BuildRequires:  mingw32-libgcrypt
BuildRequires:  mingw32-libxml2 >= 2.7.2-3
BuildRequires:  pkgconfig
BuildRequires:  autoconf, automake, libtool

Requires:       mingw32-libxml2 >= 2.7.2-3
Requires:       pkgconfig


%description
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. To use it you need to have a version of libxml2 >= 2.6.27
installed. The xsltproc command is a command line interface to the XSLT engine


%package static
Summary:        Static version of the MinGW Windows LibXSLT library
Requires:       %{name} = %{version}-%{release}
Group:          Development/Libraries

%description static
Static version of the MinGW Windows LibXSLT library.


%{_mingw32_debug_package}


%prep
%setup -q -n libxslt-%{version}

# The native version of libxslt contains a multilib patch, but
# this isn't interesting for MinGW environments
#%patch0 -p1

%patch1000 -p1

libtoolize --force --copy
autoreconf


%build
PATH=%{_mingw32_bindir}:$PATH \
%{_mingw32_configure} --without-python --enable-shared
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Remove doc and man which duplicate stuff already in Fedora native package.
rm -r $RPM_BUILD_ROOT%{_mingw32_docdir}
rm -r $RPM_BUILD_ROOT%{_mingw32_mandir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING Copyright
%{_mingw32_bindir}/xslt-config
%{_mingw32_bindir}/xsltproc.exe
%{_mingw32_includedir}/libexslt
%{_mingw32_includedir}/libxslt
%{_mingw32_bindir}/libexslt-0.dll
%{_mingw32_libdir}/libexslt.dll.a
%{_mingw32_libdir}/libexslt.la
%{_mingw32_bindir}/libxslt-1.dll
%{_mingw32_libdir}/libxslt.dll.a
%{_mingw32_libdir}/libxslt.la
%{_mingw32_libdir}/pkgconfig/libexslt.pc
%{_mingw32_libdir}/pkgconfig/libxslt.pc
%{_mingw32_libdir}/xsltConf.sh
%{_mingw32_datadir}/aclocal/libxslt.m4


%files static
%defattr(-,root,root,-)
%{_mingw32_libdir}/libexslt.a
%{_mingw32_libdir}/libxslt.a


%changelog
* Fri Feb  4 2011 Andrew Beekhof <abeekhof@redhat.com> - 1.1.26-2
- Rebuild for new version of mingw32-zlib/mingw32-glib2/mingw32-libxml2
  Related: rhbz#658833

* Tue Dec 28 2010 Andrew Beekhof <abeekhof@redhat.com> - 1.1.26-1.4
- Rebuild everything with gcc-4.4
  Related: rhbz#658833

* Fri Dec 24 2010 Andrew Beekhof <abeekhof@redhat.com> - 1.1.26-1.3
- The use of ExclusiveArch conflicts with noarch, using an alternate COLLECTION to limit builds
  Related: rhbz#658833

* Wed Dec 22 2010 Andrew Beekhof <abeekhof@redhat.com> - 1.1.26-1.2
- Only build mingw packages on x86_64
  Related: rhbz#658833

* Wed Dec 22 2010 Andrew Beekhof <abeekhof@redhat.com> - 1.1.26-1.1
- Bump the revision to avoid tag collision
  Related: rhbz#658833

* Thu Sep 24 2009 Erik van Pienbroek <epienbro@fedoraproject.org. - 1.1.26-1
- Update to 1.1.26

* Mon Sep 21 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.1.25-2
- Fix a locking bug in 1.1.25 (patch from native libxslt package)

* Thu Sep 17 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.1.25-1
- Update to 1.1.25
- Dropped upstreamed CVE patch
- Dropped upstreamed mingw32 patches
- Added a patch to never use pthreads even if it's available
- Automatically generate debuginfo subpackages

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.24-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 11 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.1.24-8
- Resolve FTBFS

* Fri May 22 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.1.24-7
- Use %%global instead of %%define
- Dropped the reference to the multilib patch as it isn't used for MinGW
- Fixed dangling-relative-symlink rpmlint warning

* Sat May  9 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.1.24-6
- Added some more comments in the .spec file
- Added -static subpackage
- Dropped the 'gzip ChangeLog' line as the ChangeLog isn't bundled anyway
- Fixed %%defattr line

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.1.24-5
- Rebuild for mingw32-gcc 4.4

* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 1.1.24-4
- Include license file.

* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.1.24-3
- Use _smp_mflags.
- Rebuild libtool.
- +BRs dlfcn and iconv.

* Sat Oct 25 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.24-2
- Initial RPM release.
