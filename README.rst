===========
pydocstring
===========


.. image:: https://travis-ci.org/robodair/pydocstring.svg?branch=master
    :target: https://travis-ci.org/robodair/pydocstring

.. image:: https://codecov.io/gh/robodair/pydocstring/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/robodair/pydocstring

.. image:: https://readthedocs.org/projects/pydocstring/badge/?version=latest
    :target: https://pydocstring.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/pypi/l/pydocstring.svg
    :target: https://pypi.org/project/pydocstring/

.. image:: https://img.shields.io/pypi/v/pydocstring.svg
    :target: https://pypi.org/project/pydocstring/

.. image:: https://img.shields.io/pypi/pyversions/pydocstring.svg
    :target: https://pypi.org/project/pydocstring/

.. image:: https://img.shields.io/pypi/status/pydocstring.svg
    :target: https://pypi.org/project/pydocstring/


Python package for autogenerating python docstrings, built on top of `Parso <https://github.com/davidhalter/parso>`_.


This project can be wrapped by an editor extension to provide docstrings as autocompletion or in response to a shortcut command.

Status
======

Ready for basic use - Supports **Google**, **Numpy**, and **reST** docstring formats, and it's pretty simple to create your own formatter.

Types are able to be inferred for some things, but if they can't be worked out '``TYPE``' is just inserted instead.

Doesn't support more complicated things like converting between styles or updating docstrings.

Future
======

Check the issues for any more, but the nice-to-haves are:

- Docstring insertion for a whole file
- Updating docstrings for methods with changed paramenters/exeptions/Types
- Conversion between docstring styles

Docs
====

Documentation is on `Read The Docs <http://pydocstring.readthedocs.io/>`_

API
===

For integration with editors, there's a really simple api avaialble (just a single call), check out the docs for more on that.

Download
========

pydocstring is on `PyPI <https://pypi.org/project/pydocstring/>`_ and can be installed with pip:

.. code-block:: bash

    pip install pydocstring

Development
===========

Testing/Coverage is automanted with `tox <http://tox.readthedocs.io/>`_. Pull requests are welcome.
