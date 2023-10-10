dobles
=======

.. image:: https://badge.fury.io/py/dobles.svg
    :target: http://badge.fury.io/py/dobles

.. image:: https://travis-ci.org/uber/dobles.svg?branch=master
    :target: https://travis-ci.org/uber/dobles

.. image:: https://readthedocs.org/projects/dobles/badge/?version=latest
    :target: https://dobles.readthedocs.io/en/latest/?badge=latest

.. image:: https://coveralls.io/repos/github/uber/dobles/badge.svg?branch=master
    :target: https://coveralls.io/github/uber/dobles?branch=master


**dobles** is a Python package that provides test dobles for use in automated tests.

It provides functionality for stubbing, mocking, and verification of test dobles against the real objects they double.
In contrast to the Mock package, it provides a clear, expressive syntax and better safety guarantees to prevent API
drift and to improve confidence in tests using dobles. It comes with drop-in support for test suites run by Pytest,
Nose, or standard unittest.

Documentation
-------------

Documentation is available at http://dobles.readthedocs.org/en/latest/.

Development
-----------

Source code is available at https://github.com/uber/dobles.

To install the dependencies on a fresh clone of the repository, run ``make bootstrap``.

To run the test suite, run ``make test``.

To build the documentation locally, run ``make docs``.

License
-------

MIT: http://opensource.org/licenses/MIT
