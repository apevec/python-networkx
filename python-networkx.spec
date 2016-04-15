%if 0%{?fedora} || 0%{?rhel} >= 8
%global with_python3 1
%endif
%if !0%{?rhel}
%global with_gdal 1
%endif

%global srcname networkx

Name:           python-%{srcname}
Version:        1.11
Release:        3%{?dist}
Summary:        Creates and Manipulates Graphs and Networks
License:        BSD
URL:            http://networkx.github.io/
Source0:        https://github.com/networkx/networkx/archive/%{srcname}-%{version}.tar.gz
Patch0:         %{srcname}-optional-modules.patch
Patch1:         %{srcname}-nose1.0.patch
Patch2:         %{srcname}-skip-scipy-0.8-tests.patch
BuildArch:      noarch

%description
NetworkX is a Python 2 package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

%package -n python2-%{srcname}
Summary:        Creates and Manipulates Graphs and Networks
Requires:       python2-%{srcname}-core = %{version}-%{release}
%if 0%{?with_gdal}
Requires:       python2-%{srcname}-geo = %{version}-%{release}
Requires:       python2-%{srcname}-drawing = %{version}-%{release}
%endif

%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
NetworkX is a Python 2 package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

%package -n python2-%{srcname}-core
Summary:        Creates and Manipulates Graphs and Networks
BuildRequires:  python2-devel
BuildRequires:  python2-decorator
BuildRequires:  python2-scipy
BuildRequires:  python2-setuptools
BuildRequires:  python2-yaml
BuildRequires:  pyparsing
%if 0%{?rhel} == 6
BuildRequires:  python-nose1.1
%else
BuildRequires:  python2-nose
%endif
Requires:       python2-decorator
Requires:       python2-scipy
Requires:       python2-yaml
Requires:       pyparsing

%{?python_provide:%python_provide python2-%{srcname}-core}

%description -n python2-%{srcname}-core
NetworkX is a Python 2 package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.


%if 0%{?with_gdal}

%package -n python2-%{srcname}-geo
Summary:        GDAL I/O
Requires:       python2-%{srcname}-core = %{version}-%{release}
BuildRequires:  gdal-python
Requires:       gdal-python

%{?python_provide:%python_provide python2-%{srcname}-geo}

%description -n python2-%{srcname}-geo
NetworkX is a Python 3 package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

This package provides GDAL I/O support.


%package -n python2-%{srcname}-drawing
Summary:        visual representations for graphs and networks
Requires:       python2-%{srcname}-core = %{version}-%{release}
BuildRequires:  graphviz-python
BuildRequires:  python2-matplotlib
BuildRequires:  python2-pydotplus
Requires:       graphviz-python
Requires:       python2-matplotlib
Requires:       python2-pydotplus

%{?python_provide:%python_provide python2-%{srcname}-drawing}

%description -n python2-%{srcname}-drawing
NetworkX is a Python 3 package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

This package provides support for graph visualizations.

%endif


%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        Creates and Manipulates Graphs and Networks
Requires:       python3-%{srcname}-core = %{version}-%{release}
Requires:       python3-%{srcname}-geo = %{version}-%{release}
Requires:       python3-%{srcname}-drawing = %{version}-%{release}

%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
NetworkX is a Python 3 package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

%package -n python3-%{srcname}-core
Summary:        Creates and Manipulates Graphs and Networks
BuildRequires:  python3-devel
BuildRequires:  python3-decorator
BuildRequires:  python3-yaml
BuildRequires:  python3-scipy
BuildRequires:  python3-pyparsing
BuildRequires:  python3-setuptools
Requires:       python3-decorator
Requires:       python3-yaml
Requires:       python3-scipy
Requires:       python3-pyparsing

%{?python_provide:%python_provide python3-%{srcname}-core}

%description -n python3-%{srcname}-core
NetworkX is a Python 3 package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

%if 0%{?with_gdal}
%package -n python3-%{srcname}-geo
Summary:        GDAL I/O
Requires:       python3-%{srcname}-core = %{version}-%{release}
BuildRequires:  gdal-python3
Requires:       gdal-python3

%{?python_provide:%python_provide python3-%{srcname}-geo}

%description -n python3-%{srcname}-geo
NetworkX is a Python 3 package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

This package provides GDAL I/O support.

%package -n python3-%{srcname}-drawing
Summary:        visual representations for graphs and networks
Requires:       python3-%{srcname}-core = %{version}-%{release}
BuildRequires:  graphviz-python
BuildRequires:  python3-matplotlib
BuildRequires:  python3-pydotplus
Requires:       graphviz-python
Requires:       python3-matplotlib
Requires:       python3-pydotplus

%{?python_provide:%python_provide python3-%{srcname}-drawing}

