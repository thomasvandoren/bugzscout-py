Introduction
============

Installation
------------

.. code-block:: bash

    pip install bugzscout

    # Or, with easy_install:
    easy_install bugzscout

    # Or, from source:
    python setup.py install

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
----------------------

There is a command line interface for submitting errors. To simplify submitting
multiple errors, the FogBugz configuration can be set in the environment.

.. code-block:: bash

    # (Optional) Setup the environment.
    export BUGZSCOUT_URL=http://fogbugz/scoutSubmit.asp
    export BUGZSCOUT_USER=errors
    export BUGZSCOUT_PROJECT='My Project'
    export BUGZSCOUT_AREA=Errors

    # Submit a new error.
    bugzscout --extra 'Extra data for the case...' 'The description of the error.'

Publishing Errors Asynchronously with Celery
--------------------------------------------

The `Celery <http://celeryproject.org/>`_ extension can be used to
asynchronously publish errors. This is the recommended pattern for using
bugzscout in production environments.

.. code-block:: python

    # Import celery extension.
    import bugzscout.ext.celery_app

    # Submit errors asynchronously.
    bugzscout.ext.celery_app.submit_error.delay(
      'The description here...',
      extra='The extra information here...')

The `Celery worker
<http://docs.celeryproject.org/en/latest/userguide/workers.html>`_ can use the
same celery app for consuming messages.

.. code-block:: bash

    celery worker --app=bugzscout.ext.celery_app

A ``celeryconfig.py`` file on the PYTHONPATH can be used to configure the
celery instance. For example:

.. code-block:: bash

    export CELERY_CONFIG_MODULE=celeryconfig
    celery worker --app=bugzscout.ext.celery_app
