.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/dguitarbite/python-libvirt_provider/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Libvirt and python-libvirt version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

libvirt_provider could always use more documentation, whether as part of the
official libvirt_provider docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/dguitarbite/python-libvirt_provider/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `libvirt_provider` for local development.

1. Fork the `libvirt_provider` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/python-libvirt_provider.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv libvirt_provider
    $ cd libvirt_provider/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the tests, including testing other Python versions with tox::

    $ flake8 libvirt_provider tests
    $ python setup.py test or py.test
    $ tox

   To get flake8 and tox, just pip install them into your virtualenv.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 2.6, 2.7, 3.3, 3.4 and 3.5, and for PyPy. Check
   https://travis-ci.org/dguitarbite/python-libvirt_provider/pull_requests
   and make sure that the tests pass for all supported Python versions.

Release Model
-------------

This project follows release model specified by .. _PEP-0440.: https://www.python.org/dev/peps/pep-0440/

- Releases: Version number is stored in libvirt_provider/__init__.py and imported
  in setup.py to unify the versioning system.
- Git tags will be used to mark stable and significant releases. This should allow
  easy identification of which version to use.
- At present releasing a stable release (git tag with RC) is ad-hoc and does not follow
  strict timelines.
- Release scheme X.Y.Z (Major.Minor.Micro):
  - `X`: Major release.
  - `Y`: Minor release.
  - `Z`: Micro release.
- Incrementing `X` would signify new stable version.
  - This version bump signifies stable version.
  - Using annotated git tags for these releases.
  - Further improvements, backports etc. would be signified with a rc release tag if required.
  - Bugs are treated with higher priority.
  - Only critical feature improvements and bug fixes are backported.
- Incrementing `Y` would signify new major features.
  - This version bump signifies minor release with major features.
  - Using annotated git tags for these releases.
  - These features are usually stable enough to be used but they are not explicitly tested from the system level.
    - Test cases for integration and system level testing will be implemented.
    - But, this does not guarantee high stability and should be considered bleeding edge.
  - These release should usually be done at the sub-system level, aggregating multiple units.
- Incrementing Z would signify new minor features.
  - This version bump signifies micro release.
  - Using lightweight git tags for these releases.
  - These release should be fast moving, doing most of the new implementations and considered unstable.
    - Implementing new features mostly at the unit level.
    - Should not be relied upon, highly unstable.
    - Unit tests should be implemented.
    - Other tests are implemented as needed.

Tips
----

To run a subset of tests::

$ py.test tests.test_libvirt_provider
