BugzScout Command Line Interface
================================

There is a command line interface for submitting errors. It can be used for
non-python application (like shell scripts).

.. code-block:: bash

    usage: bugzscout [-h] [-v] [-u URL] [--user USER] [--project PROJECT] [--area AREA]
                     [-e EXTRA] [--default-message DEFAULT_MESSAGE]
                     description

    Command line interface for sumbitting cases to FogBugz via BugzScout.

    Environment variables can be used to set the FogBugz arguments with:

     * BUGZSCOUT_URL
     * BUGZSCOUT_USER
     * BUGZSCOUT_PROJECT
     * BUGZSCOUT_AREA

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         Enable verbose output. (default: False)

    FogBugz arguments:
      -u URL, --url URL     URL for bugzscout requests to be sent. Should be something like
                            .../scoutSubmit.asp. (default: None)
      --user USER           User to designate when submitting via bugzscout. (default: None)
      --project PROJECT     Fogbugz project to file cases under. (default: None)
      --area AREA           Fogbugz area to file cases under. (default: None)

    error arguments:
      -e EXTRA, --extra EXTRA
                            Extra data to send with error. (default: None)
      --default-message DEFAULT_MESSAGE
                            Set default message if case is new. (default: None)
      description           Description of error. Will be matched against existing cases.


To simplify submitting multiple errors, the FogBugz configuration can be set in
the environment.

.. code-block:: bash

    # (Optional) Setup the environment.
    export BUGZSCOUT_URL=http://fogbugz/scoutSubmit.asp
    export BUGZSCOUT_USER=errors
    export BUGZSCOUT_PROJECT='My Project'
    export BUGZSCOUT_AREA=Errors

    # Submit a new error.
    bugzscout --extra 'Extra data for the case...' 'The description of the error.'

Example shell script using cli
------------------------------

Below is an example of a bash function that can wrap other bash calls. It
reports an error to fogbugz if the call has a non-zero exit code.

.. literalinclude:: example/cli.sh
    :language: bash

For example, in a bash shell, the second line would fail and report an error
via BugzScout:

.. code-block:: bash

    source path/to/bugzscout_wrap_function.sh
    bugzscout_wrap /bin/false
