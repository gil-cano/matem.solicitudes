=======================
IM Applications package
=======================

.. image:: https://travis-ci.org/gil-cano/matem.solicitudes.svg?branch=master
    :alt: Travis CI badge
    :target: https://travis-ci.org/gil-cano/matem.solicitudes

.. image:: https://coveralls.io/repos/github/gil-cano/matem.solicitudes/badge.svg?branch=master
    :alt: Coveralls badge
    :target: https://coveralls.io/github/gil-cano/matem.solicitudes?branch=master

.. image:: https://badge.waffle.io/gil-cano/matem.solicitudes.png?label=Ready
    :alt: Stories in Ready
    :target: https://waffle.io/gil-cano/matem.solicitudes

An Application package for the IM


Features
--------

- Faculty applications
- Students applications


Documentation
-------------

Full documentation for end users can be found in the "docs" folder, and is also available online at https://github.com/gil-cano/matem.solicitudes/docs


Installation
------------

Install matem.solicitudes by adding it to your buildout::

   [buildout]

    ...

    eggs =
        matem.solicitudes


and then running "bin/buildout"


Using the development buildout
------------------------------

Create a virtualenv in the package::

    $ virtualenv --clear .

Install requirements with pip::

    $ ./bin/pip install -r requirements.txt

Run buildout::

    $ ./bin/buildout

Start Plone in foreground:

    $ ./bin/instance fg


Contribute
----------

- Issue Tracker: `@ GitHub <http://github.com/gil-cano/matem.solicitudes/issues>`_
- Source Code: `@ GitHub <https://github.com/gil-cano/matem.solicitudes.git>`_
- Documentation: `@ readthedocs.org <http://github.com/gil-cano/matem.solicitudes>`_


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: informatica.academica@matem.unam.mx

License
-------

The project is licensed under the GPLv2.
