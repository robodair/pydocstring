===========
pydocstring
===========


.. image:: https://travis-ci.org/robodair/pydocstring.svg?branch=master
    :target: https://travis-ci.org/robodair/pydocstring

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


Python package for autogenerating python docstrings


The idea is that this project can be wrapped by an editor extension to provide docstrings as autocompletion or in response to a shortcut.


Status
======

Beta, ready for basic use - Supports Google, Numpy, and reST docstring formatting but no others (it's really simple to add one though)

Doesn't support more complicated things like converting between styles or updating docstrings.

Docs
====

Documentation is on `Read The Docs <http://pydocstring.readthedocs.io/>`_

API
---

For integration with editors, there's a really simple api avaialble

Download
========

pydocstring is on `PyPI <https://pypi.org/project/pydocstring/>`_ and can be installed with pip:

.. code-block:: bash

    pip install pydocstring


TODO
====

Feel free to help out on one of these

- Conversion between docstring styles
- Updating docstrings (with parameters removed, exceptions no longer thrown, etc)

