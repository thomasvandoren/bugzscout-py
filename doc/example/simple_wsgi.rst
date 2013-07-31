Simple WSGI Server Example
==========================

This example describes how to add synchronous BugScout reporting to a WSGI
app. This is **not** intended for production use. It's purpose is to show how
easy it is to add this kind of reporting.

An example that is suitable for production is the :doc:`celery extension
example <celery_wsgi>`.

This example uses the `Paste <http://pythonpaste.org/>`_ python package.

Setup a simple WSGI server
--------------------------

A simple paste WSGI server that can handle HTTP requests is:

.. literalinclude:: src/simple_wsgi.py
    :end-before: import bugzscout
    :linenos:

To run this server:

.. code-block:: bash

    python path/to/simple_wsgi.py

Making requests to ``http://localhost:5000/`` will respond with a 200 OK and
'Hellow world!' in the body.

Adding BugzScout
----------------

When errors occur in this code, it would be great to report them to
BugzScout. In order to so, wrap the contents of the ``app`` function in a
try/except and call bugzscout in the except block.

This example creates a new function, ``bugzscout_app``, that does just that.

.. literalinclude:: src/simple_wsgi.py
    :start-after: paste.httpserver.serve
    :linenos:

The same ``__main__`` block from above can be used, substituting
``bugzscout_app`` for ``app``. When an error is thrown during a request, it
will be recorded to FogBugz via BugzScout (assuming the BugzScout configuration
is correctly set). Note that the request will still fail in the same way as it
would above, since the exception is re-raised.
