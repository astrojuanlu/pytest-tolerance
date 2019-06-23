================
pytest-tolerance
================

.. image:: https://img.shields.io/pypi/v/pytest-tolerance.svg
    :target: https://pypi.org/project/pytest-tolerance
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-tolerance.svg
    :target: https://pypi.org/project/pytest-tolerance
    :alt: Python versions

.. image:: https://travis-ci.org/Juanlu001/pytest-tolerance.svg?branch=master
    :target: https://travis-ci.org/Juanlu001/pytest-tolerance
    :alt: See Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/Juanlu001/pytest-tolerance?branch=master
    :target: https://ci.appveyor.com/project/Juanlu001/pytest-tolerance/branch/master
    :alt: See Build Status on AppVeyor

pytest plugin to optimize comparison tolerances

**Work in progress**

----

This `pytest`_ plugin was generated with `Cookiecutter`_
along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.

Installation
------------

You can install "pytest-tolerance" via `pip`_ from `PyPI`_::

    $ pip install pytest-tolerance

Usage
-----

Mark your tests and use the :code:`tolerance` fixture::

  import pytest
  @pytest.mark.tolerance(min_exponent=-10)
  def test_sth(tolerance):
      assert 1e-7 < tolerance

And the test will be re-run until the tolerance check is met.

It can be combined with :code:`pytest.approx`, :code:`numpy.testing.assert_almost_equal`
and similar.

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-tolerance" is free and open source software

Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/Juanlu001/pytest-tolerance/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
