# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '3.0.9'


setup(
    name='matem.solicitudes',
    version=version,
    description="Applications for institutional resources.",
    long_description=open('README.txt').read() + '\n' +
    open('docs/CHANGES.txt').read(),
    # Get more strings from
    #http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Plone',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    platforms='Any',
    author='Instituto de Matematicas - UNAM',
    author_email='gil@matem.unam.mx',
    url='http://www.matem.unam.mx',
    license='GPL',
    namespace_packages=['matem'],
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'Products.FacultyStaffDirectory',
        'Products.ATCountryWidget',
        'Products.MasterSelectWidget',
        'Products.ATExtensions',
        'archetypes.multifile',
        'matem.fsdextender',
        'plone.app.jquerytools',
    ],
    extras_require={
        'develop': [
            'flake8',
            'jarn.mkrelease',
            'manuel',
            'Sphinx',
            'zest.releaser',
        ],
        'test': [
            'plone.app.testing',
            'unittest2',
        ],
    },
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
