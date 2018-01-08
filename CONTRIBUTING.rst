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

Report bugs at http://prodweb4/OnlineOrdering/Product?productID=15701

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

This application could always use more documentation, whether as part of the
official application docs, in docstrings, or even on the web in wikis,
sharepoints, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at http://prodweb4/OnlineOrdering/Product?productID=15701.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up aflux-assurance-server for local development.

1. Clone you the project on Gitlab locally::

    $ git clone git@git.ent.tds.net:Some_Group/aflux-assurance-server.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv aflux-assurance-server-dev
    $ cd aflux-assurance-server/
    $ pip install -U .

4. Create a branch for local development::

    $ git checkout -b feature-name-your-branch

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the tests, including testing other Python versions with tox::

    $ flake8 aflux_assurance_server tests
    $ python setup.py test
    $ tox

   To get flake8 and tox, just pip install them into your virtualenv.

6. Commit your changes and push your branch to Gitlab::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin feature-name-your-branch

7. Submit a merge request through the Gitlab website.

Merge Request Guidelines
-----------------------

Before you submit a merge request, check that it meets these guidelines:

1. The merge request should include tests.
2. If the merge request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The merge request should work for Python 2.6, 2.7, 3.3, and 3.4, and for PyPy.

Tips
----

To run a subset of tests::

    $ python -m unittest tests.test_aflux_assurance_server