%description -n python3-%{srcname}-drawing
NetworkX is a Python 3 package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

This package provides support for graph visualizations.
%endif

%endif


%package doc
Summary:        Documentation for networkx

%if 0%{?rhel} == 6
BuildRequires:  python-sphinx10
%else
BuildRequires:  python-pandas
BuildRequires:  python2-pydotplus
BuildRequires:  python2-sphinx
BuildRequires:  python2-sphinx_rtd_theme
BuildRequires:  python2-sphinxcontrib-bibtex
BuildRequires:  python-ipython-console
BuildRequires:  python-numpydoc
%endif
BuildRequires:  tex(latex)
BuildRequires:  tex-preview
BuildRequires:  python2-matplotlib
Provides:       bundled(jquery)


%description doc
Documentation for networkx


%prep
%setup -q -n %{srcname}-%{srcname}-%{version}
%patch0 -p1
%if 0%{?rhel} == 6
%patch1 -p1
%patch2 -p1
%endif

# Fix permissions
find examples -type f -perm /0111 -exec chmod a-x {} +

%build
%py2_build
%if 0%{?rhel} == 6
PYTHONPATH=$PWD/build/lib make SPHINXBUILD=sphinx-1.0-build -C doc html
%else
PYTHONPATH=$PWD/build/lib make SPHINXBUILD=sphinx-build-2 -C doc html
%endif

%if 0%{?with_python3}
# Setup for python3
mv build build2
mv networkx/*.pyc build2

# Build for python3
%py3_build
%endif

%install
%if 0%{?with_python3}
# Install the python3 version
%py3_install

# Setup for python2
mv build build3
mv build2 build
mv -f build/*.pyc networkx
%endif

# Install the python2 version
%py2_install
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
PYTHONPATH=$PWD/site-packages python -c "import networkx; networkx.test()"

%files -n python2-%{srcname}
%doc README.rst
%license LICENSE.txt

%files -n python2-%{srcname}-core
%doc installed-docs/*
%{python2_sitelib}/*
%exclude %{python2_sitelib}/networkx/drawing/
%if 0%{?with_gdal}
%exclude %{python2_sitelib}/networkx/readwrite/nx_shp.py*
%endif

%if 0%{?with_gdal}
%files -n python2-%{srcname}-drawing
%{python2_sitelib}/networkx/drawing

%files -n python2-%{srcname}-geo
%{python2_sitelib}/networkx/readwrite/nx_shp.py*
%endif

%if 0%{?with_python3}
%files -n python3-networkx
%doc README.rst
%license LICENSE.txt

%files -n python3-networkx-core
%doc installed-docs/*
%{python3_sitelib}/*
%exclude %{python3_sitelib}/networkx/drawing/
%if 0%{?with_gdal}
%exclude %{python3_sitelib}/networkx/readwrite/nx_shp.py
%exclude %{python3_sitelib}/networkx/readwrite/__pycache__/nx_shp.*
%endif

%if 0%{?with_gdal}
%files -n python3-networkx-drawing
%{python3_sitelib}/networkx/drawing

%files -n python3-networkx-geo
%{python3_sitelib}/networkx/readwrite/nx_shp.py
%{python3_sitelib}/networkx/readwrite/__pycache__/nx_shp.*
%endif
%endif


%files doc
%doc doc/build/html/*


%changelog
* Thu Apr 14 2016 Jerry James <loganjerry@gmail.com> - 1.11-3
- Change pydot dependencies to pydotplus (bz 1326957)

* Sat Apr  2 2016 Jerry James <loganjerry@gmail.com> - 1.11-2
- Fix gdal and pydot dependencies

* Sat Mar  5 2016 Jerry James <loganjerry@gmail.com> - 1.11-1
- New upstream version
- Drop upstreamed -numpy patch

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb  1 2016 Jerry James <loganjerry@gmail.com> - 1.10-1
- Comply with latest python packaging guidelines (bz 1301767)

* Tue Dec  1 2015 Jerry James <loganjerry@gmail.com> - 1.10-1
- New upstream version
- Update URLs
- Add -numpy patch to fix test failure

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Jerry James <loganjerry@gmail.com> - 1.9.1-3
- Note bundled jquery

* Tue Oct  7 2014 Jerry James <loganjerry@gmail.com> - 1.9.1-2
- Fix python3-networkx-drawing subpackage (bz 1149980)
- Fix python(3)-geo subpackage

* Mon Sep 22 2014 Jerry James <loganjerry@gmail.com> - 1.9.1-1
- New upstream version
- Fix license handling

* Thu Jul 10 2014 Jerry James <loganjerry@gmail.com> - 1.9-2
- BR python-setuptools

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
