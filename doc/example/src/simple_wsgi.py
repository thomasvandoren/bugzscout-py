#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A simple WSGI server."""

from __future__ import print_function, unicode_literals


def app(environ, start_response):
    """Simple WSGI application that returns 200 OK response with 'Hellow
    world!' in the body.

    :param environ: WSGI environ
    :param start_response: function that accepts status string and headers
    """
    start_response('200 OK', [('content-type', 'text/html')])
    return ['Hellow world!']


if __name__ == '__main__':
    import paste.httpserver
    paste.httpserver.serve(app, host='0.0.0.0', port='5000')


import bugzscout
import sys
import traceback

# Create an instance of BugzScout to use for all errors thrown in
# bugzscout_app.
b = bugzscout.BugzScout(
    'http://fogbugz/scoutSubmit.asp', 'error-user', 'MyAppProject', 'Errors')


def bugzscout_app(environ, start_response):
    """Simple WSGI application that returns 200 OK response with 'Hellow
    world!' in the body. If an uncaught exception is thrown, it is reported to
    BugzScout.

    :param environ: WSGI environ
    :param start_response: function that accepts status string and headers
    """
    try:
        start_response('200 OK', [('content-type', 'text/html')])
        return ['Hellow world!']
    except Exception as ex:
        # Set the description to a familiar string with the exception
        # message. Add the stack trace to extra.
        b.submit_error('An error occurred in MyApp: {0}'.format(ex.message),
                       extra=traceback.extract_tb(*sys.exc_info()))

        # Reraise the exception.
        raise ex
