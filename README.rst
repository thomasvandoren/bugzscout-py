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

Command Line Interface
~~~~~~~~~~~~~~~~~~~~~~

There is a command line interface for submitting errors. To simplify submitting
multpile errors, the FogBugz configuration can be set in the environment.

.. code-block:: bash

    # (Optional) Setup the environment.
    export BUGZSCOUT_URL=http://fogbugz/scoutSubmit.asp
    export BUGZSCOUT_USER=errors
    export BUGZSCOUT_PROJECT='My Project'
    export BUGZSCOUT_AREA=Errors

    # Submit a new error.
    bugzscout --extra 'Extra data for the case...' 'The description of the error.'

License
-------
BSD

Authors
-------
Thomas Van Doren
