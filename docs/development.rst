Development
===========

All assistance is appreciated! New features, documentation fixes, bug reports,
bug fixes, and more are graciously accepted.

Getting started
---------------

To get set up, fork the project on our `Github page`_. You can then
install from source by following the instructions in :doc:`install`. There are
a few additional dependencies for compiling the docs and running the tests:

* black_
* isort_
* pre-commit_
* sphinx_ (for docs only)

You can install the package, and all dependencies, in editiable mode using pip_ from the `pyproject.toml` file:

.. code-block:: bash

    pip install -e .

To install additional dependencies for development, testing, or documentation, use the following commands:

.. code-block:: bash

    pip install -e .[dev]
    pip install -e .[test]
    pip install -e .[docs]

These can be combined to install all dependencies:

.. code-block:: bash

    pip install -e .[dev,test,docs]

.. _Github page: https://github.com/robberwick/pylibrelinkup
.. _black: https://github.com/psf/black
.. _isort: https://github.com/PyCQA/isort
.. _pre-commit: https://pre-commit.com/
.. _sphinx: http://sphinx.pocoo.org/
.. _pip: http://www.pip-installer.org/

Running the tests
-----------------

Once you're all installed, ensure that the tests pass by running them. You
can run the local unit tests with the following command:

.. code-block:: bash

    pytest

Testing in all supported Python versions
----------------------------------------

Since PyLibreLinkUp supports multiple Python versions, running the tests in
your currently installed Python version may not be enough. We use GitHub Actions to automate running the tests in all supported versions of Python. You can check the configuration in the `.github/workflows` directory.

Submitting bugs and patches
---------------------------

If you have a bug to report, please do so on our `Github issues`_ page. If
you've got a fork with a new feature or a bug fix with tests, please send us a
pull request.

.. _Github issues: https://github.com/robberwick/pylibrelinkup/issues