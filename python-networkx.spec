%if 0%{?fedora} >= 12 || 0%{?rhel} >= 8
%global with_python3 1
%endif
%if !0%{?rhel}
%global with_gdal 1
%endif

# see https://fedoraproject.org/wiki/Packaging:Python#Macros
%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%global pkgname networkx

Name:           python-%{pkgname}
Version:        1.9
Release:        1%{?dist}
Summary:        Creates and Manipulates Graphs and Networks
Group:          Development/Languages
License:        BSD
URL:            http://networkx.github.io/
Source0:        https://pypi.python.org/packages/source/n/%{pkgname}/%{pkgname}-%{version}.tar.gz
Source1:        http://networkx.github.io/documentation/%{pkgname}-%{version}/_downloads/networkx_reference.pdf
Source2:        http://networkx.github.io/documentation/%{pkgname}-%{version}/_downloads/networkx_tutorial.pdf
Source3:        http://networkx.github.io/documentation/%{pkgname}-%{version}/_downloads/networkx-documentation.zip
Patch0:         %{pkgname}-optional-modules.patch
Patch1:         %{pkgname}-nose1.0.patch
Patch2:         %{pkgname}-skip-scipy-0.8-tests.patch
BuildArch:      noarch

Requires:       %{name}-core = %{version}-%{release}
%if 0%{?with_gdal}
Requires:       %{name}-geo = %{version}-%{release}
Requires:       %{name}-drawing = %{version}-%{release}
%endif

%description
NetworkX is a Python 2 package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

%package core
Summary:        Creates and Manipulates Graphs and Networks
BuildRequires:  python2-devel
BuildRequires:  python-decorator
BuildRequires:  PyYAML
BuildRequires:  scipy
BuildRequires:  pyparsing
%if 0%{?rhel} == 6
BuildRequires:  python-nose1.1
%else
BuildRequires:  python-nose
%endif
Requires:       python-decorator
Requires:       PyYAML
Requires:       scipy
Requires:       pyparsing

%description core
NetworkX is a Python 2 package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.


%if 0%{?with_gdal}

%package geo
Summary:        GDAL I/O
Requires:       %{name}-core = %{version}-%{release}
BuildRequires:  gdal-python
Requires:       gdal-python

%description geo
NetworkX is a Python 3 package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

This package provides GDAL I/O support.


%package drawing
Summary:        visual representations for graphs and networks
Requires:       %{name}-core = %{version}-%{release}
BuildRequires:  graphviz-python
BuildRequires:  pydot
Requires:       graphviz-python
Requires:       pydot
Requires:       python-matplotlib

%description drawing
NetworkX is a Python 3 package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

This package provides support for graph visualizations.

%endif


%if 0%{?with_python3}
%package -n python3-%{pkgname}
Summary:        Creates and Manipulates Graphs and Networks
Requires:       python3-%{pkgname}-core = %{version}-%{release}
Requires:       python3-%{pkgname}-geo = %{version}-%{release}
Requires:       python3-%{pkgname}-drawing = %{version}-%{release}

%description -n python3-%{pkgname}
NetworkX is a Python 3 package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

%package -n python3-%{pkgname}-core
Summary:        Creates and Manipulates Graphs and Networks
BuildRequires:  python3-devel
BuildRequires:  python3-decorator
BuildRequires:  python3-PyYAML
BuildRequires:  python3-scipy
BuildRequires:  python3-pyparsing
Requires:       python3-decorator
Requires:       python3-PyYAML
Requires:       python3-scipy
Requires:       python3-pyparsing

%description -n python3-%{pkgname}-core
NetworkX is a Python 3 package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

%if 0%{?with_gdal}
%package -n python3-%{pkgname}-geo
Summary:        GDAL I/O
Requires:       python3-%{pkgname}-core = %{version}-%{release}
BuildRequires:  gdal-python
Requires:       gdal-python

%description -n python3-%{pkgname}-geo
NetworkX is a Python 3 package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

This package provides GDAL I/O support.

%package -n python3-%{pkgname}-drawing
Summary:        visual representations for graphs and networks
Requires:       python3-%{pkgname}-core = %{version}-%{release}
BuildRequires:  graphviz-python
BuildRequires:  pydot
BuildRequires:  python3-matplotlib
Requires:       graphviz-python
Requires:       pydot
Requires:       python3-matplotlib

%description -n python3-%{pkgname}-drawing
NetworkX is a Python 3 package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

This package provides support for graph visualizations.
%endif

%endif


%package doc
Summary:        Documentation for networkx
Group:          Documentation

%if 0%{?rhel} == 6
BuildRequires:  python-sphinx10
%else
BuildRequires:  python-sphinx
BuildRequires:  python-sphinx_rtd_theme
BuildRequires:  python-numpydoc
%endif
BuildRequires:  tex(latex)
BuildRequires:  tex-preview
BuildRequires:  python-matplotlib


%description doc
Documentation for networkx


%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%if 0%{?rhel} == 6
%patch1 -p1
%patch2 -p1
%endif

# Fix permissions
find examples -type f -perm /0111 | xargs chmod a-x

# Avoid downloading the doc files while building
cp -pf %{SOURCE1} %{SOURCE2} %{SOURCE3} doc/source

