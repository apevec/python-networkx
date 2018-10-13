%global srcname networkx

Name:           python-%{srcname}
Version:        2.2
Release:        1%{?dist}
Summary:        Creates and Manipulates Graphs and Networks
License:        BSD
URL:            http://networkx.github.io/
Source0:        https://github.com/networkx/networkx/archive/%{srcname}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(decorator)
BuildRequires:  python3dist(gdal)
BuildRequires:  python3dist(lxml)
BuildRequires:  python3dist(matplotlib)
BuildRequires:  python3dist(nb2plots)
BuildRequires:  python3dist(nose)
BuildRequires:  python3dist(nose-ignore-docstring)
BuildRequires:  python3dist(numpy)
BuildRequires:  python3dist(numpydoc)
BuildRequires:  python3dist(pandas)
BuildRequires:  python3dist(pillow)
BuildRequires:  python3dist(pydot)
BuildRequires:  python3dist(pygraphviz)
BuildRequires:  python3dist(pyyaml)
BuildRequires:  python3dist(scipy)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(sphinx-gallery)
BuildRequires:  xdg-utils

# Documentation
BuildRequires:  tex(latex)
BuildRequires:  tex-preview

%description
NetworkX is a Python package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

%package -n python3-%{srcname}
Summary:        Creates and Manipulates Graphs and Networks
Requires:       python3dist(decorator)
Requires:       python3dist(gdal)
Requires:       python3dist(lxml)
Requires:       python3dist(matplotlib)
Requires:       python3dist(numpy)
Requires:       python3dist(pandas)
Requires:       python3dist(pillow)
Requires:       python3dist(pydot)
Requires:       python3dist(pygraphviz)
Requires:       python3dist(pyparsing)
Requires:       python3dist(pyyaml)
Requires:       python3dist(scipy)
Requires:       xdg-utils

%{?python_provide:%python_provide python3-%{srcname}}

# This can be removed when Fedora 29 reaches EOL
Obsoletes:      python2-%{srcname} < 2.0
Provides:       python2-%{srcname} = %{version}-%{release}
Obsoletes:      python2-%{srcname}-core < 2.0
Provides:       python2-%{srcname}-core = %{version}-%{release}
Obsoletes:      python2-%{srcname}-geo < 2.0
Provides:       python2-%{srcname}-geo = %{version}-%{release}
Obsoletes:      python2-%{srcname}-drawing < 2.0
Provides:       python2-%{srcname}-drawing = %{version}-%{release}
Obsoletes:      python3-%{srcname}-core < 2.0
Provides:       python3-%{srcname}-core = %{version}-%{release}
Obsoletes:      python3-%{srcname}-geo < 2.0
Provides:       python3-%{srcname}-geo = %{version}-%{release}
Obsoletes:      python3-%{srcname}-drawing < 2.0
Provides:       python3-%{srcname}-drawing = %{version}-%{release}

%description -n python3-%{srcname}
NetworkX is a Python 3 package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

%package doc
Summary:        Documentation for networkx
Provides:       bundled(jquery)

%description doc
Documentation for networkx

%prep
%autosetup -n %{srcname}-%{srcname}-%{version}

# Do not use env
for f in $(grep -FRl %{_bindir}/env .); do
  sed -e 's,%{_bindir}/env python,%{__python3},' \
      -e 's,%{_bindir}/env ,%{_bindir},' \
      -i.orig $f
  touch -r $f.orig $f
  rm $f.orig
done

# Examples that require network access fail on the koji builders, the
# sphinx_gallery version of system.out has no attribute named 'buffer', and
# the Unix email example has multiple python 3 incompatibilities
sed -i "/expected_failing_examples/s|]|,'../examples/graph/plot_football.py','../examples/graph/plot_erdos_renyi.py','../examples/basic/plot_read_write.py'&|" doc/conf.py
rm -f examples/drawing/plot_unix_email.py

%build
%py3_build

# Build the documentation
PYTHONPATH=$PWD/build/lib make SPHINXBUILD=sphinx-build-3 -C doc html

%install
%py3_install
mv %{buildroot}%{_docdir}/networkx-%{version} ./installed-docs
rm -f installed-docs/INSTALL.txt

# Temporarily disabled until a bug in graphviz > 2.38 is fixed that causes
# multigraphs to not work.  (Adding the same edge with multiple keys yields
# only the initial edge.)  This is slated to be fixed in graphviz 2.42.  Once
# that is built for Fedora, we can reenable the tests.
#%%check
#nosetests-3 -v

%files -n python3-networkx
%doc README.rst installed-docs/*
%license LICENSE.txt
%{python3_sitelib}/networkx*

%files doc
%doc doc/build/html/*

%changelog
* Sat Oct 13 2018 Jerry James <loganjerry@gmail.com> - 2.2-1
- New upstream version (bz 1600361)
- Drop all patches
- Drop the python2 subpackages (bz 1634570)
- Figure out the BuildRequires all over again (bz 1576805)
- Consolidate BuildRequires so I can tell what is actually on the list
- Drop conditionals for RHEL < 8; this version can never appear there anyway
- Consolidate back to a single package for the same reason
- Temporarily disable tests due to multigraph bug in graphviz > 2.38

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.11-12
- Rebuilt for Python 3.7

* Fri May 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.11-11
- Update graphviz dependency for python2
- Drop graphviz dependency for python3 (graphviz doesn't support python3)

* Fri Mar 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.11-10
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 07 2017 Merlin Mathesius <mmathesi@redhat.com> - 1.11-8
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 23 2016 Orion Poplawski <orion@cora.nwra.com> - 1.11-5
- Add patch to fix sphinx build

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.11-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

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
