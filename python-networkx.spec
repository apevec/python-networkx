%{!?python_sitelib: %global python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-networkx
Version:        1.0.1
Release:        2%{?dist}
Summary:        Creates and Manipulates Graphs and Networks
Group:          Development/Languages
License:        BSD
URL:            https://networkx.lanl.gov/trac
Source0:        http://networkx.lanl.gov/download/networkx/networkx-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  graphviz-python
BuildRequires:  pydot
BuildRequires:  pyparsing
BuildRequires:  python-devel
BuildRequires:  python-matplotlib
BuildRequires:  PyYAML
BuildRequires:  scipy
Requires:       graphviz-python
Requires:       ipython
Requires:       numpy
Requires:       pydot
Requires:       python-matplotlib
Requires:       PyYAML
Requires:       scipy


%description
NetworkX is a Python package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.


%prep
%setup -q -n networkx-%{version}
chmod -x examples/*/*.py
chmod -x examples/*/*.bz2
sed -i '1,1d' networkx/tests/test.py


%build
python setup.py build


%install
rm -rf $RPM_BUILD_ROOT
python setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT%{_docdir}/networkx-%{version} ./installed-docs

 
%check
# Tests don't pass for a variety of reasons; among them it looks
# like they try to use Gtk which is obviously not available.
#python -c "import networkx; networkx.test()"


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc installed-docs/*
%{python_sitelib}/*


%changelog
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
