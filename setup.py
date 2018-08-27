# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


version = '4.2.dev0'
description = 'license applications'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='matem.solicitudes',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ],
    keywords='plone license',
    author='Informática Académica',
    author_email='informaticaacademica@matem.unam.mx',
    url='https://github.com/imatem/matem.solicitudes',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['matem'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'archetypes.multifile',
        'collective.datagridcolumns',
        'plone.api',
        'Products.ATCountryWidget',
        'Products.ATExtensions',
        'Products.DataGridField',
        'Products.FacultyStaffDirectory',
        'Products.MasterSelectWidget',
        'setuptools',
    ],
    extras_require={
        'test': [
            'mock',
            'plone.app.robotframework',
            'plone.app.testing',
            'unittest2',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
