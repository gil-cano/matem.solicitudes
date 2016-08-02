# -*- coding: utf-8 -*-
"""Installer for the matem.solicitudes package."""

from setuptools import find_packages
from setuptools import setup

long_description = (
    open('README.rst').read() +
    '\n' +
    'Contributors\n' +
    '============\n' +
    '\n' +
    open('CONTRIBUTORS.rst').read() +
    '\n' +
    open('CHANGES.rst').read() +
    '\n')


setup(
    name='matem.solicitudes',
    version='4.0.1',
    description="Applications for institutional resources.",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
    ],
    keywords='Plone Python',
    author='Informática Académica',
    author_email='computoacademico@im.unam.mx',
    url='https://github.com/imatem/matem.solicitudes',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['matem'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.api',
        'setuptools',
        'Products.FacultyStaffDirectory',
        'Products.ATCountryWidget',
        'Products.MasterSelectWidget',
        'Products.ATExtensions',
        'Products.DataGridField',
        'archetypes.multifile',
        'collective.datagridcolumns',
    ],
    extras_require={
        'develop': [
            'plone.reload',
            'Products.PDBDebugMode',
            'Products.PrintingMailHost',
        ],
        'test': [
            'mock',
            'plone.app.robotframework',
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