%build
python2 setup.py build
%if 0%{?rhel} == 6
PYTHONPATH=$PWD/build/lib make SPHINXBUILD=sphinx-1.0-build -C doc html
%else
PYTHONPATH=$PWD/build/lib make -C doc html
%endif

%if 0%{?with_python3}
# Setup for python3
mv build build2
mv networkx/*.pyc build2

# Build for python3
python3 setup.py build
%endif

%install
%if 0%{?with_python3}
# Install the python3 version
python3 setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

# Setup for python2
mv build build3
mv build2 build
mv -f build/*.pyc networkx
%endif

# Install the python2 version
python2 setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT%{_docdir}/networkx-%{version} ./installed-docs
rm -f installed-docs/INSTALL.txt

# Fix permissions and binary paths
for f in `grep -FRl /usr/bin/env $RPM_BUILD_ROOT%{python2_sitelib}`; do
  sed 's|/usr/bin/env python|%{_bindir}/python2|' $f > $f.new
  touch -r $f $f.new
  chmod a+x $f.new
  mv -f $f.new $f
done

%if 0%{?with_python3}
for f in `grep -FRl /usr/bin/env $RPM_BUILD_ROOT%{python3_sitelib}`; do
  sed 's|/usr/bin/env python|%{_bindir}/python3|' $f > $f.new
  touch -r $f $f.new
  chmod a+x $f.new
  mv -f $f.new $f
done
%endif

%clean
rm -fr %{buildroot}
rm -f /tmp/tmp??????

%check
mkdir site-packages
mv networkx site-packages
PYTHONPATH=`pwd`/site-packages python -c "import networkx; networkx.test()"

%files
%doc README.txt LICENSE.txt

%files core
%doc installed-docs/*
%{python2_sitelib}/*
%exclude %{python2_sitelib}/networkx/drawing/
%if 0%{?with_gdal}
%exclude %{python2_sitelib}/networkx/readwrite/nx_shp.py
%endif

%if 0%{?with_gdal}
%files drawing
%{python2_sitelib}/networkx/drawing

%files geo
%{python2_sitelib}/networkx/readwrite/nx_shp.py
%endif

%if 0%{?with_python3}
%files -n python3-networkx
%doc README.txt LICENSE.txt

%files -n python3-networkx-core
%doc installed-docs/*
%{python3_sitelib}/*
%exclude %{python3_sitelib}/networkx/drawing/
%if 0%{?with_gdal}
%exclude %{python3_sitelib}/networkx/readwrite/nx_shp.py
%endif

%if 0%{?with_gdal}
%files -n python3-networkx-drawing
%{python2_sitelib}/networkx/drawing

%files -n python3-networkx-geo
%{python3_sitelib}/networkx/readwrite/nx_shp.py
%endif
%endif


%files doc
%doc doc/build/html/*


%changelog
* Tue Jul  8 2014 Jerry James <loganjerry@gmail.com> - 1.9-1
- New upstream version
- Drop upstreamed -test-rounding-fix patch
- Upstream no longer bundles python-decorator; drop the workaround

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.8.1-13
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu Mar 13 2014 Pádraig Brady <pbrady@redhat.com> - 1.8.1-12
- Split to subpackages and support EL6 and EL7

* Thu Oct  3 2013 Jerry James <loganjerry@gmail.com> - 1.8.1-2
- Update project and source URLs

* Fri Aug  9 2013 Jerry James <loganjerry@gmail.com> - 1.8.1-1
- New upstream version

* Mon Jul 29 2013 Jerry James <loganjerry@gmail.com> - 1.8-1
- New upstream version
- Add tex-preview BR for documentation

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug  6 2012 Jerry James <loganjerry@gmail.com> - 1.7-1
- New upstream version

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 10 2012 Jerry James <loganjerry@gmail.com> - 1.6-2
- Mass rebuild for Fedora 17

* Mon Nov 28 2011 Jerry James <loganjerry@gmail.com> - 1.6-1
- New upstream version
- Do not use bundled python-decorator
- Remove Requires: ipython, needed by one example only
- Clean junk files left in /tmp

* Wed Jun 22 2011 Jerry James <loganjerry@gmail.com> - 1.5-1
- New upstream version
- Drop defattr
- Build documentation

* Sat Apr 23 2011 Jerry James <loganjerry@gmail.com> - 1.4-1
- New upstream version
- Build for both python2 and python3
- Drop BuildRoot, clean script, and clean at start of install script

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jan 20 2010 Conrad Meyer <konrad@tylerc.org> - 1.0.1-1
- Bump version to 1.0.1.
- License changed LGPLv2+ -> BSD.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 24 2009 Conrad Meyer <konrad@tylerc.org> - 0.99-3
- Replace __python macros with direct python invocations.
- Disable checks for now.
- Replace a define with global.

* Thu Mar 12 2009 Conrad Meyer <konrad@tylerc.org> - 0.99-2
- License is really LGPLv2+.
- Include license as documentation.
- Add a check section to run tests.

* Sat Dec 13 2008 Conrad Meyer <konrad@tylerc.org> - 0.99-1
- Initial package.
