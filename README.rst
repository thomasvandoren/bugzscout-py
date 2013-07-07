bugzscout-py
============
Python interface for the FogBugz BugzScout API.

.. image:: https://travis-ci.org/thomasvandoren/bugzscout-py.png?branch=master
    :target: https://travis-ci.org/thomasvandoren/bugzscout-py

Installation
------------

.. code-block:: bash

    pip install bugzscout-py

Supported python versions
~~~~~~~~~~~~~~~~~~~~~~~~~

* 2.7
* 3.3
* pypy

Getting Started
---------------

.. code-block:: pycon

    >>> import bugzscout
    >>> b = bugzscout.BugzScout('http://fogbugz/scoutSubmit.asp',
                                'fb-user',
                                'the-project',
                                'the-area')
    >>> b.submit_error('An eror occurred of type blah', extra='Extra info')

License
-------
BSD

Authors
-------
Thomas Van Doren
