#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A simple WSGI server that reports errors to FogBugz via BugzScout
asynchronously.
"""

from __future__ import print_function, unicode_literals

import bugzscout.ext.celery_app
import sys
import traceback

# Set celery here, so this module can be designated as the app when running the
# celery work.
celery = bugzscout.ext.celery_app.celery


def _handle_exc(exception):
    """Record exception with stack trace to FogBugz via BugzScout,
    asynchronously. Returns an empty string.

    Note that this will not be reported to FogBugz until a celery worker
    processes this task.

    :param exception: uncaught exception thrown in app
    """
    # Set the description to a familiar string with the exception
    # message. Add the stack trace to extra.
    bugzscout.ext.celery_app.submit_error.delay(
        'http://fogbugz/scoutSubmit.asp',
        'error-user',
        'MyAppProject',
        'Errors',
        'An error occurred in MyApp: {0}'.format(exception.message),
        extra=traceback.extract_tb(*sys.exc_info()))

    # Return an empty body.
    return ['']


def app(environ, start_response):
    """Simple WSGI application. Returns 200 OK response with 'Hellow world!' in
    the body for GET requests. Returns 405 Method Not Allowed for all other
    methods.

    Returns 500 Internal Server Error if an exception is thrown. The response
    body will not include the error or any information about it. The error and
    its stack trace will be reported to FogBugz via BugzScout, though.

    :param environ: WSGI environ
    :param start_response: function that accepts status string and headers
    """
    try:
        if environ['REQUEST_METHOD'] == 'GET':
            start_response('200 OK', [('content-type', 'text/html')])
            return ['Hellow world!']
        else:
            start_response(
                '405 Method Not Allowed', [('content-type', 'text/html')])
            return ['']
    except Exception as ex:
        # Call start_response with exception info.
        start_response(
            '500 Internal Server Error',
            [('content-type', 'text/html')],
            sys.exc_info())

        # Record the error to FogBugz and this will return the body for the
        # error response.
        return _handle_exc(ex)


if __name__ == '__main__':
    import paste.httpserver
    paste.httpserver.serve(app, host='0.0.0.0', port='5000')
