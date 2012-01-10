Name:           python-networkx
Version:        1.6
Release:        2%{?dist}
Summary:        Creates and Manipulates Graphs and Networks
Group:          Development/Languages
License:        BSD
URL:            http://networkx.lanl.gov/
Source0:        http://pypi.python.org/packages/source/n/networkx/networkx-%{version}.tar.gz
Source1:        http://networkx.lanl.gov/networkx_reference.pdf
Source2:        http://networkx.lanl.gov/networkx_tutorial.pdf
Source3:        http://networkx.lanl.gov/networkx-documentation.zip
BuildArch:      noarch

BuildRequires:  gdal-python
BuildRequires:  graphviz-python
BuildRequires:  pydot
BuildRequires:  pyparsing, python3-pyparsing
BuildRequires:  python2-devel
BuildRequires:  python3-devel
BuildRequires:  python-decorator, python3-decorator
BuildRequires:  python-matplotlib
BuildRequires:  python-nose
BuildRequires:  python-sphinx
BuildRequires:  PyYAML, python3-PyYAML
BuildRequires:  scipy, python3-scipy
BuildRequires:  tex(latex)

Requires:       gdal-python
Requires:       graphviz-python
Requires:       pydot
Requires:       pyparsing
Requires:       python-decorator
Requires:       PyYAML
Requires:       scipy


%description
NetworkX is a Python 2 package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.


%package -n python3-networkx
Summary:        Creates and Manipulates Graphs and Networks
Group:          Development/Languages
Requires:       python3-decorator
Requires:       python3-pyparsing
Requires:       python3-PyYAML
Requires:       python3-scipy


%description -n python3-networkx
NetworkX is a Python 3 package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.


%package doc
Summary:        Documentation for networkx
Group:          Documentation
Requires:       %{name} = %{version}-%{release}


%description doc
Documentation for networkx


%prep
%setup -q -n networkx-%{version}

# Fix permissions
find examples -type f -perm /0111 | xargs chmod a-x

# Overwrite the 0-length doc files with the real doc files
cp -pf %{SOURCE1} %{SOURCE2} %{SOURCE3} doc/source

# Use the system python-decorator instead of the bundled version
sed -i '/          "networkx\.external.*",/d' setup.py
cd networkx
rm -fr external
sed "/import networkx\.external/d" __init__.py > init.py
touch -r __init__.py init.py
mv -f init.py __init__.py
for f in utils/decorators.py utils/misc.py; do
  sed "s/networkx\.external\.//" $f > fixed.py
  touch -r $f fixed.py
  mv -f fixed.py $f
done
cd ..

%build
python setup.py build
PYTHONPATH=`pwd`/build/lib make -C doc html

# Setup for python3
mv build build2
mv networkx/*.pyc build2

# Build for python3
python3 setup.py build


%install
# Install the python3 version
python3 setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

# Setup for python2
mv build build3
mv build2 build
mv -f build/*.pyc networkx

# Install the python2 version
python setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT%{_docdir}/networkx-%{version} ./installed-docs
rm -f installed-docs/INSTALL.txt

# Fix permissions
grep -FRl /usr/bin/env $RPM_BUILD_ROOT%{python_sitelib} | xargs chmod a+x
grep -FRl /usr/bin/env $RPM_BUILD_ROOT%{python3_sitelib} | xargs chmod a+x

# Except unfix the one where the shebang was muffed
chmod a-x $RPM_BUILD_ROOT%{python_sitelib}/networkx/algorithms/link_analysis/hits_alg.py
chmod a-x $RPM_BUILD_ROOT%{python3_sitelib}/networkx/algorithms/link_analysis/hits_alg.py


%clean
rm -f /tmp/tmp??????

 
%check
mkdir site-packages
mv networkx site-packages
PYTHONPATH=`pwd`/site-packages python -c "import networkx; networkx.test()"


%files
%doc installed-docs/*
%{python_sitelib}/*


%files -n python3-networkx
%doc installed-docs/*
%{python3_sitelib}/*


%files doc
%doc doc/build/html/*


%changelog
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
